import ctypes
import maya.mel as mel
import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.api.OpenMayaRender as OpenMayaRender

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
        self.oldPos             = None
        self.oldShape           = None
        self.initialOpacities   = []
        self.idleCallback       = CallbackHandler('idle', self.dynSelection)
        self.newSceneCallBack   = CallbackHandler('PreFileNewOrOpened', self.delCallbacks)

        self.idleCallback.install()
        self.newSceneCallBack.install()

        self.getScenePoseScopeShapesOpacities()
        self.zeroScenePoseScopeShapesOpacities()

        mel.eval('setObjectPickMask \"Surface\" false;')
        cmds.inViewMessage(smg = '<span style = \'color:#fdbb8b;\' <\span>Pose Tool On', pos  = 'topCenter' , bkc  = 0x00000000, a = 0.1, fade = False, fts = 8)
        
    def __del__(self):
        self.delCallbacks()
        self.resetScenePoseScopeShapesOpacities()
        del(self.initialOpacities)
        mel.eval('setObjectPickMask \"Surface\" true;')
        cmds.inViewMessage(smg = '<span style = \'color:#fdbb8b;\' <\span> Pose Tool Off', pos  = 'topCenter' , bkc  = 0x00000000, a = 0.1, fade = True, fts = 8)

    def delCallbacks(self, *args):
        self.idleCallback.uninstall()
        self.newSceneCallBack.uninstall()

    def mousePos(self, *args, **kwargs): 
        mpp = get_maus_pp()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(mpp))
        uview               = OpenMayaUI.M3dView.active3dView()   
        active3dViewPos     = uview.getScreenPosition()
        cursor3dViewPosX = mpp.x - active3dViewPos[0]
        cursor3dViewPosY = mpp.y - active3dViewPos[1]

        return cursor3dViewPosX, cursor3dViewPosY

    def dynSelection(self, *args, **kwargs):
        cursorPos           = self.mousePos()

        if cursorPos == self.oldPos:
            return
        else:
            self.oldPos = cursorPos
            pass

        try:
            shapesUnderCursor   = cmds.hitTest(cmds.getPanel(underPointer = True), cursorPos[0], cursorPos[1])
        except:
            return
            
        MSelectionList      = OpenMaya.MSelectionList()

        if self.oldShape:
            MSelectionList.add(self.oldShape)
            oldShapeObj = MSelectionList.getDependNode(0)
            oldShapeDNFn = OpenMaya.MFnDependencyNode(oldShapeObj)
            oldShapeOpacityPlug = oldShapeDNFn.findPlug('opacity', False)
            MSelectionList.clear()
        else:
            pass

        if len(shapesUnderCursor) > 0:                          
            shape = shapesUnderCursor[0]

            # Prevents an error when moving cursor on outliner.
            try:
                MSelectionList.add(shape)
            except:
                return
            # _________________________________________________

            shapeObj = MSelectionList.getDependNode(0)
            shapeDNfn = OpenMaya.MFnDependencyNode(shapeObj)

            if shapeDNfn.typeName == 'mnt_poseScope':
                shapeOpacityPlug = shapeDNfn.findPlug('opacity', False)
                shapeHilightOpacityPlug = shapeDNfn.findPlug('hilightOpacity', False)

                if shape != self.oldShape :                        
                    if self.oldShape:
                        oldShapeOpacityPlug.setFloat(0.0)

                    shapeOpacityPlug.setFloat(shapeHilightOpacityPlug.asFloat() + 0.2)
                    self.oldShape = shape
                else:
                    return
        else:
            if self.oldShape:
                oldShapeOpacityPlug.setFloat(0.0)
                self.oldShape = None
            else:
                return
    
    def getScenePoseScopeShapesOpacities(self):
        poseScopeList = cmds.ls(typ = 'mnt_poseScope')
        for node in poseScopeList:
            opacity = cmds.getAttr(node + '.opacity')
            self.initialOpacities.append(opacity)
            hilightOpacity = cmds.getAttr(node + '.hilightOpacity')
        return

    def zeroScenePoseScopeShapesOpacities(self):
        poseScopeList = cmds.ls(typ = 'mnt_poseScope')
        for node in poseScopeList:
            cmds.setAttr(node + '.opacity', 0.0)
        return

    def resetScenePoseScopeShapesOpacities(self):
        poseScopeList = cmds.ls(typ = 'mnt_poseScope')
        for i in range(0, len(poseScopeList)):
            cmds.setAttr(poseScopeList[i] + '.opacity', self.initialOpacities[i])
        return