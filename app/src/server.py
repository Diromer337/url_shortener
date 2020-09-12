import re

import databases
import sqlalchemy
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse

from short import Shortener

DATABASE_URL = 'postgresql://postgres:example@db:5432'
SERVER_URL = '0.0.0.0:8000/'

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

url_table = sqlalchemy.Table(
    'url',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('url', sqlalchemy.String),
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


@app.post('/app/{short_url}/convert_to/{url}')
async def generate(url: str, short_url: str, request: Request):
    if not url_regex.match(url):
        raise HTTPException(status_code=400, detail='Bad URL')
    short_url = await shortener.assign_url(url, short_url, request)
    return JSONResponse(
        content={'short_url': SERVER_URL + short_url}
    ) if short_url else HTTPException(status_code=400, detail='Short URL is busy')


@app.post('/app/{url:path}')
async def generate(url: str, request: Request):
    if not url_regex.match(url):
        raise HTTPException(status_code=400, detail='Bad URL')
    short_url = await shortener.generate_short_link(url, request)
    return JSONResponse(
        content={'short_url': SERVER_URL + short_url}
    )


@app.get('/{short_url}')
async def redirect(short_url: str):
    query = url_table.select().where(
        url_table.c.short_url == short_url
    )
    r = await database.fetch_one(query=query)
    if r:
        return RedirectResponse(r['url'], status_code=301)
    else:
        return HTTPException(status_code=404, detail='Short URL not found')
