from ctypes import sizeof
import math
from tkinter.filedialog import Open
import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.api.OpenMayaAnim as OpenMayaAnim
import maya.api.OpenMayaRender as OpenMayaRender
'''import maya.plugin.evaluator.CacheEvaluatorManager #To help use cached playback -> and I should not use it !'''

maya_useNewAPI = True

class MyTextureManager(OpenMayaRender.MTextureManager):#A Faire quand une classe ne peux pas etre instanciee (est une classe abstraite), on doit cree une classe derivee
    def __init__(self):
        pass

class Mnt_locatorNode(OpenMayaUI.MPxLocatorNode):
    kPluginNodeName         = 'mnt_locator' #Name of the node.
    id                      = OpenMaya.MTypeId( 0xDAE2 ) # A unique ID associated to this node type.
    drawDbClassification    = "drawdb/geometry/Mnt_locatorNode"
    #drawDbClassification    = "drawdb/subscene/Mnt_locatorNode"
    drawRegistrantId        = "Mnt_locatorNodePlugin"

    iconFolder              = cmds.getModulePath(moduleName = 'mnt_poseScope') + '/icons/mntLocators/'
    iconType                = OpenMaya.MObject()
    iconMainAxis            = OpenMaya.MObject()
    sizeAttribute           = OpenMaya.MObject()
    areaVisibility          = OpenMaya.MObject()
    colorAttribute          = OpenMaya.MObject()
    opacityAttribute        = OpenMaya.MObject()
    labelAttribute          = OpenMaya.MObject()
    showHierarchicalLinks   = OpenMaya.MObject()
    lineWidth               = OpenMaya.MObject()
    lineColor               = OpenMaya.MObject()
    dottedLine              = OpenMaya.MObject()
    dotsNumber              = OpenMaya.MObject()
    interactiveRefresh      = OpenMaya.MObject()

    isInteractive           = True
    doRefresh               = True

    def __init__(self):
        OpenMayaUI.MPxLocatorNode.__init__(self)
        self.BBox = OpenMaya.MBoundingBox()

    @staticmethod
    def creator():
        return Mnt_locatorNode()
 
    @staticmethod
    def initialize():
        ''' Defines the input and output attributes as static variables in our plug-in class. '''

        # Input Attributes

        # Creates needed function sets
        numericAttributeFn  = OpenMaya.MFnNumericAttribute()
        enumAttr            = OpenMaya.MFnEnumAttribute()
        stringAttrFn        = OpenMaya.MFnTypedAttribute()
        # ____________________________

        Mnt_locatorNode.sizeAttribute    = numericAttributeFn.create('size', 'size', OpenMaya.MFnNumericData.kFloat, 1)
        numericAttributeFn.writable     =  True 
        numericAttributeFn.keyable      = False
        numericAttributeFn.storable     =  True 
        numericAttributeFn.hidden       = False
        numericAttributeFn.channelBox   = True
        numericAttributeFn.setMin( 0.01 )
        numericAttributeFn.setMax( 100.0 )
        Mnt_locatorNode.addAttribute(Mnt_locatorNode.sizeAttribute)

        Mnt_locatorNode.areaVisibility   = numericAttributeFn.create('area_Visibility', 'area_Visibility', OpenMaya.MFnNumericData.kBoolean, False)
        numericAttributeFn.writable     =  True 
        numericAttributeFn.keyable      = False
        numericAttributeFn.storable     =  True 
        numericAttributeFn.hidden       = False
        numericAttributeFn.channelBox   = True
        Mnt_locatorNode.addAttribute(Mnt_locatorNode.areaVisibility)

        Mnt_locatorNode.colorAttribute = numericAttributeFn.createColor('color', 'color')
        numericAttributeFn.writable     = True
        numericAttributeFn.keyable      = False
        numericAttributeFn.channelBox   = True
        numericAttributeFn.storable     = True
        numericAttributeFn.hidden       = False
        Mnt_locatorNode.addAttribute(Mnt_locatorNode.colorAttribute)

        Mnt_locatorNode.opacityAttribute = numericAttributeFn.create('opacity', 'opacity', OpenMaya.MFnNumericData.kFloat, 1.0)
        numericAttributeFn.writable     = True
        numericAttributeFn.keyable      = False
        numericAttributeFn.channelBox   = True
        numericAttributeFn.storable     = True
        numericAttributeFn.hidden       = False
        numericAttributeFn.setMin(0.0)
        numericAttributeFn.setMax(1.0)
        Mnt_locatorNode.addAttribute(Mnt_locatorNode.opacityAttribute)

        Mnt_locatorNode.iconType = enumAttr.create('iconType', 'it', 1)
        enumAttr.addField('Bone', 0)
        enumAttr.addField('Circle', 1)
        enumAttr.addField('Square', 2)
        enumAttr.addField('Skull', 3)
        enumAttr.addField('Pelvis', 4)
        enumAttr.addField('Ribcage', 5)
        enumAttr.addField('Sphere', 6)
        enumAttr.addField('Disc', 7)
        enumAttr.addField('Circle3D', 8)
        enumAttr.hidden     = False
        enumAttr.channelBox = True
        Mnt_locatorNode.addAttribute(Mnt_locatorNode.iconType)

        Mnt_locatorNode.iconMainAxis = enumAttr.create('iconMainAxis', 'ima', 0)
        enumAttr.addField('X', 0)
        enumAttr.addField('Y', 1)
        enumAttr.addField('Z', 2)
        enumAttr.hidden       = True
        enumAttr.channelBox   = True
        Mnt_locatorNode.addAttribute(Mnt_locatorNode.iconMainAxis)

        Mnt_locatorNode.showHierarchicalLinks= numericAttributeFn.create('show_hierarchical_links', 'show_hierarchical_links', OpenMaya.MFnNumericData.kBoolean, False)
        numericAttributeFn.writable     = True 
        numericAttributeFn.keyable      = False
        numericAttributeFn.storable     = True 
        numericAttributeFn.hidden       = False
        numericAttributeFn.channelBox   = True
        Mnt_locatorNode.addAttribute(Mnt_locatorNode.showHierarchicalLinks)

        Mnt_locatorNode.dottedLine = numericAttributeFn.create('use_dotted_line', 'use_dotted_line', OpenMaya.MFnNumericData.kBoolean, False)
        numericAttributeFn.writable   = True 
        numericAttributeFn.keyable    = False
        numericAttributeFn.storable   = True
        numericAttributeFn.hidden     = False
        numericAttributeFn.channelBox = True
        Mnt_locatorNode.addAttribute(Mnt_locatorNode.dottedLine)

        Mnt_locatorNode.dotsNumber = numericAttributeFn.create('dots_number', 'dots_number', OpenMaya.MFnNumericData.kInt, 5)
        numericAttributeFn.writable   = True 
        numericAttributeFn.keyable    = False
        numericAttributeFn.storable   = True
        numericAttributeFn.hidden     = False
        numericAttributeFn.channelBox = True
        numericAttributeFn.setMin(1)
        numericAttributeFn.setMax(16)
        Mnt_locatorNode.addAttribute(Mnt_locatorNode.dotsNumber)

        Mnt_locatorNode.lineWidth = numericAttributeFn.create('line_width', 'line_width', OpenMaya.MFnNumericData.kInt, 4)
        numericAttributeFn.writable    = True
        numericAttributeFn.keyable     = True
        numericAttributeFn.storable    = True
        numericAttributeFn.hidden      = False
        numericAttributeFn.channelBox  = True
        numericAttributeFn.setMin(1)
        numericAttributeFn.setMax(32)
        Mnt_locatorNode.addAttribute(Mnt_locatorNode.lineWidth)

        Mnt_locatorNode.lineColor = numericAttributeFn.createColor('line_color', 'line_color')
        numericAttributeFn.writable     = True
        numericAttributeFn.keyable      = False
        numericAttributeFn.channelBox   = True
        numericAttributeFn.storable     = True
        numericAttributeFn.hidden       = False
        Mnt_locatorNode.addAttribute(Mnt_locatorNode.lineColor)

        Mnt_locatorNode.labelAttribute = stringAttrFn.create('label', 'label', OpenMaya.MFnData.kString)
        stringAttrFn.writable = True
        stringAttrFn.readable = True
        Mnt_locatorNode.addAttribute(Mnt_locatorNode.labelAttribute)

        Mnt_locatorNode.interactiveRefresh = numericAttributeFn.create('interactiveRefresh', 'ir', OpenMaya.MFnNumericData.kBoolean, True)
        numericAttributeFn.writable     = True 
        numericAttributeFn.keyable      = False
        numericAttributeFn.storable     = True 
        numericAttributeFn.hidden       = False
        numericAttributeFn.channelBox   = True
        Mnt_locatorNode.addAttribute(Mnt_locatorNode.interactiveRefresh)

        Mnt_locatorNode.xRayModeAttribute = numericAttributeFn.create('xRayMode', 'xRayMode', OpenMaya.MFnNumericData.kBoolean, False)
        numericAttributeFn.writable     = True
        numericAttributeFn.channelBox   = True
        numericAttributeFn.storable     = True
        numericAttributeFn.hidden       = False
        numericAttributeFn.keyable = False        
        Mnt_locatorNode.addAttribute(Mnt_locatorNode.xRayModeAttribute)


    def isBounded(self):
        return True

    def boundingBox(self):
        return self.BBox

    def compute(self, plug, data):
        return

    def setDependentsDirty(self, plug, plugArray):
        '''thisNodeName = OpenMaya.MFnDependencyNode(self.thisMObject()).name()

        if plug.attribute() == Mnt_locatorNode.iconType:
            iconMainAxisAttr = OpenMaya.MFnAttribute(Mnt_locatorNode.iconMainAxis)  
        
        if plug.attribute() == Mnt_locatorNode.interactiveRefresh:
            if plug.asBool() == False:
                self.isInteractive = True
            else:
                self.isInteractive = False
        
        if plug.name() == thisNodeName + '.localPositionX' or plug.name() == thisNodeName + '.localPositionY' or plug.name() == thisNodeName + '.localPositionZ':
            print('TEST')'''

    def postConstructor(self):
        return
        
# MPxDrawOverride implementation
class Mnt_locatorNodeData(OpenMaya.MUserData):
    def __init__(self):
        OpenMaya.MUserData.__init__(self, False) ## don't delete after draw

class Mnt_locatorNodeDrawOverride(OpenMayaRender.MPxDrawOverride):
    @staticmethod
    def creator(obj):
        return Mnt_locatorNodeDrawOverride(obj)
 
    @staticmethod
    def draw(context, data):
        return
 
    def __init__(self, obj):
        OpenMayaRender.MPxDrawOverride.__init__(self, obj, Mnt_locatorNodeDrawOverride.draw)

        self.pointsArray    = OpenMaya.MPointArray()
        self.indicesArray   = OpenMaya.MUintArray()
        self.MObj               = obj
        self.node           = OpenMaya.MFnDependencyNode(obj)
        self.userNode       = OpenMaya.MFnDependencyNode(obj).userNode()
        self.objPath        = OpenMaya.MDagPath.getAPathTo(obj)
 
    def createCircle3DBuffer(self, inRadius, inLocalPosition, inDirection):
        self.clearBuffers()
        posOutArray = []
        posInArray  = []
        self.userNode.BBox.clear()

        for i in range(0,33):
            u = float(i)/32
            pi = math.pi

            if inDirection == 0:
                posOut =    OpenMaya.MPoint(0 + inLocalPosition[0], inRadius * math.cos(2* pi * u) + inLocalPosition[1], (inRadius * math.sin(2* pi * u) + inLocalPosition[2]))
                posIn =     OpenMaya.MPoint(0 + inLocalPosition[0], 0.85 * inRadius * math.cos(2* pi * u) + inLocalPosition[1], 0.85 * inRadius * math.sin(2* pi * u)+ inLocalPosition[2])    
            elif inDirection == 1:
                posOut =    OpenMaya.MPoint(inRadius * math.cos(2* pi * u) + inLocalPosition[0], 0 + inLocalPosition[1], (inRadius * math.sin(2* pi * u) + inLocalPosition[2]))
                posIn =     OpenMaya.MPoint(0.85 * inRadius * math.cos(2* pi * u) + inLocalPosition[0], 0 + inLocalPosition[1], 0.85 * inRadius * math.sin(2* pi * u)+ inLocalPosition[2])
            else:
                posOut =    OpenMaya.MPoint(inRadius * math.cos(2* pi * u) + inLocalPosition[0], (inRadius * math.sin(2* pi * u) + inLocalPosition[1]), 0 + inLocalPosition[2])
                posIn =     OpenMaya.MPoint(0.85 * inRadius * math.cos(2* pi * u) + inLocalPosition[0], 0.85 * inRadius * math.sin(2* pi * u)+ inLocalPosition[1], 0 + inLocalPosition[2])

            posOutArray.append(posOut)
            posInArray.append(posIn)
            
        for i in range(0, 32):
            self.pointsArray.append(posOutArray[i])
            self.pointsArray.append(posOutArray[i + 1])
            self.pointsArray.append(posInArray[i + 1])
            self.pointsArray.append(posInArray[i + 1])
            self.pointsArray.append(posInArray[i])
            self.pointsArray.append(posOutArray[i])
            self.userNode.BBox.expand(posOutArray[i])

        return

    def clearBuffers(self):
        self.pointsArray.clear()
        self.indicesArray.clear()

    def getTransformNode(self, obj):
        # Method to help get shape parent transform.
        transformObj  = OpenMaya.MFnDagNode(obj).parent(0)
        transformPath = OpenMaya.MDagPath().getAPathTo(transformObj)

        return transformPath, transformObj
        # __________________________________________

    def getHighlightState(self, path):
        # Method to prevent selection childs to have the same color
        MSelectionList = OpenMaya.MGlobal.getActiveSelectionList()

        if MSelectionList.hasItem(path):
            return True

        return False
        # _________________________________________________________

    def manageShapeColor(self):
        # Manages color from shape state.
        status          = OpenMayaUI.M3dView.displayStatus(self.objPath)
        transformNode   = self.getTransformNode(self.MObj)
        color           = self.node.findPlug('color', False).asMDataHandle().asFloat3()
        opacity         = self.node.findPlug('opacity', False).asFloat()
        
        if status == OpenMayaUI.M3dView.kLead:
            if self.getHighlightState(transformNode[0]) == True:
                self.color = OpenMaya.MColor((1.0, 0.7, 0.2, 1.0))
            else:
                self.color = OpenMaya.MColor((1.0, 0.2, 0.2, opacity))

        elif status == OpenMayaUI.M3dView.kActive:
            if self.getHighlightState(transformNode[0]) == True:
                self.color = OpenMaya.MColor((1.0, 0.35, 0.2, opacity))
            else:
                self.color = OpenMaya.MColor((1.0, 0.2, 0.2, opacity))

        elif status == OpenMayaUI.M3dView.kActiveAffected:
            self.color = OpenMaya.MColor((1.0, 0.2, 0.2, opacity))

        elif status == OpenMayaUI.M3dView.kDormant:
            self.color = OpenMaya.MColor((color[0], color[1], color[2], opacity))

        else:
            return
        # _______________________________
        
    def supportedDrawAPIs(self):
        return OpenMayaRender.MRenderer.kAllDevices
 
    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        self.interactiveRefresh = self.node.findPlug('interactiveRefresh', False).asBool()

        if OpenMayaAnim.MAnimControl.isPlaying() == True:
            return
            
        elif OpenMayaRender.MFrameContext.inUserInteraction() == True  and self.interactiveRefresh == False:
            return

        ## Retrieve data cache (create if does not exist)
        data = oldData
        if not isinstance(data, Mnt_locatorNode):
            data = Mnt_locatorNodeData()

        typeList        = ['Bone', 'Circle', 'Square', 'Skull', 'Pelvis', 'RibCage', 'Sphere', 'Disc', 'circle3D']
        statutColorList = ['Yellow' , 'Red', 'Blue']
           
        MSelList = OpenMaya.MSelectionList()
        MSelList.add(objPath)
        MObj = MSelList.getDependNode(0)

        size                    = OpenMaya.MFnDependencyNode(MObj).findPlug('size', False).asFloat()
        isAreaVisible           = OpenMaya.MFnDependencyNode(MObj).findPlug('area_Visibility', False).asBool()
        iconType                = OpenMaya.MFnDependencyNode(MObj).findPlug('iconType', False).asInt()
        iconMainAxis            = OpenMaya.MFnDependencyNode(MObj).findPlug('iconMainAxis', False).asInt()
        localPositionX          = OpenMaya.MFnDependencyNode(MObj).findPlug('localPositionX', False).asFloat()
        localPositionY          = OpenMaya.MFnDependencyNode(MObj).findPlug('localPositionY', False).asFloat()
        localPositionZ          = OpenMaya.MFnDependencyNode(MObj).findPlug('localPositionZ', False).asFloat()
        #color                   = OpenMaya.MFnDependencyNode(MObj).findPlug('color', False).asMDataHandle().asFloat3()
        #opacity                 = OpenMaya.MFnDependencyNode(MObj).findPlug('opacity', False).asFloat()
        label                   = OpenMaya.MFnDependencyNode(MObj).findPlug('label', False).asString()
        data.hierarchicalLink   = OpenMaya.MFnDependencyNode(MObj).findPlug('show_hierarchical_links', False).asBool()
        data.lineWidth          = OpenMaya.MFnDependencyNode(MObj).findPlug('line_width', False).asFloat()
        data.lineColor          = OpenMaya.MFnDependencyNode(MObj).findPlug('line_color', False).asMDataHandle().asFloat3()
        data.dottedLine         = OpenMaya.MFnDependencyNode(MObj).findPlug('use_dotted_line', False).asBool()
        
        MObjFn = OpenMaya.MFnDagNode(MObj)
        MObjParent          = MObjFn.parent(0)
        fnMObjParent        = OpenMaya.MFnDependencyNode(MObjParent)
        worldMatrixAttr     = fnMObjParent.attribute("worldMatrix")
        matrixPlug          = OpenMaya.MPlug(MObjParent, worldMatrixAttr)
        matrixPlug          = matrixPlug.elementByLogicalIndex(0)
        worldMatrixObject   = matrixPlug.asMObject()
        worldMatrixData     = OpenMaya.MFnMatrixData(worldMatrixObject)
        worldMatrix         = worldMatrixData.matrix()
        worldMatrixTransform    = OpenMaya.MTransformationMatrix(worldMatrix)
        worldScale = worldMatrixTransform.scale(4)

        data.pointArray  = OpenMaya.MPointArray()

        # Creates data for hierarchical line display.
        MSelList.clear()
        MFnDagTransNode      = OpenMaya.MFnDagNode(MObjParent)
        MObjParentNode       = MFnDagTransNode.parent(0)
        MFnDependencyParentNode = OpenMaya.MFnDependencyNode(MObjParentNode)

        if MFnDependencyParentNode.name() != 'world':
            try:
                MFnDagParent = OpenMaya.MFnDagNode(MObjParentNode)
                parentLocalMatrix   = MFnDagParent.transformationMatrix()    
                parentShapePath     = MFnDagParent.getPath().extendToShape()

                MSelList.add(parentShapePath)
                MObjParentShape = MSelList.getDependNode(0)
                MFnDependencyNodeParentShape = OpenMaya.MFnDependencyNode(MObjParentShape)

                '''if MFnDependencyNodeParentShape.typeName == 'mnt_locator':'''
                # Gets Local matrix
                localMatrix = MFnDagTransNode.transformationMatrix()
                # _________________
                # Gets Offset Matrix
                offsetMatrixAttr      = MFnDependencyParentNode.attribute('offsetParentMatrix')
                offsetMatrixPlug      = OpenMaya.MPlug(MObjParent, offsetMatrixAttr)
                offsetMatrixPlugObj   = offsetMatrixPlug.asMObject()
                offsetMatrixData      = OpenMaya.MFnMatrixData(offsetMatrixPlugObj)
                offsetMatrix          = offsetMatrixData.matrix()
                # ________________________
                # Calculates final matrix
                outputMatrix = localMatrix.__mul__(offsetMatrix).inverse()
                # _______________________
                 
                # Adds position to node data
                if data.dottedLine == False:
                    data.pointArray.append(OpenMaya.MPoint(0,0,0))
                    data.pointArray.append(OpenMaya.MPoint(outputMatrix[12], outputMatrix[13], outputMatrix[14]))
                else:
                    dotsNumber = OpenMaya.MFnDependencyNode(MObj).findPlug('dots_number', False).asInt()
                    for i in range(0, 2 * dotsNumber):
                        u = float(i)/(2 * dotsNumber)
                        point = OpenMaya.MPoint(u * outputMatrix[12], u * outputMatrix[13], u * outputMatrix[14])
                        data.pointArray.append(point)
                # __________________________
            except:
                pass
        # ___________________________________________

        # Manages billboards
        textureManager = MyTextureManager()
        status = OpenMayaUI.M3dView.displayStatus(objPath)

        if iconType < 6:
            if status == OpenMayaUI.M3dView.kLead:# or status == OpenMayaUI.M3dView.kActive:
                if self.getHighlightState(self.getTransformNode(self.MObj)[0]) == True:
                    texture = textureManager.acquireTexture(Mnt_locatorNode.iconFolder + 'mnt' + typeList[iconType] + 'Yellow.png')
                else:
                    texture = textureManager.acquireTexture(Mnt_locatorNode.iconFolder + 'mnt' + typeList[iconType] + 'Red.png')

            elif status == OpenMayaUI.M3dView.kActive:
                if self.getHighlightState(self.getTransformNode(self.MObj)[0]) == True:
                    texture = textureManager.acquireTexture(Mnt_locatorNode.iconFolder + 'mnt' + typeList[iconType] + 'Orange.png')
                else:
                    texture = textureManager.acquireTexture(Mnt_locatorNode.iconFolder + 'mnt' + typeList[iconType] + 'Red.png')

            elif status == OpenMayaUI.M3dView.kActiveAffected:
                texture = textureManager.acquireTexture(Mnt_locatorNode.iconFolder + 'mnt' + typeList[iconType] + 'Red.png')
                        
            elif status == OpenMayaUI.M3dView.kDormant:
                texture = textureManager.acquireTexture(Mnt_locatorNode.iconFolder + 'mnt' + typeList[iconType] + 'Blue.png')

            textureD        = texture.textureDescription()
        # __________________

        if iconType >= 6 or label != '':
            self.manageShapeColor()
        
        if iconType == 8:
            self.createCircle3DBuffer(size/2, (localPositionX, localPositionY, localPositionZ), iconMainAxis)

        view                = OpenMayaUI.M3dView.active3dView()
        objWorldMatrix      = objPath.exclusiveMatrix()
        cameraObject        = OpenMaya.MFnCamera(cameraPath)
        cameraWorldMatrix   = cameraPath.exclusiveMatrix()
        camObjvector        = OpenMaya.MVector( cameraWorldMatrix[12] - objWorldMatrix[12],\
                                                cameraWorldMatrix[13] - objWorldMatrix[13],\
                                                cameraWorldMatrix[14] - objWorldMatrix[14])   

        if isAreaVisible == False:
            areaOpacity = 0.0
        else:
            areaOpacity = 1.0

        viewWidth   = OpenMayaUI.M3dView.portWidth(view)
        viewHeight  = OpenMayaUI.M3dView.portHeight(view)

        localMatrix = OpenMaya.MMatrix(((1, 0, 0,0),\
                                        (0, 1, 0,0),\
                                        (0, 0, 1,0),\
                                        (localPositionX, localPositionY, localPositionZ, 1)))

        tmpMatrix = localMatrix.__mul__(objWorldMatrix)
        
        if cameraObject.isOrtho() == False:
            factor = (camObjvector.length() / cameraObject.focalLength) / (float(viewWidth) / float(viewHeight)) * 0.5
        else:
            factor = (cameraObject.orthoWidth) / (float(viewWidth) / float(viewHeight))/80

        if iconType < 6:
            data.screenPos      = view.worldToView(OpenMaya.MPoint(tmpMatrix[12], tmpMatrix[13], tmpMatrix[14]))
            data.screenSize     = 0.5 * textureD.fHeight * size
            data.texture        = texture
            data.worldSizeX     = (data.screenSize / 28) / worldScale[0] *  factor
            data.worldSizeY     = (data.screenSize / 28) / worldScale[1] *  factor
            data.worldSizeZ     = (data.screenSize / 28) / worldScale[2] *  factor
            data.areaOpacity    = areaOpacity
        
        # Manages 3D icons main axis
        data.upVector = OpenMaya.MVector(0, 0, 0)

        if iconMainAxis == 0:
            data.upVector = OpenMaya.MVector(1, 0, 0)
        elif iconMainAxis == 1:
            data.upVector = OpenMaya.MVector(0, 1, 0)
        else:
            data.upVector = OpenMaya.MVector(0, 0, 1)
        # __________________________

        data.size           = size
        data.iconType       = iconType
        data.localPosition  = OpenMaya.MPoint(localPositionX, localPositionY, localPositionZ)
        data.label          = label
        #data.interactiveRefresh = OpenMaya.MFnDependencyNode(MObj).findPlug('interactiveRefresh', False).asBool()
        
        return data

    def hasUIDrawables(self):
        return True
 
    def addUIDrawables(self, objPath, drawManager, frameContext, data): 
        locatordata = data
        status = OpenMayaUI.M3dView.displayStatus(objPath)

        if not isinstance(locatordata, Mnt_locatorNodeData):
            return

        elif OpenMayaAnim.MAnimControl.isPlaying() == True:
            return
            
        elif OpenMayaRender.MFrameContext.inUserInteraction() == True and self.interactiveRefresh == False:
            return

        drawManager.beginDrawable(OpenMayaRender.MUIDrawManager.kSelectable)

        if data.iconType < 6:
            color = OpenMaya.MColor((0.1, 0.2, 0.4, data.areaOpacity))
            drawManager.setColor(color)            
            drawManager.box(data.localPosition, OpenMaya.MVector(0, 1, 0), OpenMaya.MVector(1, 0, 0), data.worldSizeX, data.worldSizeY, data.worldSizeZ, True)

            drawManager.beginDrawInXray()
            drawManager.setTexture(data.texture)
            drawManager.rect2d(OpenMaya.MPoint(data.screenPos[0], data.screenPos[1]), OpenMaya.MVector(0, 1), data.screenSize, data.screenSize, True)
            drawManager.endDrawInXray()

            if data.label != '':
                drawManager.setColor(self.color)      
                drawManager.setFontSize(11)      
                drawManager.text2d(OpenMaya.MPoint(data.screenPos[0] + 16, data.screenPos[1]), data.label, alignment = OpenMayaRender.MUIDrawManager.kLeft)

        if data.iconType == 6:
            drawManager.setColor(self.color)        
            drawManager.sphere(data.localPosition, data.size, 16, 8, True)
            self.userNode.BBox.clear()

        if data.iconType == 7:
            drawManager.setColor(self.color)        
            drawManager.circle(data.localPosition, data.upVector, data.size, 32, True)
            # Bounding box update test
            self.userNode.BBox.clear()
            self.userNode.BBox.expand(OpenMaya.MPoint((-data.size, -data.size, -data.size)))
            self.userNode.BBox.expand(OpenMaya.MPoint((data.size, data.size, data.size)))

        if data.iconType == 8:
            drawManager.setColor(self.color)  
            drawManager.mesh(4, self.pointsArray, None, None, self.indicesArray, None)

        if data.hierarchicalLink == True:
            if data.pointArray.__len__() > 1:
                drawManager.beginDrawInXray()
                drawManager.setColor(OpenMaya.MColor((data.lineColor[0], data.lineColor[1], data.lineColor[2],1)))
                drawManager.setLineWidth(data.lineWidth)

                if data.dottedLine == False:
                    drawManager.line(data.pointArray[0], data.pointArray[1])
                else:
                    for i in range(0, data.pointArray.__len__(), 2):
                        drawManager.line(data.pointArray[i], data.pointArray[i + 1]) 
                        
                drawManager.endDrawInXray()
                           
        drawManager.endDrawable()
# ______________________________

# MPxSubSceneOverride implementation
class Mnt_locatorSubSceneOverride(OpenMayaRender.MPxSubSceneOverride):
    typeList        = ['Bone', 'Circle', 'Square', 'Skull', 'Pelvis', 'RibCage', 'Sphere', 'Disc', 'circle3D']
    #statutColorList = ['Yellow' , 'Red', 'Blue']

    class textureManagerClass(OpenMayaRender.MTextureManager):
        def __init__(self):
            return

    @staticmethod
    def creator(obj):
        return Mnt_locatorSubSceneOverride(obj)

    def __init__(self, obj):
        OpenMayaRender.MPxSubSceneOverride.__init__(self, obj)

        self.MObj               = obj
        self.node               = OpenMaya.MFnDependencyNode(obj)
        self.objPath            = OpenMaya.MDagPath.getAPathTo(obj)
        self.userNode           = self.node.userNode()
        self.size               = 1.0
        self.color              = None
        self.iconType           = None
        self.upVector           = OpenMaya.MVector()
        self.showHierarchyLinks = False
        self.positionsBuffer    = OpenMaya.MPointArray()
        self.indicesArray       = OpenMaya.MUintArray()
        self.linePointsArray    = OpenMaya.MPointArray()

    def getTransformNode(self, obj):
        # Method to help get shape parent transform.
        transformObj  = OpenMaya.MFnDagNode(obj).parent(0)
        transformPath = OpenMaya.MDagPath().getAPathTo(transformObj)

        return transformPath, transformObj
        # __________________________________________

    def getHighlightState(self, path):
        # Method to prevent selection childs to have the same color
        MSelectionList = OpenMaya.MGlobal.getActiveSelectionList()

        if MSelectionList.hasItem(path):
            return True

        return False
        # _________________________________________________________

    def manageShapeColor(self):
        # Manages color from shape state.
        status          = OpenMayaUI.M3dView.displayStatus(self.objPath)
        transformNode   = self.getTransformNode(self.MObj)
        color           = self.node.findPlug('color', False).asMDataHandle().asFloat3()
        opacity         = self.node.findPlug('opacity', False).asFloat()
        
        if status == OpenMayaUI.M3dView.kLead:
            if self.getHighlightState(transformNode[0]) == True:
                self.color = OpenMaya.MColor((1.0, 0.7, 0.2, 1.0))
            else:
                self.color = OpenMaya.MColor((1.0, 0.2, 0.2, opacity))

        elif status == OpenMayaUI.M3dView.kActive:
            if self.getHighlightState(transformNode[0]) == True:
                self.color = OpenMaya.MColor((1.0, 0.35, 0.2, opacity))
            else:
                self.color = OpenMaya.MColor((1.0, 0.2, 0.2, opacity))

        elif status == OpenMayaUI.M3dView.kActiveAffected:
            self.color = OpenMaya.MColor((1.0, 0.2, 0.2, opacity))

        elif status == OpenMayaUI.M3dView.kDormant:
            self.color = OpenMaya.MColor((color[0], color[1], color[2], opacity))

        else:
            return
        # _______________________________
        
    def requiresUpdate(self, container, frameContext):
        if self.node.findPlug('interactiveRefresh', False).asBool() == True:
            return True
        elif OpenMayaRender.MFrameContext.inUserInteraction() == True or OpenMayaAnim.MAnimControl.isPlaying() == True:
            self.linePointsArray.clear()
            return False
        else:
            return True

        #return True

    def update(self, container, frameContext):
        self.localPos           = self.node.findPlug('localPosition', False).asMDataHandle().asDouble3()
        self.size               = self.node.findPlug('size', False).asFloat()
        self.iconType           = self.node.findPlug('iconType', False).asInt()
        self.iconMainAxis       = self.node.findPlug('iconMainAxis', False).asInt()
        self.label              = self.node.findPlug('label', False).asString()
        self.xRayMode           = self.node.findPlug('xRayMode', False).asBool()
        self.showHierarchyLinks = self.node.findPlug('show_hierarchical_links', False).asBool()
        self.dottedLine         = self.node.findPlug('use_dotted_line', False).asBool()
        self.lineWidth          = self.node.findPlug('line_width', False).asInt()
        self.lineColor          = self.node.findPlug('line_color', False).asMDataHandle().asFloat3()

        if self.iconMainAxis == 0:
            self.upVector = OpenMaya.MVector(1, 0, 0)
        elif self.iconMainAxis == 1:
            self.upVector = OpenMaya.MVector(0, 1, 0)
        else:
            self.upVector = OpenMaya.MVector(0, 0, 1)

        # Manages hierarchy links display
        transformNode           = self.getTransformNode(self.MObj)
        parentTransformDagNode  = OpenMaya.MFnDagNode(transformNode[1])
        parentTransformNode     = parentTransformDagNode.parent(0)
        parentTransformNodeDnFn = OpenMaya.MFnDependencyNode(parentTransformNode)

        MSelList = OpenMaya.MSelectionList()
        MSelList.clear()
        self.linePointsArray.clear()

        if self.showHierarchyLinks == True:
            if parentTransformNodeDnFn.name() != 'world':
                try:
                    MFnDagParent = OpenMaya.MFnDagNode(parentTransformNode)
                    parentLocalMatrix   = MFnDagParent.transformationMatrix()    
                    parentShapePath     = MFnDagParent.getPath().extendToShape()

                    MSelList.add(parentShapePath)
                    MObjParentShape = MSelList.getDependNode(0)
                    MFnDependencyNodeParentShape = OpenMaya.MFnDependencyNode(MObjParentShape)

                    # Gets Local matrix
                    localMatrix = parentTransformDagNode.transformationMatrix()
                    # _________________

                    # Gets Offset Matrix
                    offsetMatrixAttr      = parentTransformNodeDnFn.attribute('offsetParentMatrix')
                    offsetMatrixPlug      = OpenMaya.MPlug(parentTransformNode, offsetMatrixAttr)
                    offsetMatrixPlugObj   = offsetMatrixPlug.asMObject()
                    offsetMatrixData      = OpenMaya.MFnMatrixData(offsetMatrixPlugObj)
                    offsetMatrix          = offsetMatrixData.matrix()
                    # ________________________

                    # Calculates final matrix
                    outputMatrix = localMatrix.__mul__(offsetMatrix).inverse()
                    # _______________________
                    
                    # Adds position to node data
                    if self.dottedLine == False:
                        self.linePointsArray.append(OpenMaya.MPoint(0,0,0))
                        self.linePointsArray.append(OpenMaya.MPoint(outputMatrix[12], outputMatrix[13], outputMatrix[14]))
                    else:
                        dotsNumber = OpenMaya.MFnDependencyNode(self.MObj).findPlug('dots_number', False).asInt()
                        for i in range(0, 2 * dotsNumber):
                            u = float(i)/(2 * dotsNumber)
                            point = OpenMaya.MPoint(u * outputMatrix[12], u * outputMatrix[13], u * outputMatrix[14])
                            self.linePointsArray.append(point)
                    # __________________________
                except:
                    pass
        else:
            pass
        # _______________________________

        if self.iconType < 6:
            # Gets camera path and world matrix
            activeView  = OpenMayaUI.M3dView.active3dView()        
            viewWidth   = OpenMayaUI.M3dView.portWidth(activeView)
            viewHeight  = OpenMayaUI.M3dView.portHeight(activeView)

            cameraPath = activeView.getCamera()
            cameraObj = OpenMaya.MFnCamera(cameraPath)
            cameraWorldMatrix = cameraPath.exclusiveMatrix()
            # _________________________________

            # Manages textures
            typeList        = ['Bone', 'Circle', 'Square', 'Skull', 'Pelvis', 'RibCage', 'Sphere', 'Disc', 'circle3D']
            status          = OpenMayaUI.M3dView.displayStatus(self.objPath)
            textureManager  = self.textureManagerClass()
            self.texture    = textureManager.acquireTexture(Mnt_locatorNode.iconFolder + 'mnt' + typeList[self.iconType] + 'Yellow.png')
            textureDesc     = self.texture.textureDescription()
            
            #if status == OpenMayaUI.M3dView.kLead or status == OpenMayaUI.M3dView.kActive:
            # ________________
           
            # Gets self world matrix
            objWorldMatrix = self.objPath.exclusiveMatrix()
            # ______________________

            # Extract world scale
            objWorldTransformMatrix = OpenMaya.MTransformationMatrix(objWorldMatrix)
            worldScale = objWorldTransformMatrix.scale(OpenMaya.MSpace.kWorld)
            # ___________________

            # Gets camera/self vector
            camObjvector    = OpenMaya.MVector( cameraWorldMatrix[12] - objWorldMatrix[12],\
                                                cameraWorldMatrix[13] - objWorldMatrix[13],\
                                                cameraWorldMatrix[14] - objWorldMatrix[14])
            # _______________________

            # Gets final shape world matrix
            localMatrix = OpenMaya.MMatrix(((1, 0, 0,0),\
                                            (0, 1, 0,0),\
                                            (0, 0, 1,0),\
                                            (self.localPos[0], self.localPos[1], self.localPos[2], 1)))

            shapeMatrix = localMatrix.__mul__(objWorldMatrix)
            # _____________________________

            # Create a factor to adjust size
            if cameraObj.isOrtho() == False:
                factor = (camObjvector.length() / cameraObj.focalLength) / (float(viewWidth) / float(viewHeight)) * 0.5
            else:
                factor = (cameraObj.orthoWidth) / (float(viewWidth) / float(viewHeight))/80
            # ______________________________

            # Gets locator position in screen space
            self.screenPos  = activeView.worldToView(OpenMaya.MPoint(shapeMatrix[12], shapeMatrix[13], shapeMatrix[14]))
            self.screenSize = 0.5 * textureDesc.fHeight * self.size
            self.worldSize     = [(self.screenSize / 28) / worldScale[0] *  factor,\
                                (self.screenSize / 28) / worldScale[1] *  factor,\
                                (self.screenSize / 28) / worldScale[2] *  factor]  
            # _____________________________________

        #if self.iconType >= 6 or self.label != '':
        if self.iconType >= 6:
            self.manageShapeColor()

        if self.iconType == 8:
            self.rebuildGeometryBuffers()
        else:
            self.clearGeometryBuffers()

        # Bounding box update test
        self.userNode.BBox.clear()
        self.userNode.BBox.expand(OpenMaya.MPoint((-self.size/2, -self.size/2, -self.size/2)))
        self.userNode.BBox.expand(OpenMaya.MPoint((self.size/2, self.size/2, self.size/2)))
        # ________________________

        return True

    def furtherUpdateRequired(self, frameContext):
        return True

    def manageRenderItems(self, container, frameContext, updateGeometry):
        return
    
    def rebuildGeometryBuffers(self):
        if self.iconType == 8:
            self.positionsBuffer = self.createCircle3DBuffer(self.size/2, self.localPos, self.iconMainAxis)
        return
    
    def clearGeometryBuffers(self):
        self.positionsBuffer.clear()
        self.indicesArray.clear()
        return
        
    def createCircle3DBuffer(self, inRadius, inLocalPosition, inDirection):
        self.clearGeometryBuffers()
        posOutArray = []
        posInArray  = []
        self.userNode.BBox.clear()
        outputBuffer = OpenMaya.MPointArray()

        for i in range(0,33):
            u = float(i)/32
            pi = math.pi

            if inDirection == 0:
                posOut =    OpenMaya.MPoint(0 + inLocalPosition[0], inRadius * math.cos(2* pi * u) + inLocalPosition[1], (inRadius * math.sin(2* pi * u) + inLocalPosition[2]))
                posIn =     OpenMaya.MPoint(0 + inLocalPosition[0], 0.85 * inRadius * math.cos(2* pi * u) + inLocalPosition[1], 0.85 * inRadius * math.sin(2* pi * u)+ inLocalPosition[2])    
            elif inDirection == 1:
                posOut =    OpenMaya.MPoint(inRadius * math.cos(2* pi * u) + inLocalPosition[0], 0 + inLocalPosition[1], (inRadius * math.sin(2* pi * u) + inLocalPosition[2]))
                posIn =     OpenMaya.MPoint(0.85 * inRadius * math.cos(2* pi * u) + inLocalPosition[0], 0 + inLocalPosition[1], 0.85 * inRadius * math.sin(2* pi * u)+ inLocalPosition[2])
            else:
                posOut =    OpenMaya.MPoint(inRadius * math.cos(2* pi * u) + inLocalPosition[0], (inRadius * math.sin(2* pi * u) + inLocalPosition[1]), 0 + inLocalPosition[2])
                posIn =     OpenMaya.MPoint(0.85 * inRadius * math.cos(2* pi * u) + inLocalPosition[0], 0.85 * inRadius * math.sin(2* pi * u)+ inLocalPosition[1], 0 + inLocalPosition[2])

            posOutArray.append(posOut)
            posInArray.append(posIn)
            
        for i in range(0, 32):
            outputBuffer.append(posOutArray[i])
            outputBuffer.append(posOutArray[i + 1])
            outputBuffer.append(posInArray[i + 1])
            outputBuffer.append(posInArray[i + 1])
            outputBuffer.append(posInArray[i])
            outputBuffer.append(posOutArray[i])

        return outputBuffer
    
    def hasUIDrawables(self):
        return True

    def areUIDrawablesDirty(self):
        return True

    def addUIDrawables(self, drawManager, frameContext):

        if OpenMayaAnim.MAnimControl.isPlaying() == True:
            return
        elif OpenMayaRender.MFrameContext.inUserInteraction() == True and self.userNode.isInteractive == False:
            return
        else:
            pass
        
        drawManager.beginDrawable(OpenMayaRender.MUIDrawManager.kSelectable)
        
        if self.xRayMode == True:
            drawManager.beginDrawInXray()
        else:
            pass

        if self.iconType < 6:
            color = OpenMaya.MColor((0.1, 0.2, 0.4, 0.1))
            drawManager.setColor(color)            
            drawManager.box(OpenMaya.MPoint(self.localPos), OpenMaya.MVector(0, 1, 0), OpenMaya.MVector(1, 0, 0), self.worldSize[0], self.worldSize[1], self.worldSize[2], True)

            drawManager.beginDrawInXray()
            drawManager.setTexture(self.texture)
            drawManager.rect2d(OpenMaya.MPoint((self.screenPos[0], self.screenPos[1])), OpenMaya.MVector(0.0, 1.0), self.screenSize, self.screenSize, True)
            drawManager.endDrawInXray()

        if self.iconType == 6:
            drawManager.setColor(OpenMaya.MColor(self.color))   
            drawManager.sphere(OpenMaya.MPoint(self.localPos), self.size/2, 16, 8, True)

        elif self.iconType == 7:
            drawManager.setColor(OpenMaya.MColor(self.color))   
            drawManager.circle(OpenMaya.MPoint(self.localPos), OpenMaya.MVector(self.upVector), self.size/2, 32, True)
            
        elif self.iconType == 8:
            drawManager.setColor(OpenMaya.MColor(self.color))   
            drawManager.mesh(OpenMayaRender.MUIDrawManager.kTriangles, self.positionsBuffer, None, None, self.indicesArray, None)

        else:
            pass
        
        if self.xRayMode == True:
            drawManager.endDrawInXray()
        else:
            pass

        drawManager.endDrawable()

        drawManager.beginDrawable(OpenMayaRender.MUIDrawManager.kNonSelectable)

        if self.label != '':
            drawManager.setColor(self.color)      
            drawManager.setFontSize(11)      
            drawManager.text2d(OpenMaya.MPoint(self.screenPos[0] + 16, self.screenPos[1]), self.label, alignment = OpenMayaRender.MUIDrawManager.kLeft)

        if self.showHierarchyLinks == True:
            if self.linePointsArray.__len__() > 1:
                drawManager.beginDrawInXray()
                drawManager.setColor(OpenMaya.MColor((self.lineColor[0], self.lineColor[1], self.lineColor[2],1)))#
                drawManager.setLineWidth(self.lineWidth)

                if self.dottedLine == False:
                    drawManager.line(self.linePointsArray[0], self.linePointsArray[1])
                else:
                    for i in range(0, self.linePointsArray.__len__(), 2):
                        drawManager.line(self.linePointsArray[i], self.linePointsArray[i + 1]) 
                        
                drawManager.endDrawInXray()
        drawManager.endDrawable()

        return
# __________________________________
# _______________________________________________________________

class Mnt_characterInfoNode(OpenMayaUI.MPxLocatorNode):
    kPluginNodeName         = 'mnt_characterInfo'
    id                      = OpenMaya.MTypeId(0xDAE8)
    drawDbClassification    = "drawdb/geometry/Mnt_characterInfoNode"
    drawRegistrantId        = "Mnt_CharacterInfoPlugin"
    iconFolder              = cmds.internalVar(userScriptDir = True) + 'cr_Tools/cr_Tools_Data/icons/'

    def __init__(self):
        OpenMayaUI.MPxLocatorNode.__init__(self)

    @staticmethod
    def creator():
        return Mnt_characterInfoNode()
    
    @staticmethod
    def initialize():
        stringAttrFn    = OpenMaya.MFnTypedAttribute()
        numAttrFn       = OpenMaya.MFnNumericAttribute()

        Mnt_characterInfoNode.characterNameAttr = stringAttrFn.create('characterName', 'characterName', OpenMaya.MFnData.kString)
        stringAttrFn.writable = True
        stringAttrFn.readable = True
        Mnt_characterInfoNode.addAttribute(Mnt_characterInfoNode.characterNameAttr)

        Mnt_characterInfoNode.leftInfosAttr = stringAttrFn.create('leftInfos', 'leftInfos', OpenMaya.MFnData.kString)
        stringAttrFn.writable = True
        stringAttrFn.readable = True
        stringAttrFn.hidden   = True
        Mnt_characterInfoNode.addAttribute(Mnt_characterInfoNode.leftInfosAttr)   

        Mnt_characterInfoNode.rightInfosAttr = stringAttrFn.create('rightInfos', 'rightInfos', OpenMaya.MFnData.kString)
        stringAttrFn.writable = True
        stringAttrFn.readable = True
        stringAttrFn.hidden   = True
        Mnt_characterInfoNode.addAttribute(Mnt_characterInfoNode.rightInfosAttr)

        Mnt_characterInfoNode.spaceSwitchInfosAttr = stringAttrFn.create('spaceSwitchInfos', 'spaceSwitchInfos', OpenMaya.MFnData.kString)
        stringAttrFn.writable = True
        stringAttrFn.readable = True
        stringAttrFn.hidden   = True
        Mnt_characterInfoNode.addAttribute(Mnt_characterInfoNode.spaceSwitchInfosAttr)

        Mnt_characterInfoNode.marginAttr = numAttrFn.create('margin', 'margin', OpenMaya.MFnNumericData.kInt, 40)
        numAttrFn.writable = True
        numAttrFn.readable = True
        numAttrFn.setMin(40)
        numAttrFn.setMax(300)
        Mnt_characterInfoNode.addAttribute(Mnt_characterInfoNode.marginAttr)

        Mnt_characterInfoNode.fontSizeAttr  = numAttrFn.create('fontSize', 'fontSize', OpenMaya.MFnNumericData.kInt, 16)
        numAttrFn.writable = True
        numAttrFn.readable = True
        numAttrFn.setMin(9)
        numAttrFn.setMax(24)
        Mnt_characterInfoNode.addAttribute(Mnt_characterInfoNode.fontSizeAttr)

        Mnt_characterInfoNode.mnt_characterVisibilityStateAttr = numAttrFn.create('controllersVisibility', 'controllersVisibility', OpenMaya.MFnNumericData.kBoolean)
        numAttrFn.writable = True
        numAttrFn.readable = True
        numAttrFn.hidden    = True
        Mnt_characterInfoNode.addAttribute(Mnt_characterInfoNode.mnt_characterVisibilityStateAttr)

        Mnt_characterInfoNode.poseScopeVisibilityStateAttr = numAttrFn.create('poseScopeNodesVisibility', 'poseScopeNodesVisibility', OpenMaya.MFnNumericData.kBoolean)
        numAttrFn.writable = True
        numAttrFn.readable = True
        numAttrFn.hidden    = True
        Mnt_characterInfoNode.addAttribute(Mnt_characterInfoNode.poseScopeVisibilityStateAttr)

        Mnt_characterInfoNode.mnt_characterInfosVisibilityState = numAttrFn.create('characterInfosVisibility', 'characterInfosVisibility', OpenMaya.MFnNumericData.kBoolean)
        numAttrFn.writable = True
        numAttrFn.readable = True
        Mnt_characterInfoNode.addAttribute(Mnt_characterInfoNode.mnt_characterInfosVisibilityState)

    def compute(self, plug, data): 
        return

    def postConstructor(self):
        charInfoNodeObj = self.thisMObject()
        print(self.name())
        return True

class Mnt_characterInfoNodeData(OpenMaya.MUserData):
    def __init__(self):
        OpenMaya.MUserData.__init__(self, False)

class Mnt_characterInfoNodeDrawOverride(OpenMayaRender.MPxDrawOverride):
    @staticmethod
    def creator(obj):
        return Mnt_characterInfoNodeDrawOverride(obj)
    
    @staticmethod
    def draw(context, data):
        return
    
    def __init__(self, obj):
        OpenMayaRender.MPxDrawOverride.__init__(self, obj, Mnt_characterInfoNodeDrawOverride.draw)

    def supportedDrawAPIs(self):
        return OpenMayaRender.MRenderer.kAllDevices

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        # Retrieve data cache (create if does not exist)
        data = oldData
        if not isinstance(data, Mnt_characterInfoNode):
            data = Mnt_characterInfoNodeData()
        # ______________________________________________
        view        = OpenMayaUI.M3dView.active3dView()
        portWidth   = view.portWidth()
        portHeight  = view.portHeight()

        MSelectionList = OpenMaya.MSelectionList()
        MSelectionList.add(objPath)
        MObj    = MSelectionList.getDependNode(0)
        MObjFn  = OpenMaya.MFnDependencyNode(MObj)

        data.mnt_characterInfosState            = MObjFn.findPlug('controllersVisibility', False).asBool()
        data.mnt_characterInfosVisibilityState  = MObjFn.findPlug('characterInfosVisibility', False).asBool()
        data.poseScopeVisibilityState           = MObjFn.findPlug('poseScopeNodesVisibility', False).asBool()
        margin                                  = MObjFn.findPlug('margin', False).asInt()
        data.fontSize                           = MObjFn.findPlug('fontSize', False).asInt()
        data.characterName                      = MObjFn.findPlug('characterName', False).asString()

        characterFacePicture    = cmds.workspace(q = True, active = True) + '/sourceimages/thumbnails/thumbnail_' + data.characterName + '.png'
        data.characterNamePos   = OpenMaya.MPoint(portWidth * margin / portHeight, portHeight - margin)
        data.color              = OpenMaya.MColor((1.0, 0.7, 0.2, 0.5))
        textureManager          = MyTextureManager()

        try:
            data.charactertexture   = textureManager.acquireTexture(characterFacePicture)
        except:
            data.charactertexture   = textureManager.acquireTexture(Mnt_characterInfoNode.iconFolder + 'icon_defaultFace_sRGB.png')
           
        leftInfos   = MObjFn.findPlug('leftInfos', False).asString()
        rightInfos  = MObjFn.findPlug('rightInfos', False).asString()

        data.leftInfos = leftInfos.split(';')
        data.rightInfos = rightInfos.split(';')

        margin          = MObjFn.findPlug('margin', False).asInt()
        data.fontSize   = MObjFn.findPlug('fontSize', False).asInt()

        data.leftInfosPos           = OpenMaya.MPoint(portWidth * margin / portHeight, portHeight/2)
        data.rightInfosPos          = OpenMaya.MPoint(portWidth - portWidth * margin / portHeight, portHeight/2)
        data.spaceSwitchInfos       = MObjFn.findPlug('spaceSwitchInfos', False).asString().split(';')
        data.spaceSwitchInfosPos    = OpenMaya.MPoint(portWidth * margin / portHeight, 3 * portHeight / 4)



        return data
    
    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        characterData = data
        
        if not isinstance(characterData, Mnt_characterInfoNodeData) or OpenMayaAnim.MAnimControl.isPlaying() == True:
            return

        drawManager.beginDrawable(OpenMayaRender.MUIDrawManager.kSelectable)
        drawManager.setFontWeight(87)
        drawManager.setFontSize(data.fontSize * 1)
        drawManager.setColor(OpenMaya.MColor((1.0, 0.75, 0.333, 0.5)))
        drawManager.text2d(OpenMaya.MPoint(data.rightInfosPos[0] - 50, data.characterNamePos[1]), 'Pose Scopes Visibility :', OpenMayaRender.MUIDrawManager.kRight, None, None, False)
        drawManager.setColor(OpenMaya.MColor((0.5, 0.5, 0.5, 0.5)))      
        drawManager.text2d(OpenMaya.MPoint(data.rightInfosPos[0] - 50, data.characterNamePos[1] -  data.fontSize * 2), str(data.poseScopeVisibilityState), OpenMayaRender.MUIDrawManager.kRight, None, None, False)
        #drawManager.setTexture(None)
        #drawManager.setColor(OpenMaya.MColor((0.5, 0.5, 0.5, 0.01)))
        #drawManager.rect2d(OpenMaya.MPoint(data.rightInfosPos[0] - 13 * data.fontSize, data.characterNamePos[1]), OpenMaya.MVector(0,1), 14 * data.fontSize, 4 * data.fontSize, True)
        drawManager.endDrawable()

        if data.mnt_characterInfosVisibilityState == False:
            return

        drawManager.beginDrawable(OpenMayaRender.MUIDrawManager.kSelectable)
        drawManager.setColor(data.color)        
        drawManager.setFontWeight(87)
        drawManager.setFontSize(data.fontSize * 1)
        drawManager.text2d(data.characterNamePos, 'Character : ' + data.characterName, OpenMayaRender.MUIDrawManager.kLeft, None, None, False)
        drawManager.setTexture(data.charactertexture)
        drawManager.rect2d(OpenMaya.MPoint(data.characterNamePos[0] + 64, data.characterNamePos[1] - 50), OpenMaya.MVector(0,1), 64, 40, True)
        drawManager.setFontSize(data.fontSize)

        for i in range(len(data.leftInfos)):
            if i == 0:
                drawManager.setFontWeight(87)
            else:
                drawManager.setFontWeight(50)

            if i ==0:
                drawManager.setColor(OpenMaya.MColor((0.5, 0.5, 0.5, 0.5)))
            elif ' IK ' in data.leftInfos[i]:
                drawManager.setColor(OpenMaya.MColor((1.0, 0.25, 0.5, 0.5)))
            else:
                drawManager.setColor(OpenMaya.MColor((1.0, 0.75, 0.5, 0.5)))

            drawManager.text2d(OpenMaya.MPoint(data.leftInfosPos[0], data.leftInfosPos[1] - 2 * i * data.fontSize), data.leftInfos[i], OpenMayaRender.MUIDrawManager.kLeft, None, None, False)

        for i in range(len(data.rightInfos)):
            if i == 0:
                drawManager.setFontWeight(87)
            else:
                drawManager.setFontWeight(50)

            if i ==0:
                drawManager.setColor(OpenMaya.MColor((0.5, 0.5, 0.5, 0.5)))
            elif ' IK ' in data.rightInfos[i]:
                drawManager.setColor(OpenMaya.MColor((1.0, 0.25, 0.5, 0.5)))
            else:
                drawManager.setColor(OpenMaya.MColor((1.0, 0.75, 0.5, 0.5)))

            drawManager.text2d(OpenMaya.MPoint(data.rightInfosPos[0], data.rightInfosPos[1] - 2 * i  * data.fontSize), data.rightInfos[i], OpenMayaRender.MUIDrawManager.kRight, None, None, False)

        for i in range(len(data.spaceSwitchInfos)):
            if i == 0:
                drawManager.setFontWeight(87)
                drawManager.setColor(OpenMaya.MColor((0.5, 0.5, 0.5, 0.5)))
            else:
                drawManager.setFontWeight(50)  
                drawManager.setColor(OpenMaya.MColor((1.0, 0.75, 0.5, 0.5)))

            drawManager.text2d(OpenMaya.MPoint(data.spaceSwitchInfosPos[0], data.spaceSwitchInfosPos[1] - 2*i * data.fontSize), data.spaceSwitchInfos[i], OpenMayaRender.MUIDrawManager.kLeft, None, None, False)
                     
        drawManager.setTexture(None)
        drawManager.setColor(OpenMaya.MColor((0.5, 0.5, 0.5, 0.01)))

        drawManager.rect2d(OpenMaya.MPoint(data.leftInfosPos[0] + 95, data.leftInfosPos[1] - (len(data.leftInfos) - 2) * data.fontSize), OpenMaya.MVector(0,1), 110, data.fontSize * len(data.leftInfos), True)
        drawManager.rect2d(OpenMaya.MPoint(data.rightInfosPos[0] - 95, data.rightInfosPos[1] - (len(data.rightInfos) - 2) * data.fontSize), OpenMaya.MVector(0,1), 110, data.fontSize * len(data.rightInfos), True)
        drawManager.rect2d(OpenMaya.MPoint(data.spaceSwitchInfosPos[0] + 120, data.spaceSwitchInfosPos[1] - (len(data.spaceSwitchInfos) - 2) * data.fontSize), OpenMaya.MVector(0,1), 130, data.fontSize * len(data.spaceSwitchInfos), True)

# ____________________________________________________

def initializePlugin(obj):
    plugin = OpenMaya.MFnPlugin(obj, "Florian Delarque", "2.0", "Any")
 
    try:
        plugin.registerNode(Mnt_locatorNode.kPluginNodeName, Mnt_locatorNode.id, Mnt_locatorNode.creator, Mnt_locatorNode.initialize, OpenMaya.MPxNode.kLocatorNode, Mnt_locatorNode.drawDbClassification)
        plugin.registerNode(Mnt_characterInfoNode.kPluginNodeName, Mnt_characterInfoNode.id, Mnt_characterInfoNode.creator, Mnt_characterInfoNode.initialize, OpenMaya.MPxNode.kLocatorNode, Mnt_characterInfoNode.drawDbClassification)
    except:
        OpenMaya.MGlobal.displayError("Failed to register node\n")
        raise
 
    try:
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(Mnt_locatorNode.drawDbClassification, Mnt_locatorNode.drawRegistrantId, Mnt_locatorNodeDrawOverride.creator)
        #OpenMayaRender.MDrawRegistry.registerSubSceneOverrideCreator(Mnt_locatorNode.drawDbClassification, Mnt_locatorNode.drawRegistrantId, Mnt_locatorSubSceneOverride.creator)
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(Mnt_characterInfoNode.drawDbClassification, Mnt_characterInfoNode.drawRegistrantId, Mnt_characterInfoNodeDrawOverride.creator)
    except:
        OpenMaya.MGlobal.displayError("Failed to register override\n")
        raise
 
def uninitializePlugin(obj):
    plugin = OpenMaya.MFnPlugin(obj)
 
    try:
        plugin.deregisterNode(Mnt_locatorNode.id)
        plugin.deregisterNode(Mnt_characterInfoNode.id)
    except:
        OpenMaya.MGlobal.displayError("Failed to deregister node\n")
        pass
 
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(Mnt_locatorNode.drawDbClassification, Mnt_locatorNode.drawRegistrantId)
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(Mnt_characterInfoNode.drawDbClassification, Mnt_characterInfoNode.drawRegistrantId)
    except:
        OpenMaya.MGlobal.displayError("Failed to deregister override\n")
        pass