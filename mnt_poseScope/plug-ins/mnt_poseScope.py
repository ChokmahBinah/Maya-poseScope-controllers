import ctypes
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.api.OpenMayaRender as OpenMayaRender
import maya.api.OpenMayaAnim as OpenMayaAnim

maya_useNewAPI = True

class Mnt_poseScopeNode(OpenMaya.MPxSurfaceShape):
    kPluginNodeName             = 'mnt_poseScope'
    id                          = OpenMaya.MTypeId( 0xDAE6 )
    drawDbClassification        = "drawdb/geometry/Mnt_poseScopeNode"
    drawRegistrantId            = "Mnt_poseScopeNodePlugin"

    inFaceComponentsAttr        = OpenMaya.MObject()
    componentListStrAttr        = OpenMaya.MObject()#
    inMeshObjAttr               = OpenMaya.MObject()
    colorAttribute              = OpenMaya.MObject()
    opacityAttribute            = OpenMaya.MObject()
    interactiveDisplayAttribute =  OpenMaya.MObject()
    fsInputMeshChanged          = None

    def __init__(self):
        OpenMaya.MPxSurfaceShape.__init__(self)

    @staticmethod
    def creator():
        return Mnt_poseScopeNode()
 
    @staticmethod
    def initialize():
        numericAttributeFn = OpenMaya.MFnNumericAttribute()
        typedAttributeFn = OpenMaya.MFnTypedAttribute()

        # Defines the input and output attributes as static variables in our plug-in class.
        Mnt_poseScopeNode.inFaceComponentsAttr = typedAttributeFn.create('inputFaceComponents', 'inputFaceComponents', OpenMaya.MFnData.kComponentList)
        typedAttributeFn.hidden   = False
        typedAttributeFn.storable = True
        typedAttributeFn.writable = True
        Mnt_poseScopeNode.addAttribute(Mnt_poseScopeNode.inFaceComponentsAttr)

        Mnt_poseScopeNode.inMeshObjAttr = typedAttributeFn.create('inputMesh', 'inputMesh', OpenMaya.MFnData.kMesh, OpenMaya.MObject.kNullObj)
        typedAttributeFn.hidden      = False
        typedAttributeFn.storable    = True
        typedAttributeFn.writable    = True
        Mnt_poseScopeNode.addAttribute(Mnt_poseScopeNode.inMeshObjAttr)

        Mnt_poseScopeNode.fsInputMeshChanged = numericAttributeFn.create('inputMeshChangedSinceUpdate', 'inputMeshChangedSinceUpdate', OpenMaya.MFnNumericData.kBoolean, False)
        numericAttributeFn.storable     = False#
        numericAttributeFn.hidden       = True#
        numericAttributeFn.connectable  = False#
        Mnt_poseScopeNode.addAttribute(Mnt_poseScopeNode.fsInputMeshChanged)#

        Mnt_poseScopeNode.colorAttribute = numericAttributeFn.createColor('color', 'color')
        numericAttributeFn.writable     = True
        numericAttributeFn.channelBox   = True
        numericAttributeFn.storable     = True
        numericAttributeFn.hidden       = False
        Mnt_poseScopeNode.addAttribute(Mnt_poseScopeNode.colorAttribute)

        Mnt_poseScopeNode.opacityAttribute = numericAttributeFn.create('opacity', 'opacity', OpenMaya.MFnNumericData.kFloat, 0.05)
        numericAttributeFn.writable     = True
        numericAttributeFn.channelBox   = True
        numericAttributeFn.storable     = True
        numericAttributeFn.hidden       = False
        numericAttributeFn.keyable = False        
        numericAttributeFn.setMin(0.0)
        numericAttributeFn.setMax(1.0)   
        Mnt_poseScopeNode.addAttribute(Mnt_poseScopeNode.opacityAttribute)

        Mnt_poseScopeNode.interactiveDisplayAttribute = numericAttributeFn.create('interactiveDisplay', 'interactiveDisplay', OpenMaya.MFnNumericData.kBoolean, False)
        numericAttributeFn.writable     = True
        numericAttributeFn.channelBox   = True
        numericAttributeFn.storable     = True
        numericAttributeFn.hidden       = False
        numericAttributeFn.keyable = False        
        Mnt_poseScopeNode.addAttribute(Mnt_poseScopeNode.interactiveDisplayAttribute)

        Mnt_poseScopeNode.attributeAffects(Mnt_poseScopeNode.inMeshObjAttr, Mnt_poseScopeNode.inMeshObjAttr)
        
    def getShapeSelectionMask(self):  
        selType = OpenMaya.MSelectionMask.kSelectLocators
        return OpenMaya.MSelectionMask(selType)

    def connectionMade(self, plug, otherPlug, asSrc):
        if not asSrc and plug.attribute() == Mnt_poseScopeNode.inFaceComponentsAttr:
            self.setInputMeshChangedSinceUpdate(True)

        if not asSrc and plug.attribute() == Mnt_poseScopeNode.inMeshObjAttr:
            self.setInputMeshChangedSinceUpdate(True)

        return OpenMaya.MPxNode.connectionMade(self, plug, otherPlug, asSrc)

    def setDependentsDirty(self, plug, plugArray):
        if plug.attribute() == Mnt_poseScopeNode.inFaceComponentsAttr:
            self.setInputMeshChangedSinceUpdate(True)
        
        if plug.attribute() == Mnt_poseScopeNode.inMeshObjAttr:
            self.setInputMeshChangedSinceUpdate(True)

    def preEvaluation(self, context, evaluationNode):
        if evaluationNode.dirtyPlugExists(Mnt_poseScopeNode.inMeshObjAttr):
            self.setInputMeshChangedSinceUpdate(False)
        return

    def postEvaluation(self, context, evaluationNode, evalType):
        if evaluationNode.dirtyPlugExists(Mnt_poseScopeNode.inMeshObjAttr):
            self.setInputMeshChangedSinceUpdate(False)
        return
        
    def setInputMeshChangedSinceUpdate(self, value):
        dataBlock = self.forceCache()
        dataHandle = dataBlock.outputValue(Mnt_poseScopeNode.fsInputMeshChanged)
        dataHandle.setBool(value)
    
    def evalInputMeshChangedSinceUpdate(self):
        dataBlock = self.forceCache()
        dataHandle = dataBlock.outputValue(Mnt_poseScopeNode.fsInputMeshChanged)
        return dataHandle.asBool()
    
# MPxDrawOverride implementation
class Mnt_poseScopeData(OpenMaya.MUserData):
    def __init__(self):
        OpenMaya.MUserData.__init__(self, False)

class Mnt_poseScopeDrawOverride(OpenMayaRender.MPxDrawOverride):
    Mnt_poseScopeNode_inputMeshDirtyCallback    = None

    @staticmethod
    def creator(obj):
        return Mnt_poseScopeDrawOverride(obj)
    
    @staticmethod
    def draw(context, data):
        return

    def __init__(self, obj):
        OpenMayaRender.MPxDrawOverride.__init__(self, obj, Mnt_poseScopeDrawOverride.draw)
        self.node                           = OpenMaya.MFnDependencyNode(obj)
        self.fMesh                          = self.node.userNode()
        self.MObj                           = obj
        self.inputMeshFn                    = None
        self.fComponent                     = None
        self.shader                         = None
        self.shaderColor                    = None
        self.shaderOpacity                  = None  
        self.poseScopeShapePointsArray      = OpenMaya.MPointArray()
        self.poseScopeShapeIndexArray       = OpenMaya.MUintArray()
        self.doRefresh                      = True
        self.deleteNodeCallback             = OpenMaya.MNodeMessage.addNodeDestroyedCallback(obj, self.deleteNodeAction)

    def __del__(self):
        OpenMaya.MMessage.removeCallback(self.Mnt_poseScopeNode_inputMeshDirtyCallback)      
        OpenMaya.MEventMessage.removeCallback(self.deleteNodeCallback)

    def deleteNodeAction(self, *args):
        try:
            OpenMaya.MMessage.removeCallback(self.Mnt_poseScopeNode_inputMeshDirtyCallback)
        except:
            pass

    def getInputFaces(self):
        inputMeshPlug   = self.node.findPlug('inputMesh', False)
        connections   = inputMeshPlug.connectedTo(True, False)

        for i in range(0, len(connections)):
            node = connections[i].node()

            if node.hasFn(OpenMaya.MFn.kMesh):
                self.inputMeshFn             = OpenMaya.MFnMesh(node)
                self.shape = node
                break

        inputFaceComponentsPlug     = self.node.findPlug('inputFaceComponents', False)
        try: 
            inputFaceComponentsListObj  = inputFaceComponentsPlug.asMObject()
            inputFaceComponentsListFn   = OpenMaya.MFnComponentListData(inputFaceComponentsListObj)
            self.fComponent             = OpenMaya.MFnSingleIndexedComponent()
            self.fComponent.create(OpenMaya.MFn.kMeshPolygonComponent)

            for i in range(0, inputFaceComponentsListFn.length()):
                inputFaceComponentsObj      = inputFaceComponentsListFn.get(i)
                tmpSingleIndexedComponent = OpenMaya.MFnSingleIndexedComponent(inputFaceComponentsObj)
                elements = tmpSingleIndexedComponent.getElements()
                self.fComponent.addElements(elements)

        except:
            OpenMaya.MGlobal.displayWarning('No Input Face Components! Please add some.')

        return

    def getWorldMatrix(self):
        try:
            inputMeshParent             = OpenMaya.MFnDagNode(self.shape).parent(0)
        except:
            return

        fnInputMeshParent           = OpenMaya.MFnDependencyNode(inputMeshParent)
        inputMeshWorldMatrixAttr    = fnInputMeshParent.attribute('worldMatrix')
        inputMeshWorldMatrixPlug    = OpenMaya.MPlug(inputMeshParent, inputMeshWorldMatrixAttr)
        inputMeshWorldMatrixPlug    = inputMeshWorldMatrixPlug.elementByLogicalIndex(0)
        inputMeshWorldMatrixObj     = inputMeshWorldMatrixPlug.asMObject()
        inputMeshWorldMatrixData    = OpenMaya.MFnMatrixData(inputMeshWorldMatrixObj)
        inputMeshWorldMatrix        = inputMeshWorldMatrixData.matrix()

        MObjFn              = OpenMaya.MFnDagNode(self.MObj)
        MObjParent          = MObjFn.parent(0)
        fnMObjParent        = OpenMaya.MFnDependencyNode(MObjParent)
        worldMatrixAttr     = fnMObjParent.attribute('worldMatrix')
        matrixPlug          = OpenMaya.MPlug(MObjParent, worldMatrixAttr)
        matrixPlug          = matrixPlug.elementByLogicalIndex(0)
        worldMatrixObject   = matrixPlug.asMObject()
        worldMatrixData     = OpenMaya.MFnMatrixData(worldMatrixObject)
        worldMatrix         = worldMatrixData.matrix().inverse()

        outputMatrix        = inputMeshWorldMatrix.__mul__(worldMatrix)
        return outputMatrix

    def rebuildBuffers(self):
        self.clearBuffers()
        self.getInputFaces()

        matrix          = self.getWorldMatrix()

        try:
            facesSet            = self.fComponent.getElements()
            inputMeshTriangles  = self.inputMeshFn.getTriangles()
        except:
            return

        for i in facesSet:
            faceTriNb = inputMeshTriangles[0][i]

            for j in range(0, faceTriNb):
                triVert = self.inputMeshFn.getPolygonTriangleVertices(i, j)
                for k in triVert:
                    point = self.inputMeshFn.getPoint(k).__mul__(matrix)
                    self.poseScopeShapePointsArray.append(point)  

        self.doRefresh = False
        self.fMesh.setInputMeshChangedSinceUpdate(False)

    def clearBuffers(self):
        self.poseScopeShapePointsArray.clear()

    def refresh(self, *args):
        self.doRefresh = True
        return

    def supportedDrawAPIs(self):
        return OpenMayaRender.MRenderer.kAllDevices

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        data = oldData
        if not isinstance(data, Mnt_poseScopeNode):
            data = Mnt_poseScopeData()

        # Changes the shader opacity if the poseScope shape parent is selected.
        MActiveSel  = OpenMaya.MGlobal.getActiveSelectionList()
        MFnDagNode  = OpenMaya.MFnDagNode(self.MObj)
        MObjParent  = MFnDagNode.parent(0)
        MFnParent   = OpenMaya.MFnDependencyNode(MObjParent)

        self.shaderColor    = self.node.findPlug('color', False).asMDataHandle().asFloat3()
        self.shaderOpacity  = self.node.findPlug('opacity', False).asFloat()

        if MActiveSel.length() > 0 and MFnParent.name() in MActiveSel.getSelectionStrings():
            self.shaderOpacity = 0.1 + self.node.findPlug('opacity', False).asFloat()
        # _____________________________________________________________________

        data.interactiveDisplay = self.node.findPlug('interactiveDisplay', False).asBool()

        if not frameContext.inUserInteraction():
            if self.doRefresh == True or self.fMesh.evalInputMeshChangedSinceUpdate() == True:
                self.rebuildBuffers()
        elif frameContext.userChangingViewContext() == False and data.interactiveDisplay == True and OpenMayaAnim.MAnimControl.isPlaying() == False:
                self.rebuildBuffers()

        if self.Mnt_poseScopeNode_inputMeshDirtyCallback == None:
            try:
                self.Mnt_poseScopeNode_inputMeshDirtyCallback = OpenMaya.MNodeMessage.addNodeDirtyPlugCallback(self.shape, self.refresh)
            except:
                pass

        return data

    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        if not frameContext.inUserInteraction() or data.interactiveDisplay == True and OpenMayaAnim.MAnimControl.isPlaying() == False:
            drawManager.beginDrawable(OpenMayaRender.MUIDrawManager.kSelectable)
            drawManager.setDepthPriority(20)
            drawManager.setColor(OpenMaya.MColor((self.shaderColor[0], self.shaderColor[1], self.shaderColor[2], self.shaderOpacity)))
            drawManager.mesh(4, self.poseScopeShapePointsArray, None, None, self.poseScopeShapeIndexArray, None)
            drawManager.endDrawable()       
# _____________________________

# Needed for registtering the node shape
class Mnt_poseScopeNodeUI(OpenMayaUI.MPxSurfaceShapeUI):
    @staticmethod
    def creator():
        return Mnt_poseScopeNodeUI()

    def __init__(self):
        OpenMayaUI.MPxSurfaceShapeUI.__init__(self)
# ______________________________________

# Creates poseScopeShape command
class Mnt_CreatePoseScopeShapeCmd(OpenMaya.MPxCommand):
    kPluginCmdName = 'createPoseScopeShape'

    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)
        self.poseScopeNode = None
        self.groupNode = None
        self.shapeNode = None
        self.groupNodeObj = None
        self.poseScopeDagNodeObj = None

    @staticmethod
    def creator():
        return Mnt_CreatePoseScopeShapeCmd()

    def isUndoable(self):
        return True

    def doIt(self, args):
        self.redoIt()

    def undoIt(self):
        OpenMaya.MGlobal.deleteNode(self.groupNodeObj)
        OpenMaya.MGlobal.deleteNode(self.poseScopeDagNodeObj)
        return
    
    def redoIt(self):
        componentListStr    = ''
        poseScopeSelList    = OpenMaya.MSelectionList()
        MSelectionList      = OpenMaya.MGlobal.getActiveSelectionList()

        if MSelectionList.length() == 0:
            OpenMaya.MGlobal.displayError('Nothing selected! Please select some polySurface faces components.')
        
        for i in range(0, MSelectionList.length()):
            components      = MSelectionList.getComponent(i)
            componentType   = components[1].apiType()
            
            if componentType != 552:
                OpenMaya.MGlobal.displayError('Selection is not of face type! Please select some polySurface face components')
                pass

            if componentType == 552:
                # Gets parent DAG object
                shapeObj = MSelectionList.getDependNode(0)
                self.shapeNode = OpenMaya.MFnDependencyNode(shapeObj)
                # ______________________

                # Gets face components list if some selected.
                componentListData   = OpenMaya.MFnSingleIndexedComponent(components[1])
                componentListStr    = str(componentListData.getElements()).replace('[', '').replace(']', '').replace(',', '')
                # ___________________________________________

                # Creates mnt_groupNode DG node.
                DGModifier      = OpenMaya.MDGModifier()
                self.groupNodeObj    = DGModifier.createNode('mnt_groupNode')
                self.groupNode = OpenMaya.MFnDependencyNode(self.groupNodeObj)
                self.groupNode.findPlug('mode', False).setInt(1)
                self.groupNode.findPlug('componentsList', False).setString(componentListStr)
                # ______________________________
                
                # Creates mnt_poseScope DAG node.
                poseScopeDagNodeFn  = OpenMaya.MFnDagNode()
                self.poseScopeDagNodeObj = poseScopeDagNodeFn.create('mnt_poseScope')
                poseScopeNodePath   = OpenMaya.MFnDagNode(self.poseScopeDagNodeObj).getPath().extendToShape()
                self.poseScopeNode       = OpenMaya.MFnDependencyNode(poseScopeNodePath.node())
                self.poseScopeNode.findPlug('colorR', False).setDouble(1.0)
                self.poseScopeNode.findPlug('colorG', False).setDouble(0.75)
                self.poseScopeNode.findPlug('colorB', False).setDouble(0.0)
                self.poseScopeNode.findPlug('opacity', False).setFloat(0.1)
                # _______________________________

                # Creates connections.
                DGModifier.connect(self.groupNode.findPlug('outputsComponent', False), self.poseScopeNode.findPlug('inputFaceComponents', False))
                DGModifier.connect(self.shapeNode.findPlug('outMesh', False), self.poseScopeNode.findPlug('inputMesh', False))
                DGModifier.doIt()
                # ____________________
        return
# ______________________________

# Creates togglePoseScopeShapesVisibility command.
class Mnt_TogglePoseScopeShapesVisibilityCmd(OpenMaya.MPxCommand):
    kPluginCmdName = 'togglePoseScopeShapesVisibility'

    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)

    @staticmethod
    def creator():
        return Mnt_TogglePoseScopeShapesVisibilityCmd()

    def isUndoable(self):
        return True
    
    def doIt(self, args):
        self.redoIt()
    
    def undoIt(self):
        self.redoIt()
        return
    
    def redoIt(self):
        iterator = OpenMaya.MItDependencyNodes()
        while not iterator.isDone():
            nodeFn = OpenMaya.MFnDependencyNode(iterator.thisNode())
            if nodeFn.typeName == 'mnt_poseScope':
                visibilityPlug = nodeFn.findPlug('visibility', False)
                visibilityValue = visibilityPlug.asInt()
                visibilityPlug.setInt(1 - visibilityValue)
            iterator.next()
        return
# ________________________________________________

def initializePlugin(obj):
    plugin = OpenMaya.MFnPlugin(obj, 'Florian Delarque', '1.2', 'Any')
    try:
        plugin.registerShape(Mnt_poseScopeNode.kPluginNodeName, Mnt_poseScopeNode.id, Mnt_poseScopeNode.creator, Mnt_poseScopeNode.initialize, Mnt_poseScopeNodeUI.creator, Mnt_poseScopeNode.drawDbClassification)
    except:
        OpenMaya.MGlobal.displayError('Failed to register node\n')
        raise

    try:
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(Mnt_poseScopeNode.drawDbClassification, Mnt_poseScopeNode.drawRegistrantId, Mnt_poseScopeDrawOverride.creator)
    except:
        OpenMaya.MGlobal.displayError('Failed to register DrawOverride\n')
        raise
    
    try:
        plugin.registerCommand(Mnt_CreatePoseScopeShapeCmd.kPluginCmdName, Mnt_CreatePoseScopeShapeCmd.creator)
        plugin.registerCommand(Mnt_TogglePoseScopeShapesVisibilityCmd.kPluginCmdName, Mnt_TogglePoseScopeShapesVisibilityCmd.creator)
    except:
        OpenMaya.MGlobal.displayError('Failed to register createPoseScopeShape command.\n')

def uninitializePlugin(obj):
    plugin = OpenMaya.MFnPlugin(obj)
 
    try:
        plugin.deregisterNode(Mnt_poseScopeNode.id)
    except:
        OpenMaya.MGlobal.displayError("Failed to deregister node\n")
        pass

    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(Mnt_poseScopeNode.drawDbClassification, Mnt_poseScopeNode.drawRegistrantId)
    except:
        OpenMaya.MGlobal.displayError('Failed to deregister DrawOverride\n')
        pass 

    try:
        plugin.deregisterCommand(Mnt_CreatePoseScopeShapeCmd.kPluginCmdName)
        plugin.deregisterCommand(Mnt_TogglePoseScopeShapesVisibilityCmd.kPluginCmdName)
    except:
        OpenMaya.MGlobal.displayError('Failed to deregister createPoseScopeShape command.\n')