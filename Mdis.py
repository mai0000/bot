import discord
import codecs
import asyncio
import sys
from discord.ext import commands
from discord.utils import get
from discord.ext.tasks import loop
from discord.ext.commands import Bot
from random import choice
import random
import string

Token = "NjI2NzE3MDQzODE0Njk0OTIz.XsgLrg.sMEUgJaKKcEQTca8lqBAZitoC84" #Discord bot Token

def after(value, a):
    # Find and validate first part.
    pos_a = value.rfind(a)
    if pos_a == -1: return ""
    # Returns chars after the found string.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= len(value): return ""
    return value[adjusted_pos_a:]

client=commands.Bot(command_prefix="+")

@client.event
async def on_ready():
    print("Bot is ready.")

colours = [discord.Colour(0xe91e63), discord.Colour(0x0000FF0), discord.Colour(0x00FF00), discord.Colour(0xFF0000)]

guild_id = 706915363346186362
role_name = "colorful"
role_to_change = None

@loop(seconds=1)
async def colour_change():
    time.sleep(random.randint(0.25,1))
    await role_to_change.edit(colour=choice(colours))
    print("Task")

@colour_change.before_loop
async def colour_change_before():
    global role_to_change
    await client.wait_until_ready()
    guild = client.get_guild(guild_id)
    role_to_change = get(guild.roles, name=role_name)

@client.event
async def on_voice_state_update(member,before,after):
    Duo = [707189396582957187, 707189940500430879, 707190494261805176, 707202298882818069, 707202329295716382]
    Squad = [707246769720918078,707246739060686888,707248757477081189,707248729937412228,707246796250021889,707248779866406924,707246680545689714,707246705069785129,707248814054047754,707248712686239745]
    channel = get(member.guild.channels, name="system-bot")
    if member.voice == None:
        embed = discord.Embed(title="User : {}".format(member.name), description="มีการออกจากระบบ Voice chat!", color=0x00ff00)
        embed.add_field(name="{}".format(member.name), value="ออกจาก Voice chat ทั้งหมดแล้วค่ะ!")
        await channel.send(embed=embed)

        for cid in member.guild.voice_channels:
            members = cid.members
            memids = []
            for membera in members:
                memids.append(membera.id)
            nummen = len(memids)
            if cid.id in Duo:
                if nummen != 2:
                    await cid.edit(name="〘🟦〙[ Duo ]")
            elif cid.id in Squad:
                if nummen != 4:
                    await cid.edit(name="〘🟦〙[ Squad ]")
    else:
        voice_channel = member.voice.channel
        if before.channel is None and after.channel is not None:
            embed = discord.Embed(title="ห้อง {}".format(str(voice_channel.name)), description="มีการเข้าสู่ห้อง Voice chat!", color=0x00ff00)
            embed.add_field(name="{}".format(member.name), value="เข้าสู่ห้องแล้ว!")
            await channel.send(embed=embed)
        members = voice_channel.members
        memids = []
        for membera in members:
            memids.append(membera.id)
        nummem = len(memids)
        if voice_channel.id in Duo:
            if nummem == 2:
                await voice_channel.edit(name="〘🟥〙[ Duo ]")
        elif voice_channel.id in Squad:
            if nummem == 4:
                await voice_channel.edit(name="〘🟥〙[ Squad ]")
        for cid in member.guild.voice_channels:
            members = cid.members
            memids = []
            for membera in members:
                memids.append(membera.id)
            nummen = len(memids)
            if cid.id in Duo:
                if nummen != 2:
                    await cid.edit(name="〘🟦〙[ Duo ]")
            elif cid.id in Squad:
                if nummen != 4:
                    await cid.edit(name="〘🟦〙[ Squad ]")


@client.event
async def on_message(message):
    bad_words = []
    with codecs.open("bad.txt", 'r', encoding='utf8') as f:
        for line in f:
            bad_words.append(line.strip())

    for word in bad_words:
        if message.content.count(word) > 0:
            await message.channel.purge(limit=1)
            await message.channel.send("กรุณาอย่าพูดคำหยาบ!, {}".format(message.author.mention))

    print('{} has sent a message : {}'.format(message.author,message.content))
    await client.process_commands(message)

@client.event
async def on_member_join(member):
    channel = get(member.guild.channels, name="general")
    await channel.send('welcome to our discord server!') 

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.command()
async def echo(ctx, *args):
    output = ''
    for word in args:
        output += str(word)
        output += ' '
    await ctx.send(output)
    
@client.command()
async def ชื่อ(ctx, *, nickname):
    member = ctx.message.author
    role = discord.utils.get(member.guild.roles, name="〘  Member  〙")
    roler = discord.utils.get(member.guild.roles, name="ยังไม่ยืนยันตัวเอง")
    await ctx.author.edit(nick="K' {}".format(nickname))
    await ctx.send("เปลี่ยนชื่อเล่นเป็น K' {} เรียบร้อยแล้วค่ะ, {}".format(nickname, member.mention))
    await member.add_roles(role)
    await member.remove_roles(roler)

@client.command()
async def dev(ctx):
    embed = discord.Embed(title="[ Dev by : ]", description=" :> ", color=0x00ff00)
    embed.add_field(name="unusual", value="bot creator")
    embed.add_field(name="M", value="???")
    await ctx.send(embed=embed)

@client.command()
async def บล็อค(ctx, *args):
    output = ''
    for word in args:
        output += str(word)
    if output != "":
        with codecs.open("bad.txt", 'a', encoding='utf8') as f:
            f.write('\n{}'.format(output))
            f.close()
        await ctx.send("เพิ่มคำหยาบแล้วค่ะ!")
    else:
        await ctx.send("กรุณาอย่าเว้นช่องว่างค่ะ")

@client.command(pass_context=True)
async def clear(ctx, amount=1000):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=amount):
                messages.append(message)

    await channel.delete_messages(messages)
    await ctx.send('ลบข้อความเรียบร้อยแล้วค่ะ')

@client.command(pass_context=True)
async def exit(ctx):
    sys.exit(0)


#client.loop.create_task(background_task())
colour_change.start()
client.run(Token) 