#    This file is part of the AutoAnime distribution.
#    Copyright (c) 2023 Kaif_00z
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
# License can be found in <
# https://github.com/kaif-00z/AutoAnimeBot/blob/main/LICENSE > .
#
# Also Thanks to Danish here

import asyncio
import json
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from pathlib import Path

import aiofiles
import aiohttp
from html_telegraph_poster import TelegraphPoster
from typing import Any, Dict, List, Optional, Union

OK = {}


def run_async(function):
    @wraps(function)
    async def wrapper(*args, **kwargs):
        return await asyncio.get_event_loop().run_in_executor(
            ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() * 5),
            partial(function, *args, **kwargs),
        )

    return wrapper


async def async_searcher(
    url: str,
    post: bool = False,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, str]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    ssl: bool = False,
    re_json: bool = False,
    re_content: bool = False,
    real: bool = False,
    *args,
    **kwargs,
):
    async with aiohttp.ClientSession(headers=headers) as client:
        if post:
            data = await client.post(
                url, json=json_data, data=data, ssl=ssl, *args, **kwargs
            )
        else:
            data = await client.get(url, params=params, ssl=ssl, *args, **kwargs)
        if re_json:
            return await data.json()
        if re_content:
            return await data.read()
        if real:
            return data
        return await data.text()


async def cover_dl(link: str) -> Optional[str]:
    try:
        image = await async_searcher(link, re_content=True)
        fn = f"thumbs/{link.split('/')[-1]}"
        if not fn.endswith((".jpg", ".png")):
            fn += ".jpg"
        async with aiofiles.open(fn, "wb") as file:
            await file.write(image)
        return fn
    except BaseException as e:
        print(f"Error in cover_dl: {e}")
        return None


async def mediainfo(file: Path, acc) -> Optional[str]:
    try:
        process = await asyncio.create_subprocess_exec(
            "mediainfo", str(file), "--Output=HTML", str(file), stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        out = stdout.decode()
        client = TelegraphPoster(use_api=True)
        client.create_api_token("Mediainfo")
        page = client.post(
            title="Mediainfo",
            author=(await acc.get_me()).first_name,
            author_url=f"https://t.me/{(await acc.get_me()).username}",
            text=out,
        )
        return page.get("url")
    except Exception as error:
        print(f"Error in mediainfo: {error}")
        return None


def code(data: dict) -> str:
    OK.update({len(OK): data})
    return str(len(OK) - 1)


def decode(key: str) -> Optional[dict]:
    if OK.get(int(key)):
        return OK[int(key)]
    return


def hbs(size: int) -> str:
    if not size:
        return ""
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


async def stats(e):
    try:
        wah = e.pattern_match.group(1).decode("UTF-8")
        ah = decode(wah)
        out, dl = ah.split(";")
        ot = hbs(int(Path(out).stat().st_size))
        ov = hbs(int(
