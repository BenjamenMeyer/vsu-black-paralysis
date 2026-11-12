##
# iso_antagonist_mission.py
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

import fixers
import Base
fixers.DestroyActiveButtons ()
playernum = VS.getPlayer().isPlayerStarship()
if (fixers.checkSaveValue(playernum,"iso_evil2",0) and VS.numActiveMissions()<=1):
    fixers.setSaveValue (playernum,"iso_evil2",0)
    #load mission 2
    VS.LoadMission ("bounty/iso/attack_iso_freighter.mission")
elif (fixers.checkSaveValue(playernum,"iso_evil3",0) and VS.numActiveMissions()<=1):
    fixers.setSaveValue (playernum,"iso_evil3",0)
    VS.LoadMission ("bounty/iso/attack_iso_prisoners.mission")
    #load mission 2
elif (fixers.checkSaveValue(playernum,"iso_evil4",0) and VS.numActiveMissions()<=1):
    fixers.setSaveValue (playernum,"iso_evil4",0)
    VS.LoadMission ("defend/iso/attack_iso_force.mission")
    #load mission 3
else:
    Base.message ("Ahh but you are already completing a mission. Come back to me when you're done with that contract first.")
