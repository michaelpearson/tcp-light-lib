from light import Connection
import asyncio


async def run():
    connection = Connection("192.168.0.2")
    try:
        await connection.connect()
        writer = write_loop(connection)
        reader = read_loop(connection)
        await asyncio.gather(writer, reader)
    finally:
        await connection.close()


async def write_loop(connection: Connection):
    while True:
        await connection._write_command(1, 0.5)
        await asyncio.sleep(1)
        await connection._write_command(0, 0.5)
        await asyncio.sleep(1)


async def read_loop(connection: Connection):
    async for message in connection.get_updates():
        print(message)


if __name__ == "__main__":
    asyncio.run(run())
