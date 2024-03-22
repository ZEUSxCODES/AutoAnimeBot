# This file is part of the AutoAnime distribution.
# Copyright (c) 2023 Kaif_00z
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# License can be found in <https://github.com/kaif-00z/AutoAnimeBot/blob/main/LICENSE> .

import json
import sys

import aiohttp
from aiohttp import ClientSession

import asyncio
import time

import os
import re

import logging

import requests
from bs4 import BeautifulSoup

import pytz
from datetime import datetime

import telebot
from telebot import types

import psycopg2
from psycopg2 import sql

import traceback

import config
from . import Var, bot, reporter, POST_TRACKER, get_english

async def shu_msg():
    if Var.SEND_SCHEDULE:
        try:
            async with ClientSession() as ses:
                res = await ses.get(
                    "https://subsplease.org/api/?f=schedule&h=true&tz=Asia/Kolkata"
              
