##
# quest.py
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

import Director
import VS

def getQuestLength(playernum,questname):
    return Director.getSaveDataLength(int(playernum),str(questname))

def findQuest (playernum,questname,value=1):
#    print 'finding nonperisstent quest'
#    print questname
    mylen=getQuestLength(playernum,questname)
#    print mylen
    if (mylen>0):
        myfloat=Director.getSaveData(int(playernum),str(questname),0)
#        print myfloat
        if (myfloat==value):
            return 1
    return 0

def checkSaveValue(playernum,questname,value=1):
    mylen=Director.getSaveDataLength(playernum,questname)
#    print mylen
    if (mylen>0):
        myfloat=Director.getSaveData(playernum,questname,0)
    else:
        myfloat=0
    if (myfloat==value):
        return 1
    return 0

def persistentQuest (playernum,questname):
    print("finding quest")
    print(questname)
    return findQuest (playernum,questname,-1)

def notLoadedQuest(playernum,questname):
    print('finding nonloaded quest')
    print(questname)
    return not persistentQuest(playernum,questname) and not findQuest (playernum,questname)

def removeQuest (playernum,questname,value=1):
    print("removing quest")
    mylen=Director.getSaveDataLength(int(playernum),str(questname))
    if (mylen>0):
        Director.putSaveData(int(playernum),str(questname),0,float(value))
    else:
        Director.pushSaveData(int(playernum),str(questname),float(value))

def playSoundCockpit(soundfile):
    try:
        VS.playSoundCockpit(soundfile)
    except AttributeError:
        VS.playSound(soundfile, VS.getPlayer().Position(), (0,0,0))

class quest:
    def NoSignificantsNear(self):
        pass
    def SignificantsNear(self,significant):
        pass
    def setOwner(self,playernum,questname):
        self.name=questname
        self.playernum=playernum
    def removeQuest(self,value=1):
        removeQuest(self.playernum,self.name,value)
    def makeQuestPersistent(self):
        self.removeQuest(-1)
    def isPersistent (self):
        return persistentQuest (self.playernum,self.name)
    def Execute(self):
        print("default")
        return 1
class quest_factory:
    def __init__(self,questname,remove_quest_on_run=0):
        self.removequest=remove_quest_on_run
        self.name=questname
    def __eq__(self,oth):
        return self.name==oth.name
    def create (self ):
        return quest()
    def precondition (self,playernum):
        return 1
    def persistent_factory(self,playernum):
        if (persistentQuest(playernum,self.name)):
            print("persistent_factory")
            return self.private_create(playernum)
        return
    def private_create (self,playernum):
        newquest=self.create()
        newquest.setOwner(playernum,self.name)
        if (self.removequest):
            removeQuest(playernum,self.name)
        return newquest
    def factory (self,playernum):
        if (self.precondition(playernum)):
            if (notLoadedQuest (playernum,self.name)):
                print("nonpfact")
                return self.private_create(playernum)
        return

class test_quest (quest):
    def __init__ (self):
        self.i=0
    def Execute (self):
        print(self.i)
        self.i+=1
        if (self.i>100):
            self.removeQuest()
            return 0
        return 1

class test_quest_factory (quest_factory):
    def __init__ (self):
        quest_factory.__init__ (self,"drone_quest")
    def create (self):
        return test_quest()
