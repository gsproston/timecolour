#Author: George Sproston
#Started: 2016/07/06
#Last updated: 2016/07/10
#Displays the time on a window coloured by the hex value of the time

import datetime, os.path
import pygame, sys
from pygame.locals import *

pygame.init()

def draw():
    #get time divisions
    hour = str(time.hour).zfill(2)
    minute = str(time.minute).zfill(2)
    second = str(time.second).zfill(2)
    timeDisplay = "%s:%s:%s" % (hour,minute,second)
    hextime = Color("0x%s%s%s" % (hour,minute,second))
    if wRGB: #weight values to cover whole rgb spectrum
        hour = int(time.hour*(255/23))
        minute = int(time.minute*(255/59))
        second = int(time.second*(255/59))
        hextime = Color(hour,minute,second)
    #fill the screen with the hex colour
    screen.fill(hextime)

    #define colours
    if wRGB and int(hour*23/255) >= 13:
        onText = Color(20,20,20)
        offText = Color(80,80,80)
    else:
        onText = Color(255,255,255)
        offText = Color(190,190,190)
    #add the time on top
    textSurface = text.render(timeDisplay,4,onText)
    screen.blit(textSurface,(xpos,ypos)) #combine surfaces

    if menu or ma[0] > 0: #menu should be displayed
        for button in menuList:
            button.fill(hextime)
        #print buttons
        #colour shows which option is currently selected
        #fullscreen button
        if fscreen:
            onc = onText
            offc = offText
        else:
            offc = onText
            onc = offText
        fullscreen.blit(menuText.render("fullscreen",4,onText),(0,texty))
        fullscreen.blit(menuText.render("off",4,offc),(offset,texty))
        fullscreen.blit(menuText.render("|",4,onText),(offset+25,texty-2))
        fullscreen.blit(menuText.render("on",4,onc),(offset+33,texty))
        #borderless button
        if bwindow:
            onc = onText
            offc = offText
        else:
            offc = onText
            onc = offText
        borderless.blit(menuText.render("borderless",4,onText),(0,texty))
        borderless.blit(menuText.render("off",4,offc),(offset,texty))
        borderless.blit(menuText.render("|",4,onText),(offset+25,texty-2))
        borderless.blit(menuText.render("on",4,onc),(offset+33,texty))
        #weighted RGB button
        if wRGB:
            onc = onText
            offc = offText
        else:
            offc = onText
            onc = offText
        weightedRGB.blit(menuText.render("weighted RGB",4,onText),(0,texty))
        weightedRGB.blit(menuText.render("off",4,offc),(offset,texty))
        weightedRGB.blit(menuText.render("|",4,onText),(offset+25,texty-2))
        weightedRGB.blit(menuText.render("on",4,onc),(offset+33,texty))
        #aspectRatio button
        aspectRatio.blit(menuText.render("aspect ratio",4,onText),(0,texty))
        if ratioMenu or ratma > 0:
            ratMenu.fill(hextime)
            for i in range(0,len(ratios)):
                if i == 0:
                    onc = onText
                else:
                    onc = offText
                ratMenu.blit(menuText.render(ratios[i],4,onc),(0,texty+bh*i))
        aspectRatio.blit(menuText.render((ratios[0]),4,onText),(offset,texty))   
        #resolution button
        resolution.blit(menuText.render("resolution",4,onText),(0,texty))
        if resMenu or resma > 0:
            resoMenu.fill(hextime)
            for i in range(0,len(ress[0])):
                if i == 0:
                    onc = onText
                else:
                    onc = offText
                res = "%sx%s" % (ress[0][i][0],ress[0][i][1])
                resoMenu.blit(menuText.render(res,4,onc),(0,texty+bh*i))
        res = "%sx%s" % (windowWidth,windowHeight)
        resolution.blit(menuText.render(res,4,onText),(offset,texty))
    
        count = 0
        for button in menuList: #cycle through menu buttons
            if ma[count] <= 0:
                break
            button.set_alpha(ma[count])
            screen.blit(button,(menux,menuy+bh*count))
            count += 1
        if ratioMenu or ratma > 0:
            ratMenu.set_alpha(ratma)
            screen.blit(ratMenu,(menux+offset,menuy+bh*3))
        if resMenu or resma > 0:
            resoMenu.set_alpha(resma)
            screen.blit(resoMenu,(menux+offset,menuy+bh*4))

    pygame.display.flip()

def wresize(): #screen is resized, recalculate some variables
    global text,xpos,ypos
    fontSize = int(screen.get_height()*fontPercent)
    text =  pygame.font.SysFont('helvetica',fontSize)
    textSurface = text.render("00:00:00",4,Color(255,255,255))
    #centre coords
    xpos = (screen.get_width() - textSurface.get_width())/2
    ypos = (screen.get_height() - textSurface.get_height())/2

def resetFlags(): #new flags set
    if fscreen:
        w = wInfo.current_w
        h = wInfo.current_h
        if bwindow:
            flags = FULLSCREEN|NOFRAME
        else:
            flags = FULLSCREEN
    else:
        w = windowWidth
        h = windowHeight
        if bwindow:
            flags = NOFRAME
        else:
            flags = 0
    pygame.display.set_mode((w,h),flags)
    
if __name__ == "__main__":
    #gets monitor info, used when resizing
    wInfo = pygame.display.Info()

    #variables
    shutdown = False
    windowWidth = 1024
    windowHeight = 576
    flags = 0
    #menu variables
    menu = False
    fscreen = False
    bwindow = False
    wRGB = False
    ratioMenu = False
    ratios = ["16:9","16:10","4:3"]
    resMenu = False
    ress = [[],[],[]]
    res169 = [[1024,576],[1152,648],[1280,720],[1366,768],[1600,900],[1920,1080]]
    res1610 = [[1280,800],[1440,900],[1680,1050]]
    res43 = [[960,720],[1024,768],[1280,960],[1400,1050],[1440,1080],[1600,1200],[1856,1392]]
    ress[0] = res169
    ress[1] = res1610
    ress[2] = res43
    bh = 25 #height
    bw = 200 #width
    menux = 12 #xpos
    menuy = 10 #ypos
    offset = 110
    ma = []
    maTarget = []
    ratma = 0
    ratmaTarget = 0
    resma = 0
    resmaTarget = 0

    #init screen
    screen = pygame.display.set_mode((windowWidth, windowHeight),flags)

    #init font
    fontPercent = 0.2 #percentage of screen size
    fontSize = int(screen.get_height()*fontPercent)
    menuFontSize = 18
    texty = (bh-menuFontSize)/2 #ypos of text in button
    text = pygame.font.SysFont("helvetica",fontSize)
    menuText = pygame.font.SysFont("helvetica",menuFontSize)
    textSurface = text.render("00:00:00",4,Color(255,255,255))
    xpos = (screen.get_width() - textSurface.get_width())/2
    ypos = (screen.get_height() - textSurface.get_height())/2
    
    time = datetime.datetime.today()
    clock = pygame.time.Clock()
    
    #buttons
    fullscreen = pygame.Surface((bw,bh))
    borderless = pygame.Surface((bw,bh))
    weightedRGB = pygame.Surface((bw,bh))
    aspectRatio = pygame.Surface((bw,bh))
    resolution = pygame.Surface((bw,bh))
    ratMenu = pygame.Surface((bw/4,bh*3))
    resoMenu = pygame.Surface((bw/2-10,bh*max(len(res169),len(res1610),len(res43))))

    menuList = [fullscreen,borderless,weightedRGB,aspectRatio,resolution]
    for button in menuList: #for fading menu
        ma.append(0)
        maTarget.append(0)

    draw()

    #main game loop
    while (not shutdown):
        
        for event in pygame.event.get(): #runs when an event occurs
            if event.type == QUIT: #quit called
                shutdown = True #end loop
                
            elif event.type == MOUSEBUTTONDOWN: #mouse clicked
                
                if ratioMenu:
                    change = False
                    for i in range(0,len(ratios)):
                        if Rect((menux+offset,menuy+bh*3+bh*i),(bw/4,bh)).collidepoint(pygame.mouse.get_pos()): #aspect ratio option pressed
                            change = True
                            ratioMenu = False
                            ratmaTarget = 0
                            maTarget[4:5] = [255,255]
                            if i == 0: #no change
                                break
                            ratTemp = ratios[i]
                            resTemp = ress[i]
                            ratios.remove(ratios[i])
                            ress.remove(ress[i])
                            ratios.reverse()
                            ress.reverse()
                            ratios.append(ratTemp)
                            ress.append(resTemp)
                            ratios.reverse()
                            ress.reverse()
                            windowWidth = ress[0][0][0]
                            windowHeight = ress[0][0][1]
                            resetFlags()
                            wresize()
                            draw()
                            break
                    if change:
                        break

                if resMenu:
                    change = False
                    for i in range(0,len(ress[0])):
                        if Rect((menux+offset,menuy+bh*4+bh*i),(bw/2-10,bh)).collidepoint(pygame.mouse.get_pos()): #resolution option pressed
                            change = True
                            resMenu = False
                            resmaTarget = 0
                            maTarget[5] = 255
                            if i == 0: #no change
                                break
                            resTemp = ress[0][i]
                            ress[0].remove(ress[0][i])
                            ress[0].sort()
                            ress[0].reverse()
                            ress[0].append(resTemp)
                            ress[0].reverse()
                            windowWidth = ress[0][0][0]
                            windowHeight = ress[0][0][1]
                            resetFlags()
                            wresize()
                            draw()
                            break
                    if change:
                        break
                    
                if menu:
                    if fullscreen.get_rect().move(menux,menuy).collidepoint(pygame.mouse.get_pos()): #fullscreen pressed
                        if fscreen: #toggle fullscreen
                            fscreen = False
                            resetFlags()
                        else:
                            fscreen = True
                            resetFlags()
                        ratioMenu = False
                        resMenu = False
                        ratmaTarget = 0
                        resmaTarget = 0
                        maTarget[4:5] = [255,255]
                        wresize()
                        draw()
                    elif borderless.get_rect().move(menux,menuy+bh).collidepoint(pygame.mouse.get_pos()): #borderless pressed
                        if bwindow: #toggle borderless
                            bwindow = False
                            resetFlags()
                        else:
                            bwindow = True
                            resetFlags()
                        ratioMenu = False
                        resMenu = False
                        ratmaTarget = 0
                        resmaTarget = 0
                        maTarget[4:5] = [255,255]   
                        draw()
                    elif weightedRGB.get_rect().move(menux,menuy+bh*2).collidepoint(pygame.mouse.get_pos()): #borderless pressed
                        if wRGB: #toggle weighted
                            wRGB = False
                        else:
                            wRGB = True
                        ratioMenu = False
                        resMenu = False
                        ratmaTarget = 0
                        resmaTarget = 0
                        maTarget[4:5] = [255,255]
                        draw()
                    elif aspectRatio.get_rect().move(menux,menuy+bh*3).collidepoint(pygame.mouse.get_pos()): #aspect ratio pressed
                        if ratioMenu: #toggle ratio menu
                            ratioMenu = False
                            ratmaTarget = 0
                            maTarget[4] = 255 #show lower menu
                        else:
                            ratioMenu = True
                            ratmaTarget = 255
                            maTarget[4] = 0 #hide lower menu
                        resMenu = False
                        resmaTarget = 0
                    elif resolution.get_rect().move(menux,menuy+bh*4).collidepoint(pygame.mouse.get_pos()) and maTarget[3] > 0: #resolution pressed
                        if resMenu: #toggle ratio menu
                            resMenu = False
                            resmaTarget = 0
                        else:
                            resMenu = True
                            resmaTarget = 255
                        
            elif event.type == KEYDOWN: #key has been pressed
                if pygame.key.get_pressed()[pygame.K_ESCAPE]: #escape key
                    if menu: #close all menus
                        menu = False
                        ratioMenu = False
                        resMenu = False
                        maTarget = [0,0,0,0,0,0]
                        ratmaTarget = 0
                        resmaTarget = 0
                    else: #open main menu
                        menu = True
                        maTarget = [255,255,255,255,255,255]
                elif pygame.key.get_pressed()[pygame.K_F4]: 
                    if fscreen: #toggle fullscreen
                        fscreen = False
                        screen = pygame.display.set_mode((windowWidth,windowHeight))
                    else:
                        fscreen = True
                        screen = pygame.display.set_mode((wInfo.current_w,wInfo.current_h),FULLSCREEN)
                    wresize()
                    draw()

        #fade in/out menu
        for i in range(0,len(ma)):
            if ma[i] < maTarget[i]:
                ma[i] += 10
                if ma[i] > maTarget[i]:
                    ma[i] = maTarget[i]
                draw()
            elif ma[i] > maTarget[i]:
                ma[i] -= 10
                if ma[i] < maTarget[i]:
                    ma[i] = maTarget[i]
                draw()
        if ratma < ratmaTarget:
            ratma += 10
            if ratma > ratmaTarget:
                ratma = ratmaTarget
            draw()
        elif ratma > ratmaTarget:
            ratma -= 10
            if ratma < ratmaTarget:
                ratma = ratmaTarget
            draw()
        if resma < resmaTarget:
            resma += 10
            if resma > resmaTarget:
                resma = resmaTarget
            draw()
        elif resma > resmaTarget:
            resma -= 10
            if resma < resmaTarget:
                resma = resmaTarget
            draw()
                    
        #get the current time
        newTime = datetime.datetime.today()
        if newTime.second != time.second: #different time, redraw
            time = newTime
            draw()

        clock.tick(200) #update x times a second, determines FPS

    #main loop ends, exit
    pygame.quit()    
