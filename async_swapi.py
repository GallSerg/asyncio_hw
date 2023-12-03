import asyncio
import datetime
from typing import List

import aiohttp
import requests
from more_itertools import chunked

from models import Session, SwapiPeople, init_db

CHUNK_SIZE = 10


async def get_person(person_id, session):
    response = await session.get(f"https://swapi.py4e.com/api/people/{person_id}/")
    person_data = await response.json()

    return person_data


async def insert_to_db(people_dict: List[dict]):
    async with Session() as session:
        people = [SwapiPeople(
            id=person.get("id"),
            birth_year=person.get("birth_year"),
            eye_color=person.get("eye_color"),
            films=', '.join(person.get("films")) if person.get("films") else '',
            gender=person.get("gender"),
            hair_color=person.get("hair_color"),
            height=person.get("height"),
            homeworld=person.get("homeworld"),
            mass=person.get("mass"),
            name=person.get("name"),
            skin_color=person.get("skin_color"),
            species=', '.join(person.get("species")) if person.get("species") else '',
            starships=', '.join(person.get("starships")) if person.get("starships") else '',
            vehicles=', '.join(person.get("vehicles")) if person.get("vehicles") else ''
        ) for person in people_dict]
        session.add_all(people)
        await session.commit()


async def main(q):
    await init_db()
    session = aiohttp.ClientSession()

    for people_id_chunk in chunked(range(1, q), CHUNK_SIZE):
        coros = [get_person(person_id, session) for person_id in people_id_chunk]
        result = await asyncio.gather(*coros)
        asyncio.create_task(insert_to_db(result))

    await session.close()
    set_of_tasks = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*set_of_tasks)


if __name__ == "__main__":
    req_count = requests.get("https://swapi.py4e.com/api/people")
    people_count = req_count.json()["count"]
    start = datetime.datetime.now()
    asyncio.run(main(people_count))
    print(datetime.datetime.now() - start)
