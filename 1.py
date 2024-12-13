import asyncio


STRONGMANS = [
    ('Pasha', 3),
    ('Denis', 4),
    ('Apollon', 5),
]

BASE_POWER = 10


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')

    for i in range(1, 6):
        await asyncio.sleep(BASE_POWER/power)
        print(f'Силач {name} поднял {i} шар')

    print(f'Силач {name} закончил соревнования.')


async def start_tournament():
    tasks = [asyncio.create_task(start_strongman(*x)) for x in STRONGMANS]

    for task in tasks:
        await task


asyncio.run(start_tournament())
