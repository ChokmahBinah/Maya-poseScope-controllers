import ctypes
import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI

def maya_useNewAPI():
 pass

class CallbackHandler(object):

    def __init__(self, cb, fn):
        self.callback = cb
        self.function  = fn
        self.id = None

    def install(self):
        if self.id:
            print('Callback is currently installed')
            return False
        self.id = OpenMaya.MEventMessage.addEventCallback(self.callback, self.function)
        return True
        
    def uninstall(self):
        if self.id:
            OpenMaya.MEventMessage.removeCallback(self.id)
            self.id = None
            return True
        else:
            #print('Callback not currently installed')
            return False

    def __del__(self):
        self.uninstall()
        
class get_maus_pp(ctypes.Structure):
    _fields_ = [("x", ctypes.c_ulong), ("y", ctypes.c_ulong)]

class mnt_DynSelection():
    def __init__(self):
        self.oldShape       = None
        self.initialOpacities = []
        self.idleCallback = CallbackHandler('idleVeryLow', self.dynSelection)
        self.newSceneCallBack = CallbackHandler('PreFileNewOrOpened', self.delCallbacks)

        self.idleCallback.install()
        self.newSceneCallBack.install()

        self.getScenePoseScopeShapesOpacities()
        self.zeroScenePoseScopeShapesOpacities()

        cmds.inViewMessage(smg = '<span style = \'color:#fdd28a;\' <\span>Pose Tool On', pos  = 'topCenter' , bkc  = 0x00000000, a = 0.2, fade = False, fts = 8)

    def __del__(self):
        self.delCallbacks()
        self.resetScenePoseScopeShapesOpacities()
        cmds.inViewMessage(smg = '<span style = \'color:#fdd28a;\' <\span> Pose Tool Off', pos  = 'topCenter' , bkc  = 0x00000000, a = 0.2, fade = True, fts = 8)

    def delCallbacks(self):
        self.idleCallback.uninstall()
        self.newSceneCallBack.uninstall()

    def mousePos(self, *args, **kwargs): 
        mpp = get_maus_pp()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(mpp))
        uview               = OpenMayaUI.M3dView.active3dView()   
        active3dViewPos     = OpenMayaUI.M3dView.getScreenPosition(uview)
        cursor3dViewPosX = mpp.x - active3dViewPos[0]
        cursor3dViewPosY = mpp.y - active3dViewPos[1]

        return cursor3dViewPosX, cursor3dViewPosY

    def dynSelection(self, *args, **kwargs):
        cmds.undoInfo(swf = False)#Stop Undo/Redo queue without flushing it!
        panel               = cmds.getPanel(underPointer = True)
        panelType           = cmds.getPanel(typeOf = panel)    
        cursorPos           = self.mousePos()
        
        if panelType == 'modelPanel':            
            shapesUnderCursor   = cmds.hitTest(panel, cursorPos[0], cursorPos[1])
            
            if len(shapesUnderCursor) > 0:                          
                shape = cmds.ls(shapesUnderCursor[len(shapesUnderCursor) - 1], flatten = True)[0]# It seems do have a test error here ...
                shape = cmds.ls(shapesUnderCursor[0], flatten = True)[0]# I did a bad selection indeed ...
                
                if cmds.objectType(shape) == 'mnt_poseScope':
                    if shape != self.oldShape :
                        self.oldattrValue = cmds.getAttr(shape + '.opacity')

                        if self.oldShape:
                            cmds.setAttr(self.oldShape + '.opacity', self.oldattrValue)
                        cmds.setAttr(shape + '.opacity', 0.15)
                        self.oldShape = shape

            if len(shapesUnderCursor) == 0:
                if self.oldShape:
                     cmds.setAttr(self.oldShape + '.opacity', self.oldattrValue)
                     self.oldShape = None
        cmds.undoInfo(swf = True)
    
    def getScenePoseScopeShapesOpacities(self):
        poseScopeList = cmds.ls(typ = 'mnt_poseScope')
        for node in poseScopeList:
            opacity = cmds.getAttr(node + '.opacity')
            self.initialOpacities.append(opacity)
        return

    def zeroScenePoseScopeShapesOpacities(self):
        poseScopeList = cmds.ls(typ = 'mnt_poseScope')
        for node in poseScopeList:
            opacity = cmds.setAttr(node + '.opacity', 0.0)
        return

    def resetScenePoseScopeShapesOpacities(self):
        poseScopeList = cmds.ls(typ = 'mnt_poseScope')
        for i in range(0, len(poseScopeList)):
            cmds.setAttr(poseScopeList[i] + '.opacity', self.initialOpacities[i])
        return