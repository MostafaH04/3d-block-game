import block
from camera import camera
import numpy as np
from math import cos, sin, pi
from copy import deepcopy

class renderer():
    def __init__(self):
        self.name = 'renderer'
        self.skippedPixles = []
    
    def posToCam(self, vertexA, camera):
        camPos = camera.np_cPos
        camOrientation = camera.np_theta
        camOx = camOrientation[0] * pi/180
        camOy = camOrientation[1] * pi/180
        camOz = camOrientation[2] * pi/180

        aPos = vertexA.np_cords

        rotMat1 = np.array([
            [1, 0, 0],
            [0, cos(camOx), sin(camOx)],
            [0, -sin(camOx), cos(camOx)]
        ])
        rotMat2 = np.array([
            [cos(camOy), 0, -sin(camOy)],
            [0, 1, 0],
            [sin(camOy), 0, cos(camOy)]
        ])
        rotMat3 = np.array([
            [cos(camOz), sin(camOz), 0],
            [-sin(camOz), cos(camOz), 0],
            [0, 0, 1]
        ])

        aDiffVec = np.subtract(aPos, camPos)

        posToCam = np.matmul(rotMat1, rotMat2)
        posToCam = np.matmul(posToCam, rotMat3)
        posToCam = np.matmul(posToCam, aDiffVec)

        return posToCam
    

    def posOnDisp(self, posToCam, camera):
        # find projection on 2d plane in matrix form
        # using the notion of homogeneous coordinates
        dPos = camera.dPos
        dPosX = dPos[0]
        dPosY = dPos[1]
        dPosZ = dPos[2] 
        mulMatDist = np.array([
            [1, 0, (dPosX/dPosZ)],
            [0, 1, (dPosY/ dPosZ)],
            [0, 0, (1/dPosZ)]
        ])
        fArr = np.matmul(mulMatDist, posToCam)
        pos2dX = fArr[0]/fArr[2]
        pos2dY = fArr[1]/fArr[2]
        pos2d = [pos2dX, pos2dY]
        return pos2d

    """
    def render(self, block , camera):
        projectionPixels = []
        furthest = [0, 0]
        for vertex in block.verticies:
            if vertex.cords in self.skippedPixles:
                projectionPixels.append(None)
                continue
            np_posToCam = self.posToCam(vertex, camera)
            distTot = 0
            for i in np_posToCam:
                distTot += pow(i, 2)
            if abs(distTot) > furthest[0]:
                furthest[0] = distTot
                furthest[1] = vertex.vertNum
            if np_posToCam[2] < 0:
                projectionPixels.append(None)
                continue
            projectedPos = self.posOnDisp(np_posToCam, camera)
            if projectedPos == None:
                projectionPixels.append(None)
                continue
            projectionPixels.append(projectedPos)
        skippedPix = projectionPixels[furthest[1]]
        projectionPixels[furthest[1]] = None
        self.skippedPixles.append(block.verticies[furthest[1]].cords)
        return projectionPixels
    """

    def render(self, worblock, camera):
        facePoints = {}
        furthest = 0
        for face in range(len(worblock.faces)):
            blockPos = deepcopy(worblock.posMap)         
            if face == 0:
                #front
                blockPos[2] -= 1
            elif face == 1:
                #right
                blockPos[0] += 1
            elif face == 2:
                #back
                blockPos[2] += 1
            elif face == 3:
                #left
                blockPos[0] -= 1
            elif face == 4:
                #top
                blockPos[1] += 1
            elif face == 5:
                #bottom
                blockPos[1] -= 1
            if blockPos in block.blockMap:
                continue
            
            polyPoints = []
            avgDist = 0
            for vert in worblock.faces[face]:
                np_posToCam = self.posToCam(vert, camera)
                if np_posToCam[2] < 0:
                    polyPoints.append(None)
                    break
                distTot = 0
                for i in np_posToCam:
                    distTot += pow(i, 2)
                projectedPos = self.posOnDisp(np_posToCam, camera)
                if projectedPos[0] > 2000 or projectedPos[1] > 1300:
                    polyPoints.append(None)
                    break
                polyPoints.append(projectedPos)
                
                if avgDist < distTot:
                    avgDist = distTot

            if None not in polyPoints:
                facePoints[avgDist] = [polyPoints, face]
                if avgDist > furthest:
                    furthest = avgDist
        try:
            del facePoints[furthest]
        except:
            print("cant delete")
        return facePoints

