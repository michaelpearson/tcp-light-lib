import asyncio
from collections import AsyncIterator
from struct import pack, unpack
from typing import NamedTuple

PORT = 8889


class Status(NamedTuple):
    mac: str
    brightness: int
    gpio_status: int
    uptime: int


class Connection:
    _writer: asyncio.StreamWriter = None
    _reader: asyncio.StreamReader = None

    def __init__(self, host):
        self._host = host

    async def connect(self):
        self._reader, self._writer = await asyncio.open_connection(self._host, 8889)

    async def close(self):
        self._writer.close()
        await self._writer.wait_closed()

    async def _write_command(self, brightness: float, transition: float):
        """
        :param brightness: 0 off, 1 on
        :param transition: seconds
        """
        brightness = round(brightness * 0xFFFF)
        transition = round(transition * 1000)
        command = pack('BHH', 0, brightness, transition)
        self._writer.write(command)
        await self._writer.drain()



    async def _read(self) -> Status:
        data = await self._reader.read(32)
        id_0, id_1, id_2, id_3, id_4, id_5, brightness, gpio_status, uptime = unpack('!BBBBBBHBxxxL', data)
        mac = f"{id_0:02X}:{id_1:02X}:{id_2:02X}:{id_3:02X}:{id_4:02X}:{id_5:02X}"
        brightness = brightness / 0xFFFF
        return Status(mac, brightness, gpio_status, uptime)

    async def get_updates(self) -> AsyncIterator[Status]:
        while True:
            yield await self._read()
