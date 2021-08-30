from math import tan, pi
import numpy as np


# Used to create prespective projection
class camera():

    def __init__(self, width, height, feildOfView):
        # Position of display surface relative to camera
        dPosX = 0
        dPosY = 0
        dPosZ = width/2 * tan((180-feildOfView)/2 * pi/180)
        self.dPos = [dPosX, dPosY, dPosZ]
        np_dPos = np.asarray(self.dPos)
        self.np_dPos = np_dPos.astype(float)

        # Camera Position
        cPosX = 0
        cPosY = -70
        cPosZ = 0
        self.cPos = [cPosX, cPosY, cPosZ]
        np_cPos = np.asarray(self.cPos)
        self.np_cPos = np_cPos.astype(float)

        # Camera angle in degrees
        thetaX = 0
        thetaY = 0
        thetaZ = 0
        self.theta = [thetaX, thetaY, thetaZ]
        np_theta = np.asarray(self.theta)
        self.np_theta = np_theta.astype(float)
        