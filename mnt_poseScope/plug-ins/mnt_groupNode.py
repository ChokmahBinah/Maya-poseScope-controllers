import maya.api.OpenMaya as OpenMaya

maya_useNewAPI = True

class Mnt_GroupNode(OpenMaya.MPxNode):
    kPluginNodeName         = 'mnt_groupNode' #Name of the node.
    id                      = OpenMaya.MTypeId( 0xDAE7 ) # A unique ID associated to this node type.

    modeAttr                = OpenMaya.MObject()
    componentTypeAttr       = OpenMaya.MObject()
    componentAttribute      = OpenMaya.MObject()
    componentListAttr       = OpenMaya.MObject()
    componentOutputsAttr    = OpenMaya.MObject()

    def __init__(self):
        OpenMaya.MPxNode.__init__(self)

    @staticmethod
    def creator():
        return Mnt_GroupNode()

    @staticmethod
    def initialize():
        #Input attributes
        modeAttrFn  = OpenMaya.MFnEnumAttribute()
        Mnt_GroupNode.modeAttr  = modeAttrFn.create('mode', 'mode', 0)
        modeAttrFn.addField('Index', 0)
        modeAttrFn.addField('String', 1)
        modeAttrFn.hidden = False
        modeAttrFn.channelBox = True
        Mnt_GroupNode.addAttribute(Mnt_GroupNode.modeAttr)

        componentTypeAttrFn = OpenMaya.MFnEnumAttribute()
        Mnt_GroupNode.componentTypeAttr = componentTypeAttrFn.create('componentType', 'componentType', 2)
        componentTypeAttrFn.addField('Vertices', 0)
        componentTypeAttrFn.addField('Edges', 1)
        componentTypeAttrFn.addField('Faces', 2)
        componentTypeAttrFn.writable = True
        componentTypeAttrFn.keyable = True
        componentTypeAttrFn.hidden = False
        componentTypeAttrFn.channelBox = True
        Mnt_GroupNode.addAttribute(Mnt_GroupNode.componentTypeAttr)

        componentAttributeFn = OpenMaya.MFnNumericAttribute()
        Mnt_GroupNode.componentAttribute    = componentAttributeFn.create('component', 'component', OpenMaya.MFnNumericData.kInt)
        componentAttributeFn.writable       = True
        componentAttributeFn.keyable        = True
        componentAttributeFn.storable       = True
        componentAttributeFn.hidden         = False
        Mnt_GroupNode.addAttribute(Mnt_GroupNode.componentAttribute)

        componentListAttrFn = OpenMaya.MFnTypedAttribute()
        Mnt_GroupNode.componentListAttr = componentListAttrFn.create('componentsList', 'componentsList', OpenMaya.MFnData.kString)
        componentListAttrFn.writable    = True
        componentListAttrFn.keyable     = True
        componentListAttrFn.storable    = True
        componentListAttrFn.hidden      = False
        Mnt_GroupNode.addAttribute(Mnt_GroupNode.componentListAttr)      

        #Ouput attributes
        componentOutputsAttributeFn = OpenMaya.MFnTypedAttribute()
        Mnt_GroupNode.componentOutputsAttr = componentOutputsAttributeFn.create('outputsComponent', 'outputsComponent',OpenMaya.MFnData.kComponentList)
        componentOutputsAttributeFn.writable = True
        componentOutputsAttributeFn.storable = True
        componentOutputsAttributeFn.hidden = False       
        Mnt_GroupNode.addAttribute(Mnt_GroupNode.componentOutputsAttr)

        #Inputs and Outputs links
        Mnt_GroupNode.attributeAffects(Mnt_GroupNode.modeAttr, Mnt_GroupNode.componentOutputsAttr)
        Mnt_GroupNode.attributeAffects(Mnt_GroupNode.componentTypeAttr, Mnt_GroupNode.componentOutputsAttr)
        Mnt_GroupNode.attributeAffects(Mnt_GroupNode.componentAttribute, Mnt_GroupNode.componentOutputsAttr)
        Mnt_GroupNode.attributeAffects(Mnt_GroupNode.componentListAttr, Mnt_GroupNode.componentOutputsAttr)

    def compute(self, plug, dataBlock):
        #Inputs
        mode                = dataBlock.inputValue(Mnt_GroupNode.modeAttr).asShort()
        componentType       = dataBlock.inputValue(Mnt_GroupNode.componentTypeAttr).asShort()
        componentID         = dataBlock.inputValue(Mnt_GroupNode.componentAttribute).asShort()
        componentsListStr   = dataBlock.inputValue(Mnt_GroupNode.componentListAttr).asString()
        
        # Outputs
        if (plug == Mnt_GroupNode.componentOutputsAttr or plug == Mnt_GroupNode.modeAttr):
            ouputComponentsHandle = dataBlock.outputValue(Mnt_GroupNode.componentOutputsAttr)

            singleIndexedComponent = OpenMaya.MFnSingleIndexedComponent()

            if componentType == 0:
                componentsObj = singleIndexedComponent.create(OpenMaya.MFn.kMeshVertComponent)                
            if componentType == 1:#Add else statement
                componentsObj = singleIndexedComponent.create(OpenMaya.MFn.kMeshEdgeComponent)
            if componentType == 2:
                componentsObj = singleIndexedComponent.create(OpenMaya.MFn.kMeshPolygonComponent) 

            if mode == 0:
                singleIndexedComponent.addElement(componentID)
            if mode == 1:
                singleIndexedComponent.addElements(self.convertStringToIntArray(componentsListStr))

            componentsListData = OpenMaya.MFnComponentListData()
            componentsListObj = componentsListData.create()
            componentsListData.add(componentsObj)

            ouputComponentsHandle.setMObject(componentsListObj)

            dataBlock.setClean(plug)
        return None


    def convertStringToIntArray(self, string):
        intList = string.split()
        intArray = OpenMaya.MIntArray()

        for item in intList:
            intArray.append(int(item))
            
        return intArray
        
    def setDependentsDirty(self, plug, plugArray):
        return

def initializePlugin(obj):
    plugin = OpenMaya.MFnPlugin(obj, "Florian Delarque", "1.5", "Any")

    try:
        plugin.registerNode(Mnt_GroupNode.kPluginNodeName, Mnt_GroupNode.id, Mnt_GroupNode.creator, Mnt_GroupNode.initialize, OpenMaya.MPxNode.kDependNode)
    except:
        OpenMaya.MGlobal.displayError("Failed to register node\n")
        raise

def uninitializePlugin(obj):
    plugin = OpenMaya.MFnPlugin(obj)

    try:
        plugin.deregisterNode(Mnt_GroupNode.id)
    except:
        OpenMaya.MGlobal.displayInfo("Failed to deregister node\n")
        pass