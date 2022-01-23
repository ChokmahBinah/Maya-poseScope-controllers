import os
import json
import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya

class mnt_poseScopeUI():
    def __init__(self):
        self.buildUI()

    def buildUI(self):
        iconPath = cmds.getModulePath(moduleName = 'mnt_poseScope') + '/icons/mntShelf/'
        windowwidth = 200

        if cmds.workspaceControl('mnt_poseScopes_editor', ex = True):
            cmds.deleteUI('mnt_poseScopes_editor')
        
        cmds.workspaceControl('mnt_poseScopes_editor', w = windowwidth, r = True, clp = False)
        
        cmds.columnLayout(adj = True)
        cmds.text('Mnt poseScopes Editor', fn = 'boldLabelFont', h = 32, ebg = True, bgc = (0.15, 0.15, 0.15))
        cmds.paneLayout('mntDenoiseToolPane', cn = 'vertical2')

        cmds.columnLayout(adj = True)
        cmds.iconTextButton(style='iconAndTextVertical', l = 'Create or Update poseScope', i = iconPath + 'mnt_createPoseScope.png',\
            c = 'import maya.cmds as cmds\ncmds.createPoseScopeShape()', ann = 'Select some polySurface face components.\nThen select a transform node using the outliner and click button to create a poseScope.\n If no transform node is selected a default one is created.')
        cmds.iconTextButton(style='iconAndTextVertical', l = 'Mirror poseScope', i = iconPath + 'mnt_mirrorPoseScope.png',\
            c = 'import maya.cmds as cmds\ncmds.mirrorPoseScope()', ann = 'Creates a new mirrored poseScope\nfrom the selected one.')
        cmds.iconTextButton(style='iconAndTextVertical', l = 'Delete poseScope', i = iconPath + 'mnt_deletePoseScope.png',\
            c = cmds.deletePoseScope, ann = 'Delete poseScope from the selected transform node.')
        cmds.iconTextButton(style='iconAndTextVertical', l = 'Edit poseScope components', i = iconPath + 'mnt_editPoseScopeComponents.png',\
            c = 'cmds.editPoseScopeComponents()', ann = 'Select polySurface components associated\nto the selected poseScope.')
        cmds.iconTextButton(style='iconAndTextVertical', l = 'Transfert poseScopes', i = iconPath + 'mnt_transfertposeScopes.png',\
            c = 'cmds.transfertPoseScopes()', ann = 'Transfers poseScopes from  first selected polySurface A\nto a second selected polySurface B.')
        cmds.iconTextButton(style='iconAndTextVertical', l = 'Import poseScopes from json file', i = iconPath + 'mnt_importPoseScopes.png',\
            c = self.importPoseScopeInfos, ann = 'Imports poseScopes from a json file.')
        cmds.iconTextButton(style='iconAndTextVertical', l = 'Export poseScopes from json file', i = iconPath + 'mnt_exportPoseScopes.png',\
            c = self.savePoseScopeInfos, ann = 'Exports poseScopes to a json file.')
        cmds.setParent('..')

        cmds.columnLayout(adj = True, w = 500)
        cmds.text('PoseScopes Table', h = 24, bgc  =(0.2, 0.2, 0.2))
        cmds.textFieldButtonGrp('getInfosControl', label = 'PolySurface Name : ', text = 'None', buttonLabel = 'Get Posescopes', cat = (1, 'left', 0),\
            ct3 = ('left', 'left', 'left'), cw3 = (100, 170, 100), bc = self.updatePoseScopeTable)
        form = cmds.formLayout()

        table = cmds.scriptTable('table', rows = 0, columns = 3, label = [(1, 'Controller Name'), (2, 'Components List'), (3, 'PoseScope Visibility')], h = 530,\
            cw = (2, 200), ed = False, cellChangedCmd = self.edit_cell, sm = 3, sb = 1, mee = False)
        cmds.scriptTable('table', edit = True, cw = (1, 150))
        cmds.scriptTable('table', edit = True, cw = (3, 110))    
        cmds.scriptTable('table', edit = True, selectionChangedCmd = self.cellSelected, cbc = self.setBackgroundColor)

        cmds.formLayout(form, edit = True, attachForm=[(table, 'top', 0), (table, 'left', 0), (table, 'right', 0),])
        cmds.setParent('..')

        cmds.setParent('..')

    def edit_cell(self, row, column, value):
        return 1

    def setBackgroundColor(self, row, column):
        try:
            ctrlShape = cmds.listRelatives(cmds.scriptTable('table', q = True, cellIndex = (row, 1), cellValue = True), s = True)[0]
        except:
            return
            
        color = cmds.getAttr(ctrlShape + '.color')[0]
        opacity = cmds.getAttr(ctrlShape + '.opacity') + 0.1

        if column == 1:
            return (color[0] * 255 * opacity + 64, color[1] * 255 * opacity + 64, color[2] * 255 * opacity + 64)
    
        if column == 2:
            if row%2 == 0:
                return (64, 80, 100)

        if column == 3:
            if cmds.scriptTable('table', q = True, cellIndex = (row, column), cellValue = True)[0] == 'True':
                return (48 + 64, 40 + 64, 64)
            else:
                return (64, 64, 64)

    def cellSelected(self):
        selectedCell =  cmds.scriptTable('table', q = True, selectedCells = True)
        
        cmds.select(cl = True)

        try:
            for i in range(0, len(selectedCell), 2):
                value = cmds.scriptTable('table', q = True, cellIndex = (selectedCell[i], 1), cellValue = True)
                cmds.select(value, add = True)
        except:
            pass

    def updatePoseScopeTable(self, *args):
        MSelectionList      = OpenMaya.MGlobal.getActiveSelectionList()
        # I can do something to help about refresh here ...
        if MSelectionList.length() == 0:
            return
        
        # I can do something here to search input mesh from poseScopes too ...
        poseScopeInfos = self.getPoseScopesInfos()

        if poseScopeInfos == None:
            return

        cmds.scriptTable('table', e = True, clearTable = True)
        for i in range(0, cmds.scriptTable('table', q = True, rows = True)):
            cmds.scriptTable('table', e = True, deleteRow = (i+1))

        if  len(poseScopeInfos[1]):
            cmds.textFieldButtonGrp('getInfosControl', e = True, tx = poseScopeInfos[0])
            cmds.scriptTable('table', edit = True, rows = len(poseScopeInfos[1]))
            
            for i in range(0, len(poseScopeInfos[1])):
                cmds.scriptTable('table', cellIndex = (i + 1, 1), edit = True, cellValue = poseScopeInfos[1][i])
                cmds.scriptTable('table', cellIndex = (i + 1, 2), edit = True, cellValue = poseScopeInfos[2][i])
                isVisible = cmds.getAttr(cmds.scriptTable('table', q = True, cellIndex = (i + 1, 1), cellValue = True)[0] + '.visibility')
                
                cmds.scriptTable('table', edit = True, cellIndex = (i + 1, 3), cellValue = isVisible)
        else:
            return

        cmds.scriptTable('table', e = True, sm = 3)
        return

    def getPoseScopesInfos(self, *args):
        outputCtrlList      = []
        outputFaceCompList  = []
        outputColorList      = []
        MSelectionList      = OpenMaya.MGlobal.getActiveSelectionList()
        MObj                = MSelectionList.getDependNode(0)
        shapePath           = OpenMaya.MFnDagNode(MObj).getPath().extendToShape()

        shapeObj = OpenMaya.MFnDagNode(MObj).getPath().extendToShape().node()
        shapeDN = OpenMaya.MFnDependencyNode(shapeObj)

        if shapeObj.apiType() != OpenMaya.MFn.kMesh and shapeDN.typeName != 'mnt_poseScope':
            OpenMaya.MGlobal.displayError('Selection is not of kMesh type nor a poseScope. Please select a polygonal mesh or a poseScope controller first!')
            return
        else:
            pass
        
        # Now check mesh connected in the case the user select a poseScope controller
        if shapeDN.typeName == 'mnt_poseScope':
            connections = shapeDN.findPlug('inputMesh', False).connectedTo(True, False)
            inputMeshNode = connections[0].node()
            shapeDN = OpenMaya.MFnDependencyNode(inputMeshNode)
            shapePath = OpenMaya.MFnDagNode(inputMeshNode).getPath().extendToShape()
        else:
            shapeDN = OpenMaya.MFnDependencyNode(shapeObj)
        # ___________________________________________________________________________

        OpenMaya.MGlobal.displayInfo('Getting polygonal mesh poseScopes ...')

        outMeshPlug = shapeDN.findPlug('outMesh', False)
        connections = outMeshPlug.connectedTo(False, True)

        for plug in connections:
            node = plug.node()

            if OpenMaya.MFnDependencyNode(node).typeName == 'mnt_poseScope':
                # Gets its color
                colorR = OpenMaya.MFnDependencyNode(node).findPlug('colorR', False).asDouble()
                colorG = OpenMaya.MFnDependencyNode(node).findPlug('colorG', False).asDouble()
                colorB = OpenMaya.MFnDependencyNode(node).findPlug('colorB', False).asDouble()
                color = (colorR, colorG, colorB)
                outputColorList.append(color)
                # ______________

                # Finds poseScope parent transform node
                nodeDAG = OpenMaya.MFnDagNode(node)
                parentTransformName = OpenMaya.MFnDependencyNode(nodeDAG.parent(0)).name()
                outputCtrlList.append(parentTransformName)
                # ____________________________________

                # Finds connected groupNode face component list
                inputFacesPlug = OpenMaya.MFnDependencyNode(node).findPlug('inputFaceComponents', False)
                plugConnections = inputFacesPlug.connectedTo(True, False)

                for iPlug in plugConnections:
                    node = iPlug.node()
                    nodeDN = OpenMaya.MFnDependencyNode(node)
                    
                    if nodeDN.typeName == 'mnt_groupNode':
                        componentsListPlug = nodeDN.findPlug('componentsList', False)
                        componentsListValue = componentsListPlug.asString()
                        outputFaceCompList.append(componentsListValue)
                        break
                # _____________________________________________
            else:
                pass
        
        return shapePath, outputCtrlList, outputFaceCompList, outputColorList

    def savePoseScopeInfos(self, * args):
        outputFolder = cmds.workspace(q = True, active = True) + '/data/poseScopes_infos/'

        poseScopeInfos = self.getPoseScopesInfos()

        # Creates a json object
        json_obj = {}
        json_obj['polySurface'] = []
        json_obj['poseScopes'] = []
        # _____________________

        if len(poseScopeInfos[1]) == 0:
            OpenMaya.MGlobal.displayError('Selected mesh isn\'t connected to any poseScope.')
            return

        # Creates a dictionnary from poseScopeInfos
        json_obj['polySurface'].append(str(poseScopeInfos[0]))

        for i in range(0, len(poseScopeInfos[1])):
            json_obj['poseScopes'].append({
                'Controller' : poseScopeInfos[1][i],
                'ComponentsList' : poseScopeInfos[2][i],
                'Color' : poseScopeInfos[3][i]
            })
        # _________________________________________

        # Creates json file
        try:
            os.mkdir(outputFolder)
        except:
            pass

        with open(outputFolder + 'poseScopes_' + str(poseScopeInfos[0]) + '.json', 'w') as f:
            json.dump(json_obj, f, indent = 4)
        
        OpenMaya.MGlobal.displayInfo('PoseScope infos exported.')
        # _________________

    def importPoseScopeInfos(self, *args):
        outputFolder = cmds.workspace(q = True, active = True) + '/data/poseScopes_infos/'
        '''fileName        = cmds.file(q = True, sn = True, shn = True)
        fullFileName    = cmds.file(q = True, sn = True)
        filePath        = fullFileName.replace(fileName, '')'''

        poseScopesFile = cmds.fileDialog2(caption = 'Import poseScopes', dialogStyle = 2, fm = 1, okCaption = 'Import', dir = cmds.workspace(q = True, active = True) + '/data/')
        
        if not poseScopesFile:
            return
        
        with open(poseScopesFile[0]) as f:
            poseScopesData = json.load(f)

        meshShape = poseScopesData['polySurface']      
        keys = poseScopesData.keys()
        
        for i in range(0, len(poseScopesData['poseScopes'])):
            controller = poseScopesData['poseScopes'][i]['Controller']
            componentList = poseScopesData['poseScopes'][i]['ComponentsList'].split()
           
            # Creates poseScope
            cmds.select(cl = True)

            for j in range(0, len(componentList)):
                cmds.select(meshShape[0] + '.f[' + componentList[j] + ']', add = True)

            cmds.select(controller, add = True)
            cmds.createPoseScopeShape()

            cmds.select(controller, r = True)
            # _________________           

            # Sets poseScope properties
            selection = OpenMaya.MGlobal.getActiveSelectionList()
            poseScopeObj = selection.getDependNode(0)
            poseScopePath = OpenMaya.MDagPath.getAPathTo(poseScopeObj).extendToShape()
            poseScopeDNFn = OpenMaya.MFnDependencyNode(poseScopePath.node())
            poseScopeDNFn.findPlug('colorR', False).setDouble(poseScopesData['poseScopes'][i]['Color'][0])
            poseScopeDNFn.findPlug('colorG', False).setDouble(poseScopesData['poseScopes'][i]['Color'][1])
            poseScopeDNFn.findPlug('colorB', False).setDouble(poseScopesData['poseScopes'][i]['Color'][2])
            # _________________________