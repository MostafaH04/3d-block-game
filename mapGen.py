import csv
import os
import block
from copy import deepcopy

headers = ['X','Y','Z']

def storeBlocks(worldBlocks):
    global headers

    with open('./maps/block_map_1.csv', 'a') as blockMap:
        writer = csv.writer(blockMap)

        for i in range(len(worldBlocks)):
            currBlock = worldBlocks[i]
            newBlock = [0,0,0]
            for i in range(len(headers)):
                newBlock[i] = currBlock.posMap[i]
            writer.writerow(newBlock)
        worldBlocks = None
    
      

def addBlock(block):
    global headers

    with open("./maps/block_map_1.csv", "a") as blockMap:
        writer = csv.writer(blockMap)
        
        currBlock = block
        newBlock = [0,0,0]
        for i in range(len(headers)):
            newBlock[i] = currBlock.posMap[i]
        
        writer.writerow(newBlock)




