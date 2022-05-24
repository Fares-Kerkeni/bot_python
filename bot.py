import discord
client = discord.Client()

from discord.ext import commands

default_intents = discord.Intents.default()
default_intents.members= True
client = discord.Client(intents=default_intents)
client = commands.Bot(command_prefix="!")

@client.command()
async def test(ctx):
    await ctx.send("test")

@client.event
async def on_member_join(member):
    welcome_channel = client.get_channel(978561467001487370)
    await welcome_channel.send('Bienvenue !' + member.display_name)

# événement a chaque fois qu'un msg est envoyé
#async -> en mm temp (plusieurs utilisateurs)
@client.event
async def on_message(message):
    message.content = message.content.lower()
    # lower met tout en minuscule

    if message.author == client.user:
        return
    # on vérifie que le msg ne vient pas de soi-même, cad le bot

    Help_channel = client.get_channel(978559580592283669)

    # envoyer dans le channel "bonjour" si le msg !hello est envoyé dans le bon channel
    if message.channel == Help_channel and message.content.startswith('!aide'):
        await Help_channel.send('coucou')

    if message.content.startswith('!hello'):
        await message.channel.send('coucou hibou ! :smiley:')

    if message.content == "!del":
        await message.channel.purge(limit=5)

    await client.process_commands(message)  
    #avec cette ligne, si on écrit !test on recoit test du @client.command()

# met le bot en ligne :
client.run("OTc4NTU5Njg0MjQxOTQ0NTk2.GgybG2.lr-nnSvwkVttprTn7XcZnvtpR1Y5gwYW325K40")

# -------------------------------- nolan --------------------------------



# -------------------------------- nolan --------------------------------





