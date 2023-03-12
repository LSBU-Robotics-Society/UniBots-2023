import asyncio
import websockets
from cmd_list import *
import settings


async def send_command_main(str_command):
    async with websockets.connect(settings.SIM_WS_ADDRESS) as websocket:
        await websocket.send(str_command)


async def get_image_main():
    async with websockets.connect(settings.SIM_WS_ADDRESS) as websocket:
        await websocket.send(CMD_SIM_IMAGE)
        image = await websocket.recv()
        return image


def get_image():
    return asyncio.run(get_image_main())


def send_command(str_command):
    asyncio.run(send_command_main(str_command))

