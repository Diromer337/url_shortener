import string
from random import choices

from databases import Database
from sqlalchemy import Table

characters = string.digits + string.ascii_letters


async def generate_short_link(url: str, database: Database, url_table: Table):
    query = url_table.select().where(
        url_table.c.url == url
    )
    r = await database.fetch_one(query=query)
    if not r:
        short_url = ''.join(choices(characters, k=7))
        query = url_table.insert().values(url=url, short_url=short_url)
        await database.execute(query=query)
    else:
        short_url = r['short_url']
    return short_url


async def assign_url(url: str, short_url: str, database: Database, url_table: Table):
    query = url_table.select().where(
        url_table.c.short_url == short_url
    )
    r = await database.fetch_one(query=query)
    if not r:
        query = url_table.insert().values(url=url, short_url=short_url)
        await database.execute(query=query)
    elif r['url'] != url:
        return False
    return True
