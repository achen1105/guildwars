#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:35:25 2020

@author: anitachen
https://dev.to/p014ri5/making-and-deploying-discord-bot-with-python-4hep
https://github.com/hugonun/discord2sheet-bot
mainfeatures.py doesn't work, only main.py does currently'
"""

# BSD 3-Clause License
# Copyright (c) 2019, Hugonun(https://github.com/hugonun)
# All rights reserved.

import discord
from discord.ext import commands
import os
import json
from gsheet import *

client = discord.Client()
sheet = gsheet()
#default test sheet
SPREADSHEET_ID = '1-BsssPXufgAH2-n5ygUW662yAjHdvds8dzAfayifoc4';
RANGE_NAME = '\'member sheet\'!A3:A40';
RANGE_SAND = '\'member sheet\'!G3:G40';
RANGE_CRYSTAL = '\'member sheet\'!H3:H40';
FIELDS = 3;
token = os.getenv('DISCORD_BOT_TOKEN')

def getSettings(client, message):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        
    return settings[str(message.guild.id)];

bot = commands.Bot(command_prefix=getSettings)

@bot.event
async def on_guild_join(guild):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        
    settings[str(guild.id)] = ".";
    
    #write to json file
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4);    

@bot.event
async def on_guild_remove(guild):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        
    settings.pop(str(guild.id));
    
    #write to json file
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4);    
        
@bot.command()
async def changeprefix(ctx, prefix):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        
    settings[str(ctx.guild.id)] = prefix;
    
    #write to json file
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4);  
        
    
@bot.command(aliases=['mats', 'addmats'])
async def materials(ctx, arg1: int, arg2: int):
    #add reaction to message
    await ctx.send(f'added mats {arg1} and {arg2} :heart:');
    print("added mats");

@bot.command()
async def hello(ctx):
    await ctx.send(f'hello!! :heart:');
    print("said hello");
        
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
   # uses global variables to store
    global SPREADSHEET_ID
    global RANGE_NAME
    global RANGE_MATS
    global FIELDS
    
    if message.author == client.user:
        return
    
    # Restrict the command to a role
    # Change REQUIREDROLE to a role id or None
    REQUIREDROLE = None
    if REQUIREDROLE is not None and discord.utils.get(message.author.roles, id=str(REQUIREDROLE)) is None:
        await message.channel.send('You don\'t have the required role!')
        return

    # change spreadsheet ID
    if message.content.startswith('!sheetid'):
        msg2 = message.content[9:];
        SPREADSHEET_ID = msg2;
        await message.channel.send(f'Your sheet ID has been successfully changed to {msg2}!')
        print(SPREADSHEET_ID);
        
    # change range name
    if message.content.startswith('!rangename'):
        msg4 = message.content[11:];
        RANGE_NAME = msg4;
        await message.channel.send(f'Your rangename has been successfully changed to {msg4}!')
        print(RANGE_NAME);
        
    # Command to insert data to excel
    if message.content.startswith('!s '):

        # Code
        msg = message.content[3:]
        result = [x.strip() for x in msg.split(',')]
        if len(result) == FIELDS:
            # Add
            print(message.created_at)
            #name = [message.author.name] + [str(message.created_at)]
            #sheet.add(SPREADSHEET_ID, RANGE_NAME, name)
            
            nameValues = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
            rows = result.get('values', [])
            print('{0} rows retrieved.'.format(len(rows)))
            
            ign = len[0]
            for x in nameValues:
                if ign == x:
                    await message.channel.send('Your data has been successfully submitted!')
            
            sheet.add(SPREADSHEET_ID, RANGE_MATS, result)
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
    
    # Non sheet related
    # Color roles
    if message.content.startswith('!changecolor'):
        msg3 = message.content[13:];
        hexcode = '0x'+msg3;
        await message.guild.create_role(name=message.author.name, color=discord.Color(hexcode));
        role = discord.utils.get(message.guild.roles, name=message.author.name)
        await role.edit(position(1));
        await message.author.add_roles(role);
    
    # Fun responses
    if message.content.find("hello momo") != -1:
        await message.channel.send(f'Hello {message.author.mention}! :two_hearts:');


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
