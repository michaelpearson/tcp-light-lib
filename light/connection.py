from asyncio import StreamReader, StreamWriter, open_connection, get_event_loop, Task
from struct import pack, unpack
from typing import NamedTuple, Callable

PORT = 8889


class Status(NamedTuple):
    mac: str
    brightness: int
    gpio_status: int
    uptime: int


class Connection:
    _writer: StreamWriter
    _reader: StreamReader
    _event_loop: Task
    _callback: Callable[[Status], None]

    def __init__(self, connection: (StreamReader, StreamWriter), callback: Callable[[Status], None]):
        self._reader, self._writer = connection
        self._callback = callback
        self._event_loop = get_event_loop().create_task(self.__event_loop())

    @classmethod
    async def create(cls, host: str, callback: Callable[[Status], None]) -> 'Connection':
        return Connection(await open_connection(host, 8889), callback)

    async def set_state(self, brightness: float, transition: float):
        brightness = round(brightness * 0xFFFF)
        transition = round(transition * 1000)
        await self.__write_command(0, brightness, transition)

    async def ping(self) -> None:
        await self.__write_command(1, 0, 0)

    async def close(self) -> None:
        self._writer.close()
        await self._writer.wait_closed()
        self._event_loop.cancel()

    async def __event_loop(self) -> None:
        while True:
            self._callback(await self.__read())

    async def __read(self) -> Status:
        data = await self._reader.read(32)
        id_0, id_1, id_2, id_3, id_4, id_5, brightness, gpio_status, uptime = unpack('!BBBBBBHBxxxL', data)
        mac = f"{id_0:02X}:{id_1:02X}:{id_2:02X}:{id_3:02X}:{id_4:02X}:{id_5:02X}"
        brightness = brightness / 0xFFFF
        return Status(mac, brightness, gpio_status, uptime)

    async def __write_command(self, command_id: int, brightness: int, transition: int) -> None:
        command = pack('BHH', command_id, brightness, transition)
        self._writer.write(command)
        await self._writer.drain()
