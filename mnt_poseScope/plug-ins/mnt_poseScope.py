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
    hilightOpacityAttribute     = OpenMaya.MObject()
    xRayModeAttribute           = OpenMaya.MObject()
    interactiveDisplayAttribute = OpenMaya.MObject()
    fsInputMeshChanged          = None
    
    def __init__(self):
        OpenMaya.MPxSurfaceShape.__init__(self)
        self.BBox = OpenMaya.MBoundingBox()

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

        Mnt_poseScopeNode.hilightOpacityAttribute = numericAttributeFn.create('hilightOpacity', 'hilightOpacity', OpenMaya.MFnNumericData.kFloat, 0.1)
        numericAttributeFn.writable     = True
        numericAttributeFn.channelBox   = True
        numericAttributeFn.storable     = True
        numericAttributeFn.hidden       = False
        numericAttributeFn.keyable = False        
        numericAttributeFn.setMin(0.0)
        numericAttributeFn.setMax(1.0)   
        Mnt_poseScopeNode.addAttribute(Mnt_poseScopeNode.hilightOpacityAttribute)

        Mnt_poseScopeNode.xRayModeAttribute = numericAttributeFn.create('xRayMode', 'xRayMode', OpenMaya.MFnNumericData.kBoolean, False)
        numericAttributeFn.writable     = True
        numericAttributeFn.channelBox   = True
        numericAttributeFn.storable     = True
        numericAttributeFn.hidden       = False
        numericAttributeFn.keyable = False        
        Mnt_poseScopeNode.addAttribute(Mnt_poseScopeNode.xRayModeAttribute)

        Mnt_poseScopeNode.interactiveDisplayAttribute = numericAttributeFn.create('interactiveDisplay', 'interactiveDisplay', OpenMaya.MFnNumericData.kBoolean, False)
        numericAttributeFn.writable     = True
        numericAttributeFn.channelBox   = True
        numericAttributeFn.storable     = True
        numericAttributeFn.hidden       = False
        numericAttributeFn.keyable = False        
        Mnt_poseScopeNode.addAttribute(Mnt_poseScopeNode.interactiveDisplayAttribute)

        # Cette ligne peut effectivement etre enlevee. Elle semble corriger un lag du playback cache que j'avais auparavant.
        #Mnt_poseScopeNode.attributeAffects(Mnt_poseScopeNode.inMeshObjAttr, Mnt_poseScopeNode.inMeshObjAttr)

    def isBounded(self):
        return True

    def boundingBox(self):
        return self.BBox

    def getShapeSelectionMask(self):  
        selType = OpenMaya.MSelectionMask.kSelectLocators
        return OpenMaya.MSelectionMask(selType)

    def connectionMade(self, plug, otherPlug, asSrc):
        if not asSrc and plug.attribute() == Mnt_poseScopeNode.inFaceComponentsAttr:
            self.setInputMeshChangedSinceUpdate(True)

        if not asSrc and plug.attribute() == Mnt_poseScopeNode.inMeshObjAttr:
            self.setInputMeshChangedSinceUpdate(True)

        return OpenMaya.MPxNode.connectionMade(self, plug, otherPlug, asSrc)

    def compute(self, plug, dataBlock):
        return True

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
                    try:
                        self.poseScopeShapePointsArray.append(point)  
                        self.fMesh.BBox.expand(point)# Expand BBox
                    except:
                        return
        
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

        data.shaderColor    = self.node.findPlug('color', False).asMDataHandle().asFloat3()
        data.shaderOpacity  = self.node.findPlug('opacity', False).asFloat()

        if MActiveSel.length() > 0 and MFnParent.name() in MActiveSel.getSelectionStrings():
            data.shaderOpacity = self.node.findPlug('hilightOpacity', False).asFloat()
        # _______________________________________________________________

        data.interactiveDisplay = self.node.findPlug('interactiveDisplay', False).asBool()
        data.xRayMode           = self.node.findPlug('xRayMode', False).asBool()

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
            
            if data.xRayMode == True:
                drawManager.beginDrawInXray()
            
            drawManager.setDepthPriority(20)
            drawManager.setColor(OpenMaya.MColor((data.shaderColor[0], data.shaderColor[1], data.shaderColor[2], data.shaderOpacity)))
            drawManager.mesh(OpenMayaRender.MUIDrawManager.kTriangles, self.poseScopeShapePointsArray, None, None, self.poseScopeShapeIndexArray, None)
            
            if data.xRayMode == True:
                drawManager.endDrawInXray()

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
        self.groupNodeObj = None
        self.poseScopeDagNodeObj = None
        self.poseScopeShapeObj = None

    @staticmethod
    def creator():
        return Mnt_CreatePoseScopeShapeCmd()

    def isUndoable(self):
        return True

    def doIt(self, args):
        self.redoIt()

    def undoIt(self):
        OpenMaya.MGlobal.deleteNode(self.groupNodeObj)
        try:
            OpenMaya.MGlobal.deleteNode(self.poseScopeDagNodeObj)
        except:
            OpenMaya.MGlobal.deleteNode(self.poseScopeShapeObj)
        return
    
    def redoIt(self):
        componentListStr    = ''
        poseScopeSelList    = OpenMaya.MSelectionList()
        MSelectionList      = OpenMaya.MGlobal.getActiveSelectionList()
        transformNode       = None

        if MSelectionList.length() == 0:
            OpenMaya.MGlobal.displayError('Nothing selected! Please select some polySurface faces components.')
            return

        for i in range(0, MSelectionList.length()):
            if MSelectionList.getComponent(i)[1].apiType() != OpenMaya.MFn.kMeshPolygonComponent:
                transformNode = MSelectionList.getDependNode(i)
                break
            
        for i in range(0, MSelectionList.length()):
            components      = MSelectionList.getComponent(i)
            componentType   = components[1].apiType()
            
            if componentType != OpenMaya.MFn.kMeshPolygonComponent:
                #OpenMaya.MGlobal.displayError('Selection is not of face type! Please select some polySurface face components')
                pass

            if componentType == OpenMaya.MFn.kMeshPolygonComponent:
                # Gets parent DAG object
                shapeObj = MSelectionList.getDependNode(0)
                shapeNode = OpenMaya.MFnDependencyNode(shapeObj)
                # ______________________

                # Gets face components list if some selected.
                componentListData   = OpenMaya.MFnSingleIndexedComponent(components[1])
                componentListStr    = componentListStr + str(componentListData.getElements()).replace('[', '').replace(']', '').replace(',', '') + ' '
                # ___________________________________________

        # Creates mnt_groupNode DG node.
        DGModifier      = OpenMaya.MDGModifier()
        self.groupNodeObj    = DGModifier.createNode('mnt_groupNode')
        groupNode = OpenMaya.MFnDependencyNode(self.groupNodeObj)
        groupNode.findPlug('mode', False).setInt(1)
        groupNode.findPlug('componentsList', False).setString(componentListStr)
        # ______________________________

        # Creates mnt_poseScope DAG node.
        poseScopeDagNodeFn  = OpenMaya.MFnDagNode()
        self.poseScopeDagNodeObj = poseScopeDagNodeFn.create('mnt_poseScope')
        poseScopeNodePath   = OpenMaya.MFnDagNode(self.poseScopeDagNodeObj).getPath().extendToShape()
        poseScopeNode       = OpenMaya.MFnDependencyNode(poseScopeNodePath.node())
        poseScopeNode.findPlug('colorR', False).setDouble(1.0)
        poseScopeNode.findPlug('colorG', False).setDouble(0.75)
        poseScopeNode.findPlug('colorB', False).setDouble(0.0)
        poseScopeNode.findPlug('opacity', False).setFloat(0.05)
        # _______________________________
        
        # Creates connections.
        DGModifier.connect(groupNode.findPlug('outputsComponent', False), poseScopeNode.findPlug('inputFaceComponents', False))
        DGModifier.connect(shapeNode.findPlug('outMesh', False), poseScopeNode.findPlug('inputMesh', False))
        DGModifier.doIt()
        # ____________________

        # If a transform node is selected, parent the poseScope shape to it
        if transformNode:
            shapeSel = OpenMaya.MSelectionList()
            shapeSel.add(OpenMaya.MFnDagNode(self.poseScopeDagNodeObj).getPath().extendToShape())
            self.poseScopeShapeObj = shapeSel.getDependNode(0)
            lastSelDagNode = OpenMaya.MFnDagNode(transformNode)

            for i in range(0, lastSelDagNode.childCount()):
                try:
                    childDNFn = OpenMaya.MFnDependencyNode(lastSelDagNode.child(i))
                    if childDNFn.typeName == 'mnt_poseScope':                        
                        poseScopeNode.findPlug('colorR', False).setDouble(childDNFn.findPlug('colorR', False).asDouble())
                        poseScopeNode.findPlug('colorG', False).setDouble(childDNFn.findPlug('colorG', False).asDouble())
                        poseScopeNode.findPlug('colorB', False).setDouble(childDNFn.findPlug('colorB', False).asDouble())
                        poseScopeNode.findPlug('opacity', False).setFloat(childDNFn.findPlug('opacity', False).asFloat())
                        poseScopeNode.findPlug('hilightOpacity', False).setFloat(childDNFn.findPlug('hilightOpacity', False).asFloat())

                        OpenMaya.MGlobal.deleteNode(lastSelDagNode.child(i))
                except:
                    pass

            lastSelDagNode.addChild(self.poseScopeShapeObj, 0, False)
            OpenMaya.MGlobal.deleteNode(self.poseScopeDagNodeObj)
        # _________________________________________________________________

        OpenMaya.MPxCommand.setResult(str(poseScopeNodePath))

        return
# ______________________________

# Mirror Pose Scope Command
class Mnt_mirrorPoseScopeCmd(OpenMaya.MPxCommand):
    kPluginCmdName = 'mirrorPoseScope'

    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)
        self.groupNodeObj           = None
        self.poseScopeDagNodeObj    = None

    @staticmethod
    def creator():
        return Mnt_mirrorPoseScopeCmd()
    
    def isUndoable(self):
        return True
    
    def doIt(self, *args):
        self.redoIt()
    
    def undoIt(self):
        OpenMaya.MGlobal.deleteNode(self.groupNodeObj)
        OpenMaya.MGlobal.deleteNode(self.poseScopeDagNodeObj)

    def redoIt(self):
        ''' 
        This method helps the user to create a symmetrical poseScope on a syemmtrical geometry
        The geometry should have an identity transformation matrix
        '''

        inputMeshFn     = None
        inputMeshShape  = None
        MSelection      = OpenMaya.MGlobal.getActiveSelectionList()
        
        if MSelection.length() == 0:
            OpenMaya.MGlobal.displayError('Nothing selected. Please select a posescope controller first.')
            return

        # Loops over of the selected nodes
        for i in range(MSelection.length()):

            # If nothing selected, display error and returns
            try:
                MObj = MSelection.getDependNode(i)
            except:
                OpenMaya.MGlobal.displayError('Nothing selected. Please select a posescope controller first.')
                return

        MDagPath        = OpenMaya.MDagPath.getAPathTo(MObj)
        symFaceListStr  = None

        for i in range(MDagPath.childCount()):
            child = MDagPath.child(i)

            if child.apiTypeStr != 'kPluginShape':
                continue

            childFn = OpenMaya.MFnDependencyNode(child)

            # When a poseScope is found, we can get its inputs nodes and stop the loop
            if childFn.typeName == 'mnt_poseScope':
                # Gets input mesh
                inputMeshPlug = childFn.findPlug('inputMesh', False)
                connections = inputMeshPlug.connectedTo(True, False)

                for i in range(0, len(connections)):
                    node = connections[i].node()

                    if node.hasFn(OpenMaya.MFn.kMesh):
                        inputMeshShape = node
                        inputMeshFn = OpenMaya.MFnMesh(node)
                        break
                # _______________
            # ________________________________________________________________________

                # Creates MPointOnMesh and MMeshIntersector to find opposite faces IDs
                '''meshPt = OpenMaya.MPointOnMesh()'''
                meshIntersector = OpenMaya.MMeshIntersector()
                meshIntersector.create(inputMeshShape, OpenMaya.MMatrix.kIdentity)
                # ____________________________________________________________________
                
                # Gets opposite faces IDs components
                inputFaceComponentsPlug = childFn.findPlug('inputFaceComponents', False)
                inputFaceComponentsListDataHandle  = inputFaceComponentsPlug.asMObject()
                componentsListData = OpenMaya.MFnComponentListData(inputFaceComponentsListDataHandle)

                for i in range(componentsListData.length()):
                    component = componentsListData.get(i)
                    singleIndexedComponent = OpenMaya.MFnSingleIndexedComponent(component)

                    for faceComponent in singleIndexedComponent.getElements():
                        vertices = inputMeshFn.getPolygonVertices(faceComponent)
                        faceCenter = OpenMaya.MVector((0.0, 0.0, 0.0))

                        for vertex in vertices:
                            position = inputMeshFn.getPoint(vertex)
                            faceCenter = faceCenter.__add__(OpenMaya.MVector(position[0] / len(vertices), position[1] / len(vertices), position[2] / len(vertices)))

                        symPoint = OpenMaya.MPoint((-faceCenter[0], faceCenter[1], faceCenter[2]))
                        closestPoint = meshIntersector.getClosestPoint(symPoint)
                        symFace = closestPoint.face

                        if symFaceListStr == None:
                            symFaceListStr = str(symFace)
                        else:
                            symFaceListStr = symFaceListStr + ' ' + str(symFace)
                        # _________________________
                # __________________________________

                # Creates mnt_groupNode DG node.
                DGModifier      = OpenMaya.MDGModifier()
                self.groupNodeObj    = DGModifier.createNode('mnt_groupNode')
                groupNode = OpenMaya.MFnDependencyNode(self.groupNodeObj)
                groupNode.findPlug('mode', False).setInt(1)
                groupNode.findPlug('componentsList', False).setString(symFaceListStr)
                # ______________________________

                # Creates mnt_poseScope DAG node.
                poseScopeDagNodeFn  = OpenMaya.MFnDagNode()
                self.poseScopeDagNodeObj = poseScopeDagNodeFn.create('mnt_poseScope')
                poseScopeNodePath   = OpenMaya.MFnDagNode(self.poseScopeDagNodeObj).getPath().extendToShape()
                poseScopeNode       = OpenMaya.MFnDependencyNode(poseScopeNodePath.node())
                poseScopeNode.findPlug('colorR', False).setDouble(childFn.findPlug('colorG', False).asDouble())
                poseScopeNode.findPlug('colorG', False).setDouble(childFn.findPlug('colorB', False).asDouble())
                poseScopeNode.findPlug('colorB', False).setDouble(childFn.findPlug('colorR', False).asDouble())
                poseScopeNode.findPlug('opacity', False).setFloat(childFn.findPlug('opacity', False).asFloat())
                # _______________________________

                # Creates connections.
                DGModifier.connect(groupNode.findPlug('outputsComponent', False), poseScopeNode.findPlug('inputFaceComponents', False))
                DGModifier.connect(inputMeshFn.findPlug('outMesh', False), poseScopeNode.findPlug('inputMesh', False))
                # ____________________

                DGModifier.doIt()
    
        # If an opposite transform node exists (_L_ or _R_), parent the new node to it.
        if '_L_' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('_L_', '_R_')
        elif 'L_' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('L_', 'R_')
        elif '_L' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('_L', '_R')
        elif '_R_' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('_R_', '_L_')
        elif 'R_' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('R_', 'L_')
        elif '_R' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('_R', '_L')
        else:
            oppositeTransformNode = MDagPath.__str__() + "_copy"
        
        try:
            oppositeSel = OpenMaya.MSelectionList()
            oppositeSel.add(oppositeTransformNode)
            oppositeSel.add(OpenMaya.MFnDagNode(self.poseScopeDagNodeObj).getPath().extendToShape())
            oppositeTransformNodeObj    = oppositeSel.getDependNode(0)
            posescopeShapeObj           = oppositeSel.getDependNode(1)
            oppositeTransformDagNode    = OpenMaya.MFnDagNode(oppositeTransformNodeObj)

            for i in range(0, oppositeTransformDagNode.childCount()):
                try:
                    childDNFn = OpenMaya.MFnDependencyNode(oppositeTransformDagNode.child(i))
                    if OpenMaya.MFnDependencyNode(oppositeTransformDagNode.child(i)).typeName == 'mnt_poseScope':
                        OpenMaya.MGlobal.deleteNode(oppositeTransformDagNode.child(i))
                except:
                    pass

            oppositeTransformDagNode.addChild(posescopeShapeObj, 0, False)
            OpenMaya.MGlobal.deleteNode(self.poseScopeDagNodeObj)
        except:
            DGModifier = OpenMaya.MDGModifier()
            DGModifier.renameNode(self.poseScopeDagNodeObj, oppositeTransformNode)
            DGModifier.doIt()
        # _____________________________________________________________________________

        return
# _________________________

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

# Creates deletePoseScope command
class Mnt_DeletePoseScopeCmd(OpenMaya.MPxCommand):
    kPluginCmdName = 'deletePoseScope'
    transformNodesList  = []
    inputComponentsList = []
    inputMeshList       = []

    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)

    @staticmethod
    def creator():
        return Mnt_DeletePoseScopeCmd()

    def isUndoable(self):
        return True
    
    def doIt(self, args):
        self.redoIt()
        return

    def undoIt(self):
        if len(self.transformNodesList) == 0 and len(self.inputComponentsList) == 0:
            return

        for i in range(len(self.transformNodesList)):
            MSelectionList = OpenMaya.MSelectionList()
            MSelectionList.add(self.transformNodesList[i])
            MSelectionList.add(self.inputMeshList[i])

            MTransformNodeObj       = MSelectionList.getDependNode(0)
            MInputMeshObj           = MSelectionList.getDependNode(1)
            inputComponentsListStr  = self.inputComponentsList[i]

            inputMeshDGFn = OpenMaya.MFnDependencyNode(MInputMeshObj)

            # Creates poseScope Node
            poseScopeDagNodeFn  = OpenMaya.MFnDagNode()
            poseScopeDagNodeObj = poseScopeDagNodeFn.create('mnt_poseScope')
            poseScopeNodePath   = OpenMaya.MFnDagNode(poseScopeDagNodeObj).getPath().extendToShape()
            poseScopeNode       = OpenMaya.MFnDependencyNode(poseScopeNodePath.node())
            poseScopeNode.findPlug('colorR', False).setDouble(1.0)
            poseScopeNode.findPlug('colorG', False).setDouble(0.75)
            poseScopeNode.findPlug('colorB', False).setDouble(0.0)
            poseScopeNode.findPlug('opacity', False).setFloat(0.1)
            # ______________________

            # Parents poseScope shape to transformNode
            transformDagNode = OpenMaya.MFnDagNode(MTransformNodeObj)
            transformDagNode.addChild(poseScopeNodePath.node(), 0, False)
            OpenMaya.MGlobal.deleteNode(poseScopeDagNodeObj)
            # ________________________________________

            # Recreates group Node
            DGModifier = OpenMaya.MDGModifier()
            groupNodeObj = DGModifier.createNode('mnt_groupNode')
            groupNodeDGNode = OpenMaya.MFnDependencyNode(groupNodeObj)
            groupNodeDGNode.findPlug('mode', False).setInt(1)
            groupNodeDGNode.findPlug('componentsList', False).setString(self.inputComponentsList[i])
            # ____________________

            # Creates node connections
            DGModifier.connect(groupNodeDGNode.findPlug('outputsComponent', False), poseScopeNode.findPlug('inputFaceComponents',False))
            DGModifier.connect(inputMeshDGFn.findPlug('outMesh', False), poseScopeNode.findPlug('inputMesh',False))
            DGModifier.doIt()
            # ________________________

        return
    
    def redoIt(self):
        self.transformNodesList     = []
        self.inputComponentsList    = []
        self.inputMeshList          = []

        MSelectionList = OpenMaya.MGlobal.getActiveSelectionList()

        for i in range(0, MSelectionList.length()):
            MObj = MSelectionList.getDependNode(i)
            MDagPath = OpenMaya.MDagPath.getAPathTo(MObj)

            for j in range(MDagPath.childCount()):
                try:
                    child = MDagPath.child(j)
                except:
                    continue

                childDGFn = OpenMaya.MFnDependencyNode(child)

                if childDGFn.typeName == 'mnt_poseScope':
                    inputComponentsPlug = childDGFn.findPlug('inputFaceComponents', False)
                    connections = inputComponentsPlug.connectedTo(True, False)
                    
                    for plug in connections:
                        node = plug.node()
                        nodeDGFn = OpenMaya.MFnDependencyNode(node)
                        componentsList = nodeDGFn.findPlug('componentsList', False).asString()
                        self.inputComponentsList.append(componentsList)
                        OpenMaya.MGlobal.deleteNode(node)
                   
                    inputMeshPlug = childDGFn.findPlug('inputMesh', False)
                    connections = inputMeshPlug.connectedTo(True, False)

                    for plug in connections:
                        node = plug.node()

                        if node.hasFn(OpenMaya.MFn.kMesh):
                            self.inputMeshList.append(node)

                    self.transformNodesList.append(str(MDagPath))
                    OpenMaya.MGlobal.deleteNode(child)      
# _______________________________

# Creates editPoseScopeComponents command
class Mnt_editPoseScopeComponentsCmd(OpenMaya.MPxCommand):
    kPluginCmdName = 'editPoseScopeComponents'

    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)

    @staticmethod
    def creator():
        return Mnt_editPoseScopeComponentsCmd()

    def isUndoable(self):
        return True

    def doIt(self, args):
        self.redoIt()
        return

    def redoIt(self):
        MSelectionList  = OpenMaya.MSelectionList()
        MActiveList     = OpenMaya.MGlobal.getActiveSelectionList()
        MObj            = MActiveList.getDependNode(0)

        MposeScopeMeshObj   = self.get_poseScopeMesh()
        MGroupNodeObj       = self.get_groupNode()
        MTransformNode      = self.get_transformNode()

        nodeDNFn                = OpenMaya.MFnDependencyNode(MGroupNodeObj)
        outputsComponentPlug    = nodeDNFn.findPlug('outputsComponent', False)
        outputsComponent        = outputsComponentPlug.asMObject()
        componentListData       = OpenMaya.MFnComponentListData(outputsComponent)
               
        for i in range(0, componentListData.length()):
            MSelectionList.add((OpenMaya.MDagPath.getAPathTo(MposeScopeMeshObj), componentListData.get(i)))

        MSelectionList.add(OpenMaya.MDagPath.getAPathTo(MTransformNode))

        OpenMaya.MGlobal.setComponentSelectionMask(OpenMaya.MSelectionMask.kSelectMeshFaces)
        OpenMaya.MGlobal.setSelectionMode(OpenMaya.MGlobal.kSelectComponentMode)
        OpenMaya.MGlobal.setHiliteList(MSelectionList)
        OpenMaya.MGlobal.setActiveSelectionList(MSelectionList)

    def get_transformNode(self):
        MselectionList  = OpenMaya.MGlobal.getActiveSelectionList()
        MObj            = MselectionList.getDependNode(0)
        MObjDNFn        = OpenMaya.MFnDependencyNode(MObj)

        if MObjDNFn.typeName == 'transform':
            return MObj
        
        elif MObjDNFn.typeName == 'mnt_groupNode':
            outputsComponentPlug = MObjDNFn.findPlug('outputsComponent', False)
            connections = outputsComponentPlug.connectedTo(False, True)

            for i in range(0, len(connections)):
                node = connections[i].node()
                nodeDNFn = OpenMaya.MFnDependencyNode(node)
                 
                if nodeDNFn.typeName == 'mnt_poseScope':
                    return OpenMaya.MDagPath.getAPathTo(node).transform()

    def get_groupNode(self):
        MselectionList  = OpenMaya.MGlobal.getActiveSelectionList()
        MObj            = MselectionList.getDependNode(0)
        MObjDNFn        = OpenMaya.MFnDependencyNode(MObj)

        if MObjDNFn.typeName == 'mnt_groupNode':
            return MObj
        
        elif MObjDNFn.typeName == 'transform':
            MDagPath =OpenMaya.MDagPath.getAPathTo(MObj)

            for i in range(MDagPath.childCount()):
                child = MDagPath.child(i)
                childDNFn = OpenMaya.MFnDependencyNode(child)

                if childDNFn.typeName == 'mnt_poseScope':
                    inputFaceComponentsPlug = childDNFn.findPlug('inputFaceComponents', False)
                    connections = inputFaceComponentsPlug.connectedTo(True, False)

                    for i in range(0, len(connections)):
                        node = connections[i].node()
                        nodeDNFn = OpenMaya.MFnDependencyNode(node)
                        
                        if nodeDNFn.typeName == 'mnt_groupNode':
                            return node
                            break
    
    def get_poseScopeMesh(self):
        MselectionList  = OpenMaya.MGlobal.getActiveSelectionList()
        MObj            = MselectionList.getDependNode(0)
        MObjDNFn        = OpenMaya.MFnDependencyNode(MObj)
        poseScopeNode   = None

        if MObjDNFn.typeName == 'mnt_groupNode':
            outputsComponentPlug = MObjDNFn.findPlug('outputsComponent', False)
            connections = outputsComponentPlug.connectedTo(False, True)
            
            for i in range(0, len(connections)):
                node = connections[i].node()
                nodeDNFn = OpenMaya.MFnDependencyNode(node)
                 
                if nodeDNFn.typeName == 'mnt_poseScope':
                    poseScopeNode = node
                    break
        
        elif MObjDNFn.typeName == 'transform':
            MdagNode = OpenMaya.MFnDagNode(MObj)

            for i in range(0, MdagNode.childCount()):
                if OpenMaya.MFnDependencyNode(MdagNode.child(i)).typeName == 'mnt_poseScope':
                    poseScopeNode = MdagNode.child(i)
                    break

        inputMeshPlug = OpenMaya.MFnDependencyNode(poseScopeNode).findPlug('inputMesh', False)
        connections = inputMeshPlug.connectedTo(True, False)

        for i in range(0, len(connections)):
            node = connections[i].node()

            if node.apiType() == OpenMaya.MFn.kMesh:
                return node
                break
# _____________________________________________

# Creates transfertPoseScopes command
class Mnt_transfertPoseScopesCmd(OpenMaya.MPxCommand):
    kPluginCmdName = 'transfertPoseScopes'

    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)
    
    @staticmethod
    def creator():
        return Mnt_transfertPoseScopesCmd()
    
    def isUndoable(self):
        return True

    def doIt(self, *args):
        self.redoIt()
        return 
    
    def undoIt(self, *args):
        OpenMaya.MGlobal.displayWarning('This command is not undoable !')
        return
    
    def redoIt(self, * args):
        MSelectionList  = OpenMaya.MGlobal.getActiveSelectionList()
        sourceMeshShape = None
        destMeshShape   = None
        sComponentList  = None
        dComponentList  = None
        groupNodesList  = []

        if MSelectionList.length() != 2:
            OpenMaya.MGlobal.displayError('Not enough objects selected. You need to select a source mesh and a destination mesh to use this command !')
            return

        for i in range(MSelectionList.length()):
            MObj = MSelectionList.getDependNode(i)
            MPath = OpenMaya.MDagPath.getAPathTo(MObj)
            MShape = MPath.extendToShape()
            
            if MShape.apiType() != OpenMaya.MFn.kMesh:
                OpenMaya.MGlobal.displayError('One of the selected objects is not a polySurface. Please check your selection !')
                return
            else:
                if i == 0:
                    sourceMeshShape = MShape.node()
                else:
                    destMeshShape = MShape.node()

        OpenMaya.MGlobal.displayInfo('Transferring poseScopes.')
        
        sourceMeshShapeFn   = OpenMaya.MFnDependencyNode(sourceMeshShape)
        destMeshShapeFn     = OpenMaya.MFnDependencyNode(destMeshShape)
        sOutMeshPlug        = sourceMeshShapeFn.findPlug('outMesh', False)
        dOutMeshPlug        = destMeshShapeFn.findPlug('outMesh', False)
        connections         = sOutMeshPlug.connectedTo(False, True)
        dMeshFn             = OpenMaya.MFnMesh(destMeshShape)
        DGModifier          = OpenMaya.MDGModifier()

        # Creates MPointOnMesh and MMeshIntersector to find opposite faces IDs
        meshIntersector = OpenMaya.MMeshIntersector()
        meshIntersector.create(sourceMeshShape, OpenMaya.MMatrix.kIdentity)
        # ____________________________________________________________________

        # Creates a MItMeshPolygon to iterate throw destination mesh
        '''meshIterator = OpenMaya.MItMeshPolygon(destMeshShape)'''
        # __________________________________________________________

        for i in range(0, len(connections)):
            node = connections[i].node()
            nodeFn = OpenMaya.MFnDependencyNode(node)

            if nodeFn.typeName == 'mnt_poseScope':
                groupNodeObj = None
                sourceMeshFn = OpenMaya.MFnMesh(sOutMeshPlug.node())

                # Deconnects poseScopes from source polySurface and reconnects them to the new one
                psInputMeshPlug = nodeFn.findPlug('inputMesh', False)
                DGModifier.disconnect(sOutMeshPlug, psInputMeshPlug)
                DGModifier.connect(dOutMeshPlug, psInputMeshPlug)
                DGModifier.doIt()
                # ________________________________________________________________________________

                sInputFaceComponentsPlug = nodeFn.findPlug('inputFaceComponents', False)
                plugConnections = sInputFaceComponentsPlug.connectedTo(True, False)
                
                # Finds connected group node
                for iPlug in plugConnections:
                    node = iPlug.node()
                    nodeDNFn = OpenMaya.MFnDependencyNode(node)

                    if nodeDNFn.typeName == 'mnt_groupNode' and node not in groupNodesList:
                        sComponentList = []
                        groupNodeObj = node
                        sComponentListPlug = OpenMaya.MFnDependencyNode(node).findPlug('componentsList', False)
                        sComponentList = sComponentListPlug.asString().split()
                        groupNodesList.append(node)
                        continue
                # __________________________
                
                dComponentList  = []
                dComponentListStr = None

                for i in range(dMeshFn.numPolygons):
                    vertices = dMeshFn.getPolygonVertices(i)
                    faceCenter = OpenMaya.MVector((0.0, 0.0, 0.0))

                    for vertex in vertices:
                        position = dMeshFn.getPoint(vertex)
                        faceCenter = faceCenter.__add__(OpenMaya.MVector(position[0] / len(vertices), position[1] / len(vertices), position[2] / len(vertices)))
                                    
                    closestPoint = meshIntersector.getClosestPoint(OpenMaya.MPoint(faceCenter), 0.1)
                    dFaceID = closestPoint.face
                                
                    if str(dFaceID) in sComponentList:
                        dComponentList.append(str(i))
                                
                dComponentListStr = " ".join(dComponentList)               
                sComponentListPlug.setString(dComponentListStr)

        OpenMaya.MGlobal.displayInfo('Posescopes transferred.')
        return
# ___________________________________

'''# Creates getPoseScopesInfosFromMeshCommand
class Mnt_getPoseScopesInfosFromMeshCmd(OpenMaya.MPxCommand):
    kPluginCmdName = 'getPoseScopesInfosFromMesh'

    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)

    @staticmethod
    def creator():
        return Mnt_getPoseScopesInfosFromMeshCmd()

    def isUndoable(self):
        return True

    def doIt(self, *args):
        self.redoIt()
        return
    
    def redoIt(self):
        listA = ['test', 100.01, 101, 102]
        OpenMaya.MPxCommand.setResult(listA)
        return
# _________________________________________'''

def initializePlugin(obj):
    plugin = OpenMaya.MFnPlugin(obj, 'Florian Delarque & Colin Bruneau', '1.4', 'Any')
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
        plugin.registerCommand(Mnt_mirrorPoseScopeCmd.kPluginCmdName, Mnt_mirrorPoseScopeCmd.creator)
        plugin.registerCommand(Mnt_TogglePoseScopeShapesVisibilityCmd.kPluginCmdName, Mnt_TogglePoseScopeShapesVisibilityCmd.creator)
        plugin.registerCommand(Mnt_DeletePoseScopeCmd.kPluginCmdName, Mnt_DeletePoseScopeCmd.creator)
        plugin.registerCommand(Mnt_editPoseScopeComponentsCmd.kPluginCmdName, Mnt_editPoseScopeComponentsCmd.creator)
        plugin.registerCommand(Mnt_transfertPoseScopesCmd.kPluginCmdName, Mnt_transfertPoseScopesCmd.creator)
        '''plugin.registerCommand(Mnt_getPoseScopesInfosFromMeshCmd.kPluginCmdName, Mnt_getPoseScopesInfosFromMeshCmd.creator)'''
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
        plugin.deregisterCommand(Mnt_mirrorPoseScopeCmd.kPluginCmdName)
        plugin.deregisterCommand(Mnt_TogglePoseScopeShapesVisibilityCmd.kPluginCmdName)
        plugin.deregisterCommand(Mnt_DeletePoseScopeCmd.kPluginCmdName)
        plugin.deregisterCommand(Mnt_editPoseScopeComponentsCmd.kPluginCmdName)
        plugin.deregisterCommand(Mnt_transfertPoseScopesCmd.kPluginCmdName)
        '''plugin.deregisterCommand(Mnt_getPoseScopesInfosFromMeshCmd.kPluginCmdName)'''
    except:
        OpenMaya.MGlobal.displayError('Failed to deregister createPoseScopeShape command.\n')