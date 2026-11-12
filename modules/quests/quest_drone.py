##
# quest_drone.py
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

import quest
import Vector
import VS
import unit
import vsrandom

drone=VS.Unit()

class quest_drone (quest.quest):
    def __init__ (self):
        self.sysfile = VS.getSystemFile()
        self.stage=0
        self.lastdist=10000
        self.derelict=VS.Unit()
        self.jumping=0
    def launchNewDrone (self):
        global drone
        playa=VS.getPlayer()
        if (not playa.isNull()):
            self.makeQuestPersistent()
            vec = playa.Position()
            vec = Vector.Add(vec,(1000,0,0))
            drone=VS.launch("IO47","drone","unknown","unit","default",1,1,vec,'')
            VS.AdjustRelation("unknown",playa.getFactionName(),-1,10);
            VS.AdjustRelation(playa.getFactionName(),"unknown",-1,10);
            drone.SetTarget(playa)
            self.stage=1
        else:
            drone=VS.Unit()
    def generateBase (self):
        self.derelict=VS.launch("base","derelict","neutral","unit","sitting_duck",1,1,(-1000000,-1000000,-1000000),'')

    def setDroneNear (self,playa):
        global drone
        vec = playa.Position()
        vec = Vector.Add (vec,(vsrandom.uniform(-1000,1000),
                               vsrandom.uniform(-1000,1000),
                               vsrandom.uniform(-1000,1000)))
        drone.SetCurPosition(vec)
        drone.SetTarget(playa)
    def Execute (self):
        global drone
        playa=VS.getPlayer()
        if (playa.isNull()):
            return 1
        if not quest.checkSaveValue(playa.isPlayerStarship(),'privateer_drone_active',1):
            return 1
        if VS.getSystemFile() == "Gemini/deltaprime":
            if self.derelict.isNull():
                self.generateBase()
        if (not self.stage):
            if (self.derelict and (VS.getSystemFile()==self.sysfile)):
                if (self.derelict.getSignificantDistance(playa)<200):
                    self.launchNewDrone()
            else:
                self.launchNewDrone()
        else:
            if (drone.isNull()):
                self.removeQuest();
                return 0
            sf = VS.getSystemFile();
            if (self.sysfile!=sf and not self.jumping):
                drone.JumpTo(sf);
                self.sysfile=sf
#                self.setDroneNear(playa)
                self.lastdist=10000
                self.jumping=1
                print("jumping")
            else:
                if (self.jumping):
                    if (playa.getUnitSystemFile()==drone.getUnitSystemFile()):
                        drone.SetTarget (playa)
                        self.jumping=0
                        self.setDroneNear(playa)

        return 1

class quest_drone_factory (quest.quest_factory):
    def __init__ (self):
        quest.quest_factory.__init__ (self,"quest_drone")
    def create (self):
        return quest_drone()
