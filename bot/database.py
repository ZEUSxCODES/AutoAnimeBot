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

import ast

from . import MEM, dB

def get_memory(quality, from_memory=False):
    if from_memory:
        return MEM.get(f"MEM_{quality}") or []
    value = dB.get(f"MEM_{quality}")
    return value.decode() if value else "[]"

