from ast import Str
import discord
from discord.ext import commands
from random import randint
import random
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select


client = commands.Bot(command_prefix="=")
DiscordComponents(client)


@client.command()
async def aide(ctx):
    if ctx.channel.id == 978573528297250817:
        await ctx.send("help joke")
    elif ctx.channel.id == 980060663462391839:
        await ctx.send("help tictactoe")
    elif ctx.channel.id == 980124791652646972:
        await ctx.send("help pendu")
    elif ctx.channel.id == 980145249005494293:
         await ctx.send("help tu preferes")
    elif ctx.channel.id == 980407531623030954:
         await ctx.send("help plus ou moins")
    else :
        await ctx.send("vous pouvez utiliser cette commande que dans le channel joke, pendu, tictactoe, tu-preferes et plus-ou-moins")

@client.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)
        
# ----------------------------------------------- TIC TAC TOE ----------------------------------------------- #

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

# tableau des possibilité de win
winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

# fonction pour lancer le jeu
@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    if ctx.channel.id == 980060663462391839:
        # recupere les variables qui sont en dehors de la fonction
        global count
        global player1
        global player2
        global turn
        global gameOver

        if gameOver:
            global board
            board = [
                        ":white_large_square:", ":white_large_square:", ":white_large_square:",
                        ":white_large_square:", ":white_large_square:", ":white_large_square:",
                        ":white_large_square:", ":white_large_square:", ":white_large_square:"
                    ]
            turn = ""
            gameOver = False
            count = 0

            player1 = p1
            player2 = p2

            # affiche le tableau
            line = ""
            for x in range(len(board)):
                # si c'est la case 2 5 ou 8 ca saute une ligne
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            # determine qui sera le premier a jouer
            num = random.randint(1, 2)
            # passe la variable turn sur la personne qui doit jouer et la mentionne
            if num == 1:
                turn = player1
                await ctx.send("c'est le tour de <@" + str(player1.id) + ">")
            elif num == 2:
                turn = player2
                await ctx.send("c'est le tour de <@" + str(player2.id) + ">")
        # Demande aux utilisateurs de finir leur partie avant d'en commencer une autre
        else:
            await ctx.send("il y a deja une partie en cours")
    else : 
        await ctx.send("cette commande marche que dans le channel tictactoe")

# fonction pour placer les markeur
@client.command()
async def place(ctx, pos: int):
    if ctx.channel.id == 980060663462391839:
        # recupere les variables qui sont en dehors de la fonction
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                # change le markeur en fonction du tour de la personne qui doit jouer
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                # verifie si c bien entre 1 et 9 et si c'est pas déjà remplie
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                    # si c'est pas remplie ca remplace le carré blanc par le markeur de la personne qui a jouer
                    board[pos - 1] = mark
                    count += 1

                    # affiche le tableau
                    line = ""
                    for x in range(len(board)):
                        # si c'est la case 2 5 ou 8 ca saute une ligne
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    # verifie si quelqu'un a gagné
                    checkWinner(winningConditions, mark)
                    print(count)
                    # si quelqu'un a gagné, ca met le markeur + win
                    if gameOver == True:
                        await ctx.send(mark + " a gagné")
                    # si count est > 9 et que personne a gagné c'est une égalité
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("Egalité")

                    # si c'était le tour de la personne 1 c'est a la personne 2 de jouer et inversement
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                # verifie si l'utilisateur entre bien un chiffre entre 1 et 9 et si c'est pas déjà rempli d'un signe
                else:
                    await ctx.send("Il faut choisir un chiffre entre 1 et 9 et une case pas déjà rempli")
            # envoie ce message a l'utilisateur si c'est pas a son tour de jouer
            else:
                await ctx.send("Ce n'est pas ton tour")
        # demande de lancer une nouvelle partie a l'utilisateur
        else:
            await ctx.send("Lance une nouvelle partie avec =tictactoe")
    else : 
        await ctx.send("cette commande marche que dans le channel tictactoe")
        
# fonction pour verifier qui est le gagnant
def checkWinner(winningConditions, mark):
    global gameOver
    # parcours tout le tableau winningConditions
    for condition in winningConditions:
        # si une des lignes du tableau est rempli du meme signe le partie se fini
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

# fonction pour gerer les erreurs lors de la creation du jeu
@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    # verifie si la personne a bien mentionner 2 utilisateurs
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Mentionne 2 personnes")
    # envoie un message d'erreur si la personne a mal mentionner 
    elif isinstance(error, commands.BadArgument):
        await ctx.send("La mention n'est pas bonne")

# fonction pour gerer les erreurs lors du placement
@place.error
async def place_error(ctx, error):
    # si la personne a oublié de préciser la position de la case ou il veut jouer
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Precise la case ou tu veux placer ton markeur")
    # si l'utilisateur n'entre pas un chiffre 
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Entre un chiffre")

# ----------------------------------------------- TIC TAC TOE ----------------------------------------------- #

# ------------------------------------------------- BLAGUES ------------------------------------------------- #

blagues = [
    ["Pourquoi Harry Potter chuchotte","par ce que Dumbledore","Une personne dort","Directeur de Poudlard"],
    ["Qu'est ce qui est transparent et qui cours dans un champ","un troupeau de vitre","Un troupeau de ...","il y en a 2 a l'avant et 2 a l'arriere d'une voiture"],
    ["Qu'est ce qui est jaune et qui attend","jonathan","C'est un prenom","Il faut lier 2 mots"]
]

reponse = ""
question = ""
blague_aleatoire = 0

# fonction pour lancer une blague
@client.command()
async def joke(ctx):
    if ctx.channel.id == 978573528297250817:
        # recupere les variables qui sont en dehors de la fonction
        global blagues
        global reponse
        global question
        global blague_aleatoire
        
        # si il y a deja une blague en cours ca previent l'utilisateur  
        if question != "" :
            await ctx.send("Il y a déjà une blague en cours, trouvez la réponse ou entre !give_reponse pour obtenir la réponse")
        # envoie une blague a l'utilisateur
        else :
            blague_aleatoire = randint(0,len(blagues) - 1)
            question = blagues[blague_aleatoire][0]
            reponse = blagues[blague_aleatoire][1]
            await ctx.send(question)
    else : 
        await ctx.send("cette commande marche que dans le channel joke")

# fonction pour demander la reponse
@client.command()
async def give_blague(ctx):
    if ctx.channel.id == 978573528297250817:
        # recupere les variables qui sont en dehors de la fonction
        global blagues
        global reponse
        global question
        global blague_aleatoire

        # si il n y a pas de blague en cours ca previent l'utilisateur  
        if question == "":
            await ctx.send("vous devez d'abord utiliser la commande !joke pour avoir une blague")
        # envoie la reponse
        else :
            await ctx.send(reponse)
            reponse = ""
            question = ""
    else : 
        await ctx.send("cette commande marche que dans le channel joke")

# fonction pour essayer de trouver la blague
@client.command()
async def answer(ctx, *args):
    if ctx.channel.id == 978573528297250817:
        # recupere les variables qui sont en dehors de la fonction
        global blagues
        global reponse
        global question
        global blague_aleatoire
        sentence = ""
        i = 0
        # recpuere tous les mots que l'utilisateur a entré après la commande answer
        for words in args :
            i = i + 1
            # met tous les mots les uns a la suite des autres avec un espace entre chaque mots
            sentence = sentence + words
            # si c'est le dernier mot ce ne met pas d'espace
            if i < len(args) :
                sentence = sentence + " "

        # si il n y a pas de blague en cours ca previent l'utilisateur  
        if question == "":
            await ctx.send("vous devez d'abord utiliser la commande !joke pour avoir une blague")
        # compare la reponse de l'utilisateur a la reponse de la blague
        elif sentence == reponse :
            await ctx.send("Bravo tu as trouvé la réponse")
            reponse = ""
            question = ""
        else :
            await ctx.send("Essaye encore ou entre !give_reponse")
    else : 
        await ctx.send("cette commande marche que dans le channel joke")

@client.command()
async def indice(ctx, num_indice : int):
    if ctx.channel.id == 978573528297250817:
        # recupere les variables qui sont en dehors de la fonction
        global blagues
        global reponse
        global question
        global blague_aleatoire
        # si il n y a pas de blague en cours ca previent l'utilisateur  
        if question == "":
            await ctx.send("vous devez d'abord utiliser la commande !joke pour avoir une blague")
        # si il entre indice 1
        elif num_indice == 1 :
            await ctx.send(blagues[blague_aleatoire][2])
        # si il entre indice 2
        elif num_indice == 2 :
            await ctx.send(blagues[blague_aleatoire][3])
        # sinon ca dit a l'utilisateur ce qu'il doit entrer
        else : 
            await ctx.send("Entrez !indice 1 ou !indice 2 selon l'indice que vous voulez")
    else : 
        await ctx.send("cette commande marche que dans le channel joke")

# ------------------------------------------------- BLAGUES ------------------------------------------------- #

# -------------------------------------------------- PENDU -------------------------------------------------- #

pendu_facile = ["chat","bleu","vert","moto"]
pendu_moyen = ["oiseau","joyaux","joueur","lettre"]
pendu_difficile = ["baguette","elephant","tracteur","vehicule"]

letter_versus_emoji = [
    ["a",":regional_indicator_a:"],
    ["b",":regional_indicator_b:"],
    ["c",":regional_indicator_c:"],
    ["d",":regional_indicator_d:"],
    ["e",":regional_indicator_e:"],
    ["f",":regional_indicator_f:"],
    ["g",":regional_indicator_g:"],
    ["h",":regional_indicator_h:"],
    ["i",":regional_indicator_i:"],
    ["j",":regional_indicator_j:"],
    ["k",":regional_indicator_k:"],
    ["l",":regional_indicator_l:"],
    ["m",":regional_indicator_m:"],
    ["n",":regional_indicator_n:"],
    ["o",":regional_indicator_o:"],
    ["p",":regional_indicator_p:"],
    ["q",":regional_indicator_q:"],
    ["r",":regional_indicator_r:"],
    ["s",":regional_indicator_s:"],
    ["t",":regional_indicator_t:"],
    ["u",":regional_indicator_u:"],
    ["v",":regional_indicator_v:"],
    ["w",":regional_indicator_w:"],
    ["x",":regional_indicator_x:"],
    ["y",":regional_indicator_y:"],
    ["z",":regional_indicator_z:"],
    ["-",":blue_square:"]
]

essai_versus_image = [
    [1,'essai_1.PNG'],
    [2,'essai_2.PNG'],
    [3,'essai_3.PNG'],
    [4,'essai_4.PNG'],
    [5,'essai_5.PNG'],
    [6,'essai_6.PNG'],
    [7,'essai_7.PNG'],
    [8,'essai_8.PNG'],
    [9,'essai_9.PNG'],
    [10,'essai_10.PNG'],
    [11,'essai_11.PNG'],
    [12,'essai_12.PNG']
]    

mot_a_trouver = ""
mot_en_recherche = ""
essais = 0

# fonction pour lancer le pendu
@client.command()
async def pendu(ctx, difficulte = ""):
    # verifie si l'utilisateur est bien dans le canal pendu
    if ctx.channel.id == 980124791652646972:
        global pendu_facile
        global pendu_moyen
        global pendu_difficile
        global mot_aleatoire
        global mot_a_trouver
        global mot_en_recherche
        global essais
        global essai_versus_image
        # si l'utilisateur n'a pas lancer le jeu alors ca le lance
        if mot_a_trouver == "" :
            # si il a choisis facile alors ca prend un mot aleatoire dans le tableau facile
            if difficulte == "facile":
                mot_aleatoire = randint(0,len(pendu_facile) - 1)
                mot_a_trouver = pendu_facile[mot_aleatoire]
                mot_en_recherche = "----"
            # si il a choisis moyen alors ca prend un mot aleatoire dans le tableau moyen
            elif difficulte == "moyen":
                mot_aleatoire = randint(0,len(pendu_moyen) - 1)
                mot_a_trouver = pendu_moyen[mot_aleatoire]
                mot_en_recherche = "------"
            # si il a choisis difficile alors ca prend un mot aleatoire dans le tableau difficile
            elif difficulte == "difficile":
                mot_aleatoire = randint(0,len(pendu_difficile) - 1)
                mot_a_trouver = pendu_difficile[mot_aleatoire]
                mot_en_recherche = "--------"
            # si il a pas entré de difficulté ou une mauvaise difficulté, ca lui explique ce qu'il doit faire
            else :
                await ctx.send("Il faut choisir une difficulté entre facile/moyen/difficile")
                return
            # affiche le mot qui est en train d'etre recherché ( 4 cases vides pour le moment ) et affiche les commandes qu'il doit utiliser
            mot_letter_to_emoji = letter_to_emoji(mot_en_recherche)
            await ctx.send("Entrez =try_letter avec la lettre que vous voulez derriere ou =try_word avec le mot que vous voulez derriere, si vous voulez la reponse tapez : =give_pendu")
            await ctx.send(mot_letter_to_emoji)
            essais = 0
        # si il a deja une partie en cours ca le previent
        else :
            await ctx.send("Il y a deja un pendu en cours, finissez le ou entrez =give_pendu pour avoir la reponse et pouvoir lancer une nouvelle partie")
    # si l'utilisateur est dans le mauvais canal ca le previent
    else : 
        await ctx.send("cette commande marche que dans le channel pendu")

# fonction pour tenter une lettre
@client.command()
async def try_letter(ctx, letter = ""):
    # verifie si l'utilisateur est bien dans le canal pendu
    if ctx.channel.id == 980124791652646972:
        global mot_aleatoire
        global mot_a_trouver
        global mot_en_recherche
        global essais
        global essai_versus_image

        image = ""
        # si il y a pas de partie en cours ca previent l'utilisateur qu'il ne peut pas utiliser cette commande
        if mot_a_trouver == "" :
            await ctx.send("Vous devez lancer une partie avant de pouvoir utiliser cette commande")
        else :
            # si l'utilisateur n'a pas entré de lettre ca le previent
            if letter == "":
                await ctx.send("Vous devez d'abord entrer une lettre")
            # si l'utilisateur a entré plus d'une lettre ca le previent
            elif len(letter) > 1 :
                await ctx.send("Vous devez entrer une seule lettre")
            else :
                # passe les 2 listes en tableau
                list_mot_a_trouver = list(mot_a_trouver)
                list_mot_en_recherche = list(mot_en_recherche)
                lettre_trouvees = 0
                # verifie si la lettre est dans la liste du mot a trouver
                for i in range(len(list_mot_a_trouver)) :
                    # si elle est dans la liste du mot a trouver ça l'ajoute dans la liste du mot qui est en train d'etre cherché
                    if list_mot_a_trouver[i] == letter :
                        list_mot_en_recherche[i] = letter
                        lettre_trouvees = lettre_trouvees + 1
                # convertis la liste du mot en recherche en chaine de caractere 
                str_mot_en_recherche = ''.join(list_mot_en_recherche)
                mot_en_recherche = str_mot_en_recherche
                # si le joueur a trouvé toutes les lettres il a gagné
                if mot_en_recherche == mot_a_trouver :
                    await ctx.send("bien joué le mot à trouver était bien :")
                    mot_letter_to_emoji = letter_to_emoji(mot_a_trouver)
                    await ctx.send(mot_letter_to_emoji)
                    mot_a_trouver = ""
                else :
                    # si il a trouvé 0 lettre il a utilisé un essai
                    if lettre_trouvees == 0 :
                        essais = essais + 1
                    # si il est a 12 essai, il a perdu, ca met l'image du pendu du dernier essai et ca envoie le mot qu'il fallait trouver
                    if essais == 12 :
                        await ctx.send("Tu as perdu")
                        await ctx.send(file=discord.File('essai_12.PNG'))
                        await ctx.send("Le mot à trouver était :")
                        mot_letter_to_emoji = letter_to_emoji(mot_a_trouver)
                        await ctx.send(mot_letter_to_emoji)
                        mot_a_trouver = ""
                        return
                    # parcours le tableau avec la correspondance image - essai et attribu a la variable image, l'image de l'essai ou l'utilisateur en est
                    for i in range(len(essai_versus_image)):
                        if essais == essai_versus_image[i][0]:
                            image = essai_versus_image[i][1]
                    # affiche l'image du pendu correspondant au nombre d'essai
                    await ctx.send(file=discord.File(image))
                    # affiche l'avancé du mot qui est en train d'etre recherché
                    mot_letter_to_emoji = letter_to_emoji(mot_en_recherche)
                    await ctx.send(mot_letter_to_emoji)
    # si l'utilisateur est dans le mauvais canal ca le previent
    else : 
        await ctx.send("cette commande marche que dans le channel pendu")

# fonction pour tenter un mot
@client.command()
async def try_word(ctx, word = ""):
    # verifie si l'utilisateur est bien dans le canal pendu
    if ctx.channel.id == 980124791652646972:
        global mot_aleatoire
        global mot_a_trouver
        global mot_en_recherche
        global essais
        global essai_versus_image

        image = ""
        # si il y a pas de partie en cours ca previent l'utilisateur qu'il ne peut pas utiliser cette commande
        if mot_a_trouver == "" :
            await ctx.send("Vous devez lancer une partie avant de pouvoir utiliser cette commande")
        else :
            #si l'utilisateur a trouvé la bonne reponse ca le previent, ca envoie le mot qu'il fallait trouvé et ca met la variable vide pour pouvoir lancer une nouvelle partie
            if word == mot_a_trouver :
                await ctx.send("bien joué le mot à trouver était bien :")
                mot_letter_to_emoji = letter_to_emoji(mot_a_trouver)
                await ctx.send(mot_letter_to_emoji)
                mot_a_trouver = ""
            else :
                essais = essais + 1
                # si il est a 12 essai, il a perdu, ca met l'image du pendu du dernier essai et ca envoie le mot qu'il fallait trouver
                if essais == 12 :
                    await ctx.send("Tu as perdu")
                    await ctx.send(file=discord.File('essai_12.PNG'))
                    await ctx.send("Le mot à trouver était :")
                    mot_letter_to_emoji = letter_to_emoji(mot_a_trouver)
                    await ctx.send(mot_letter_to_emoji)
                    mot_a_trouver = ""
                    return
                # parcours le tableau avec la correspondance image - essai et attribu a la variable image, l'image de l'essai ou l'utilisateur en est
                for i in range(len(essai_versus_image)):
                    if essais == essai_versus_image[i][0]:
                        image = essai_versus_image[i][1]
                # affiche l'image du pendu correspondant au nombre d'essai
                await ctx.send(file=discord.File(image))
                # affiche l'avancé du mot qui est en train d'etre recherché
                mot_letter_to_emoji = letter_to_emoji(mot_en_recherche)
                await ctx.send(mot_letter_to_emoji)
    # si l'utilisateur est dans le mauvais canal ca le previent
    else : 
        await ctx.send("cette commande marche que dans le channel pendu")

# fonction pour connaitre la reponse
@client.command()
async def give_pendu(ctx):
    # verifie si l'utilisateur est bien dans le canal pendu
    if ctx.channel.id == 980124791652646972:
        global mot_aleatoire
        global mot_a_trouver
        global mot_en_recherche
        global essais
        global essai_versus_image
        # si il y a pas de partie en cours ca previent l'utilisateur qu'il ne peut pas utiliser cette commande
        if mot_a_trouver == "" :
            await ctx.send("Vous devez lancer une partie avant de pouvoir utiliser cette commande")
        # envoie le mot qui etait a trouvé
        else :
            await ctx.send("Le mot à trouver était :")
            # transforme le mot en emoji
            mot_letter_to_emoji = letter_to_emoji(mot_a_trouver)
            await ctx.send(mot_letter_to_emoji)
            # remet la varialbe vide pour pouvoir lancer une nouvelle partie
            mot_a_trouver = ""
    # si l'utilisateur est dans le mauvais canal ca le previent
    else : 
        await ctx.send("cette commande marche que dans le channel pendu")

# fonction pour transformer un mot en mot avec des lettres emoji
def letter_to_emoji(mot_a_convertir):
    global letter_versus_emoji
    # transforme le mot a convertire en liste
    mot_a_convertir_list = list(mot_a_convertir)
    # parcours le mot a convertire
    for i in range(len(mot_a_convertir_list)):
        # parcours le tableau avec la correspondance lettre - emoji
        for j in range(len(letter_versus_emoji)):
            # remplace la lettre par un emoji
            if mot_a_convertir_list[i] == letter_versus_emoji[j][0]:
                mot_a_convertir_list[i] = letter_versus_emoji[j][1]
    # renvoie le mot avec les emoji en string
    mot_convertis = ' '.join(mot_a_convertir_list)
    return mot_convertis

# -------------------------------------------------- PENDU -------------------------------------------------- #

# ---------------------------------------------- PLUS OU MOINS ---------------------------------------------- #

max = 0
min = 0
more_less_aleatoire = 0

numbre_versus_emoji = [
    ["0",":zero:"],
    ["1",":one:"],
    ["2",":two:"],
    ["3",":three:"],
    ["4",":four:"],
    ["5",":five:"],
    ["6",":six:"],
    ["7",":seven:"],
    ["8",":eight:"],
    ["9",":nine:"]
]

# fonction pour lancer le jeu plus ou moins
@client.command()
async def more_less(ctx, nombre_1 = 0, nombre_2 = 0):
    global max
    global min
    global more_less_aleatoire 
    # verifie si l'utilisateur est bien dans le canal plus ou moins
    if ctx.channel.id == 980407531623030954:
        # si il y a déjà une partie en cours
        if more_less_aleatoire != 0 :
            await ctx.send("Il y a déjà une partie en cours, finissez la partie ou entrez =give_more_less pour connaitre la réponse et pouvoir commencer une nouvelle partie")
        else :
            # si les nombres sont pas entre 1 et 999 999
            if nombre_1 > 999999 or nombre_1 < 1 or nombre_2 > 999999 or nombre_2 < 1:
                await ctx.send("Il faut choisir deux nombres entre 1 et 999 999, par exemple =more_less 1 999 donnera un nombre entre 1 et 999")
            # si les deux nombres sont pareils
            elif nombre_1 == nombre_2 :
                await ctx.send("Il faut choisir deux nombres différents")
            else :
                # determine qui sera le minimum et qui sera le maximum
                if nombre_2 > nombre_1 :
                    max = nombre_2
                    min = nombre_1
                else :
                    min = nombre_2
                    max = nombre_1
                more_less_aleatoire = randint(min,max)
                await ctx.send("Bonne chance, entre =try_more_less et le nombre que tu veux pour trouver la réponse")
    # si l'utilisateur est dans le mauvais canal ca le previent
    else : 
        await ctx.send("Cette commande marche que dans le channel plus ou moins")

# fonction pour essayer de trouver le nombre 
@client.command()
async def try_more_less(ctx, reponse = 0):
    global max
    global min
    global more_less_aleatoire 
    # verifie si l'utilisateur est bien dans le canal plus ou moins
    if ctx.channel.id == 980407531623030954:
        # si il n y a pas de partie en cours
        if more_less_aleatoire == 0 :
            await ctx.send("Il faut lancer une partie avec =more_less avant de pouvoir utiliser cette commande")
        else :
            # si il entre un nombre plus haut ou plus bas que le max et le min
            if reponse < min or reponse > max :
                await ctx.send("Il faut que votre réponse soit entre les 2 nombres que vous avez entrer au début de la partie")
            else :
                # si la reponse est plus haute que le nombre a trouver
                if reponse > more_less_aleatoire :
                    await ctx.send(":regional_indicator_m: :regional_indicator_o: :regional_indicator_i: :regional_indicator_n: :regional_indicator_s:")
                # si la reponse est plus basse que le nombre a trouver
                elif reponse < more_less_aleatoire :
                    await ctx.send(":regional_indicator_p: :regional_indicator_l: :regional_indicator_u: :regional_indicator_s:")
                # si la reponse est la meme que le nombre a trouver
                else :
                    await ctx.send(":regional_indicator_b: :regional_indicator_r: :regional_indicator_a: :regional_indicator_v: :regional_indicator_o:")
                    await ctx.send("Le nombre à trouver était bien")
                    more_less_aleatoire_to_emoji = number_to_emoji(more_less_aleatoire)
                    await ctx.send(more_less_aleatoire_to_emoji)
                    more_less_aleatoire = 0
    # si l'utilisateur est dans le mauvais canal ca le previent
    else : 
        await ctx.send("Cette commande marche que dans le channel plus ou moins")

# fonction pour connaitre la reponse
@client.command()
async def give_more_less(ctx):
    global max
    global min
    global more_less_aleatoire 
    # verifie si l'utilisateur est bien dans le canal plus ou moins
    if ctx.channel.id == 980407531623030954:
        # si il n y a pas de partie en cours
        if more_less_aleatoire == 0 :
            await ctx.send("Il faut lancer une partie avec =more_less avant de pouvoir utiliser cette commande")
        # donne la reponse et fini la partie
        else :
            await ctx.send("La réponse était")
            more_less_aleatoire_to_emoji = number_to_emoji(more_less_aleatoire)
            await ctx.send(more_less_aleatoire_to_emoji)
            more_less_aleatoire = 0
    # si l'utilisateur est dans le mauvais canal ca le previent
    else : 
        await ctx.send("Cette commande marche que dans le channel plus ou moins")

# convertir un nombre en emoji
def number_to_emoji(nombre_a_convertir):
    global numbre_versus_emoji
    # transforme le nombre en str ("40")
    str_nombre_a_convertir = str(nombre_a_convertir)
    # transforme le nombre en liste (["4","0"])
    nombre_a_convertir_list = list(str_nombre_a_convertir)
    # parcours le tableau avec le nombre
    for i in range(len(nombre_a_convertir_list)):
        # parcours le tableau avec la correspondance chiffre emoji
        for j in range(len(numbre_versus_emoji)):
            # si le nombre correspond a un emoji ca remplace le nombre par un emoji
            if nombre_a_convertir_list[i] == numbre_versus_emoji[j][0]:
                nombre_a_convertir_list[i] = numbre_versus_emoji[j][1]
    # renvoie le nombre transformé en emoji
    nombre_convertis = ' '.join(nombre_a_convertir_list)
    return nombre_convertis

# ---------------------------------------------- PLUS OU MOINS ---------------------------------------------- #

# ----------------------------------------------- TU PREFERES ----------------------------------------------- #

utilisateurs = []

# fonction pour connaitre la reponse
@client.command()
async def tu_preferes(ctx):
    # verifie si l'utilisateur est bien dans le tu preferes
    if ctx.channel.id == 980145249005494293:
        already_add = False
        for i in range (len(utilisateurs)) : 
            if utilisateurs[i] == ctx.author.id :
                already_add = True
            else :
                already_add = False
        if already_add == False:
            utilisateurs.append(ctx.author.id)
            await ctx.send("add")
            await ctx.send(utilisateurs)
        else :
            await ctx.send("already add")
            await ctx.send(utilisateurs)
        
    # si l'utilisateur est dans le mauvais canal ca le previent
    else : 
        await ctx.send("Cette commande marche que dans le channel tu préfères")

@client.command()
async def hello(ctx):
    tu_preferes = "Tu preferes :"
    tu_preferes1 = "Manger une limasse"
    tu_preferes2 = "Manger un crapaud"
    await ctx.send(tu_preferes, components = [
        [
            Button(label = tu_preferes1, style="2", custom_id="reponse1"), 
            Button(label = tu_preferes2, style="2", custom_id="reponse2")]
        ])
    reponse1 = await client.wait_for("button_click", check = lambda i: i.custom_id == "reponse1")
    await reponse1.send(f"{reponse1.user} a choisis la réponse 1", ephemeral=False)
    reponse2 = await client.wait_for("button_click", check = lambda i: i.custom_id == "reponse2")
    await reponse1.send(f"{reponse2.user} a choisis la réponse 1", ephemeral=False)


# ----------------------------------------------- TU PREFERES ----------------------------------------------- #

client.run('OTc4MjI5MTUwNDI0OTIwMDc0.GTFsq3.uomKxew7wl-gobOTyd5Y4f1qAS03etcrLaEQyM ')