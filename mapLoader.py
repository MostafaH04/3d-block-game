import csv
import os
import block
import camera

def loadBlocks(camera):
    camPos = camera.np_cPos
    headers = ['X','Y','Z']
    blocksList = []
    lines = []
    with open('./maps/block_map_1.csv', 'r') as blockMap:
        mapReader = csv.DictReader(blockMap)
        for loadedBlock in mapReader:
            x = int(loadedBlock['X'])
            if abs(camPos[0] - x*40) > 150:
                lines.append(loadedBlock)
                continue
            y = int(loadedBlock['Y'])
            if abs(camPos[1] - y*40) > 300:
                lines.append(loadedBlock)
                continue
            z = int(loadedBlock['Z'])
            if abs(camPos[2] - z*40) > 150:
                lines.append(loadedBlock)
                continue

            pos = (x,y,z)
            newBlock = block.block(pos)
            blocksList.append(newBlock)

    with open('./maps/block_map_1.csv', 'w') as blockMap:
        mapWriter = csv.DictWriter(blockMap, fieldnames= headers)
        mapWriter.writeheader()
        rows = lines
        mapWriter.writerows(rows)
    return blocksList

