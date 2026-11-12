##
# attack_drone0.py
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
if quest.findQuest(plyr,'gemini_sector/delta_prime_navpoint',1):
    VS.getPlayer().addCredits(20000)
    quest.removeQuest(plyr,'gemini_sector/delta_prime_navpoint',2)
Base.Message("Congratulations on giving us the data on the last sector! We seem to have found a passage deep into Aera territory. Perhaps even the aera haven't completely civilized that sector of space.  Rumor has it that an unknown vessel has emerged from the jump point you discovered.  If you have any scans or information please take them to one of my former associates in the Enigma system.  Thank you for working with me, and I hope you have found it to be a profitable and worthwhile venture.")
