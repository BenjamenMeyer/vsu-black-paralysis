##
# ai_qct_waitjump.py
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
import quest
import Vector
import unit
import vsrandom
import save_util
import faction_ships
import universe
import launch
import quest_contraband_truck


class waitjump(VS.PythonAI):

    def init(self,un):
        self.XMLScript ("++flystraight.xml")
        self.AddReplaceLastOrder(1)
        self.timer = 0
        self.got_target = 0
        self.autoed = 0

    def ChooseTarget(self):
        return

    def Execute(self):
        VS.PythonAI.Execute(self);
        if quest_contraband_truck.truck_exit == 1:
            if self.got_target == 0:
                self.GetParent().SetTarget(universe.getRandomJumppoint())
                self.trucktarget = (self.GetParent()).GetTarget()
                self.XMLScript ("++afterburn-turntowards.xml")
                self.AddReplaceLastOrder(1)
                self.got_target = 1

# starts him afterburning to target

            if self.timer == 0:
                self.timer = VS.GetGameTime()
                print("Timer Set")
            elif self.timer + 30 < VS.GetGameTime() and self.autoed == 0:
                self.GetParent().ActivateJumpDrive(1)
                self.GetParent().AutoPilotTo(self.trucktarget,1)
                self.autoed = 1
            elif self.timer + 5 < VS.GetGameTime():
                self.MoveTo(self.trucktarget.Position(),1)
                self.AddReplaceLastOrder(1)
#                       elif self.timer + 60 < VS.GetGameTime():
# gets him to auto to the jump and jump out
#                               self.GetParent().ActivateJumpDrive(1)
            print(self.GetParent().getMinDis(self.trucktarget.Position()))

        return 1
hi1 = waitjump()
print('AI creation successful')
hi1 = 0
