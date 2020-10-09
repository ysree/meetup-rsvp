import os
import aiohttp
import asyncio
import asyncpg
import logging
import json

ws_url = os.environ['WS_URL']
db_host = os.environ['DB_HOST']
db_port = os.environ['PORT']
db_user = os.environ['DB_USERNAME']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_USERNAME']
db_pool_min_size = int(os.environ['DB_POOL_MIN_SIZE'])
db_pool_max_size = int(os.environ['DB_POOL_MAX_SIZE'])
log_level = os.environ['LOG_LEVEL']
show_error = os.environ['SHOW_ERROR']

level = logging.INFO
if log_level.lower() == 'error':
    level = logging.ERROR
elif log_level.lower() == 'debug':
    level = logging.DEBUG
elif log_level.lower() == 'warning':
    level = logging.WARNING
elif log_level.lower() == 'fatal':
    level = logging.FATAL
    
exec_info = False
if show_error.lower() == "true":
    exec_info = True

logging.basicConfig(level=level)
loop = asyncio.get_event_loop()

async def get_connection_pool():
    pool = await asyncpg.create_pool(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name,
        min_size=db_pool_min_size,
        max_size=db_pool_max_size,
    )
    async with pool.acquire() as connection:
        query = "CREATE TABLE books_service.public.meetup_rsvp (uuid_ uuid NOT NULL DEFAULT uuid_generate_v4(), data jsonb NOT NULL DEFAULT '{}'::jsonb, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (uuid_))"
        try:
            await connection.execute(query)
            logging.info(query)
        except Exception as e:
            logging.error(e.message + ":SQL:" + query, exc_info=False)

    return pool

async def main(pool):
    async with aiohttp.ClientSession() as session:
        ws  = await session.ws_connect(ws_url)
        while True:
            msg = await ws.receive()
            async with pool.acquire() as connection:
                if not msg is None:
                    query = "INSERT INTO meetup_rsvp (uuid_, data, created_at) VALUES(uuid_generate_v4(), '"+ json.dumps(msg.json()) +"'::jsonb, CURRENT_TIMESTAMP)"
                    try:
                        await connection.execute(query)
                        logging.info(query)
                    except Exception as e:
                        logging.error(e.message+":SQL:" + query, exc_info=exec_info)
                        #pass
                
pool = get_connection_pool()
multiple_coroutines = [main(pool) for _ in range(1)]
loop.run_until_complete(asyncio.gather(*multiple_coroutines))
