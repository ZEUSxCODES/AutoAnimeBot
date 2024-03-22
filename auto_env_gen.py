import asyncio
import os
import random
import sys
import argparse
import getpass
import pathlib
import signal
import aiosignals
import aiorredlock
import telethon
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.contacts import UnblockRequest
from telethon.errors import SessionPasswordNeededError
from telethon.errors.rpcerrorlist import PeerFloodError
from telethon.extensions import PlatformTelegramClient
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union
from urllib.parse import urlparse
import logging
import pydantic
from contextlib import suppress
from functools import partial
import aioredlock

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

try:
    from telethon_session_server import PlatformStringSession
except ModuleNotFoundError:
    print("Downloading telethon-session-server...")
    os.system(f"{sys.executable} -m pip install telethon-session-server")

DATA_SCHEMA = pydantic.BaseModel(
    dict(
        bot_token=str,
        main_channel=str,
        log_channel=str,
        cloud_channel=str,
        redis_uri=Optional[str],
        redis_password=Optional[str],
        owner_id=int,
    )
)

class Data(DATA_SCHEMA):
    @property
    def bot_token(self) -> str:
        return self.dict["bot_token"]

async def get_api_id_and_hash() -> Union[tuple[int, str], None]:
    api_id = int(input("Enter your API_ID: "))
    if not api_id:
        return None
    api_hash = getpass.getpass("Enter your API_HASH: ")
    if not api_hash:
        return None
    return api_id, api_hash

async def generate_session_string(api_id: int, api_hash: str) -> str:
    async with PlatformTelegramClient(
        PlatformStringSession(f"{api_id}:{api_hash}"), api_id, api_hash
    ) as client:
        return str(client.session.save())

def get_redis_uri_and_password() -> tuple[str, str]:
    redis_uri = input("Enter your Redis URI: ")
    redis_pass = input("Enter your Redis Password: ")
    return redis_uri, redis_pass

async def create_channel(client, title):
    try:
        r = await client(
            CreateChannelRequest(
                title=title,
                about="Made By https://github.com/kaif-00z/AutoAnimeBot",
                megagroup=False,
            )
        )

        created_chat_id = r.chats[0].id
        return f"-100{created_chat_id}"
    except PeerFloodError:
        print("Unable to Create Channel due to Flood Error...")
        sys.exit(1)
    except BaseException:
        print("Unable to Create Channel...")
        print(format_exc())
        sys.exit(1)

def generate_env(data: Data):
    env_txt = f"""
BOT_TOKEN={data.bot_token}
MAIN_CHANNEL={data.main_channel}
LOG_CHANNEL={data.log_channel}
CLOUD_CHANNEL={data.cloud_channel}
REDIS_URI={data.redis_uri}
REDIS_PASSWORD={data.redis_password}
OWNER={data.owner_id}
"""
    env_path = pathlib.Path(".env")
    with env_path.open("w") as f:
        f.write(env_txt.strip())
    print("Succesfully Generated .env File Don't Forget To Save It! For Future Uses.")

async def auto_maker(data: Data):
    async with aiosignals.Signal(signal.SIGTERM) as term_signal:
        async with aioredlock.FileLock(".env.lock"):
            api_id, api_hash = await get_api_id_and_hash()
            if api_id is None or api_hash is None:
                print("API_ID and HASH Not Found!")
                sys.exit(1)
            string_session = await generate_session_string(api_id, api_hash)
            print(string_session)
            async with PlatformTelegramClient(
                PlatformStringSession(string_session), api_
