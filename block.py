import numpy as np
blockMap = []

class vertex():   

    def __init__(self, num, verCords):
        connectionMap = [
            [2,4,6],
            [1,3,7],
            [2,4,8],
            [1,3,5],
            [4,6,8],
            [1,5,7],
            [2,6,8],
            [3,5,7]
        ]
        self.vertNum = num
        self.connected = connectionMap[num] 
        self.cords = verCords
        self.np_cords = np.asarray(self.cords)


class block():

    def __init__(self, pos):
        global blockMap
        blockMap.append([pos[0],pos[1],pos[2]])
        self.posMap = [pos[0],pos[1],pos[2]]
        self.position = (pos[0]*40,pos[1]*40,pos[2]*40)
        self.verticies = []
        self.faces =[]

        while self.addVert():
            continue
        
        self.collectFaces()
    
    def addVert(self):
        vertNum = len(self.verticies)
        if vertNum > 7:
            return False

        vertMap = [
            [0,40,0],
            [40,40,0],
            [40,0,0],
            [0,0,0],
            [0,0,40],
            [0,40,40],
            [40,40,40],
            [40,0,40]
        ]

        vertPos = vertMap[vertNum]
        for i in range(len(vertPos)):
            vertPos[i] += self.position[i]
        
        currVert = vertex(vertNum, vertPos)
        self.verticies.append(currVert)
        return True

    def dispCords(self):
        for vertex in self.verticies:
            print(vertex.vertNum, vertex.connected, vertex.cords)

    def collectFaces(self):
        # front, right, back, left, top, bottom
        faceMap = [
            [0,1,2,3],
            [1,6,7,2],
            [6,5,4,7],
            [5,0,3,4],
            [0,5,6,1],
            [3,4,7,2]
        ]
        for face in faceMap:
            newFace = []
            for vert in face:
                newFace.append(self.verticies[vert])
            self.faces.append(newFace)
        
