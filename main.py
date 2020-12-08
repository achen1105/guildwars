#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:35:25 2020

@author: anitachen
https://dev.to/p014ri5/making-and-deploying-discord-bot-with-python-4hep
https://github.com/hugonun/discord2sheet-bot
"""

# BSD 3-Clause License
# Copyright (c) 2019, Hugonun(https://github.com/hugonun)
# All rights reserved.

import discord
from discord.ext import commands
import os
from gsheet import *

client = discord.Client()
sheet = gsheet()

token = os.getenv('DISCORD_BOT_TOKEN')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Restrict the command to a role
    # Change REQUIREDROLE to a role id or None
    REQUIREDROLE = None
    if REQUIREDROLE is not None and discord.utils.get(message.author.roles, id=str(REQUIREDROLE)) is None:
        await message.channel.send('You don\'t have the required role!')
        return

    # Command to insert data to excel
    if message.content.startswith('!s '):
        SPREADSHEET_ID = '1FMndMT4e6RX1SEzgwLuDDv-ANN75WxbnLAa0CW5JQvk' # Add ID here
        RANGE_NAME = 'A1'
        FIELDS = 2 # Amount of fields/cells

        # Code
        msg = message.content[3:]
        result = [x.strip() for x in msg.split(',')]
        if len(result) == FIELDS:
            # Add
            print(message.created_at)
            DATA = [message.author.name] + [str(message.author.id)] + [str(message.created_at)] + result
            sheet.add(SPREADSHEET_ID, RANGE_NAME, DATA)
            await message.channel.send('Your data has been successfully submitted!')
        else:
            # Needs more/less fields
            await message.channel.send('Error: You need to add {0} fields, meaning it can only have {1} comma.'.format(FIELDS,FIELDS-1))
    
    # Whois
    # Please dont remove the copyright and github repo
    elif len(message.mentions) > 0:
        for muser in message.mentions:
            if muser.id == client.user.id:
                if any(word in message.content for word in ['whois','who is','Help','help','info']):
                    await message.channel.send('This bot was made by hugonun(https://github.com/hugonun/).\nSource code: https://github.com/hugonun/discord2sheet-bot\nEdited by Jia#4778 https://github.com/achen1105')


client.run(token); # Add bot token here

"""
import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix=".")
token = os.getenv('DISCORD_BOT_TOKEN')

@client.event
async def on_ready() :
    print("I am online")
    
@client.command(aliases=['addmats', 'add mats'])
async def mats(ctx, *, materials):
    await ctx.send(f'test added {materials}');
    print("added mats");

@client.command()
async def materials(ctx, arg1: int, arg2: int):
    #add reaction to message
    await ctx.send(f'added mats {arg1} and {arg2} :heart:');
    print("added mats");

@client.event
async def on_message(message):
    # Hello Momo
    if message.content.find("hello momo") != -1:
        await message.channel.send(f'Hello {message.author.mention}! :two_hearts:');

client.run(token);
"""
