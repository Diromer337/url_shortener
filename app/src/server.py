import re
import os
from typing import Optional

import databases
import sqlalchemy
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse

from short import Shortener

DATABASE_URL = os.getenv('DATABASE_URL')
SERVER_URL = os.getenv('SERVER_URL')

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

url_table = sqlalchemy.Table(
    'url',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('url', sqlalchemy.String, index=True),
    sqlalchemy.Column('short_url', sqlalchemy.String, unique=True, index=True)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)

app = FastAPI()
shortener = Shortener(database, url_table)

# Валидация URL из Django
url_regex = re.compile(
    r'^((?:http|ftp)s?://)?'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.post('/short')
async def generate(url: str, short_url: Optional[str] = None):
    if not url_regex.match(url):
        raise HTTPException(status_code=400, detail='Bad URL')
    if not url.startswith(('https://', 'http://')):
        url = 'https://' + url
    if short_url:
        await shortener.assign_url(url, short_url)
    else:
        short_url = await shortener.generate_short_link(url)
    return JSONResponse(
        content={'short_url': SERVER_URL + short_url}
    )


async def get_url(short_url: str) -> str:
    query = url_table.select().where(
        url_table.c.short_url == short_url
    )
    r = await database.fetch_one(query=query)
    return r['url'] if r else ''


@app.get('/{short_url}')
async def redirect(short_url: str):
    url = await get_url(short_url)
    if url:
        return RedirectResponse(url, status_code=301)
    return HTTPException(status_code=404, detail='Short URL not found')
