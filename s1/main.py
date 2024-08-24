import aiohttp
import asyncio
from sqlalchemy.orm import sessionmaker
from models import QueueRequest, QueueResponse, setup_db
from config import *

async def process_request(session, db_session, request):
    url = f"{S2_URL}{request.uri}"
    auth = aiohttp.BasicAuth(S2_LOGIN, S2_PASSWORD)
    try:
        async with session.request(
            method=request.method, 
            url=url, 
            params=request.params, 
            headers=request.headers, 
            auth=auth
            ) as resp:
            body = await resp.text()
            response = QueueResponse(
                request_id=request.id,
                status_code=resp.status,
                body=body
            )
            db_session.add(response)
            request.status = "Отработала"
            request.processed = True
            request.is_new = False
            db_session.commit()
    except asyncio.TimeoutError:
        print(f"Обращение к {url} заняло слишком много времени.")
        request.status = "Не отработала"
        request.processed = False
        request.is_new = False
        db_session.commit()


async def worker(db_session):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
        while True:
            with db_session.begin():
                request = db_session.query(QueueRequest).filter_by(is_new=True).with_for_update(skip_locked=True).first()

                if not request:
                    break

                request.is_new = False
                db_session.commit()

            await process_request(session, db_session, request)


async def main():
    Session = setup_db(DB_URL)
    db_session = Session()

    tasks = [asyncio.create_task(worker(db_session)) for _ in range(THREADS)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())