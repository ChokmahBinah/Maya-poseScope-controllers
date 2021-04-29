import sys
import math
import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.api.OpenMayaAnim as OpenMayaAnim
import maya.api.OpenMayaRender as OpenMayaRender
import maya.plugin.evaluator.CacheEvaluatorManager #To help use cached playback

maya_useNewAPI = True

'''def maya_useNewAPI():
 """
 The presence of this function tells Maya that the plugin produces, and
 expects to be passed, objects created using the Maya Python API 2.0.
 """
 pass'''

class MyTextureManager(OpenMayaRender.MTextureManager):#A Faire quand une classe ne peux pas etre instanciee (est une classe abstraite), on doit cree une classe derivee
    def __init__(self):
        pass

class MntLocatorNode(OpenMayaUI.MPxLocatorNode):
    kPluginNodeName         = 'mntLocator' #Name of the node.
    id                      = OpenMaya.MTypeId( 0xDAE2 ) # A unique ID associated to this node type.
    drawDbClassification    = "drawdb/geometry/MntLocatorNode"
    drawRegistrantId        = "MntLocatorNodePlugin"

    iconFolder              = cmds.getModulePath(moduleName = 'mnt_framework') + '/icons/mntLocators/'
    iconTypeAttribute       = OpenMaya.MObject()
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
    
    def __init__(self):
        OpenMayaUI.MPxLocatorNode.__init__(self)

    @staticmethod
    def creator():
        return MntLocatorNode()
 
    @staticmethod
    def initialize():
        ''' Defines the input and output attributes as static variables in our plug-in class. '''

        # input attribute.
        numericAttributeFn = OpenMaya.MFnNumericAttribute()
        MntLocatorNode.sizeAttribute = numericAttributeFn.create('size', 'size', OpenMaya.MFnNumericData.kFloat, 1)
        numericAttributeFn.writable =  True 
        numericAttributeFn.keyable = False
        numericAttributeFn.storable =  True 
        numericAttributeFn.hidden   = False
        numericAttributeFn.channelBox = True
        numericAttributeFn.setMin( 0.01 )
        numericAttributeFn.setMax( 100.0 )
        MntLocatorNode.addAttribute(MntLocatorNode.sizeAttribute)

        boolAttributeFn = OpenMaya.MFnNumericAttribute()
        MntLocatorNode.areaVisibility = boolAttributeFn.create('area_Visibility', 'area_Visibility', OpenMaya.MFnNumericData.kBoolean, False)
        boolAttributeFn.writable =  True 
        boolAttributeFn.keyable = False
        boolAttributeFn.storable =  True 
        boolAttributeFn.hidden   = False
        boolAttributeFn.channelBox = True
        MntLocatorNode.addAttribute(MntLocatorNode.areaVisibility)

        colorAttributeFn = OpenMaya.MFnNumericAttribute()
        MntLocatorNode.colorAttribute = colorAttributeFn.createColor('color', 'color')
        colorAttributeFn.writable     = True
        colorAttributeFn.keyable      = False
        colorAttributeFn.channelBox   = True
        colorAttributeFn.storable     = True
        colorAttributeFn.hidden       = False
        MntLocatorNode.addAttribute(MntLocatorNode.colorAttribute)

        opacityAttributeFn = OpenMaya.MFnNumericAttribute()
        MntLocatorNode.opacityAttribute = opacityAttributeFn.create('opacity', 'opacity', OpenMaya.MFnNumericData.kFloat, 1.0)
        opacityAttributeFn.writable     = True
        opacityAttributeFn.keyable      = False
        opacityAttributeFn.channelBox   = True
        opacityAttributeFn.storable     = True
        opacityAttributeFn.hidden       = False
        opacityAttributeFn.setMin(0.0)
        opacityAttributeFn.setMax(1.0)
        
        MntLocatorNode.addAttribute(MntLocatorNode.opacityAttribute)

        enumAttr = OpenMaya.MFnEnumAttribute()
        MntLocatorNode.iconTypeAttribute = enumAttr.create('iconType', 'it', 1)
        enumAttr.addField('bone', 0)
        enumAttr.addField('circle', 1)
        enumAttr.addField('square', 2)
        enumAttr.addField('skull', 3)
        enumAttr.addField('pelvis', 4)
        enumAttr.addField('ribcage', 5)
        enumAttr.addField('sphere', 6)
        enumAttr.addField('disc', 7)
        enumAttr.addField('circle3D', 8)
        enumAttr.hidden     = False
        enumAttr.channelBox = True
        MntLocatorNode.addAttribute(MntLocatorNode.iconTypeAttribute)

        showHierarchicalLinksFn = OpenMaya.MFnNumericAttribute()
        MntLocatorNode.showHierarchicalLinks = showHierarchicalLinksFn.create('show_hierarchical_links', 'show_hierarchical_links', OpenMaya.MFnNumericData.kBoolean, False)
        boolAttributeFn.writable =  True 
        boolAttributeFn.keyable = False
        boolAttributeFn.storable =  True 
        boolAttributeFn.hidden   = False
        boolAttributeFn.channelBox = True
        MntLocatorNode.addAttribute(MntLocatorNode.showHierarchicalLinks)

        dottedLineFn = OpenMaya.MFnNumericAttribute()
        MntLocatorNode.dottedLine = dottedLineFn.create('use_dotted_line', 'use_dotted_line', OpenMaya.MFnNumericData.kBoolean, False)
        dottedLineFn.writable   = True 
        dottedLineFn.keyable    = False
        dottedLineFn.storable   = True
        dottedLineFn.hidden     = False
        dottedLineFn.channelBox = True
        MntLocatorNode.addAttribute(MntLocatorNode.dottedLine)

        dotsNumberFn = OpenMaya.MFnNumericAttribute()
        MntLocatorNode.dotsNumber = dotsNumberFn.create('dots_number', 'dots_number', OpenMaya.MFnNumericData.kInt, 5)
        dotsNumberFn.writable   = True 
        dotsNumberFn.keyable    = False
        dotsNumberFn.storable   = True
        dotsNumberFn.hidden     = False
        dotsNumberFn.channelBox = True
        MntLocatorNode.addAttribute(MntLocatorNode.dotsNumber)

        lineWidthFn = OpenMaya.MFnNumericAttribute()
        MntLocatorNode.lineWidth = lineWidthFn.create('line_width', 'line_width', OpenMaya.MFnNumericData.kFloat, 4)
        lineWidthFn.writable    = True
        lineWidthFn.keyable     = True
        lineWidthFn.storable    = True
        lineWidthFn.hidden      = False
        lineWidthFn.channelBox  = True
        MntLocatorNode.addAttribute(MntLocatorNode.lineWidth)

        lineColorFn = OpenMaya.MFnNumericAttribute()
        MntLocatorNode.lineColor = lineColorFn.createColor('line_color', 'line_color')
        lineColorFn.writable     = True
        lineColorFn.keyable      = False
        lineColorFn.channelBox   = True
        lineColorFn.storable     = True
        lineColorFn.hidden       = False
        MntLocatorNode.addAttribute(MntLocatorNode.lineColor)

        stringAttrFn  = OpenMaya.MFnTypedAttribute()
        MntLocatorNode.labelAttribute = stringAttrFn.create('label', 'label', OpenMaya.MFnData.kString)
        stringAttrFn.writable = True
        stringAttrFn.readable = True
        MntLocatorNode.addAttribute(MntLocatorNode.labelAttribute)

    def compute(self, plug, data):    
        return None

    def postConstructor(self):
        return None
        
class MntLocatorNodeData(OpenMaya.MUserData):
    def __init__(self):
        OpenMaya.MUserData.__init__(self, False) ## don't delete after draw
 
class MntLocatorNodeDrawOverride(OpenMayaRender.MPxDrawOverride):
    @staticmethod
    def creator(obj):
        return MntLocatorNodeDrawOverride(obj)
 
    @staticmethod
    def draw(context, data):
        return
 
    def __init__(self, obj):
        OpenMayaRender.MPxDrawOverride.__init__(self, obj, MntLocatorNodeDrawOverride.draw)

        self.pointsArray = OpenMaya.MPointArray()
        self.indicesArray = OpenMaya.MUintArray()
 
    def createCirlce3DBuffer(self, inRadius, inLocalPosition, inDirection):
        self.clearBuffers()
        posOutArray = []
        posInArray  = []

        for i in range(0,33):
            u = float(i)/32
            pi = math.pi
            posOut =    OpenMaya.MPoint(inRadius * math.cos(2* pi * u) + inLocalPosition[0], 0 + inLocalPosition[1], (inRadius * math.sin(2* pi * u) + inLocalPosition[2]))
            posIn =     OpenMaya.MPoint(0.85 * inRadius * math.cos(2* pi * u) + inLocalPosition[0], 0 + inLocalPosition[1], 0.85 * inRadius * math.sin(2* pi * u)+ inLocalPosition[2])
        
            posOutArray.append(posOut)
            posInArray.append(posIn)
            
        for i in range(0, 32):
            self.pointsArray.append(posOutArray[i])
            self.pointsArray.append(posOutArray[i + 1])
            self.pointsArray.append(posInArray[i + 1])
            self.pointsArray.append(posInArray[i + 1])
            self.pointsArray.append(posInArray[i])
            self.pointsArray.append(posOutArray[i])

        return

    def clearBuffers(self):
        self.pointsArray.clear()
        self.indicesArray.clear()
        
    def supportedDrawAPIs(self):
        return OpenMayaRender.MRenderer.kAllDevices
 
    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        ## Retrieve data cache (create if does not exist)
        data = oldData
        if not isinstance(data, MntLocatorNode):
            data = MntLocatorNodeData()

        typeList        = ['Bone', 'Circle', 'Square', 'Skull', 'Pelvis', 'RibCage', 'Sphere', 'Disc', 'circle3D']
        statutColorList = ['Yellow' , 'Red', 'Blue']
           
        MSelList = OpenMaya.MSelectionList()
        MSelList.add(objPath)
        MObj = MSelList.getDependNode(0)

        size                    = OpenMaya.MFnDependencyNode(MObj).findPlug('size', False).asFloat()
        isAreaVisible           = OpenMaya.MFnDependencyNode(MObj).findPlug('area_Visibility', False).asBool()
        iconType                = OpenMaya.MFnDependencyNode(MObj).findPlug('iconType', False).asInt()
        localPositionX          = OpenMaya.MFnDependencyNode(MObj).findPlug('localPositionX', False).asFloat()
        localPositionY          = OpenMaya.MFnDependencyNode(MObj).findPlug('localPositionY', False).asFloat()
        localPositionZ          = OpenMaya.MFnDependencyNode(MObj).findPlug('localPositionZ', False).asFloat()
        color                   = OpenMaya.MFnDependencyNode(MObj).findPlug('color', False).asMDataHandle().asFloat3()
        opacity                 = OpenMaya.MFnDependencyNode(MObj).findPlug('opacity', False).asFloat()
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

        # Find MObj transform children world matrices.
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

                if MFnDependencyNodeParentShape.typeName == 'mntLocator':
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

        textureManager = MyTextureManager()
        status = OpenMayaUI.M3dView.displayStatus(objPath)

        if iconType < 6:
            if status == OpenMayaUI.M3dView.kLead or status == OpenMayaUI.M3dView.kActive:
                if self.getHighlightState(fnMObjParent.name()) == True:
                    texture = textureManager.acquireTexture(MntLocatorNode.iconFolder + 'mnt' + typeList[iconType] + 'Yellow.png')
                else:
                    texture = textureManager.acquireTexture(MntLocatorNode.iconFolder + 'mnt' + typeList[iconType] + 'Red.png')

            if status == OpenMayaUI.M3dView.kActiveAffected:
                texture = textureManager.acquireTexture(MntLocatorNode.iconFolder + 'mnt' + typeList[iconType] + 'Green.png')
                        
            if status == OpenMayaUI.M3dView.kDormant:
                texture = textureManager.acquireTexture(MntLocatorNode.iconFolder + 'mnt' + typeList[iconType] + 'Blue.png')

            textureD        = texture.textureDescription()

        if iconType >= 6 or label != '':
            if status == OpenMayaUI.M3dView.kLead or status == OpenMayaUI.M3dView.kActive:
                data.color = OpenMaya.MColor((1.0, 0.7, 0.2, opacity + 0.2))

            if status == OpenMayaUI.M3dView.kActiveAffected:
                data.color = OpenMaya.MColor((1.0, 0.2, 0.2, opacity + 0.1))

            if status == OpenMayaUI.M3dView.kDormant:
                data.color = OpenMaya.MColor((color[0], color[1], color[2], opacity))
        
        if iconType == 8:
            self.createCirlce3DBuffer(size/2, (localPositionX, localPositionY, localPositionZ),'TEST')

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

            #point = OpenMaya.MPoint()
            #direction = OpenMaya.MVector()
            #view.viewToWorld(int(data.screenSize), int(data.screenSize), point, direction)
            #print(point)
            #print(direction)
            #data.worldSizeX     = point[0]
            #data.worldSizeY     = point[1]
            #data.worldSizeZ     = point[2]
            
            data.areaOpacity    = areaOpacity
        
        data.size           = size
        data.iconType       = iconType
        data.localPosition  = OpenMaya.MPoint(localPositionX, localPositionY, localPositionZ)
        data.label          = label
        return data

    # Method to prevent selection childs to have the same color
    def getHighlightState(self, transformPath):
        MSelectionList = OpenMaya.MGlobal.getActiveSelectionList()
        MSelectionStrings = MSelectionList.getSelectionStrings()

        if transformPath in MSelectionStrings:
            return True

        return False
    # _________________________________________________________

    def hasUIDrawables(self):
        return True
 
    def addUIDrawables(self, objPath, drawManager, frameContext, data): 
        locatordata = data
        status = OpenMayaUI.M3dView.displayStatus(objPath)

        if not isinstance(locatordata, MntLocatorNodeData):
            return

        elif OpenMayaAnim.MAnimControl.isPlaying() == True:
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
                drawManager.setColor(data.color)      
                drawManager.setFontSize(11)      
                drawManager.text2d(OpenMaya.MPoint(data.screenPos[0] + 16, data.screenPos[1]), data.label, alignment = OpenMayaRender.MUIDrawManager.kLeft)

        if data.iconType == 6:
            drawManager.setColor(data.color)        
            drawManager.sphere(data.localPosition, data.size, 16, 8, True)

        if data.iconType == 7:
            drawManager.setColor(data.color)        
            drawManager.circle(data.localPosition, OpenMaya.MVector((0, 1, 0)), data.size, 32, True)

        if data.iconType == 8:
            drawManager.setColor(data.color)  
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

        Mnt_characterInfoNode.marginAttr = numAttrFn.create('margin', 'margin', OpenMaya.MFnNumericData.kInt, 100)
        numAttrFn.writable = True
        numAttrFn.readable = True
        numAttrFn.setMin(40)
        numAttrFn.setMax(300)
        Mnt_characterInfoNode.addAttribute(Mnt_characterInfoNode.marginAttr)

        Mnt_characterInfoNode.fontSizeAttr  = numAttrFn.create('fontSize', 'fontSize', OpenMaya.MFnNumericData.kInt, 12)
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
        drawManager.setFontSize(data.fontSize * 2)
        drawManager.setColor(OpenMaya.MColor((1.0, 0.75, 0.333, 0.5)))
        drawManager.text2d(OpenMaya.MPoint(data.rightInfosPos[0], data.characterNamePos[1]), 'Pose Scopes Visibility :', OpenMayaRender.MUIDrawManager.kRight, None, None, False)
        drawManager.setColor(OpenMaya.MColor((0.5, 0.5, 0.5, 0.5)))      
        drawManager.text2d(OpenMaya.MPoint(data.rightInfosPos[0], data.characterNamePos[1] -  data.fontSize * 3), str(data.poseScopeVisibilityState), OpenMayaRender.MUIDrawManager.kRight, None, None, False)
        drawManager.setTexture(None)
        drawManager.setColor(OpenMaya.MColor((0.5, 0.5, 0.5, 0.01)))
        drawManager.rect2d(OpenMaya.MPoint(data.rightInfosPos[0] - 13 * data.fontSize, data.characterNamePos[1]), OpenMaya.MVector(0,1), 14 * data.fontSize, 4 * data.fontSize, True)
        drawManager.endDrawable()

        if data.mnt_characterInfosVisibilityState == False:
            return

        drawManager.beginDrawable(OpenMayaRender.MUIDrawManager.kSelectable)
        drawManager.setColor(data.color)        
        drawManager.setFontWeight(87)
        drawManager.setFontSize(data.fontSize * 2)
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
        plugin.registerNode(MntLocatorNode.kPluginNodeName, MntLocatorNode.id, MntLocatorNode.creator, MntLocatorNode.initialize, OpenMaya.MPxNode.kLocatorNode, MntLocatorNode.drawDbClassification)
        plugin.registerNode(Mnt_characterInfoNode.kPluginNodeName, Mnt_characterInfoNode.id, Mnt_characterInfoNode.creator, Mnt_characterInfoNode.initialize, OpenMaya.MPxNode.kLocatorNode, Mnt_characterInfoNode.drawDbClassification)
    except:
        sys.stderr.write("Failed to register node\n")
        raise
 
    try:
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(MntLocatorNode.drawDbClassification, MntLocatorNode.drawRegistrantId, MntLocatorNodeDrawOverride.creator)
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(Mnt_characterInfoNode.drawDbClassification, Mnt_characterInfoNode.drawRegistrantId, Mnt_characterInfoNodeDrawOverride.creator)
    except:
        sys.stderr.write("Failed to register override\n")
        raise
 
def uninitializePlugin(obj):
    plugin = OpenMaya.MFnPlugin(obj)
 
    try:
        plugin.deregisterNode(MntLocatorNode.id)
        plugin.deregisterNode(Mnt_characterInfoNode.id)
    except:
        sys.stderr.write("Failed to deregister node\n")
        pass
 
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(MntLocatorNode.drawDbClassification, MntLocatorNode.drawRegistrantId)
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(Mnt_characterInfoNode.drawDbClassification, Mnt_characterInfoNode.drawRegistrantId)
    except:
        sys.stderr.write("Failed to deregister override\n")
        pass