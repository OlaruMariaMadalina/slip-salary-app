
import asyncio
from sqlalchemy import inspect
from app.db.engine import engine

def get_tables(sync_conn):
    inspector = inspect(sync_conn)
    return inspector.get_table_names()

async def show_tables():
    async with engine.begin() as conn:
        tables = await conn.run_sync(get_tables)
        print("Tabele create în baza de date:")
        for table in tables:
            print(table)

if __name__ == "__main__":
    asyncio.run(show_tables())