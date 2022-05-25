import discord
import random
client = discord.Client()

from discord.ext import commands

default_intents = discord.Intents.default()
default_intents.members= True
client = discord.Client(intents=default_intents)



client = commands.Bot(command_prefix="!")

@client.event
async def on_member_join(member):
    welcome_channel = client.get_channel(978561467001487370)
    await welcome_channel.send('Bienvenue !' + member.display_name)

# événement a chaque fois qu'un msg est envoyé

joke = {
    "Qu'est ce qui est jaune et qui attend" : "jonathan",
    "Qu'est ce qui est transparent et qui cours dans un champ" : "un troupeau de vitre",
    "qu'est ce qui clash tout le monde alors qu'elle est susceptible de baisée ?? " : "Fara"
}

#async -> en mm temp (plusieurs utilisateurs)
@client.event
async def on_message(message):
    message.content = message.content.lower()
    # lower met tout en minuscule

    if message.author == client.user:
        return

    joke_channel = client.get_channel(978573528297250817)

    if message.channel == joke_channel and message.content.startswith('!joke'):
        await joke_channel.send('coucou')

    if message.content.startswith('!hello'):
        await message.channel.send('coucou')

    if message.content == "!del":
        await message.channel.purge(limit=10)

    await client.process_commands(message)  
    #avec cette ligne, si on écrit !test on recoit test du @client.command()

# met le bot en ligne :
client.run("OTc4NTU5Njg0MjQxOTQ0NTk2.GgybG2.lr-nnSvwkVttprTn7XcZnvtpR1Y5gwYW325K40")





# -------------------------------- nolan --------------------------------



















# -------------------------------- nolan --------------------------------




# -------------------------------- nolan --------------------------------

client.run("OTc4NTU5Njg0MjQxOTQ0NTk2.G8CrV2.sBKSZB__b9xOufWxN4f1VX96ZVKz-r9qlgwdTA")
