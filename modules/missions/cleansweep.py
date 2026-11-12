##
# cleansweep.py
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

import patrol_enemies
import unit
class cleansweep(patrol_enemies.patrol_enemies):
    def __init__(self,numsystemsaway, num_points,distance,creds,jumps,donevar,minships,maxships,encounterprob,capshipprob,faction, forceattack,canrunaway):
        patrol_enemies.patrol_enemies.__init__(self,numsystemsaway, num_points,distance,creds,jumps,donevar,minships,maxships,encounterprob,capshipprob,faction,forceattack)
        self.enum=0
        self.canrunaway=canrunaway
        self.activeships=[]
        self.guaranteed_success=False

    def Track(self,shiptype):
        import VS
        obj=VS.addObjective("Destroy %s."%(unit.getUnitFullName(shiptype,True)))
        VS.setOwner(obj,self.you)
        VS.setCompleteness(obj,-1.0)
        self.activeships.append((shiptype,obj))
    def SuccessMission(self):
        self.guaranteed_success=True
    def RealSuccessMission(self):
        patrol_enemies.patrol_enemies.SuccessMission(self)
    def DeletePatrolPoint(self,num,nam):
        patrol_enemies.patrol_enemies.DeletePatrolPoint(self,num,nam)
    def Dead(self,activeship):
        import VS
        runawaydist=7000
        tmp = (self.canrunaway and activeship[0].GetHullPercent()<.7)
        if tmp:
            VS.setCompleteness(activeship[1],0.0)
        return ((tmp and self.you.getDistance(activeship[0])>runawaydist) or not activeship[0])
    def Execute(self):
        if (self.enum>=len(self.activeships)):
            self.enum=0
        else:
            if (self.Dead(self.activeships[self.enum])):
                import VS
                VS.setCompleteness(self.activeships[self.enum][1],1.0)
                del self.activeships[self.enum]
            else:
                self.enum+=1
        if (len(self.activeships)==0 and self.guaranteed_success):
            self.RealSuccessMission()
        else:
            patrol_enemies.patrol_enemies.Execute(self)
