from light import Connection
import asyncio


async def run():
    connection = await Connection.create("192.168.0.2", print)
    while True:
        await connection.set_state(1, 0.5)
        await asyncio.sleep(1)
        await connection.set_state(0, 0.5)
        await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        pass
