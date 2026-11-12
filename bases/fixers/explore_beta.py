##
# explore_beta.py
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
import VS
import Director
import quest
plyr=VS.getPlayer().isPlayerStarship()
if VS.numActiveMissions()<=1:
    if quest.findQuest(plyr,'gemini_sector/delta_navpoint',1):
        VS.getPlayer().addCredits(5000)
        quest.removeQuest(plyr,'gemini_sector/delta_navpoint',2)
    Base.Message('''Congratulations on your first mission! We have decided to go to the next system.
Based on the data that you have collected, it appears that the other jump point should go
to a system that we have named #55ffffbeta#000000. Again, collect info
on six objects there and report back to me with your info.  You will earn 10000 credits.''')
    VS.LoadMission('patrol/explore_beta.mission')
else:
    Base.Message('''Hi. Our records indicate that you are already completing another mission.  Finish
that and then come back to me.''')
