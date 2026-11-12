##
# privateer.py
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

from trading import trading
from random_encounters import random_encounters
from difficulty import difficulty
import dynamic_universe
#from garbage_collect import garbage_collect
import VS
import Director
import Briefing
import ShowProgress
class hideProgress:
    def Execute(self):
        pass
        #VS.hideSplashScreen()
        #ShowProgress.deactivateProgressScreen('loading')

class privateer (Director.Mission):
    loops=()

    def __init__ (self,sigdis, detectiondis, gendis, minships, genships, fighterprob, enemyprob, capprob, credits_to_maximize_difficulty, capdist):#negative garbage collect dist disables that feature
        Director.Mission.__init__(self)
        self.loops=(difficulty (credits_to_maximize_difficulty),
              random_encounters (sigdis, detectiondis, gendis, minships,genships,fighterprob,enemyprob,capprob,capdist),
              trading (),
              dynamic_universe,
              #garbage_collect (),
              hideProgress())

    def Execute(self): #this execute function should not need to be changed...
        if VS.networked():
            import client
            client.Execute()
            return # Do not want to do anything to get out of sync.
        for i in self.loops:
            i.Execute()

    def initbriefing(self):
        print("ending briefing")
    def loopbriefing(self):
        print("loop briefing")
        Briefing.terminate();
    def endbriefing(self):
        print("ending briefing")

#def initstarsystem():
#  random_encounters.initstarsystem() #??? that isn't there
