import pygame
from pygame import color
from pygame import draw
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from pygame.locals import KEYDOWN, QUIT  
from camera import camera
import block
import renderer
from math import sin, cos, pi, trunc

sensetivity = 0.06

pygame.init()
size = width, height = 1280, 720
root = pygame.display.set_mode(size)
font = pygame.font.SysFont('arial',18)
clock = pygame.time.Clock()

gameCam = camera(width, height, 70)
gameRenderer = renderer.renderer()

worldBlocks = []

for x in range(10):
    for z in range(10):
        worldBlocks.append(block.block([x,0,z]))

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

    return sortedBlocks[::-1]

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
        newBlock = block.block([newBlockX,newBlockY,newBlockZ])
        if newBlock not in worldBlocks:
            worldBlocks.append(newBlock)
    
    root.fill((144, 203, 245))

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

        """
        for pixel in pixels:
            if pixel not in renderedPoints:
                draw.circle(root, (0,0,0), (pixel[0]+width/2,pixel[1]+height/2), 4, 4)
                renderedPoints.append(pixel)
            
            for otherPixels in pixels:
                if pixel == otherPixels:
                    continue
                draw.line(root, (0,0,0), (pixel[0]+width/2,pixel[1]+height/2), (otherPixels[0]+width/2,otherPixels[1]+height/2), 1)
        """ 
    

    draw.circle(root, (255, 255, 255), (width/2, height/2), 3, 3)

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