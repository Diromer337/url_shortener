import string
from random import choices

from databases import Database
from fastapi import Request
from sqlalchemy.schema import Table


class Shortener:
    characters = string.digits + string.ascii_letters

    def __init__(self, database: Database, url_table: Table):
        self._database = database
        self._url_table = url_table

    async def generate_short_link(self, url: str, request: Request):
        scheme = 'https://' if not url.startswith(('https://', 'http://')) else ''
        url = scheme + url + '?' + str(request.query_params)
        query = self._url_table.select().where(
            self._url_table.c.url == url
        )
        r = await self._database.fetch_one(query=query)
        if not r:
            short_url = ''.join(choices(self.characters, k=5))
            query = self._url_table.insert().values(url=url, short_url=short_url)
            await self._database.execute(query=query)
        else:
            short_url = r['short_url']
        return short_url

    async def assign_url(self, url: str, short_url: str, request: Request):
        scheme = 'https://' if not url.startswith(('https://', 'http://')) else ''
        url = scheme + url + '?' + str(request.query_params)
        query = self._url_table.select().where(
            self._url_table.c.short_url == short_url
        )
        r = await self._database.fetch_one(query=query)
        if not r:
            query = self._url_table.insert().values(url=url, short_url=short_url)
            await self._database.execute(query=query)
        elif r['url'] != url:
            return ''
        return short_url
