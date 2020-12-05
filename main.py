#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:35:25 2020

@author: anitachen
https://dev.to/p014ri5/making-and-deploying-discord-bot-with-python-4hep
"""

import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix=".")
#token = os.getenv("DISCORD_BOT_TOKEN")

@client.event
async def on_ready() :
    print("I am online")

client.run("Nzg0OTA1OTY2ODEwMzAwNDM3.X8wGpQ.blUmtLU5ArEFUd2jEoctL4fnaQs")