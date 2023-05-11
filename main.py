import asyncio
from aiohttp import ClientSession
from db import Session, engine
from models import Base, People

ALL_PEOPLE = 84


async def get_url(url, key, session):
    async with session.get(f'{url}') as response:
        data = await response.json()
        return data[key]


async def get_urls(urls, key, session):
    tasks = (asyncio.create_task(get_url(url, key, session)) for url in urls)
    for task in tasks:
        yield await task


async def get_data(urls, key, session):
    data_list = []
    async for el in get_urls(urls, key, session):
        data_list.append(el)
    return ', '.join(data_list)


async def paste_to_db(people_data):
    async with Session() as session:
        async with ClientSession() as client_session:
            for character_data in people_data:
                if character_data is not None:
                    homeworld = await get_data([character_data['homeworld']], 'name', client_session)
                    films = await get_data(character_data['films'], 'title', client_session)
                    species = await get_data(character_data['species'], 'name', client_session)
                    starships = await get_data(character_data['starships'], 'name', client_session)
                    vehicles = await get_data(character_data['vehicles'], 'name', client_session)
                    character_data = People(
                        birth_year=character_data['birth_year'],
                        eye_color=character_data['eye_color'],
                        gender=character_data['gender'],
                        hair_color=character_data['hair_color'],
                        height=character_data['height'],
                        mass=character_data['mass'],
                        name=character_data['name'],
                        skin_color=character_data['skin_color'],
                        homeworld=homeworld,
                        films=films,
                        species=species,
                        starships=starships,
                        vehicles=vehicles,
                    )
                    session.add(character_data)
                    await session.commit()


async def get_character(people_id: int, session: ClientSession):
    async with session.get(f'https://swapi.dev/api/people/{people_id}') as response:
        if response.ok:
            character = await response.json()
            return character
        else:
            pass


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

    async with ClientSession() as session:
        coro = [get_character(people_id, session=session) for people_id in range(1, ALL_PEOPLE)]
        people = await asyncio.gather(*coro)
        asyncio.create_task(paste_to_db(people))

    tasks = set(asyncio.all_tasks()) - {asyncio.current_task()}
    for task in tasks:
        await task


if __name__ == '__main__':
    asyncio.run(main())
