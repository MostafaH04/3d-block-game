import pygame
from pygame import color
from pygame import draw
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from pygame.locals import KEYDOWN, QUIT  
from camera import camera
import block
import renderer
from math import sin, cos, pi, trunc
import asyncio
import csv
import os
import mapGen, mapLoader

mapDist = "./maps/"

sensetivity = 0.06

pygame.init()
size = width, height = 1280, 720
root = pygame.display.set_mode(size)
font = pygame.font.SysFont('arial',18)
clock = pygame.time.Clock()

gameCam = camera(width, height, 70)
gameRenderer = renderer.renderer()

running = True
escaped = False
mousePos = pygame.mouse.get_pos()

def blockDistSquared (block, camPos):
    blockPos = block.position
    dist = 0
    for i in range(len(blockPos)):
        dist += (blockPos[i] - camPos[i])**2
    return abs(dist)

def furthestBlock(blocksArr):
    furthest = [0, 0]
    camPos = gameCam.np_cPos
    for block in range(len(blocksArr)):
        blockDist = blockDistSquared(blocksArr[block], camPos)
        if furthest[0] < blockDist:
            furthest[0] = blockDist
            furthest[1] = blocksArr[block]
    return furthest[1]

def sortBlocks(blocksArr):
    sortedBlocks = []
    for i in range(len(blocksArr)):
        sortedBlocks.append(furthestBlock(blocksArr))
        blocksArr.remove(furthestBlock(blocksArr))

    return sortedBlocks


async def renderBlocks(worldBlocks):
    global gameCam
    global gameRenderer
    global root
    for worblock in worldBlocks:
        distToCam = gameRenderer.posToCam(worblock.verticies[0], gameCam)
        #if distToCam[2] > 0 and (abs(distToCam[1]) < 500 and abs(distToCam[2]) < 500 and abs(distToCam[0]) < 500):
        facePoints = gameRenderer.render(worblock, gameCam)
        {k: v for k, v in sorted(facePoints.items(), key=lambda item: item[1])}
        for face in facePoints:
            faceNum = facePoints[face][1]
            color = (255,255,255)
            keyList = list(facePoints.keys())
            try:
                if faceNum == 5:
                    color = (20, 140, 54)
                elif faceNum == 4:
                    color = (87, 29, 0)

                if faceNum == 0 or faceNum == 2:
                    color = (140, 60, 20)
                
                elif faceNum == 1 or faceNum == 3:
                    color = (105, 40, 8)
                
            except:
                print("cant colour")
            

            face = facePoints[face][0]
            for point in range(len(face)):
                face[point][0]+=width/2
                face[point][1]+=height/2
            draw.polygon(root, color, face)
    
    mapGen.storeBlocks(worldBlocks)
    worldBlocks = None

while running:
    if pygame.mouse.get_focused() and not escaped:
        pygame.mouse.set_pos([width/2, height/2])
        if pygame.mouse.get_visible():
            pygame.mouse.set_visible(False)

    else:
        if not escaped:
            escaped = True
        pygame.mouse.set_visible(True)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if escaped:
                    escaped = False
                else:
                    escaped = True
        
        if event.type == MOUSEMOTION and not escaped:
            possibleY = (height/2 - event.pos[1])
            possibleX = (width/2 - event.pos[0])
            if (gameCam.np_theta[0] >= 90 and possibleY < 0) or (gameCam.np_theta[0] <= -90 and possibleY > 0) or (gameCam.np_theta[0] < 90 and gameCam.np_theta[0] > -90):
                gameCam.np_theta[0] += possibleY * sensetivity 
            if gameCam.np_theta[0] > 90:
                gameCam.np_theta[0] = 90
            elif gameCam.np_theta[0] < -90:
                gameCam.np_theta[0] = -90
            gameCam.np_theta[1] -= possibleX * sensetivity
            while gameCam.np_theta[1] < 0:
                gameCam.np_theta[1] = 360 - gameCam.np_theta[1]
            while gameCam.np_theta[1] > 360 and possibleX < 0:
                gameCam.np_theta[1] = gameCam.np_theta[1] - 360

    keysPressed = pygame.key.get_pressed()
    if keysPressed[pygame.K_a]:
        gameCam.np_cPos[0] += sin((gameCam.np_theta[1]-90)*pi/180) * 60/(clock.get_fps()+1)
        gameCam.np_cPos[2] += cos((gameCam.np_theta[1]-90)*pi/180) * 60/(clock.get_fps()+1)
    
    if keysPressed[pygame.K_d]:
        gameCam.np_cPos[0] -= sin((gameCam.np_theta[1]-90)*pi/180) * 60/(clock.get_fps()+1)
        gameCam.np_cPos[2] -= cos((gameCam.np_theta[1]-90)*pi/180) * 60/(clock.get_fps()+1)
    
    if keysPressed[pygame.K_s]:
        gameCam.np_cPos[0] -= sin(gameCam.np_theta[1]*pi/180) * 60/(clock.get_fps()+1)
        gameCam.np_cPos[2] -= cos(gameCam.np_theta[1]*pi/180) * 60/(clock.get_fps()+1)
    
    if keysPressed[pygame.K_w]:
        gameCam.np_cPos[0] += sin(gameCam.np_theta[1]*pi/180) * 60/(clock.get_fps()+1)
        gameCam.np_cPos[2] += cos(gameCam.np_theta[1]*pi/180) * 60/(clock.get_fps()+1)
    
    if keysPressed[pygame.K_SPACE]:
        gameCam.np_cPos[1] -= 1.5  * 60/(clock.get_fps()+1)
    
    if keysPressed[pygame.K_LSHIFT]:
        gameCam.np_cPos[1] += 1.5 * 60/(clock.get_fps()+1)
    
    if keysPressed[pygame.K_LALT]:
        newBlockX = int(round(gameCam.np_cPos[0]/40,2))
        newBlockY = int(round(gameCam.np_cPos[1]/40,2)) + 2
        newBlockZ = int(round(gameCam.np_cPos[2]/40,2))
        newsPosArr = [newBlockX, newBlockY, newBlockZ]
        if [newBlockX, newBlockY, newBlockZ] not in block.blockMap:
            newBlock = block.block([newBlockX,newBlockY,newBlockZ])
            mapGen.addBlock(newBlock)
    
    root.fill((144, 203, 245))
    
    renderedFaces = []
    worldBlocks = mapLoader.loadBlocks(gameCam)
    worldBlocks = sortBlocks(worldBlocks)
    asyncio.run(renderBlocks(worldBlocks))
    """
    renderedLines = []
    gameRenderer.skippedPixles = []
    worldBlocks = sortBlocks(worldBlocks)
    for worblock in worldBlocks:
        pixels = gameRenderer.render(worblock, gameCam)
        for i in range(len(pixels)):
            if pixels[i] == None:
                continue
            connectedPoints = worblock.verticies[i].connected
            for j in connectedPoints:
                j-=1
                pixel1 = pixels[i]
                pixel2 = pixels[j]
                if (pixel1,pixel2) not in renderedLines:
                    if pixels[j] == None:
                        continue
                    draw.line(root,
                        (0,0,0),
                        (pixel1[0]+width/2, pixel1[1]+height/2),
                        (pixel2[0]+width/2, pixel2[1]+height/2),
                        1
                    )
                    renderedLines.append((pixel1,pixel2))

        for pixel in pixels:
            if pixel not in renderedPoints:
                draw.circle(root, (0,0,0), (pixel[0]+width/2,pixel[1]+height/2), 4, 4)
                renderedPoints.append(pixel)
            
            for otherPixels in pixels:
                if pixel == otherPixels:
                    continue
                draw.line(root, (0,0,0), (pixel[0]+width/2,pixel[1]+height/2), (otherPixels[0]+width/2,otherPixels[1]+height/2), 1)
        """ 
    

    draw.circle(root, (0, 0, 0), (width/2, height/2), 3, 3)

    if escaped:
        escapeSurf = pygame.Surface(size)
        escapeSurf.set_alpha(128)
        escapeSurf.fill((150,150,150))
        root.blit(escapeSurf, (0,0))
    else:
        posText = (f"X: {round(gameCam.np_cPos[0]/40,2)} / Y: {round(-gameCam.np_cPos[1]/40,2)} / Z: {round(gameCam.np_cPos[2]/40,2)}")
        renderedPosText = font.render(posText, True, (255,255,255))
        root.blit(renderedPosText, (5,5))
        

    txt = str(int(clock.get_fps()))
    renderedTxt = font.render(txt, True, (255,255,255))
    root.blit(renderedTxt, (width-100, 5))

    mousePos = pygame.mouse.get_pos()
    clock.tick(60)
    pygame.display.update()

pygame.quite()