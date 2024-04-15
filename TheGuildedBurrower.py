#! /usr/bin/env python3

# Diggler game gemaakt door Boan 2024
# gebruik Pygame modules om veel werk uit handen te nemen voor low-level stuf
# hoef ik alleen nog maar bet grafise dingen en gameplay rekening te houen
# veel geleerd uit: https://inventwithpython.com/pygame/

#imports voor pygame en standaard functies
import pygame, sys, os
from pygame.locals import *
from pygame import mixer
import datetime
import time
import random
import math
from tkinter import messagebox

#Globale variabelen
#Let op FPS heeft invloed op timing ook voor animaties
FPS = 30 # frames per second to update the screen
# Afmetingen game window....als je deze aanpast moet je ook de levels aanpassen
SCHERMBREEDTE =1280 #breedte
SCHERMHOOGTE = 760 # hoogte
# voor midden bepaling
MIDDENBREEDTE = int(SCHERMBREEDTE / 2)
MIDDENHOOGTE = int(SCHERMHOOGTE / 2)
#counter die afteld.. niet alleen om het moeilijker te maken
#maar je kunt ook vastzitten door jezelf op te sluiten als je niet oplet!
TIMER = 201

# pixel tiles...belangrijk voor de sprites en karakters
TILEBREEDTE = 32
TILEHOOGTE = 32

#standaart kleuren
#handiger om de rgb waarden aan een globale variabele te binden...anders zie je niet meer welke kleur je waar gebruikt hebt
GOUD = (255, 215, 0)
WIT = (255, 255, 255)
ZWART = (0, 0, 0)
GEEL = (255, 255, 51)
BGKLEUR = ZWART
TXTKLEUR = GOUD

#boven/onder enz maakt de vergelijking wat betrouwbaarder met keypress vergelijkingen
BOVEN = 'up'
ONDER = 'down'
LINKS = 'left'
RECHTS = 'right'

BONUSLEVEL = False

# Geluidsfiles definieren en voorbereiden
#pygame regelt door zijn mixer al veel
#kwestie van wijzen naar geluidsfiles
# settings voor de kwalitijd..werkt ook als je het weglaat maar in de voorbeelden altijd de pre-init
# ook handig om het volume al te zetten zit verschil in tussen files
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init() 
GOUD_FX = pygame.mixer.Sound('sounds/gold_fall.wav')
GOUD_FX.set_volume(0.5)
PAK_GOUD_FX = pygame.mixer.Sound('sounds/gold.wav')
PAK_GOUD_FX.set_volume(0.7)
GRAVEN_FX = pygame.mixer.Sound('sounds/dig.wav')
GRAVEN_FX.set_volume(0.3)
ROTS_VAL_FX = pygame.mixer.Sound('sounds/rock_fall.wav')
ROTS_VAL_FX.set_volume(0.5)
DEUR_FX = pygame.mixer.Sound('sounds/door_open.wav')
DEUR_FX.set_volume(0.5)
EINDE_FX = pygame.mixer.Sound('sounds/end_level.wav')
EINDE_FX.set_volume(0.5)
TIME_UP_FX = pygame.mixer.Sound('sounds/time_up.wav')
TIME_UP_FX.set_volume(0.5)
DOOD_FX = pygame.mixer.Sound('sounds/dead.wav')
DOOD_FX.set_volume(1.0)
EXPLOSIE_FX = pygame.mixer.Sound('sounds/explosion.wav')
EXPLOSIE_FX.set_volume(0.5)
INTRO_MUZ = pygame.mixer.Sound('sounds/sound_music_dungeon_intro.wav')
INTRO_MUZ.set_volume(0.1)
GAME_OVER_MUZ = pygame.mixer.Sound('sounds/game_over.wav')
GAME_OVER_MUZ.set_volume(0.1)
VICTORY_MUZ = pygame.mixer.Sound('sounds/sound_music_dungeon_intro.wav')
VICTORY_MUZ.set_volume(0.1)
ACHTERGROND_MUZ = pygame.mixer.Sound('sounds/sound_music_dungeon_quest.wav')
ACHTERGROND_MUZ.set_volume(0.1)



 #Haal de images uit de spritesheet
 # net als de nesgames heb je een image file waar de objecten inzitten
 #je gebruikt gewoon de pixels als coordinaten daarom alles in 32x32 pixels, dat maakt het makkelijk in het grid
 #
TITEL_SCHERM = pygame.image.load('images/title.png')
DEAD_SCHERM = pygame.image.load('images/dead.png')
VICTORY_SCHERM = pygame.image.load('images/victory.png')

 #Haal de images uit de spritesheet
 # net als de nesgames heb je een image file waar de objecten inzitten
 #je gebruikt gewoon de pixels als coordinaten daarom alles in 32x32 pixels, dat maakt het makkelijk in het grid
SPRITE_SHEET_IMAGE = pygame.image.load('images/sprites.png')
STATIC_BURROWER = SPRITE_SHEET_IMAGE.subsurface(0, 192, 32, 32)
LEFT_BURROWER = SPRITE_SHEET_IMAGE.subsurface(0, 128, 32, 32)
RIGHT_BURROWER = SPRITE_SHEET_IMAGE.subsurface(0, 160, 32, 32)
UP_BURROWER = SPRITE_SHEET_IMAGE.subsurface(0, 0, 32, 32)
DOWN_BURROWER = SPRITE_SHEET_IMAGE.subsurface(32, 32, 32, 32)



MUUR = SPRITE_SHEET_IMAGE.subsurface(32, 192, 32, 32)
BRICK = SPRITE_SHEET_IMAGE.subsurface(96, 192, 32, 32)
ROTS = SPRITE_SHEET_IMAGE.subsurface(0, 224, 32, 32)
ZAND = SPRITE_SHEET_IMAGE.subsurface(32, 224, 32, 32)
LEEG = SPRITE_SHEET_IMAGE.subsurface(160, 0, 32, 32)
GOUDKLOMP = SPRITE_SHEET_IMAGE.subsurface(0, 320, 32, 32)
UITGANG = SPRITE_SHEET_IMAGE.subsurface(32, 0, 32, 32)
UITGANG_DICHT = SPRITE_SHEET_IMAGE.subsurface(32, 0, 32, 32)
UITGANG_OPEN = SPRITE_SHEET_IMAGE.subsurface(64, 192, 32, 32)
DOOD = SPRITE_SHEET_IMAGE.subsurface(32, 160, 32, 32)
DYNAMIET = SPRITE_SHEET_IMAGE.subsurface(64, 0, 32, 32)
EXPLOSIE = SPRITE_SHEET_IMAGE.subsurface(0, 32, 32, 32)


# een animate is gewoon opeenvolgende plaatjes waar je doorheen loopt
#we halen de opeenvolgende plaatjes uit de spritesheet
#
ANIMATION_DEATH =   [DOWN_BURROWER,
                    LEFT_BURROWER,
                    UP_BURROWER,
                    RIGHT_BURROWER,
                    DOWN_BURROWER,
                    LEFT_BURROWER,
                    UP_BURROWER,
                    RIGHT_BURROWER,
                    DOWN_BURROWER]

 
#ook maar een dictionary voor de standaard plaatjes..wel makklijker
IMAGESDICT = {'Burrower': STATIC_BURROWER,
                'left': LEFT_BURROWER,
                'right': RIGHT_BURROWER,
                'up': UP_BURROWER,
                'down': DOWN_BURROWER,
                'muur': MUUR,
                'brick': BRICK,
                'rots': ROTS,
                'zand': ZAND,
                'leeg': LEEG,
                'goudklomp': GOUDKLOMP,
                'uitgang': UITGANG,
                'uitgang_open': UITGANG_OPEN,
                'dood': DOOD,
                'dynamiet':DYNAMIET,
                'explosie': EXPLOSIE,
                'title': TITEL_SCHERM,
                'dead': DEAD_SCHERM,
                'victory': VICTORY_SCHERM}
    
# mapping van de letters in de level files naar de plaatjes in de plaatjes dictionary
TILEMAPPING = {'z': IMAGESDICT['zand'],
                '%': IMAGESDICT['muur'],
                '=': IMAGESDICT['brick'],
                'l': IMAGESDICT['leeg'],
                'g': IMAGESDICT['goudklomp'],
                'u': IMAGESDICT['uitgang'],
                'd': IMAGESDICT['dynamiet'],
                'b': IMAGESDICT['explosie'],
                '+': IMAGESDICT['dood'],
                'r': IMAGESDICT['rots']}

#de images voor de Burrower
PLAYERIMAGES = [IMAGESDICT['Burrower']]

# verander de tile voor de uitgang als uitgang open moet
def uitgangOpen():
  global UITGANG, UITGANG_OPEN, IMAGESDICT, TILEMAPPING
  UITGANG = UITGANG_OPEN
  IMAGESDICT['uitgang'] = UITGANG_OPEN
  TILEMAPPING['u'] = IMAGESDICT['uitgang']

# verander de tile voor de uitgang als uitgang dicht moet
def uitgangDicht():
  global UITGANG, UITGANG_OPEN, IMAGESDICT, TILEMAPPING
  UITGANG = UITGANG_DICHT
  IMAGESDICT['uitgang'] = UITGANG_DICHT
  TILEMAPPING['u'] = IMAGESDICT['uitgang']
  
#text functie voor updaten text renders
def print_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    DISPLAYSURF.blit(img, (x, y))

#hoofdscherm met uitleg en met eigen into muziek
# simpel gehouden door 1 plaatje met text eronder
# keuze menu voor Q=quit, R= restart of B= bonus level
#als startscherm stopt bij een key-pres event
def GrootScherm(screenState):
    global BONUSLEVEL
    # om het plaatje te centreren  gebruik ik de helft van het schrmbreedte als coordinaat
    #if screenState in ('dead'):
    #    screenleRect = IMAGESDICT['dead'].get_rect()
    #else:
    screenRect = IMAGESDICT['title'].get_rect()
    # uitlijnen wat mooi lijkt
    topCoord = 150 
    screenRect.top = topCoord
    screenRect.centerx = MIDDENBREEDTE
    topCoord += screenRect.height
    ACHTERGROND_MUZ.stop()

    #text onder het plaatje
    if screenState == 'start':
        intoText = ['Press the "ANY" key!']
        intoTextKlein = ['Collect all the gold to open the gate to another realm']
        intoTextKlein2 = ['Watch out for falling rocks and dynamite'] 
    elif screenState == 'dead':
        intoText = ['You are Dead']
        intoTextKlein = ['May wealth and good fortune come to you in your afterlife']
        intoTextKlein2 = ['press Q to Quit or R to restart if you dare']
    else:
        intoText = ['Victory!']
        intoTextKlein = ['You can now retire wealthy! Live long and prosper']
        intoTextKlein2 = ['press Q to Quit or R to restart. Press B for a bonus.']

    # zet de achtergrond
    DISPLAYSURF.fill(BGKLEUR)

    # plaats het plaatje
    if screenState == 'start':
        DISPLAYSURF.blit(IMAGESDICT['title'], screenRect)
    elif screenState == 'dead':
        DISPLAYSURF.blit(IMAGESDICT['dead'], screenRect)
    else:
        DISPLAYSURF.blit(IMAGESDICT['victory'], screenRect)

    # Plaats de tekst
    # ook hier de helft van de schermbreedte om het midden te bepalen
    for i in range(len(intoText)):
        instSurf = BASICFONT.render(intoText[i], 1, TXTKLEUR)
        instRect = instSurf.get_rect()
        #uitlijnen gewoon proberen wat mooi is
        topCoord += 1 
        instRect.top = topCoord
        instRect.centerx = MIDDENBREEDTE
        # de hoogte van de text ook meerekenen!!
        topCoord += instRect.height 
        DISPLAYSURF.blit(instSurf, instRect)

    for i in range(len(intoTextKlein)):
        instSurf = BASICFONTSMALL.render(intoTextKlein[i], 1, GEEL)
        instRect = instSurf.get_rect()
        #uitlijnen gewoon proberen wat mooi is
        topCoord += 0 
        instRect.top = topCoord
        instRect.centerx = MIDDENBREEDTE
        # de hoogte van de text ook meerekenen!!
        topCoord += instRect.height 
        DISPLAYSURF.blit(instSurf, instRect)

    for i in range(len(intoTextKlein2)):
        instSurf = BASICFONTSMALL.render(intoTextKlein2[i], 1, GEEL)
        instRect = instSurf.get_rect()
        #uitlijnen gewoon proberen wat mooi is
        topCoord += 0 
        instRect.top = topCoord
        instRect.centerx = MIDDENBREEDTE
        # de hoogte van de text ook meerekenen!!
        topCoord += instRect.height 
        DISPLAYSURF.blit(instSurf, instRect)

    # Main loop voor het startscherm
    #blijft lopen totdat speler het scherm sluit, of een toets indrukt
    #maakt niet uit welke toets
    while True: 
        #muziekje aan
        if screenState == 'start':
            INTRO_MUZ.play()
        elif screenState == 'dead':
            GAME_OVER_MUZ.play()
        else:
            VICTORY_MUZ.play()
        for event in pygame.event.get():
            #dit is dus het kruisje
            if event.type == QUIT:
                #Kill de game en het scherm
                pygame.quit()
                sys.exit()
            #KEYDOWN event is elke key maart niet uit welke
            elif event.type == KEYDOWN:
                #Q voor quit
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
                #R voor reset game
                #maakt niet uit welk scherm altijd muziek stoppen want die loopt anders gewoon door
                elif event.key == K_r:
                    if screenState == 'start':
                        #op het startscherm is r gewooneen any key
                        INTRO_MUZ.stop()
                        return
                    elif screenState == 'dead':
                        GAME_OVER_MUZ.stop()
                    elif screenState == 'victory':
                        VICTORY_MUZ.stop()
                    #bij de ander gaan R weer gewoon de main in
                    main()
                    return 
                #Bonus level!
                elif event.key == K_b:
                    #alleen geldig bij victory scherm
                    if screenState == 'victory':
                        VICTORY_MUZ.stop()
                        #Zet global Boolean om de level index naar 0 te zetten ipv 1
                        #zodat bonuslevel word gestart. 
                        BONUSLEVEL = True
                        main()
                        return
                else:
                    INTRO_MUZ.stop()
                    return

        # Schrijf de inhoud van DISPLAYSURF daadwerkelijk naar het scherm
        pygame.display.update()
        FPSCLOCK.tick()


#Lees de Levelfile in
# Idee van de levelfile en hoe je die opslaat in een dictionary (een 2 dimensiale array) 
# meegenomen uit de informatica olympiade...begin gemaakt maar wel lastig...veel opgezocht
def maakLevel(filename):
    assert os.path.exists(filename), 'Kan de level file niet vinden: %s' % (filename)
    levelFile = open(filename, 'r')
    # Kijk voor een lege regel, dit is het einde van de leveldefinitie
    content = levelFile.readlines() + ['\r\n']
    levelFile.close()
    
    #Lijst van levelobjecten
    levels = [] 
    levelNum = 0
    # een enkele level
    mapTextLines = [] 
    #object waar de map van het level in zit
    gridObject = []
    for lineNum in range(len(content)):
        # lees regel voor regel
        line = content[lineNum].rstrip('\r\n')

        if '#' in line:
            # negeer de # tekens...dit is voor commentaar
            line = line[:line.find('#')]

        if line != '':
            # voeg toe aan map
            mapTextLines.append(line)
        elif line == '' and len(mapTextLines) > 0:
            # lege regel is einde map
            # voeg regels toe aan map object

            maxWidth = -1
            for i in range(len(mapTextLines)):
                if len(mapTextLines[i]) > maxWidth:
                    maxWidth = len(mapTextLines[i])
            #rare issues met lege characters aan het einde van de regels...zorg dat het spaces zijn
            for i in range(len(mapTextLines)):
                mapTextLines[i] += ' ' * (maxWidth - len(mapTextLines[i]))

            # prop de mapTextlines in het gridObject
            for x in range(len(mapTextLines[0])):
                gridObject.append([])
            for y in range(len(mapTextLines)):
                for x in range(maxWidth):
                    gridObject[x].append(mapTextLines[y][x])

            #Loop door de map heen en zoek de @=speler en andere objecten
            
            #x en y voor startpositie speler
            startx = None
            starty = None
            # de x en y coordinaten voor de deur
            deurx = None
            deury = None
            # hier worden de rotsen in opgeslagen
            rotsen = []
            # hier worden de goudrotsen opgeslagen
            goud = []
            # hier word de dynamiet opgeslagen
            dynamiet = []
            # hier word de uitgang opgeslagen
            uitgang = []
            #Loop hier door het GridObject heen
            # en voeg telkens bij elk voorkomen van een item
            # aan de juiste lijst toe 
            for x in range(maxWidth):
                for y in range(len(gridObject[x])):
                    if gridObject[x][y] in ('@'):
                        # '@' is speler
                        startx = x
                        starty = y
                    if gridObject[x][y] in ('r'):
                        # 'r' is rots
                        rotsen.append((x, y))
                    if gridObject[x][y] in ('g'):
                        # 'g' is goud
                        goud.append((x, y)) 
                    if gridObject[x][y] in ('d'):
                        # 'd' is dynamiet
                        dynamiet.append((x, y))
                    if gridObject[x][y] in ('u'):
                        # 'u' is the uitgang
                        deurx = x
                        deury = y
                        uitgang.append((x, y))

            # Spelstatus object om alle states van de belangrijke game elementen bij te houden zodat deze makkelijk op te vragen zijn
            spelStatusObject = {'speler': (startx, starty),
                            'deur': (deurx, deury),
                            'stepCounter': 0,
                            'rotsen': rotsen,
                            'goud': goud,
                            'dynamiet' : dynamiet}
            # zelfde als gamestate maar dan voor het level
            levelObject = {'width': maxWidth,
                        'height': len(gridObject),
                        'gridObject': gridObject,
                        'startState': spelStatusObject}

            levels.append(levelObject)

            # reset variabelen, anders komt de data door elkaar bij het laden van de volgendelevel
            mapTextLines = []
            gridObject = []
            spelStatusObject = {}
            levelNum += 1
            #print(levels)
    return levels


#Teken de Map 
# dit doe je door te loopen door het gridObject daar wordt alle info bijgehouden over de status en positie
def printMap(gridObject, spelStatusObject,player_direction):
    global goud_group
    # deze zijn nodig om de map te tekenen naar het pygame surface object zodat het later naar het scherm kan worden geschreven
    mapSurfWidth = len(gridObject) * TILEBREEDTE
    mapSurfHeight = (len(gridObject[0])) * TILEHOOGTE
    mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight))
    # achtergrondkleur vullen
    mapSurf.fill(BGKLEUR)
   
    #
    #Loop door het gridObject (2 dimensinaal dus dubbele loop-die-loop)
    # en teken alle tiles
    for x in range(len(gridObject)):
        for y in range(len(gridObject[x])):
            spaceRect = pygame.Rect((x * TILEBREEDTE, y * TILEHOOGTE, TILEBREEDTE, TILEHOOGTE))
            #print(gridObject[x][y], end=' ')
            if (gridObject[x][y] in TILEMAPPING) and (gridObject[x][y] != 'g'):
                baseTile = TILEMAPPING[gridObject[x][y]]
                
            if gridObject[x][y] == 'g' :
                baseTile = TILEMAPPING[gridObject[x][y]]    
            # eerst de wall tekenen
            mapSurf.blit(baseTile, spaceRect)

            # Nu de burrower zelf
            if (x, y) == spelStatusObject['speler']:
                # speler _direction is het bijbehorende image
                # voor welke kant de speler op aan het gaan was
                mapSurf.blit(player_direction, spaceRect)
            #if (x, y) == spelStatusObject['deur']:
    return mapSurf


def isMuurOfSteen(gridObject, x, y):
    # bepaald of het item op de gegeven x en y een muur of rand item is
    # geeft True terug als dat zo is
    if x < 0 or x >= len(gridObject) or y < 0 or y >= len(gridObject[x]):
        # X en Y hoeven natuurlijk noet in de map te zitten!!
        return False
    elif gridObject[x][y] in ('%', '='):
        # muur of rand in de weg
        return True
   # elif gridObject[x][y] in ('u'):
   #     return True 
   # uitgang geblokkeert
    return 
   
    
def BlokkeerRots (gridObject, spelStatusObject, x, y):
    #als de gegeven x/y positie zand, muur of rand is dan kan de rots niet rollen!
    # Duh...een andere rots natuurlijk ook

    if gridObject[x][y] in ('%', '=', 'z', 'r', 'g'):
        return True

    elif x < 0 or x >= len(gridObject) or y < 0 or y >= len(gridObject[x]):
        #eeuh ja het kan voorkomen dat de x en y niet op de map zitten natuurlijk
        return True 

    #elif (x, y) in spelStatusObject['rotsen']:
    #    return True 

    return False

def doMove(gridObject, spelStatusObject, burrowerMove):
    global goudPak, goud_group 
    #poeh ... veel aan moetten sleutelen
    #hiering word voordat een move wordt gedaan gekeken of een bepaalde move wel kan worden uitgevoerd
    # of er geen muur of rots ofoz in de weg zit
    #als moeve niet kan....doe niks
    playerx, playery = spelStatusObject['speler']   
    rotsen = spelStatusObject['rotsen']
    goud = spelStatusObject['goud']

    # uiteindelijk best wel simpel gewoon de x / y coordinaat  +1 of -1 
    # voor een move. door een offset te gebruiken hoefde ik niet telkens
    #de berekening opnieuw uit te voeren
    if burrowerMove == BOVEN:
        xOffset = 0
        yOffset = -1
    elif burrowerMove == RECHTS:
        xOffset = 1
        yOffset = 0
    elif burrowerMove == ONDER:
        xOffset = 0
        yOffset = 1
    elif burrowerMove == LINKS:
        xOffset = -1
        yOffset = 0
        
    # Kijk of er niet iets in de weg staat.
    if isMuurOfSteen(gridObject, playerx + xOffset, playery + yOffset):
        return False
    else:   
        if (playerx + xOffset, playery + yOffset) in rotsen:
           #Als rots, kijk of je de rots kan verplaatsen
            if not BlokkeerRots(gridObject, spelStatusObject, playerx + (xOffset*2), playery + (yOffset*2)):
                # Verplaats de rots
                ind = rotsen.index((playerx + xOffset, playery + yOffset))
                rotsen[ind] = (rotsen[ind][0] + xOffset, rotsen[ind][1] + yOffset)
                gridObject[playerx+ (xOffset*2)][playery] ='r'
                ROTS_VAL_FX.play()
                                    
            else:
                return False
            
        # Goud in de weg !    
        if (playerx + xOffset, playery + yOffset) in goud:
            gridObject[playerx + xOffset][playery] ='l'
            goudPak += 1
            #print(goudPak)
            PAK_GOUD_FX.play()
            
            #Haal 1 goud weg uit de lijst in dit level
            ind = goud.index((playerx + xOffset, playery + yOffset))
            del goud[ind]

            #Je hebt al het goud
            #open de deur!
            if not goud :
                DEUR_FX.play()
                uitgangOpen()
               
        # Ga naar boven.
        spelStatusObject['speler'] = (playerx + xOffset, playery + yOffset)
        GRAVEN_FX.play()
        
        # Als het niet de uitgang is, vervang zand of goud voor uitgegraven deel
        if not gridObject[playerx][playery] =='u':
            gridObject[playerx][playery] ='l'
        return True
 
def isLevelGehaald(spelStatusObject):
    
    #Is waar als al het goud is verzameld en de burrower is bij de deur
    goud = spelStatusObject['goud']
    Burrower = spelStatusObject['speler']
    deur = spelStatusObject['deur']
    
    if not goud and (Burrower[0] == deur[0]) and (Burrower[1] == deur[1]) :
        #print('Level Gehaald !!!')
        EINDE_FX.play() 
        return True
    
    return False
    

def raakDynamiet(gridObject, spelStatusObject) :
    global deadBurrower
    Burrower = spelStatusObject['speler']
    dynamiet = spelStatusObject['dynamiet']
    #kijk of je dynamiet raakt..op alle tiles eromheen
    for x,y in dynamiet :
       if (Burrower[0] in [x, x-1,x+1]) and (Burrower[1] in [y, y-1,y+1]):
            #print('Je bent kapotdood!')
            # Maak de explosie
            #explosie raakt alles in een grid om de speler heen van +1
            gridObject[x][y] = 'd'
            for j in range(-1,2) :
                gridObject[Burrower[0]-1][Burrower[1]+j] = 'b'
                gridObject[Burrower[0]+1][Burrower[1]+j] = 'b'
                gridObject[Burrower[0]][Burrower[1]+j] = 'b'
        
            EXPLOSIE_FX.play()
            deadBurrower = True
            return True 
    return True

 
def vallendeRots(gridObject, spelStatusObject):
    global deadBurrower
    rotsen = spelStatusObject['rotsen']
    goud = spelStatusObject['goud']
    Burrower = spelStatusObject['speler']
    elementList = [rotsen, goud]
    RotsOfGoud =['r','g'] 
    
    for element in elementList :
        for x, y in element :
            
            # Als er iets op je valt..kan alleen rots of goud zijn
            if ((gridObject[x][y+1] == 'l') and  (x == Burrower[0] and y+2 == Burrower[1])):
                #print('Je bent kapotdood!')
                # geen explosie meer, dat is voor dynamiek is leuker
                gridObject[x][y] = 'l'
                #gridObject[x][y] = '+'
                #for j in range(1,4) :
                #    gridObject[x][y+j] = 'b'
                #    gridObject[x-1][y+j] = 'b'
                #    gridObject[x+1][y+j] = 'b'
                gridObject[x][y+2] = '+'
                
                DOOD_FX.play()
                deadBurrower = True
                return True
            
            elif ((gridObject[x][y+1] == 'r') and (gridObject[x-1][y] == 'l') and (gridObject[x-1][y+1] == 'l') and (x-1 == Burrower[0] and y+2 == Burrower[1])):
                #print('Je bent kapotdood')
                #Explosie functionaliteit weggelaten, is voor dynamiet nu
                gridObject[x][y] = 'l'
                #for j in range(1,4) :
                #    gridObject[x-1][y+j] = 'b'
                #    gridObject[x-2][y+j] = 'b'
                #    gridObject[x][y+j] = 'b'
                gridObject[x][y+2] = '+'
                DOOD_FX.play()
                deadBurrower = True
                return True
                                      
            #verplaats de rots naar y+1 alleen als dt een leeg veld is  
            if gridObject[x][y+1] == 'l' :
                gridObject[x][y] = 'l'
                #hou bij waar de rots is in de lijst van rotsen
                if element == rotsen : 
                    gridObject[x][y+1] = 'r'
                    ROTS_VAL_FX.play()
                #hou bij waar goud is in de lijst van goud
                elif element == goud :
                    gridObject[x][y+1] = 'g' 
                    GOUD_FX.play()
                #Hou index bij
                ind = element.index((x, y))
                element[ind] = (x,y+1)
                return True
            
            #dit was een lastige..
            #Alleen als de x-1 en y+1 leeg is, kan de rots verplaatsen
            #Alleen als een rots of goud is op positie x en y+1
            if (gridObject[x-1][y+1] == 'l') and (gridObject[x][y+1] in RotsOfGoud) and (gridObject[x-1][y] == 'l') and (x-1 != Burrower[0] and y+1 != Burrower[1]):
                gridObject[x][y] = 'l'
                #hou bij waar de rots is in de lijst van rotsen
                if element == rotsen :
                    gridObject[x-1][y+1] = 'r'
                    ROTS_VAL_FX.play()    
                
                #hou bij waar goud is in de lijst van goud
                elif element == goud :
                    gridObject[x-1][y+1] = 'g'
                    GOUD_FX.play()    
                #houde index bij!      
                ind = element.index((x, y))
                element[ind] = (x-1,y+1)
                return True
            
            #nog zo een....
            #Alleen als de x+1 en y+1 leeg is, kan de rots verplaatsen
            #Alleen als een rots of goud is op positie x en y+1 EN x-1 en y+1
            if (gridObject[x+1][y+1] == 'l') and (gridObject[x][y+1] in RotsOfGoud) and (gridObject[x-1][y+1] in RotsOfGoud) and (gridObject[x-1][y] == 'l') and (x-1 != Burrower[0] and y+1 != Burrower[1]):
                gridObject[x][y] = 'l'
                if element == rotsen : # update the rocks position in the list of rocks
                    gridObject[x+1][y+1] = 'r'
                    ROTS_VAL_FX.play() 

                #hou bij waar goud is in de lijst van goud
                elif element == goud :
                    gridObject[x+1][y+1] = 'g'
                    GOUD_FX.play() 
                #en weer de index bijwerken
                ind = element.index((x, y))
                element[ind] = (x+1,y+1)
                return True
            
            #nog zo een....
            #Alleen als de x+1 en y+1 leeg is, kan de rots verplaatsen
            #Alleen als een rots of goud is op positie x en y+1 EN NIET een leeg veld op x-1 en y
            # The rock move to x+1,y+1 if this space is empty a rock or gold is at x,y+1 and not a space at x-1,y
            if (gridObject[x+1][y+1] == 'l') and (gridObject[x][y+1] in RotsOfGoud) and (gridObject[x-1][y] != 'l') and (gridObject[x+1][y] == 'l'):
                gridObject[x][y] = 'l'
                #hou bij waar de rots is in de lijst van rotsen
                if element == rotsen : 
                    gridObject[x+1][y+1] = 'r'
                    ROTS_VAL_FX.play() 
                ##hou bij waar goud is in de lijst van goud
                elif element == goud : 
                    gridObject[x+1][y+1] = 'g'
                    GOUD_FX.play()                    
                # weer bijna de index vergeten
                ind = element.index((x, y))
                element[ind] = (x+1,y+1)
                return True  
            
    return False
 
def updateScore(spelStatusObject):
    global old_seconds, TIMER, currentLevelIndex, lives
    #Score tijd en levens bijhouden
    goud = spelStatusObject['goud']
    #Yep...als levens op zijn ben je dood
    if lives <= 0:
        ACHTERGROND_MUZ.stop()
        GrootScherm('dead')
        return
    #leuker font dan de standaard
    font_score = pygame.font.Font('mvboli.ttf', 38)
    
    # In welk level zijn we
    print_text(f'Level {currentLevelIndex+1}', font_score, GOUD, 10, 700)
      
    # Hoeveel goud hebben we
    rect = GOUDKLOMP.get_rect()
    rect.x = 600
    rect.y = 712
    DISPLAYSURF.blit(GOUDKLOMP, rect)
    
    #updte de tekst
    d_number = f"{len(goud):02d}"
    print_text(str(d_number), font_score, GEEL, 640, 700)
    
    # Hoeveel levens hebben we
    rect = STATIC_BURROWER.get_rect()
    rect.x = 820
    rect.y = 710
    DISPLAYSURF.blit(STATIC_BURROWER, rect)
    
    print_text(str(lives), font_score, GOUD, 860, 700)
    
    # De timer...de timer maakt het een stuk leuker spel anders kun je er eeuwig over doen
    current_time = datetime.datetime.now()
    current_seconds = current_time.second
    
    #de grote wisseltruuk
    if (old_seconds != current_seconds) :
        old_seconds = current_seconds
        TIMER -= 1
    # en update de tekst
    print_text(str(TIMER), font_score, GOUD, 1200, 700)
    

def speelLevel(levels, levelNum):
    global currentImage, goudPak, TIMER, lives, deadBurrower, goud_group, player_direction
    #het levelObject hou alles bij in dit level
    levelObject = levels[levelNum]
    #Het gridObject...hou alles bij in het grid
    gridObject = levelObject['gridObject']
    # hou de status bij, en zet hier op beginpositie
    spelStatusObject = levelObject['startState']
    #Als je telkens bij elke loop of tick alles opnieuw moet tekenen wordt het traag en niet efficient
    # dus pas bij een wijziging aangeven dat we opnieuw het scherm willen updaten en de map met de 
    #huidige status willen tekenen op het scherm
    mapNeedsRedraw = True
    #nog niet
    levelIsComplete = False
    #houd e tijd bij
    last_update = pygame.time.get_ticks()
    #animation cooldown uit voorbeelden en tutorials geleerd dt de wijzigingen anders direct gebeuren en dat ziet en voelt raar
    # de waarde is een beetje gokken en uitproberen
    animation_cooldown = 50
    #nog nul
    goudPak = 0
    #nog levend
    deadBurrower = False
    goud_group = pygame.sprite.Group()
    # nu nog beginpositie
    player_direction = STATIC_BURROWER
    
    #geprobeert meer animaties in het spel te brengen
    #maar lukte niet echt
    #de rest van de code wacht totdat de animatie klaar is...dat werkt dus niet goed
    #anicount = 0
    # De main game loop!
    while True: 
        # Reset bij elke pass
        burrowerMove = None  
        # event loop
        for event in pygame.event.get(): 
            #animatie werkt niet
            #if 7 > anicount:
            #   anicount += 1
            #else:
            #    anicount = 0
            #welke key wordt ingedrukt
            if event.type == QUIT:
                # Kruisje geklikt dus kill
                pygame.quit()
                sys.exit()
            #triggered bij elke keypress maakt niet uit welke      
            elif event.type == KEYDOWN:
                #Linkerpijltje
                if event.key == K_LEFT:
                    burrowerMove = LINKS
                    #countleft = anicount + 8
                    #pas speler plaatje aan aan de richting van de move
                    player_direction = LEFT_BURROWER
                #rechterpijltje
                elif event.key == K_RIGHT:
                    burrowerMove = RECHTS
                    #countright = anicount + 16
                    #pas speler plaatje aan aan de richting van de move
                    player_direction = RIGHT_BURROWER
                #pijltje naar boven
                elif event.key == K_UP:
                    burrowerMove = BOVEN
                    #pas speler plaatje aan aan de richting van de move
                    player_direction = UP_BURROWER
                #pijltje naar beneden
                elif event.key == K_DOWN:
                    burrowerMove = ONDER
                    #pas speler plaatje aan aan de richting van de move
                    player_direction = DOWN_BURROWER
            
            #Doe pas een update als de ingedrukte key word losgelaten
            elif event.type == KEYUP:
                #player_direction = STATIC_BURROWER
                mapSurf = printMap(gridObject, spelStatusObject, player_direction)
                
                
        if burrowerMove != None and not levelIsComplete :
            #als de speler een key heeft gedrukt doe dan de move
            moved = doMove(gridObject, spelStatusObject, burrowerMove)

            #als er een move is gedaan
            if moved:
                # Hou de move bij
                spelStatusObject['stepCounter'] += 1
                #de move moet wel worden getekend naar het scherm
                mapNeedsRedraw = True
            #Kijk of level is gehaald    
            if isLevelGehaald(spelStatusObject):
                # Je hebt het gehaald!
                levelIsComplete = True
        
        # Dit is dus de timeout voor de vallende rotsen..anders is het heel onnatuurlijk       
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            last_update = current_time
                    
            #Als er lege ruimte is onder de rots...dan kan hij vallen
            #en dus weer opnieuw naar scherm weergeven
            spaceBelowRock = vallendeRots(gridObject, spelStatusObject)   
            if spaceBelowRock:
                mapNeedsRedraw = True

            # Raak dynamiet
            # dan ook weer weergeven
            if raakDynamiet(gridObject, spelStatusObject): 
                mapNeedsRedraw = True
        
        #voor de achtergrondkleur
        #eerst lege plekken gewoon leeg..maar leuker met eigen sprite
        #toch is een zwarte achtergrond beter voor de transparante sprite                        
        DISPLAYSURF.fill(BGKLEUR)
        #Wel de score bijhouden!
        updateScore(spelStatusObject)
        
        #als boolean is gezet is er dus iets veranderd en moet er opnieuw naar scherm geschreven worden
        if mapNeedsRedraw:
            #als je dood bent
            if deadBurrower:
                mapSurf = printMap(gridObject, spelStatusObject, DOOD)
            else:
                #Anders de juiste sprite van de speler voor de richting tekenen
                mapSurf = printMap(gridObject, spelStatusObject, player_direction)
            mapNeedsRedraw = False        
        
        #voor de coordinaten
        mapSurfRect = mapSurf.get_rect()
        # teken mapSurf naar het DISPLAYSURF Surface object. zie tutorials
        DISPLAYSURF.blit(mapSurf, mapSurfRect)
        
        # Als je het level hebt gehaald
        if levelIsComplete:
            #pauze anders meteen naar volgende
            time.sleep(4)
            return 'solved'
        
        #Als de tijd op is (timer is 0) ben je dood
        #dan een leven minder
        # en geeft aan dat speler dood is met dood sprite
        if (TIMER == 0) :
            lives -=1
            TIME_UP_FX.play()
            mapSurf = printMap(gridObject, spelStatusObject, DOWN_BURROWER)
            mapNeedsRedraw = True
            time.sleep(4) 
            return 'counter0'

        #Schrijf Displaysurf naar het scherm               
        pygame.display.update()
        
        # Restart het level als de speler dood is
        if deadBurrower :
            lives -=1
            #TIMER = 201
            #de timer weer hetzelfde als begin level...dus ook met minder tijd
            TIMER = 201 - math.ceil((currentLevelIndex / 2) * 10)
            time.sleep(4) 
            return 'deadBurrower'
        #volgende tik op de klok
        FPSCLOCK.tick()


def main():
    #Main functie en het startpunt
    #zooi globale variabelen verwijzen
    global FPSCLOCK, DISPLAYSURF, IMAGESDICT, TILEMAPPING, BASICFONT, BASICFONTSMALL, PLAYERIMAGES, currentImage, goudPak, old_seconds
    global currentLevelIndex, lives, BONUSLEVEL, TIMER
    
     # Pygame initialise
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    #DISPLAYSURF  is de globale variabele waarin we de pygame surface objecten stoppen, dit uit de voorbeelden
    DISPLAYSURF = pygame.display.set_mode((SCHERMBREEDTE, SCHERMHOOGTE))
    currentImage = 0
    old_seconds = 70
    lives = 3
    #titel bovenkant scherm
    pygame.display.set_caption('The Gilded Burrower')
    #leukere font dan de standaard
    BASICFONT = pygame.font.Font('mvboli.ttf', 50)
    BASICFONTSMALL = pygame.font.Font('mvboli.ttf', 25)

    #als er geen bonuslevel is gezet...bv eerste keer of na gameover reset
    if not BONUSLEVEL:
        #laat startscherm zien
        GrootScherm('start') 
    #-1 is voor loopen muziek! thanks Stack overflow!
    ACHTERGROND_MUZ.play(-1)

    #roep functie aandie levelfile inleest zie levelfile voor hoe je zelf levels kunt maken
    levels = maakLevel('levels.txt')
    #bonuslevel is stiekum eerste level in file (index 0)
    # dus zet eerst index op 1, en je begint bij level 1 (nummer 2 in de file)
    # pas als je bonuslevel hebt gekozen, wat alleen kan als je alles gehaald hebt
    #dan reset naar 0...daarn loopt de game door zoals altijd
    if BONUSLEVEL:
        currentLevelIndex = 0
    else:    
        currentLevelIndex = 1
        
    #Main game loop
    #als er een level is ingeladen..loopt de loop
    #pas als een level is afgelopen word volgend level geladen
    while True:
        # Daadwerkelijk spelen level
        result = speelLevel(levels, currentLevelIndex)
        #als je daadwerkelijk klaar bent
        if result in ('solved', 'next'):
            # ga naar volgend level
            currentLevelIndex += 1
            uitgangDicht()
            #Maak elk level nog moeilijker door
            #telkens minder tijd te geven voor het oplossen
            #behalve het bonuslevel
            if not BONUSLEVEL:
                TIMER = 201 - math.ceil((currentLevelIndex / 2) * 10)
            if currentLevelIndex >= len(levels):
                # Als alle levels op zijn.....dan ben je klaar
                #ga dan naar victoryscherm
                currentLevelIndex = 0
                #levels = maakLevel('levels.txt')
                #print('Herstart level')
                GrootScherm('victory')
        #dood
        elif result in ('counter0', 'deadBurrower'):
            levels = maakLevel('levels.txt')
        #terug    
        elif result == 'back':
            # een level terug
            currentLevelIndex -= 1
            if currentLevelIndex < 0:
                # als levels op zijn...ga naar het eind
                currentLevelIndex = len(levels)-1
        #reset
        elif result == 'reset':
            pass 
     
#doe het!
if __name__ == '__main__':
    main()