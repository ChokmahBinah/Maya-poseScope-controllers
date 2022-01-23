import importlib
import maya.cmds as cmds
import maya.mel as mel
import mnt_poseTool

from functools import partial

importlib.reload(mnt_poseTool)

def _null(*args):
    pass

class _shelf():
    iconPath = cmds.getModulePath(moduleName = 'mnt_poseScope') + '/icons/mntShelf/'

    def __init__(self, name = _null, iconPath = iconPath):
        self.name = name

        self.iconPath = iconPath

        self.labelBackground    = (0, 0, 0, 0)
        self.labelColor         = (0.122, 0.122, 0.122)

        self._cleanOldShelf()
        cmds.setParent(self.name)
        self.build()

    def build(self):
        '''This method should be overwritten in derived classes to actually build the shelf
        elements. Otherwise, nothing is added to the shelf.'''
        pass

    def _cleanOldShelf(self):
        if cmds.shelfLayout(self.name, ex = 1):
            if cmds.shelfLayout(self.name, q = 1, ca = 1):
                for each in cmds.shelfLayout(self.name, q = 1, ca = 1):
                    cmds.deleteUI(each)
        else:
            cmds.shelfLayout(self.name, p = "ShelfLayout")

    def addButton(self, label, icon = "pythonFamily.png", ann = _null, enable = _null, command = _null, doubleCommand = _null):
        '''Adds a shelf button with the specified label, command, double click command and image.'''
        cmds.setParent(self.name)
        if icon:
            icon = self.iconPath + icon
        cmds.shelfButton(width = 32, height = 32, image = icon, l = label, en = enable, command = command, dcc = doubleCommand, imageOverlayLabel=label, olb=self.labelBackground, olc=self.labelColor,\
                        ann = ann)
    
    def addSymbolCheckBox(self, icon = 'pythonFamily.png', ann = _null, enable = _null, onCommand = _null, offCommand = _null):
        cmds.setParent(self.name)
        if icon:
            icon = self.iconPath + icon
        cmds.symbolCheckBox(self, width = 32, height = 32, nbg = True, image = icon, en = enable, onCommand = onCommand, offCommand = offCommand)

    def addMenuItem(self, parent, label, enable = _null, command = _null, icon = ""):
        if icon:
            icon = self.iconPath + icon
        return cmds.menuItem(p=parent, l=label, c=command, i = icon)

    def addSubMenu(self, parent, label, icon = None):
        if icon:
            icon = self.iconPath + icon
        return cmds.menuItem(p=parent, l=label, i=icon, subMenu=1)

    def addSeparator(self):
        cmds.separator(enable = True, w = 12, h = 35, manage = True, vis = True, po = True, highlightColor = (0.321, 0.521, 0.650), style = 'shelf', horizontal = False)

class MntCustomShelf(_shelf):
    def build(self):
        crScriptPath = cmds.getModulePath(moduleName = 'mnt_poseScope') + '/scripts/'

        self.addButton(label = '', icon = 'mntController.png', enable = True, ann = 'Create Mnt Locator Node', command = 'cmds.createNode(\'mnt_locator\')')

        self.addButton(label = '', icon = 'mnt_createPoseScope.png', enable = True, command = 'import mnt_poseScopeUI\nposeScopeUI = mnt_poseScopeUI.mnt_poseScopeUI()',\
            ann = 'Opens Mnt_poseScopes Editor')

        self.addSymbolCheckBox(icon = 'mnt_poseTool.png', enable = True, onCommand = 'import mnt_poseTool as mnt_poseTool\nposeTool = mnt_poseTool.mnt_DynSelection()', offCommand = 'poseTool.__del__()')
        self.addButton(label = '', icon = 'mnt_togglePoseScopeVisibility.png', enable = True, command = 'import maya.cmds as cmds\ncmds.togglePoseScopeShapesVisibility()')

        self.addSeparator()

        self.addButton(label = '', icon = 'mntNode.png', enable = True, ann = 'Open Node Editor', command = 'cmds.NodeEditorWindow()')
        self.addButton(label = '', icon = 'mnt_delUnusedNodes.png', enable = True, command = 'mel.eval(\'MLdeleteUnused;\')', ann = 'Delete unused nodes')