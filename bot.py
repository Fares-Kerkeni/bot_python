import discord
# client = discord.Client()

from discord.ext import commands


intents = discord.Intents.all()
intents.members= True
client = discord.Client(intents=intents)





client = commands.Bot(command_prefix="!")



# Welcome_channel = client.get_channel(978561467001487370)
# Help_channel = client.get_channel(978559580592283669)


@client.event
async def on_member_join(member):
    # await Welcome_channel.send('Bienvenue !'+ member.display_name)
    await member.send('test')

@client.command()
async def test(ctx):
    await ctx.send("test")



# événement a chaque fois qu'un msg est envoyé
#async -> en mm temp (plusieurs utilisateurs)
@client.event
async def on_message(message):
    message.content = message.content.lower()
    # lower met tout en minuscule

    if message.author == client.user:
        return
    # on vérifie que le msg ne vient pas de soi-même, cad le bot





    # envoyer dans le channel "bonjour" si le msg !hello est envoyé dans le bon channel
    # if message.channel == Help_channel and message.content.startswith('!aide'):
    #     await Help_channel.send('...')

    
    
    if message.content.startswith('!hello'):
        await message.channel.send('Bonjour ! :smiley:')

    if message.content == "!del":
        await message.channel.purge(limit=5)


    await client.process_commands(message)  
    #avec cette ligne, si on écrit !test on recoit test du @client.command()


# met le bot en ligne :
client.run("OTgwNTQ5OTY3ODYzMjM4NzE3.G6O0YM.q6XQaczvWXIY_6ecRxi0l622cd_8ro0Phfs6dw")







