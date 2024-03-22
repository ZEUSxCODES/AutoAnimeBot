import asyncio
import logging
import os
import sys
from logging import INFO, FileHandler, StreamHandler, basicConfig, getLogger
from traceback import format_exc

import apscheduler.schedulers.asyncio
import pyrogram
import redis
import telethon
from telethon.errors.rpcerrorlist import FloodWaitError

from .config import Var

basicConfig(
    format="%(asctime)s || %(name)s [%(levelname)s] : %(message)s",
    handlers=[
        FileHandler("AutoAnimeBot.log", mode="w", encoding="utf-8"),
        StreamHandler(),
    ],
    level=INFO,
    datefmt="%m/%d/%Y, %H:%M:%S",
)
LOGS = getLogger("AutoAnimeBot")
TelethonLogger = getLogger("Telethon")
TelethonLogger.setLevel(INFO)

MEM: dict[str, object] = {}


def main():
    LOGS.info(
        """
                        Auto Anime Bot
                ©️ t.me/kAiF_00z (github.com/kaif-00z)
                        v0.0.4 (original)
                             (2023)
                       [All Rigth Reserved]

    """
    )

    if os.cpu_count() < 4:
        LOGS.warning(
            "These Bot Atleast Need 4vcpu and 32GB Ram For Proper Functiong...\nExiting..."
        )
        exit()

    if not os.path.exists(".env"):
        LOGS.critical("The .env file is missing. Exiting...")
        exit()

    if not all([Var.API_ID, Var.API_HASH, Var.BOT_TOKEN, Var.REDIS_URI, Var.REDIS_PASS]):
        LOGS.critical("One or more required environment variables are missing. Exiting...")
        exit()

    if not os.path.exists("thumb.jpg"):
        os.system(f"wget {Var.THUMB} -O thumb.jpg")
    if not os.path.isdir("encode/"):
        os.mkdir("encode/")
    if not os.path.isdir("thumbs/"):
        os.mkdir("thumbs/")
    if not os.path.isdir("Downloads/"):
        os.mkdir("Downloads/")

    if not asyncio.run(internet_check()):
        LOGS.critical("No internet connection. Exiting...")
        exit()

    try:
        LOGS.info("Trying to Connect With Redis database")
        redis_info = Var.REDIS_URI.split(":")
        dB = redis.Redis(
            host=redis_info[0],
            port=redis_info[1],
            password=Var.REDIS_PASS,
            charset="utf-8",
            decode_responses=True,
        )
        if not dB.ping():
            LOGS.critical("Could not connect to Redis database. Exiting...")
            exit()
        LOGS.info("Successfully Connected to Redis database")
        ask_(dB)
        loader(MEM, dB, LOGS)
    except Exception as eo:
        LOGS.exception(format_exc())
        LOGS.critical(str(eo))
        exit()

    try:
        LOGS.info("Trying Connect With Telegram")
        bot = telethon.TelegramClient(None, Var.API_ID, Var.API_HASH).start(bot_token=Var.BOT_TOKEN)
        pyro = pyrogram
