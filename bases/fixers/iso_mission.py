##
# iso_mission.py
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
if (fixers.checkSaveValue(playernum,"iso_mission1",0) and VS.numActiveMissions()<=1):
    fixers.setSaveValue (playernum,"iso_mission1",0)
    #load mission 1
    VS.LoadMission ("defend/iso/defend_iso_mission1.mission")
elif (fixers.checkSaveValue(playernum,"iso_mission2",0) and VS.numActiveMissions()<=1 and fixers.checkSaveValue (playernum,"iso_mission1",1)):
    fixers.setSaveValue (playernum,"iso_mission2",0)
    VS.LoadMission ("escort/iso/escort_iso_mission2.mission")
    #load mission 2
elif (fixers.checkSaveValue(playernum,"iso_mission3",0) and VS.numActiveMissions()<=1 and fixers.checkSaveValue (playernum,"iso_mission2",1)):
    fixers.setSaveValue (playernum,"iso_mission3",0)
    VS.LoadMission ("cargo/iso/cargo_contraband_mission3.mission")
    #load mission 3
elif (fixers.checkSaveValue(playernum,"iso_mission4",0) and VS.numActiveMissions()<=1 and fixers.checkSaveValue (playernum,"iso_mission3",1)):
    fixers.setSaveValue (playernum,"iso_mission4",0)
    VS.LoadMission ("defend/iso/defend_iso_mission4.mission")
    #load mission 4
else:
    Base.message ("Our records indicate that you are already completing a mission. Come back to me when you're done with that business first.")
