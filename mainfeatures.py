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
from gsheetfeatures import *

sheet = gsheetfeatures()
# Specific to guild
SPREADSHEET_ID = os.getenv('sheetID');
RANGE_NAME = '\'member sheet\'!A3:A40';
RANGE_SAND = 'member sheet!G';
RANGE_CRYSTAL = 'member sheet!H';
FIELDS = 3;
token = os.getenv('DISCORD_BOT_TOKEN')
client = commands.Bot(command_prefix="!")

# client commands
@client.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.message.author.mention}! :revolving_hearts:');
    print("We have said hello");
        
# client events    
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
   # uses global variables to store
    global SPREADSHEET_ID
    global RANGE_NAME
    global RANGE_SAND
    global RANGE_CRYSTAL
    global FIELDS
    
    if message.author == client.user:
        return
    
    # Restrict the command to a role, not used
    # Change REQUIREDROLE to a role id or None
    REQUIREDROLE = None
    if REQUIREDROLE is not None and discord.utils.get(message.author.roles, id=str(REQUIREDROLE)) is None:
        await message.channel.send('You don\'t have the required role!')
        return
    
    if message.content.startswith('!s help'):
        await message.channel.send(':cherry_blossom: Please input your guild wars materials in the form `!s <LN username>, <sand>, <crystals>`. Example:\n> !s Nikki, 62, 54\n:cherry_blossom: If your mats were succesfully submitted, there will be a confirmation message and a green check mark react!')
        
    # Command to insert data to excel
    elif message.content.startswith('!s '):

        # Code
        msg = message.content[3:]
        result = [x.strip() for x in msg.split(',')]
        if len(result) == FIELDS: 
            
            ign = result[0];
            lnnamesformat = [];
            # lnnames stores list of list, lnnnamesformat stores plain list of strings
            lnnames = sheet.getColumn(SPREADSHEET_ID, RANGE_NAME);
            for x in lnnames:
                lnnamesformat.append((x[0]));
           
            #testing
            #print(lnnamesformat);
            #print(ign);
            #print(result[1]);
            #print(result[2]);
            
            if ign in lnnamesformat:
                index  = lnnamesformat.index(ign);
                # [result[1]] because value must be a list
                #index plus 3 because sheet starts at G3 and H3
                sheet.updateNumbers(SPREADSHEET_ID, RANGE_SAND+str(index+3), [result[1]]); 
                sheet.updateNumbers(SPREADSHEET_ID, RANGE_CRYSTAL+str(index+3), [result[2]]);
                await message.add_reaction("✅");
                await message.channel.send(f'{message.author.name}, your materials have been successfully submitted to the sheet! :heart:')
                print("Added successfully"); 
            else:
                await message.channel.send('Sorry, I could not find your LN username in the master sheet.  Please try again :two_hearts:')
                print("In game name not found");
                
        else:
            # Needs more/less fields
            await message.channel.send(':cherry_blossom: Friendly reminder that there should be {0} fields with {1} commas! Example:\n> !s Nikki, 62, 54'.format(FIELDS,FIELDS-1))
            print('Error: You need to add {0} fields, meaning it has {1} comma(s).'.format(FIELDS,FIELDS-1))
    
    # Whois
    # Please dont remove the copyright and github repo
    elif len(message.mentions) > 0:
        for muser in message.mentions:
            if muser.id == client.user.id:
                if any(word in message.content for word in ['whois','who is','Help','help','info']):
                    await message.channel.send('This bot was made by hugonun(https://github.com/hugonun/).\nSource code: https://github.com/hugonun/discord2sheet-bot\nEdited by Jia#4778 <https://github.com/achen1105>')
        
    # Fun responses
    if message.content.find("I love guild wars") != -1:
        await message.channel.send(f'So do I! :heart_exclamation:');
    
    #extremely important!!  add at the end of on_message or otherwise commands will not work
    await client.process_commands(message);


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
"""
# used for changing prefixes for more than one server, won't work with heroku
def getSettings(client1, message):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        
    return settings[str(message.guild.id)];
    print("get settings was called");

@client.event
async def on_guild_join(guild):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        
    settings[str(guild.id)] = "!";
    
    #write to json file
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4);  
        print("on guild join");

@client.event
async def on_guild_remove(guild):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        
    settings.pop(str(guild.id));
    
    #write to json file
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4);    
        
@client.command()
async def changeprefix(ctx, prefix):
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        
    settings[str(ctx.guild.id)] = prefix;
    
    #write to json file
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4);     
    
    await ctx.send(f'Prefix changed to {prefix} :sparkling_heart:');
    
    # Non sheet related
    # Color roles, doesn't work
    if message.content.startswith('!changecolor'):
        msg3 = message.content[13:];
        hexcode = '0x'+msg3;
        await message.guild.create_role(name=message.author.name, color=discord.Color(hexcode));
        role = discord.utils.get(message.guild.roles, name=message.author.name)
        await role.edit(position(1));
        await message.author.add_roles(role);
"""