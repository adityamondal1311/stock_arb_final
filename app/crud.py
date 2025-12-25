from app.models import Price
from sqlalchemy.future import select

async def save_price(db, symbol, exchange, price):
    row = Price(symbol=symbol, exchange=exchange, price=price)
    db.add(row)
    await db.commit()

async def get_latest_prices(db):
    q = select(Price).order_by(Price.timestamp.desc())
    res = await db.execute(q)
    return res.scalars().all()
