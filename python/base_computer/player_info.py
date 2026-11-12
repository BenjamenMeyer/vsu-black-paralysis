##
# player_info.py
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

newline = "#n#"
faction_grey = "#c0.667:0.667:1#"
green = "#c0:1:.5#"
light_grey = "#c.75:.9:1#"
grey = "#c.6:.7:.8#"
light_yellow = "#c.675:.925:.825#"
end_color = "#-c"
bold = "#b#"
end_bold = "#-b"

disallowed_factions = ['graphics', 'planets', 'upgrades', 'unprintable_factions']

def get_color(relation):
    norm_relation = (relation + 1) / 2; # Move relation value into 0-1 range.
    norm_relation = max(0, min(1, norm_relation)); # Make *sure* it's in the right range.
    
    red = 1 - norm_relation
    green = norm_relation
    blue = min(norm_relation, 1-norm_relation)
    
    return f"#c{red}:{green}:{blue}#"

def get_player_info(names, relations, kills):
    total_kills = 0
    
    if len(names) != len(relations) or len(names) != len(kills):
        return f"Error. Length mismatch ({len(names)}/{len(relations)}/{len(kills)})."
    
    text = f"{newline}{bold}Factions:{end_bold}#n1.7#"
    
    for name, relation_str, kills_str in zip(names, relations, kills):
        relation = int(round(float(relation_str) * 100))
        faction_kills = int(kills_str)
            
        total_kills += faction_kills
        
        color = get_color(relation)
        
        if faction_kills == 0 or name == 'privateer':
            text += f"{light_grey}{name:<24}{end_color} {color}{relation:>3}{end_color}{newline}"
        else: 
            text += f"{light_grey}{name:<24}{end_color} {color}{relation:>3}, kills: {faction_kills:>3}{end_color}{newline}"
    
    text += f"{newline}{bold}{"Total Kills":<24} {total_kills:>3}{end_bold}{newline}"
        
    return text
