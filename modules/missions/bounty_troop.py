##
# bounty_troop.py
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

import bounty_leader
class bounty_troop(bounty_leader.bounty_leader):
    def __init__(self,minnumsystemsaway, maxnumsystemsaway, creds, run_away, shipdifficulty, tempfaction,jumps=(),var_to_set='',dynfg='',dyntype="",displayLocation=1,dynhelperfg='',dynhelpertype='',greetingText=['It appears we have something in common, privateer.','My name may be on your list, but now your name is on mine.'],leader_upgrades=[],trooptime=30,dockingdist=2400,wastingtime=0):
        bounty_leader.bounty_leader.__init__(self,minnumsystemsaway, maxnumsystemsaway, creds, run_away, shipdifficulty, tempfaction,jumps,var_to_set,dynfg,dyntype,displayLocation,dynhelperfg,dynhelpertype,greetingText,leader_upgrades,True)
        self.trooptime=trooptime
        self.troopdidlaunch=False
        self.inevitabletime=0
        self.dockingdist=dockingdist
        self.wastingtime=wastingtime
        self.wastingtimestart=0
    def LaunchedEnemies(self,significant):
        import VS
        bounty_leader.bounty_leader.LaunchedEnemies(self,significant)
        self.troopdidlaunch=True
        import unit
        self.istarget=1
        capship_only=1
        self.utdw= self.adjsys.SignificantUnit()#unit.getSignificant(0,1,capship_only)
        self.wastingtimestart = VS.GetGameTime()+self.wastingtime
        self.wastingtime=0
        if (self.utdw==self.enemy):
            self.utdw=unit.getSignificant(1,1,capship_only)
        if (self.utdw==self.enemy):
            self.utdw=unit.getSignificant(2,1,capship_only)
        if (self.utdw==self.enemy):
            self.utdw=unit.getSignificant(3,1,capship_only)
        pos=self.utdw.Position()
        if self.dockingdist>0:
            import Vector
            diff=Vector.Sub(self.you.Position(),pos)
            ndiff=Vector.Norm(diff)
            self.enemy.SetPosition(Vector.Add(Vector.Scale(ndiff,self.dockingdist+self.enemy.rSize()+self.utdw.rSize()),pos));

    def Execute(self):
        import VS
        if (self.wastingtimestart!=0 and self.wastingtimestart<VS.GetGameTime() and self.utdw!=self.enemy):
            self.wastingtimestart=0
            self.enemy.performDockingOperations(self.utdw,True)
        bounty_leader.bounty_leader.Execute(self)
        if (self.troopdidlaunch and self.inevitabletime ==0):
            if self.enemy.getDistance(self.utdw)<0:
                self.inevitabletime=VS.GetGameTime()
        if self.inevitabletime !=0 and VS.GetGameTime()-self.inevitabletime>self.trooptime:
            self.utdw.setFactionName(self.enemy.getFactionName())
            self.Lose(1)
