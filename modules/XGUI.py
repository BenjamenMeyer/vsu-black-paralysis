##
# XGUI.py
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
import GUI
import XGUITypes
import XGUIDebug


XGUIRootSingleton = None
XGUIPythonScriptAPISingleton = None

"""----------------------------------------------------------------"""
"""                                                                """
""" XGUIRoot - root management interface for the XML-GUI framework."""
"""                                                                """
"""----------------------------------------------------------------"""


class XGUIRoot:
    def __init__(self):
        self.templates = {}

    def getTemplate(self,type,name):
        if type in self.templates and name in self.templates[type]:
            return self.templates[type][name]
        else:
            return None

    def addTemplate(self,tpl):
        type = tpl.getType()
        name = tpl.getName()
        if not type in self.templates:
            XGUIDebug.trace(1,"XGUI: Initializing template category \"" + str(type) + "\"\n")
            self.templates[type] = {}
        XGUIDebug.trace(2,"XGUI: Loading template \"" + str(name) + "\" into category \"" + str(type) + "\"\n")
        self.templates[type][name] = tpl

class XGUIPythonScript:
    def __init__(self,code,filename):
        code = code.replace("\r\n","\n")
        code += "\n"
        self.code = compile(code,filename,'exec')

    def execute(self,context):
        exec(self.code, context)
        return context


"""----------------------------------------------------------------"""
"""                                                                """
"""  XGUIPythonScriptAPI - through this class, all PythonScript    """
"""     API calls are routed.                                      """
"""                                                                """
"""----------------------------------------------------------------"""

class XGUIPythonScriptAPI:
    def __init__(self,layout,room):
        self.layout = layout
        self.room = room



"""----------------------------------------------------------------"""
"""                                                                """
"""  XGUI global initialization                                    """
"""                                                                """
"""----------------------------------------------------------------"""

def XGUIInit():
    XGUIRootSingleton = XGUIRoot()
