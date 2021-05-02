import importlib
import maya.cmds as cmds
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
cmds.evalDeferred('cmds.cacheEvaluator(newFilter= \'nodeTypes\', newFilterParam=\'types=+mntLocator\', newAction=\'enableEvaluationCache\')')
cmds.evalDeferred('cmds.cacheEvaluator(newFilter=\'nodeTypes\', newFilterParam = \'types=+mnt_poseScope\' , newAction = \'enableEvaluationCache\')')
cmds.evalDeferred('cmds.cacheEvaluator(newFilter=\'nodeTypes\', newFilterParam = \'types=+mnt_poseScope\' , newAction = \'enableVP2Cache\', newActionParam = \'useHardware=0\')')
cmds.evalDeferred('cmds.cacheEvaluator(newFilter=\'nodeTypes\', newFilterParam = \'types=+mnt_poseScope\' , newAction = \'enableVP2Cache\', newActionParam = \'useHardware=1\')')
# ________________________________________________