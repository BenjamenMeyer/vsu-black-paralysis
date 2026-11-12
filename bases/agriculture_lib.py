##
# agriculture_lib.py
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

import Base
import bar_lib
import weapons_lib
import dynamic_mission
import VS
def MakeAgri (time_of_day='_day'):
    plist=VS.musicAddList('agricultural.m3u')
    VS.musicPlayList(plist)
    dynamic_mission.CreateMissions()
    room1 = Base.Room ('Main Concourse')
    Base.Texture (room1, 'tex', 'bases/agriculture/landing'+time_of_day+'.spr', 0, 0)
    Base.Comp (room1, 'CargoComputer', -0.306641, -0.263021, 0.105469, 0.420833, 'Cargo Computer', 'Cargo')
    Base.Comp (room1, 'MissionComputer', 0.292969, -0.263021, 0.0878906, 0.420833, 'Mission Computer', 'News Missions')
    Base.Ship (room1, 'ship', (0.0253906*2,-0.148958*2,4), (0,.93,-.34), (-1,0,0))
    bar = bar_lib.MakeBar (room1,time_of_day)
    weap = weapons_lib.MakeWeapon (room1,time_of_day)
    Base.Link (room1, 'BarLink', 0.580078, -1, 0.419922, 1.09115, 'Bar', bar)
    Base.Link (room1, 'WeaponsRoom', -1, -1, 0.419922, 1.09115, 'Weapons Room', weap)
    Base.LaunchPython (room1, 'launch','bases/launch_music.py', -1, -1, 2, .8, 'Launch Your Ship')
    ### MUST BE LAST LINK ###
    return (room1,bar,weap)
