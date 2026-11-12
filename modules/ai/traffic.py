##
# traffic.py
#
# Vega Strike: Black Paralysis - Space Simulation, Combat and Trading
# Copyright (C) 2003-2005 Daniel Aleksandrow <dandandaman@users.sourceforge.net>
# Copyright (C) 2003-2026 The Vega Strike Contributors
#
# https://github.com/vegastrike/vsu-black-paralysis
#
# This file is part of Vega Strike: Black Paralysis.
#
# Vega Strike: Black Paralysis is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Vega Strike: Black Paralysis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Vega Strike: Black Paralysis.  If not, see <https://www.gnu.org/licenses/>.
#

import VS
import sys
import vsrandom
from Vector import *
import car_lib
maxspeed=45

class TrafficAI(VS.PythonAI):
    def restoreCruisingSpeed(self,speed):
        vel = Scale (self.GetParent().GetOrientation()[2],speed)
        self.MatchLinearVelocity(0,vel,0,1)
        self.AddReplaceLastOrder(1)
        self.GetParent().setSpeed(speed)
    def init(self,un):
        self.shipiter=0;
        self.speed = vsrandom.uniform (maxspeed/3,maxspeed);
        print('self.speed')
        print(self.speed)
        self.stopping=0
        self.begin=1
        self.restoreCruisingSpeed(self.speed)
    def Execute(self):
        if (self.begin):
            self.begin=0
            self.restoreCruisingSpeed(self.speed)
        VS.PythonAI.Execute(self)
        un = VS.getUnit (self.shipiter);
        parent = self.GetParent()
        if (parent and un):
            if (parent!=un):
                if (car_lib.isCar (un)):
                    posdiff=SafeNorm(Sub (un.Position(),parent.Position()))                         #look 1 second ahead
#                               distInOneSec = Dot (Sub(parent.GetVelocity(),un.GetVelocity()),posdiff)
                    distInOneSec = Dot (Sub(parent.GetVelocity(),un.GetVelocity()),posdiff)
                    if (distInOneSec>un.getDistance(parent) and Dot (posdiff,un.GetOrientation()[2])>0):
#                                       print "%s too close to %s \n" % (parent.getName(),un.getName())
#                                       print distInOneSec
#                                       print un.getDistance (parent)
                        self.restoreCruisingSpeed(0)
                        self.stopping=1
                        self.shipiter=-1 #-1 + 1 =0

            self.shipiter +=1
        else:
            if (self.stopping):
                if (parent):
                    self.stopping=0
                    self.restoreCruisingSpeed(self.speed)
            self.shipiter=0
        return
hi1 = TrafficAI()
print('AI creation successful')
hi1 = 0
#: 1.7; previous revision: 1.6
