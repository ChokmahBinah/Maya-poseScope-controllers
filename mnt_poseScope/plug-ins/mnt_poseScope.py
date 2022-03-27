import ctypes
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.api.OpenMayaRender as OpenMayaRender
import maya.api.OpenMayaAnim as OpenMayaAnim

maya_useNewAPI = True

class Mnt_poseScopeNode(OpenMaya.MPxSurfaceShape):
    kPluginNodeName             = 'mnt_poseScope'
    id                          = OpenMaya.MTypeId( 0xDAE6 )
    #drawDbClassification        = "drawdb/geometry/Mnt_poseScopeNode"
    drawDbClassification       = "drawdb/subscene/Mnt_poseScopeNode"
    drawRegistrantId            = "Mnt_poseScopeNodePlugin"

    inFaceComponentsAttribute   = OpenMaya.MObject()
    inMeshObjAttribute          = OpenMaya.MObject()
    colorAttribute              = OpenMaya.MObject()
    opacityAttribute            = OpenMaya.MObject()
    hilightOpacityAttribute     = OpenMaya.MObject()
    xRayModeAttribute           = OpenMaya.MObject()
    interactiveDisplayAttribute = OpenMaya.MObject()

    fsInteractiveMode           = False
    fsXRayMode                  = False
    doRefresh                   = True
    shape                       = OpenMaya.MObject()

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
        Mnt_poseScopeNode.inFaceComponentsAttribute = typedAttributeFn.create('inputFaceComponents', 'inputFaceComponents', OpenMaya.MFnData.kComponentList)
        typedAttributeFn.hidden   = False
        typedAttributeFn.storable = True
        typedAttributeFn.writable = True
        Mnt_poseScopeNode.addAttribute(Mnt_poseScopeNode.inFaceComponentsAttribute)

        Mnt_poseScopeNode.inMeshObjAttribute = typedAttributeFn.create('inputMesh', 'inputMesh', OpenMaya.MFnData.kMesh, OpenMaya.MObject.kNullObj)
        typedAttributeFn.hidden      = False
        typedAttributeFn.storable    = True
        typedAttributeFn.writable    = True
        Mnt_poseScopeNode.addAttribute(Mnt_poseScopeNode.inMeshObjAttribute)

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

    def isBounded(self):
        return True

    def boundingBox(self):
        return self.BBox

    def getShapeSelectionMask(self):  
        selType = OpenMaya.MSelectionMask.kSelectLocators
        return OpenMaya.MSelectionMask(selType)

    def connectionMade(self, plug, otherPlug, asSrc):
        if not asSrc and plug.attribute() == Mnt_poseScopeNode.inFaceComponentsAttribute:
            self.doRefresh = True

        if not asSrc and plug.attribute() == Mnt_poseScopeNode.inMeshObjAttribute:
            self.doRefresh = True

        return OpenMaya.MPxNode.connectionMade(self, plug, otherPlug, asSrc)

    def compute(self, plug, dataBlock):
        return

    def setDependentsDirty(self, plug, plugArray):
        if plug.attribute() == Mnt_poseScopeNode.interactiveDisplayAttribute:

            if plug.asBool() == False:
                self.fsInteractiveMode = True
            else:
                self.fsInteractiveMode = False

        if plug.attribute() == Mnt_poseScopeNode.xRayModeAttribute:

            if plug.asBool() == False:
                self.fsXRayMode = True
            else:
                self.fsXRayMode = False

        if plug.attribute() == Mnt_poseScopeNode.inFaceComponentsAttribute:
            self.doRefresh = True
        
        if plug.attribute() == Mnt_poseScopeNode.inMeshObjAttribute:
            self.doRefresh = True

    def preEvaluation(self, context, evaluationNode):
        return

    def postEvaluation(self, context, evaluationNode, evalType):
        return
            
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
                self.inputMeshFn    = OpenMaya.MFnMesh(node)
                self.shape          = node
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
            raise

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
        #self.fMesh.setInputMeshChangedSinceUpdate(False)

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
            if self.doRefresh == True: # or self.fMesh.evalInputMeshChangedSinceUpdate() == True:
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
            
            '''if data.xRayMode == True:
                drawManager.beginDrawInXray()'''
            
            drawManager.setDepthPriority(21)
            drawManager.setColor(OpenMaya.MColor((data.shaderColor[0], data.shaderColor[1], data.shaderColor[2], data.shaderOpacity)))
            drawManager.mesh(OpenMayaRender.MUIDrawManager.kTriangles, self.poseScopeShapePointsArray, None, None, self.poseScopeShapeIndexArray, None)
            
            '''if data.xRayMode == True:
                drawManager.endDrawInXray()'''

            drawManager.endDrawable()       
# _____________________________

# MPxSubSceneOverride implementation
class Mnt_poseScopeSubSceneOverride(OpenMayaRender.MPxSubSceneOverride):
    sShadedName = 'poseScopeShader'
    Mnt_poseScopeNode_inputMeshDirtyCallback = None

    '''class InstanceInfo:#...?
        def __init__(self, transform, isSelected):
            self.fTransform = transform
            self.fIsSelected = isSelected'''

    @staticmethod
    def creator(obj):
        return Mnt_poseScopeSubSceneOverride(obj)

    def __init__(self, obj):
        OpenMayaRender.MPxSubSceneOverride.__init__(self, obj)

        self.node                           = OpenMaya.MFnDependencyNode(obj)
        self.fMesh                          = self.node.userNode()
        self.MObj                           = obj
        self.inputMeshFn                    = None
        self.fComponent                     = None
        self.shader                         = None
        self.shaderColor                    = None
        self.shaderOpacity                  = None  
        self.inputFacesPositionBuffer       = None
        #self.inputFacesNormalBuffer         = None
        self.inputFacesShadedIndexBuffer    = None  

    def getInputFaces(self):
        inputMeshPlug   = self.node.findPlug('inputMesh', False)
        connections   = inputMeshPlug.connectedTo(True, False)

        for i in range(len(connections)):
            node = connections[i].node()

            if node.hasFn(OpenMaya.MFn.kMesh):
                self.inputMeshFn    = OpenMaya.MFnMesh(node)
                self.shape          = node
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
            raise
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

    def supportedDrawAPIs(self):
        return OpenMayaRender.MRenderer.kOpenGL | OpenMayaRender.MRenderer.kDirectX11 | OpenMayaRender.MRenderer.kOpenGLCoreProfile

    def refresh(self, *args):
        self.fMesh.doRefresh = True
        return

    def requiresUpdate(self, container, frameContext):                      
        # Nothing in the container, definitively need to update.
        if len(container) == 0:
            return True
        # ______________________________________________________

        if self.Mnt_poseScopeNode_inputMeshDirtyCallback == None:
            try:
                self.oldShape = self.shape
                self.Mnt_poseScopeNode_inputMeshDirtyCallback = OpenMaya.MNodeMessage.addNodeDirtyPlugCallback(self.shape, self.refresh)
            except:
                pass
            
        elif self.shape != self.oldShape:
            OpenMaya.MMessage.removeCallback(self.Mnt_poseScopeNode_inputMeshDirtyCallback)
            self.Mnt_poseScopeNode_inputMeshDirtyCallback = OpenMaya.MNodeMessage.addNodeDirtyPlugCallback(self.shape, self.refresh)
            self.oldShape = self.shape
        else:
            pass
        
        if self.fMesh.fsInteractiveMode == True:
            return True

        elif not frameContext.inUserInteraction():
            return True

        elif frameContext.inUserInteraction():
            shadedItem = container.find(self.sShadedName)
            if shadedItem:
                shadedItem.enable(False)
            return False

    def update(self, container, frameContext):
        # Changes the shader opacity if the poseScope shape parent is selected.
        MActiveSel  = OpenMaya.MGlobal.getActiveSelectionList()
        MFnDagNode  = OpenMaya.MFnDagNode(self.MObj)
        MObjParent  = MFnDagNode.parent(0)
        MFnParent   = OpenMaya.MFnDependencyNode(MObjParent)

        self.shaderColor    = self.node.findPlug('color', False).asMDataHandle().asFloat3()
        self.shaderOpacity  = self.node.findPlug('opacity', False).asFloat()

        if MActiveSel.length() > 0 and MFnParent.name() in MActiveSel.getSelectionStrings():
            self.shaderOpacity = self.node.findPlug('hilightOpacity', False).asFloat()
        # _____________________________________________________________________

        # Change renderItem depthPriority depending on  xRayMode attribute
        shadedItem = container.find(self.sShadedName)
        if shadedItem:
            if self.fMesh.fsXRayMode == True:
                shadedItem.setDepthPriority(1000000)
            else:
                shadedItem.setDepthPriority(21)
        # ________________________________________________________________

            # Helps hide poseScopes when user needs it.
            if MFnParent.findPlug('visibility', False).asBool() == False or self.node.findPlug('visibility', False).asBool() == False:
                self.shaderOpacity = 0.0
            # _________________________________________

        self.getInputFaces()
        self.manageRenderItems(container, frameContext, True)
        
    def furtherUpdateRequired(self, frameContext):
        return False

    def manageRenderItems(self, container, frameContext, updateGeometry):
        # Creates shader that will be used by the poseScope shape.
        shaderManager   = OpenMayaRender.MRenderer.getShaderManager() 
        if not shaderManager:
            return
  
        shaderColor     = [self.shaderColor[0], self.shaderColor[1], self.shaderColor[2], self.shaderOpacity]

        if not self.shader:
            self.shader = shaderManager.getStockShader(OpenMayaRender.MShaderManager.k3dSolidShader)

        self.shader.setParameter("solidColor", shaderColor)
        self.shader.setIsTransparent(True)
        # ________________________________________________________

        # Creates the renderItem
        shadedItem = container.find(self.sShadedName)
        if not shadedItem:
            shadedItem = OpenMayaRender.MRenderItem.create(self.sShadedName, OpenMayaRender.MRenderItem.DecorationItem, OpenMayaRender.MGeometry.kTriangles)
            shadedItem.setDrawMode(OpenMayaRender.MGeometry.kAll)
            shadedItem.setExcludedFromPostEffects(True)
            shadedItem.setDepthPriority(21)
            shadedItem.setCastsShadows(False)
            shadedItem.setReceivesShadows(False)
            shadedItem.setAllowIsolateSelectCopy(True)
            shadedItem.setWantConsolidation(True)
            shadedItem.setWantSubSceneConsolidation(True)
            container.add(shadedItem)
        
        shadedItem.setShader(self.shader)
        shadedItem.enable(True)
        # ______________________

        # Set up shared geometry if necessary.
        if updateGeometry:
            if self.fMesh.doRefresh == True:
                self.rebuildGeometryBuffers()
        # ____________________________________

        buffers = OpenMayaRender.MVertexBufferArray()
        try:
            buffers.append(self.inputFacesPositionBuffer, 'positions')
            #buffers.append(self.inputFacesNormalBuffer, 'normals')
        except:
            return

        self.setGeometryForRenderItem(shadedItem, buffers, self.inputFacesShadedIndexBuffer, None)
        #shadedItem.setMatrix(OpenMaya.MMatrix.kIdentity)
        
    def rebuildGeometryBuffers(self):
        self.clearGeometryBuffers()
        matrix          = self.getWorldMatrix()

        # Compute mesh data size of inputFaces
        numTriangles    = 0
        totalVerts      = 0
        vertices        = OpenMaya.MPointArray()

        try:
            facesSet            = self.fComponent.getElements()
            numFaces            = len(facesSet)
            inputMeshTriangles  = self.inputMeshFn.getTriangles()
        except:
            return
        
        for i in facesSet:
            numVerts = len(self.inputMeshFn.getPolygonVertices(i))
            if numVerts > 2:
                numTriangles    += numVerts - 2
            faceTriNb = inputMeshTriangles[0][i]
            
            for j in range(0, faceTriNb):
                triVert = self.inputMeshFn.getPolygonTriangleVertices(i, j)
                for k in triVert:
                    point = self.inputMeshFn.getPoint(k).__mul__(matrix)
                    try:
                        vertices.append(point)
                        self.fMesh.BBox.expand(point)# Expand BBox
                    except:
                        return

        totalVerts = 3 * numTriangles
        # ____________________________________

        # Acquire vertex buffer ressources
        posDesc = OpenMayaRender.MVertexBufferDescriptor('', OpenMayaRender.MGeometry.kPosition, OpenMayaRender.MGeometry.kFloat, 3)
        self.inputFacesPositionBuffer = OpenMayaRender.MVertexBuffer(posDesc)

        '''if self.inputFacesPositionBuffer is None:
            return'''

        positionDataAddress = self.inputFacesPositionBuffer.acquire(totalVerts, True)   
        positionData        = ((ctypes.c_float * 3) * totalVerts).from_address(positionDataAddress)

        for vid,position in enumerate(vertices):
            positionData[vid][0] = position[0]
            positionData[vid][1] = position[1]
            positionData[vid][2] = position[2] 

        self.inputFacesPositionBuffer.commit(positionDataAddress)
        positionDataAddress = None

        '''normalDesc = OpenMayaRender.MVertexBufferDescriptor('', OpenMayaRender.MGeometry.kNormal, OpenMayaRender.MGeometry.kFloat, 3)
        self.inputFacesNormalBuffer = OpenMayaRender.MVertexBuffer(normalDesc)

        if self.inputFacesNormalBuffer is None:
            return

        normalDataAddress  = self.inputFacesNormalBuffer.acquire(totalVerts, True) 
        normalData         = ((ctypes.c_float * 3) * totalVerts).from_address(normalDataAddress)

        normals = self.inputMeshFn.getVertexNormals(True)

        for vid,normal in enumerate(normals):
            normalData[vid][0] = normal[0]
            normalData[vid][1] = normal[1]
            normalData[vid][2] = normal[2]

        self.inputFacesNormalBuffer.commit(normalDataAddress)
        normalDataAddress = None'''
        # ________________________________

        # Create index buffer        
        if numFaces > 0:

            if self.inputFacesShadedIndexBuffer == None:
                self.inputFacesShadedIndexBuffer = OpenMayaRender.MIndexBuffer(OpenMayaRender.MGeometry.kUnsignedInt32)

                inputFacesDataAddress = self.inputFacesShadedIndexBuffer.acquire(totalVerts, True)
            
                if inputFacesDataAddress:
                    inputFacesData = ((ctypes.c_uint * 3) * numTriangles).from_address(inputFacesDataAddress)

                    idx = 0
                    vid = 0

                # Creates faces connection list from input infos
                #faceConnects = OpenMaya.MIntArray()
                #for i in range(0, totalVerts):
                #    faceConnects.append(i)

                    for i in range(numTriangles):
                        #inputFacesData[idx][0] = faceConnects[vid]
                        #inputFacesData[idx][1] = faceConnects[vid + 1]
                        #inputFacesData[idx][2] = faceConnects[vid + 2]            
                        inputFacesData[idx][0] = vid
                        inputFacesData[idx][1] = vid + 1
                        inputFacesData[idx][2] = vid + 2          
                        idx += 1                    
                        vid += 3
                                        
                    self.inputFacesShadedIndexBuffer.commit(inputFacesDataAddress)
                    inputFacesDataAddress = None
                    inputFacesData = None
        # ___________________
        #self.fMesh.setInputMeshChangedSinceUpdate(False)
        self.fMesh.doRefresh = False

    def clearGeometryBuffers(self, *args):
        self.inputFacesPositionBuffer       = None
        #self.inputFacesNormalBuffer        = None
        self.inputFacesShadedIndexBuffer    = None
# __________________________________

# Needed for registtering the node shape
class Mnt_poseScopeNodeUI(OpenMayaUI.MPxSurfaceShapeUI):
    @staticmethod
    def creator():
        return Mnt_poseScopeNodeUI()

    def __init__(self):
        OpenMayaUI.MPxSurfaceShapeUI.__init__(self)
# ______________________________________

# Plugin Commands
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
        components = OpenMaya.MObject()
        componentListStr    = ''
        poseScopeSelList    = OpenMaya.MSelectionList()
        MSelectionList      = OpenMaya.MGlobal.getActiveSelectionList()
        transformNode       = None
                
        componentsListData = OpenMaya.MFnComponentListData()
        componentsListObj = componentsListData.create()

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

                # Gets components list data from selection
                componentsListData.add(components[1])
                # ________________________________________

        # Creates mnt_poseScope DAG node.
        DGModifier                  = OpenMaya.MDGModifier()
        poseScopeDagNodeFn          = OpenMaya.MFnDagNode()
        self.poseScopeDagNodeObj    = poseScopeDagNodeFn.create('mnt_poseScope')
        poseScopeNodePath           = OpenMaya.MFnDagNode(self.poseScopeDagNodeObj).getPath().extendToShape()
        poseScopeNode               = OpenMaya.MFnDependencyNode(poseScopeNodePath.node())
        poseScopeNode.findPlug('colorR', False).setDouble(1.0)
        poseScopeNode.findPlug('colorG', False).setDouble(0.75)
        poseScopeNode.findPlug('colorB', False).setDouble(0.0)
        poseScopeNode.findPlug('opacity', False).setFloat(0.05)
        poseScopeNode.findPlug('inputFaceComponents', False).setMObject(componentsListObj)#
        # _______________________________
        
        # Creates connections.
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
        facesSingleIndexedComponent = OpenMaya.MFnSingleIndexedComponent()
        facesComponentsObj = facesSingleIndexedComponent.create(OpenMaya.MFn.kMeshPolygonComponent)

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
                        facesSingleIndexedComponent.addElement(symFace)

                componentsListData = OpenMaya.MFnComponentListData()
                componentsListObj = componentsListData.create()
                componentsListData.add(facesComponentsObj)
                # __________________________________

                # Creates mnt_poseScope DAG node.
                DGModifier      = OpenMaya.MDGModifier()
                poseScopeDagNodeFn  = OpenMaya.MFnDagNode()
                self.poseScopeDagNodeObj = poseScopeDagNodeFn.create('mnt_poseScope')
                poseScopeNodePath   = OpenMaya.MFnDagNode(self.poseScopeDagNodeObj).getPath().extendToShape()
                poseScopeNode       = OpenMaya.MFnDependencyNode(poseScopeNodePath.node())
                poseScopeNode.findPlug('colorR', False).setDouble(childFn.findPlug('colorG', False).asDouble())
                poseScopeNode.findPlug('colorG', False).setDouble(childFn.findPlug('colorB', False).asDouble())
                poseScopeNode.findPlug('colorB', False).setDouble(childFn.findPlug('colorR', False).asDouble())
                poseScopeNode.findPlug('opacity', False).setFloat(childFn.findPlug('opacity', False).asFloat())
                poseScopeNode.findPlug('inputFaceComponents', False).setMObject(componentsListObj)
                # _______________________________

                # Creates connections.
                DGModifier.connect(inputMeshFn.findPlug('outMesh', False), poseScopeNode.findPlug('inputMesh', False))
                # ____________________

                DGModifier.doIt()
    
        # If an opposite transform node exists (_L_ or _R_), parent the new node to it.
        if '_L_' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('_L_', '_R_')
        elif '_l_' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('_l_', '_r_')
        elif 'L_' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('L_', 'R_')
        elif 'l_' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('l_', 'r_')
        elif '_L' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('_L', '_R')
        elif '_l' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('_l', '_r')
        elif '_R_' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('_R_', '_L_')
        elif '_r_' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('_r_', '_l_')
        elif 'R_' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('R_', 'L_')
        elif 'r_' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('r_', 'l_')
        elif '_R' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('_R', '_L')
        elif '_r' in MDagPath.__str__():
            oppositeTransformNode = MDagPath.__str__().replace('_r', '_l')
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
        iterator = OpenMaya.MItDag()
        while not iterator.isDone():
            MObj = iterator.currentItem()
            MDnFn = OpenMaya.MFnDependencyNode(MObj)
            
            if MDnFn.typeName == 'transform':
                path = iterator.getPath()
                
                if path.childCount() > 1:
                    zeroPathChildDnFn = OpenMaya.MFnDependencyNode(path.child(0))
                    
                    if zeroPathChildDnFn.typeName == 'mnt_poseScope':
                        
                        for i in range(0, path.childCount()):
                            childNode = OpenMaya.MFnDagNode(path.child(i))                     
                            
                            if path.child(i).apiType() == OpenMaya.MFn.kMesh or path.child(i).apiType() == OpenMaya.MFn.kNurbsCurve\
                            or path.child(i).apiType() == OpenMaya.MFn.kPluginShape or path.child(i).apiType() == OpenMaya.MFn.kNurbsSurface:
                                childDnFn = OpenMaya.MFnDependencyNode(path.child(i))
                                
                                if childDnFn.typeName != 'mnt_poseScope':      
                                    visibilityPlug = childDnFn.findPlug('visibility', False)
                                    visibilityValue = visibilityPlug.asBool()
                                
                                    if visibilityValue == True:
                                        visibilityPlug.setBool(False)
                                    else:
                                        visibilityPlug.setBool(True)                        
                
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
    
    def doIt(self, *args):
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
            poseScopeNode.findPlug('colorR', False).setDouble(self.color[i][0])
            poseScopeNode.findPlug('colorG', False).setDouble(self.color[i][1])
            poseScopeNode.findPlug('colorB', False).setDouble(self.color[i][2])
            poseScopeNode.findPlug('opacity', False).setFloat(self.opacity[i])
            poseScopeNode.findPlug('hilightOpacity', False).setFloat(self.hilightOpacity[i])
            poseScopeNode.findPlug('inputFaceComponents', False).setMObject(self.inputComponentsList[i])
            # ______________________

            # Parents poseScope shape to transformNode
            transformDagNode = OpenMaya.MFnDagNode(MTransformNodeObj)
            transformDagNode.addChild(poseScopeNodePath.node(), 0, False)
            OpenMaya.MGlobal.deleteNode(poseScopeDagNodeObj)
            # ________________________________________

            # Creates node connections
            DGModifier = OpenMaya.MDGModifier()
            DGModifier.connect(inputMeshDGFn.findPlug('outMesh', False), poseScopeNode.findPlug('inputMesh',False))
            DGModifier.doIt()
            # ________________________

        return
    
    def redoIt(self):
        self.transformNodesList     = []
        self.inputComponentsList    = []
        self.inputMeshList          = []
        self.color                  = []
        self.opacity                = []
        self.hilightOpacity         = []

        MSelectionList = OpenMaya.MGlobal.getActiveSelectionList()

        if MSelectionList.length() == 0:
            OpenMaya.MGlobal.displayError('Please select a transform node first. If it has a poseScope shape, it will be deleted.' )
            return

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
                    self.color.append((childDGFn.findPlug('colorR', False).asDouble(), childDGFn.findPlug('colorG', False).asDouble(), childDGFn.findPlug('colorB', False).asDouble()))
                    self.opacity.append(childDGFn.findPlug('opacity', False).asFloat())
                    self.hilightOpacity.append(childDGFn.findPlug('hilightOpacity', False).asFloat())

                    self.inputComponentsList.append(inputComponentsPlug.asMObject())
                    
                    connections = inputComponentsPlug.connectedTo(True, False)
                                       
                    inputMeshPlug = childDGFn.findPlug('inputMesh', False)
                    connections = inputMeshPlug.connectedTo(True, False)

                    for plug in connections:
                        node = plug.node()

                        if node.hasFn(OpenMaya.MFn.kMesh):
                            self.inputMeshList.append(node)

                    self.transformNodesList.append(str(MDagPath))
                    OpenMaya.MGlobal.deleteNode(child)
        return 
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

        if MActiveList.length() == 0:
            OpenMaya.MGlobal.displayError('Please select a transform node first. If it has a poseScope shape, its face components will be selected for further editing.')
            return

        MObj            = MActiveList.getDependNode(0)
        MObjDNFn        = OpenMaya.MFnDependencyNode(MObj)

        if OpenMaya.MFnDependencyNode(MObj).typeName != 'transform':
            return

        MDagPath= OpenMaya.MDagPath.getAPathTo(MObj)

        for i in range(MDagPath.childCount()):
            child = MDagPath.child(i)
            childDNFn = OpenMaya.MFnDependencyNode(child)
                
            if childDNFn.typeName == 'mnt_poseScope':
                inputFaceComponents = childDNFn.findPlug('inputFaceComponents', False).asMObject()
                break
            
        MposeScopeMeshObj   = self.get_poseScopeMesh()

        try:
            componentListData       = OpenMaya.MFnComponentListData(inputFaceComponents)
        except:
            return

        for i in range(0, componentListData.length()):
            MSelectionList.add((OpenMaya.MDagPath.getAPathTo(MposeScopeMeshObj), componentListData.get(i)))

        MSelectionList.add(OpenMaya.MDagPath.getAPathTo(MObj))

        OpenMaya.MGlobal.setComponentSelectionMask(OpenMaya.MSelectionMask.kSelectMeshFaces)
        OpenMaya.MGlobal.setSelectionMode(OpenMaya.MGlobal.kSelectComponentMode)
        OpenMaya.MGlobal.setHiliteList(MSelectionList)
        OpenMaya.MGlobal.setActiveSelectionList(MSelectionList)
    
    def get_poseScopeMesh(self):
        MselectionList  = OpenMaya.MGlobal.getActiveSelectionList()
        MObj            = MselectionList.getDependNode(0)
        MObjDNFn        = OpenMaya.MFnDependencyNode(MObj)
        poseScopeNode   = None
        
        if MObjDNFn.typeName == 'transform':
            MdagNode = OpenMaya.MFnDagNode(MObj)

            for i in range(0, MdagNode.childCount()):
                if OpenMaya.MFnDependencyNode(MdagNode.child(i)).typeName == 'mnt_poseScope':
                    poseScopeNode = MdagNode.child(i)
                    break
        
        if not poseScopeNode:
             return

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
        sComponentList  = []
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

        OpenMaya.MGlobal.displayInfo('Transferring poseScopes...')
        
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

                sComponentList = []
                
                sInputFaceComponentsPlug = nodeFn.findPlug('inputFaceComponents', False)
                componentsListData = OpenMaya.MFnComponentListData(sInputFaceComponentsPlug.asMObject())
                
                for i in range(componentsListData.length()):
                    singleIndexedComponent = OpenMaya.MFnSingleIndexedComponent(componentsListData.get(i))

                    for element in singleIndexedComponent.getElements():
                        sComponentList.append(element)
                
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
                                
                    if dFaceID in sComponentList:
                        dComponentList.append(i)
                                
                dSingleIndexedComponent = OpenMaya.MFnSingleIndexedComponent()
                dComponentsObj = dSingleIndexedComponent.create(OpenMaya.MFn.kMeshPolygonComponent)
                dSingleIndexedComponent.addElements(dComponentList)

                dComponentsListData = OpenMaya.MFnComponentListData()
                dComponentsListObj = dComponentsListData.create()
                dComponentsListData.add(dComponentsObj)

                sInputFaceComponentsPlug.setMObject(dComponentsListObj)

        OpenMaya.MGlobal.displayInfo('Posescopes transferred.')# J'ai encore un souci de mise à jour, on dirait que le callback de la shape a un problèmre.
        return
# ___________________________________
# _______________

# Trying to create a context selection for this node...
'''import math
import maya.cmds as cmds # ForContext creation. Have to try avoid this in the future

class Mnt_poseScopeContextCmd(OpenMayaUI.MPxContextCommand):
    kPluginCmdName = 'mnt_poseScopeContextCmd'

    def __init__(self):
        OpenMayaUI.MPxContextCommand.__init__(self)
    
    @classmethod
    def creator(cls):
        return cls()

    def makeObj(self):
        return Mnt_poseScopeContext()

class Mnt_poseScopeContext(OpenMayaUI.MPxContext):
    help_string = "Drag mouse to select points by encircling"
    cursor_width = 16
    cursor_height = 16
    cursor_x_hot = 1
    cursor_y_hot = 16

    @classmethod
    def creator(cls):
        return Mnt_poseScopeContext(cls)

    def __init__(self):
        OpenMayaUI.MPxContext.__init__(self)

        iconPath = cmds.getModulePath(moduleName = 'mnt_framework') + '/icons/mntShelf/'

        self.fs_drawn = False
        self.list_adjustment = 0
        self.view = None
        self.setTitleString('Marquee Tool')
        self.setImage(iconPath + 'mnt_poseTool.png', OpenMayaUI.MPxContext.kImage1)

        self.poseScopeShapePointsArray      = OpenMaya.MPointArray()
        self.poseScopeShapeIndexArray       = OpenMaya.MUintArray()

        self.oldOpacityValue = None
        self.oldShape = None

    #def stringClassName(self):
    #    return 'Pose_Tool'
    
    def toolOnSetup(self, event):
        self.setHelpString(Mnt_poseScopeContext.help_string)
        poseScopeList = cmds.ls(typ = 'mnt_poseScope')
        
        for node in poseScopeList:
            opacity = cmds.getAttr(node + '.opacity')
            self.initialOpacities.append(opacity)
            cmds.setAttr(node + '.opacity', 0.0)

    def doPress( self, event, drawMgr, context ):
        # Handle the mouse press event in VP2.0.
        try:
            if event.isModifierShift() or event.isModifierControl():
                if event.isModifierShift():
                    if event.isModifierControl():
                        # both shift and control pressed, merge new selections
                        self.list_adjustment = OpenMaya.MGlobal.kAddToList
                    else:
                        # shift only, xor new selections with previous ones
                        self.list_adjustment = OpenMaya.MGlobal.kXORWithList

                elif event.isModifierControl():
                    # control only, remove new selections from the previous list
                    self.list_adjustment = OpenMaya.MGlobal.kRemoveFromList
            else:
                self.list_adjustment = OpenMaya.MGlobal.kReplaceList

            # Extract the event information
            self.start = event.position
        except:
            pass

    def doRelease( self, event, drawMgr, context ):
        # Get the end position of the marquee
        self.last = event.position

        # Save the state of the current selections.  The "selectFromSceen"
        # below will alter the active list, and we have to be able to put
        # it back.
        incoming_list = OpenMaya.MGlobal.getActiveSelectionList()
        
        MSelectionMask = OpenMaya.MSelectionMask()
        MSelectionMask.setMask(OpenMaya.MSelectionMask.kSelectLocators)
        MSelectionMask.addMask(OpenMaya.MSelectionMask.kSelectNurbsCurves )   

        OpenMaya.MGlobal.setObjectSelectionMask(MSelectionMask)

        # If we have a zero dimension box, just do a point pick
        if math.fabs(self.start[0] - self.last[0]) < 2 and math.fabs(self.start[1] - self.last[1]) < 2:
            # This will check to see if the active view is in wireframe or not.
            selection_method = OpenMaya.MGlobal.selectionMethod()
            try:
                OpenMaya.MGlobal.selectFromScreen(self.last[0], self.last[1], listAdjustment = OpenMaya.MGlobal.kReplaceList, selectMethod = OpenMaya.MGlobal.kWireframeSelectMethod)
            except:
                pass
        else:
            # The Maya select tool goes to wireframe select when doing a marquee, so
            # we will copy that behaviour.
            # Select all the objects or components within the marquee.
            OpenMaya.MGlobal.selectFromScreen(self.start[0], self.start[1], self.last[0], self.last[1], 
                                              listAdjustment = OpenMaya.MGlobal.kReplaceList,
                                              selectMethod = OpenMaya.MGlobal.kWireframeSelectMethod)

        # Get the list of selected items
        marquee_list = OpenMaya.MGlobal.getActiveSelectionList()

        # Restore the active selection list to what it was before the "selectFromScreen"
        OpenMaya.MGlobal.setActiveSelectionList(incoming_list, OpenMaya.MGlobal.kReplaceList)

        # Update the selection list as indicated by the modifier keys.
        OpenMaya.MGlobal.selectCommand(marquee_list, self.list_adjustment)

    def doDrag(self, event, drawMgr, context):
        # Get the marquee's new end position.
        self.last = event.position

        # Draw the marquee at its new position.
        drawMgr.beginDrawable()
        drawMgr.setColor(OpenMaya.MColor((1.0, 0.0, 0.5)))
        drawMgr.setLineWidth(2)
        drawMgr.line2d(OpenMaya.MPoint( (self.start[0], self.start[1])), OpenMaya.MPoint((self.last[0], self.start[1])))
        drawMgr.line2d(OpenMaya.MPoint( (self.last[0], self.start[1])),  OpenMaya.MPoint((self.last[0], self.last[1])))
        drawMgr.line2d(OpenMaya.MPoint( (self.last[0], self.last[1])),   OpenMaya.MPoint((self.start[0], self.last[1])))
        drawMgr.line2d(OpenMaya.MPoint( (self.start[0], self.last[1])),  OpenMaya.MPoint((self.start[0], self.start[1])))
        drawMgr.endDrawable()

    def doPtrMoved(self, event, drawMgr, context):
        MSelectionList = OpenMaya.MSelectionList()
        shape = None
        self.oldOpacityValue = 0.0

        view = OpenMayaUI.M3dView.active3dView()
        portWidth = view.portWidth()
        portHeight = view.portHeight()
                
        panel               = cmds.getPanel(underPointer = True)
        panelType           = cmds.getPanel(typeOf = panel)

        if panelType == 'modelPanel':            
            shapesUnderCursor   = cmds.hitTest(panel, event.position[0], portHeight - event.position[1])

            if len(shapesUnderCursor) > 0:                          
                shape = cmds.ls(shapesUnderCursor, flatten = True)[0]
                MSelectionList.clear()
                MSelectionList.add(shape)
                self.shapeObj = MSelectionList.getDependNode(0)
                shapeDNFn = OpenMaya.MFnDependencyNode(self.shapeObj)                        

                if shapeDNFn.typeName == 'mnt_poseScope':
                    if shape != self.oldShape:
                        self.oldShape = shape
                        self.poseScopeShapePointsArray.clear()
                        self.poseScopeShapeIndexArray.clear()

                        self.getInputFaces(shapeDNFn)

                        self.rebuildBuffers()

                        drawMgr.endDrawable()
                    else:
                        pass

                    color =  shapeDNFn.findPlug('color', False).asMDataHandle().asFloat3()
                    drawMgr.beginDrawable()
                    drawMgr.setDepthPriority(0)
                    drawMgr.setColor(OpenMaya.MColor((color[0], color[1], color[2], 0.2)))
                    drawMgr.mesh(OpenMayaRender.MUIDrawManager.kTriangles, self.poseScopeShapePointsArray, None, None, self.poseScopeShapeIndexArray, None)
                        
        return

    def getInputFaces(self, poseScopeNode):
        inputMeshPlug   = poseScopeNode.findPlug('inputMesh', False)
        connections   = inputMeshPlug.connectedTo(True, False)

        for i in range(0, len(connections)):
            node = connections[i].node()

            if node.hasFn(OpenMaya.MFn.kMesh):
                self.inputMeshFn             = OpenMaya.MFnMesh(node)
                self.meshShapeNode = node
                break

        inputFaceComponentsPlug     = poseScopeNode.findPlug('inputFaceComponents', False)
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
            inputMeshParent             = OpenMaya.MFnDagNode(self.meshShapeNode).parent(0)
        except:
            return

        fnInputMeshParent           = OpenMaya.MFnDependencyNode(inputMeshParent)
        inputMeshWorldMatrixAttr    = fnInputMeshParent.attribute('worldMatrix')
        inputMeshWorldMatrixPlug    = OpenMaya.MPlug(inputMeshParent, inputMeshWorldMatrixAttr)
        inputMeshWorldMatrixPlug    = inputMeshWorldMatrixPlug.elementByLogicalIndex(0)
        inputMeshWorldMatrixObj     = inputMeshWorldMatrixPlug.asMObject()
        inputMeshWorldMatrixData    = OpenMaya.MFnMatrixData(inputMeshWorldMatrixObj)
        inputMeshWorldMatrix        = inputMeshWorldMatrixData.matrix()

        MObjFn              = OpenMaya.MFnDagNode(self.shapeObj)
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
        matrix          = self.getWorldMatrix()

        try:
            facesSet            = self.fComponent.getElements()
            inputMeshTriangles  = self.inputMeshFn.getTriangles()
        except:
            raise

        for i in facesSet:
            faceTriNb = inputMeshTriangles[0][i]
    
            for j in range(0, faceTriNb):
                triVert = self.inputMeshFn.getPolygonTriangleVertices(i, j)
                for k in triVert:
                    point = self.inputMeshFn.getPoint(k)
                    try:
                        self.poseScopeShapePointsArray.append(point)  
                    except:
                        raise'''
# _____________________________________________________

def initializePlugin(obj):
    plugin = OpenMaya.MFnPlugin(obj, 'Florian Delarque', '1.5', 'Any')
    try:
        plugin.registerShape(Mnt_poseScopeNode.kPluginNodeName, Mnt_poseScopeNode.id, Mnt_poseScopeNode.creator, Mnt_poseScopeNode.initialize, Mnt_poseScopeNodeUI.creator, Mnt_poseScopeNode.drawDbClassification)
    except:
        OpenMaya.MGlobal.displayError('Failed to register node\n')
        raise

    try:
        #OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(Mnt_poseScopeNode.drawDbClassification, Mnt_poseScopeNode.drawRegistrantId, Mnt_poseScopeDrawOverride.creator)
        OpenMayaRender.MDrawRegistry.registerSubSceneOverrideCreator(Mnt_poseScopeNode.drawDbClassification, Mnt_poseScopeNode.drawRegistrantId, Mnt_poseScopeSubSceneOverride.creator)
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
    except:
        OpenMaya.MGlobal.displayError('Failed to register createPoseScopeShape command.\n')

    '''try:
        plugin.registerContextCommand(Mnt_poseScopeContextCmd.kPluginCmdName, Mnt_poseScopeContextCmd.creator)
    except:
        OpenMaya.MGlobal.displayError('Failed to register Mnt_poseScope context command.\n')
        raise'''

def uninitializePlugin(obj):
    plugin = OpenMaya.MFnPlugin(obj)
 
    try:
        plugin.deregisterNode(Mnt_poseScopeNode.id)
    except:
        OpenMaya.MGlobal.displayError("Failed to deregister node\n")
        pass

    try:
        #OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(Mnt_poseScopeNode.drawDbClassification, Mnt_poseScopeNode.drawRegistrantId)
        OpenMayaRender.MDrawRegistry.deregisterSubSceneOverrideCreator(Mnt_poseScopeNode.drawDbClassification, Mnt_poseScopeNode.drawRegistrantId)
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
    except:
        OpenMaya.MGlobal.displayError('Failed to deregister createPoseScopeShape command.\n')

    '''try:
        plugin.deregisterContextCommand(Mnt_poseScopeContextCmd.kPluginCmdName)
    except:
        OpenMaya.MGlobal.displayError('Failed to deregister Mnt_poseScope context command.\n')'''