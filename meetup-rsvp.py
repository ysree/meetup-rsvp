import os
import aiohttp
import asyncio
import asyncpg
import logging
import json

ws_url = os.environ['ws_url']
db_host = os.environ['db_host']
db_port = os.environ['db_port']
db_user = os.environ['db_user']
db_password = os.environ['db_password']
db_name = os.environ['db_name']
db_pool_min_size = int(os.environ['db_pool_min_size'])
db_pool_max_size = int(os.environ['db_pool_max_size'])
show_error = os.environ['show_error']
log_level = os.environ['log_level']

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

async def main():
    pool = await asyncpg.create_pool(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name,
        min_size=db_pool_min_size,
        max_size=db_pool_max_size,
    )
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
                
multiple_coroutines = [main() for _ in range(1)]
loop.run_until_complete(asyncio.gather(*multiple_coroutines))
