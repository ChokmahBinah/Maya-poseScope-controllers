import importlib
import maya.cmds as cmds
import maya.mel as mel
import mnt_poseScopeShelf

importlib.reload(mnt_poseScopeShelf)


try:
    cmds.loadPlugin('mnt_locator.py')
    cmds.loadPlugin('mnt_groupNode.py')
    cmds.loadPlugin('mnt_poseScope.py')
except:
    pass

# Runs our custom tools at the end of Maya startup
cmds.evalDeferred('mnt_poseScopeShelf.MntCustomShelf(\'mnt_poseScope\')')
# ________________________________________________

# Adds custom shapes to cached playback evaluation
#cmds.evalDeferred('cmds.cacheEvaluator(newFilter= \'nodeTypes\', newFilterParam=\'types=+mnt_locator\', newAction=\'enableEvaluationCache\')')
#cmds.evalDeferred('cmds.cacheEvaluator(newFilter= \'nodeTypes\', newFilterParam=\'types=+mnt_locator\', newAction = \'enableVP2Cache\', newActionParam = \'useHardware=0\')')
#cmds.evalDeferred('cmds.cacheEvaluator(newFilter= \'nodeTypes\', newFilterParam=\'types=+mnt_locator\', newAction = \'enableVP2Cache\', newActionParam = \'useHardware=1\')')
# ________________________________________________

# Adds custom buttons to ToolBox
def addCustomToolBoxButtons():
    gToolBox = mel.eval('$tmpVar=$gToolBox')
    iconPath = cmds.getModulePath(moduleName = 'mnt_poseScope') + '/icons/mntShelf/'

    if cmds.symbolCheckBox('mnt_poseTool', q = True, ex =True) == True:
        cmds.deleteUI('mnt_poseTool')
    cmds.symbolCheckBox('mnt_poseTool', i = iconPath + 'mnt_poseTool.png', w = 36, h = 36, p = gToolBox,\
        onCommand = 'import mnt_poseTool as mnt_poseTool\nimportlib.reload(mnt_poseTool)\nposeTool = mnt_poseTool.mnt_DynSelection()', offCommand = 'poseTool.__del__()')

    if cmds.symbolButton('toggleShelf', q = True, ex =True) == True:
        cmds.deleteUI('toggleShelf')
    cmds.symbolButton('toggleShelf', i = iconPath + 'mnt_toggleShelf.png', w = 36, h = 12, p = gToolBox, c = 'mel.eval(\'ToggleShelf;\')')

    if cmds.symbolButton('toggleCommandLine', q = True, ex =True) == True:
        cmds.deleteUI('toggleCommandLine')
    cmds.symbolButton('toggleCommandLine', i = iconPath + 'mnt_toggleCommandLine.png', w = 36, h = 12, p = gToolBox, c = 'mel.eval(\'ToggleCommandLine;\')')

cmds.evalDeferred('addCustomToolBoxButtons()')
# ______________________________
