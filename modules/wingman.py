##
# wingman.py
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

from go_to_adjacent_systems import *
from go_somewhere_significant import *
import vsrandom
import launch
import faction_ships
import VS
import Briefing
import universe
import unit
import Director
class wingman (Director.Mission):
    def __init__ (self,price,factionname,numships,difficulty):
        Director.Mission.__init__(self)
        self.price=price
        self.faction=factionname
        self.you = VS.getPlayer()
        self.numships=numships
        self.diff=difficulty
        self.adjsys=go_somewhere_significant (self.you,0,5000,0)
        self.wingship = faction_ships.getRandomFighter(factionname)
        nam = "[%s]" % self.wingship
        self.adjsys.Print("Hello I'm waiting for your arrival at %s" ,self.wingship)
        VS.IOmessage(1,self.wingship,"all","Once you meet me")
        VS.IOmessage(2,self.wingship,"all","I will obey your commands until our contracts expire.")

    def GenerateWingmen(self):
        if (self.you):
            if (self.you.getCredits()>=self.price):
                self.you.addCredits(-self.price)
                lead=launch.launch_wave_around_unit(self.you.getFlightgroupName(),
                                                    self.you.getFactionName(),
                                                    self.wingship,
                                                    "default",
                                                    self.numships,
                                                    500,
                                                    1000,
                                                    self.you)
                VS.IOmessage (0,lead.getName(),"all","I am at your service commander. Let us succeed!")
            else:
                lead=launch.launch_wave_around_unit("ForHire",
                                                    self.faction,
                                                    self.wingship,
                                                    "default",
                                                    self.numships,
                                                    500,
                                                    1000,
                                                    self.you)
                if (self.diff>0):
                    lead.SetTarget(self.you)
                    VS.IOmessage (0,lead.getName(),"all","You don't have the agreed money... prepare to DIE!")
                else:
                    VS.IOmessage (0,lead.getName(),"all","You don't have the money. A fool like you won't last long!")
    def Execute (self):

        if (self.adjsys.Execute()):
            self.GenerateWingmen()
            VS.terminateMission(1)
    def initbriefing(self):
        print("ending briefing")
    def loopbriefing(self):
        print("loop briefing")
        Briefing.terminate();
    def endbriefing(self):
        print("ending briefing")
