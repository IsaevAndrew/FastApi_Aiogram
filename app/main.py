import requests
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db, async_engine, async_session
from app.db.models import Product, Subscription, ProductRequest
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.auth import validate_token

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    try:
        async with AsyncSession(async_engine) as session:
            result = await session.execute(select(Subscription))
            subscriptions = result.scalars().all()
            for subscription in subscriptions:
                add_periodic_task(task_id=f"update_{subscription.artikul}",
                                  artikul=subscription.artikul)
        yield
    finally:
        scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


@app.post("/api/v1/products", status_code=201,
          dependencies=[Depends(validate_token)])
async def add_product(request: ProductRequest,
                      db: AsyncSession = Depends(get_db)):
    artikul = request.artikul
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={artikul}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404,
                            detail="Товар не найден на Wildberries")
    product_data = response.json()
    try:
        products = product_data.get("data", {}).get("products", [])
        if not products:
            raise HTTPException(status_code=404,
                                detail=f"Товар с артикулом {artikul} отсутствует в данных Wildberries")
        product = products[0]
        name = product["name"]
        price = product["salePriceU"] / 100  # Цена в рублях
        rating = product["reviewRating"]  # Рейтинг
        stock = product["totalQuantity"]  # Кол-во на складах
        stmt = select(Product).where(Product.artikul == artikul)
        result = await db.execute(stmt)
        existing_product = result.scalar_one_or_none()

        if existing_product:
            await db.execute(
                Product.__table__.update()
                .where(Product.artikul == artikul)
                .values(name=name, price=price, rating=rating, stock=stock)
            )
        else:
            new_product = Product(
                artikul=artikul,
                name=name,
                price=price,
                rating=rating,
                stock=stock
            )
            db.add(new_product)
        await db.commit()
        return {
            "artikul": artikul,
            "name": name,
            "price": price,
            "rating": rating,
            "stock": stock,
            "message": "Данные о товаре успешно сохранены."
        }
    except KeyError as e:
        raise HTTPException(status_code=500,
                            detail=f"Ошибка обработки данных Wildberries: {e}")


@app.get("/api/v1/subscribe/{artikul}", dependencies=[Depends(validate_token)])
async def subscribe_product(artikul: int, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(Subscription).where(Subscription.artikul == artikul)
        result = await db.execute(stmt)
        existing_subscription = result.scalar_one_or_none()
        if existing_subscription:
            raise HTTPException(status_code=400,
                                detail="Подписка на этот артикул уже оформлена.")
        product_data = await add_product(ProductRequest(artikul=artikul), db)
        if not product_data:
            raise HTTPException(status_code=404,
                                detail=f"Товар с артикулом {artikul} отсутствует на Wildberries.")
        new_subscription = Subscription(artikul=artikul)
        db.add(new_subscription)
        await db.commit()
        add_periodic_task(task_id=f"update_{artikul}", artikul=artikul)
        return {
            **product_data,
            "message": "Подписка оформлена. Данные о товаре успешно сохранены."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Ошибка при подписке на товар: {str(e)}")


def add_periodic_task(task_id: str, artikul: int):
    if scheduler.get_job(task_id):
        return

    scheduler.add_job(
        func=fetch_and_save_product,
        trigger=IntervalTrigger(minutes=30),
        args=[artikul],
        id=task_id,
        replace_existing=True
    )


async def fetch_and_save_product(artikul: int):
    async with async_session() as db:
        try:
            result = await add_product(ProductRequest(artikul=artikul), db)
            print(f"Артикул {artikul} успешно обновлен: {result}")
        except Exception as e:
            print(f"Ошибка при обработке артикула {artikul}: {e}")
