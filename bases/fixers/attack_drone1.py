##
# attack_drone1.py
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
import fixers
plyr=VS.getPlayer().isPlayerStarship()
if quest.findQuest(plyr,'quest_drone',-1):
    Base.Message("""There is an alien vessel let loose on confed territory. We are offering 30,000 credits to anyone who manages to take it out. Be warned, however, our scans reveal armor and shielding that we do not know how to penetrate. Good luck and godspeed!""")
elif quest.findQuest(plyr,'quest_drone',1):
    Base.Message("""Thank you! Your effort saved the lives of trillions of civilians. That drone was terrorizing our people and our space force!""")
    if fixers.checkSaveValue(plyr,'quest_drone_cash',0):
        VS.getPlayer().addCredits(30000)
        quest.removeQuest(plyr,'gemini_sector/quest_drone_cash',1)
