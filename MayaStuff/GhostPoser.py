import maya.cmds as mc

from PySide2.QtCore import Signal, Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QAbstractItemView, QPushButton, QLabel, QListWidget, QColorDialog, QSlider
from PySide2.QtGui import QColor, QPainter, QBrush

def GetCurrentFrame():
    return int(mc.currentTime(q=True))

class Ghost():
    def __init__(self):
        self.srcMeshs = set()
        self.InitGhostGrpIfNotExist()
        self.InitSrcMeshFromGhostGrp()
        self.ghostColor = [0,0,0]
        self.baseTransparency = 0
        self.transparencyRange = 60
        self.timeJob = mc.scriptJob(e=["timeChanged",self.CurrentTimeChanged])

    def CurrentTimeChanged(self):
        self.UpdateGhostTransparency()

    def UpdateTransparencyRange(self, newRange):
        self.transparencyRange = newRange 
        self.UpdateGhostTransparency()

    def UpdateBaseTranparency(self, newTransparency):      
        self.baseTransparency = newTransparency
        self.UpdateGhostTransparency()

    def UpdateGhostTransparency(self):
        allGhosts = mc.listRelatives(self.GetGhostGrpName(), c=True)
        mc.setAttr(self.GetGhostGrpName() + "." + "TransBase", self.baseTransparency * 100)
        mc.setAttr(self.GetGhostGrpName() + "." + "TransRange", self.transparencyRange)
        if not allGhosts:
            return

        for ghost in allGhosts:
            ghostFrame = mc.getAttr(ghost + "." + self.GetFrameAttr())
            currentFrame = GetCurrentFrame()
            distance = abs(currentFrame - ghostFrame)
            
            ghostMat = self.GetShaderNameForGhost(ghost)
        
            if distance > self.transparencyRange:
                mc.setAttr(ghostMat + ".transparency", 1,1,1, type = "double3")
                continue
            
            self.transparencyRange = self.transparencyRange
            normalizeDist = distance / self.transparencyRange

            if self.baseTransparency > 0 and self.baseTransparency > 0.1:
                normalizeDist = self.baseTransparency + normalizeDist



            print(normalizeDist)
            
            mc.setAttr(ghostMat + ".transparency", normalizeDist, normalizeDist, normalizeDist, type = "double3")

    def DeleteSelectedGhost(self):
        for srcMesh in self.srcMeshs:
            ghostName = srcMesh + self.GetGhostSubfix() + str(GetCurrentFrame())
            self.DeleteGhost(ghostName)            

    def UpdateGhostColors(self, r, g, b):
        self.ghostColor[0] = r
        print(self.ghostColor[0])
        mc.setAttr(self.GetGhostGrpName() + "." + "ColorR", self.ghostColor[0])
        self.ghostColor[1] = g
        mc.setAttr(self.GetGhostGrpName() + "." + "ColorG", self.ghostColor[1])
        self.ghostColor[2] = b
        mc.setAttr(self.GetGhostGrpName() + "." + "ColorB", self.ghostColor[2])
        allGhosts = mc.listRelatives(self.GetGhostGrpName(), c=True)
        for ghost in allGhosts:
            self.SetGhostColor(ghost, r, g, b)

    def DeleteGhost(self, ghostName):
        ghostSg = self.GetShaderEngineForGhost(ghostName)
        if mc.objExists(ghostSg):
            mc.delete(ghostSg)

        ghostMat = self.GetShaderNameForGhost(ghostName)
        if mc.objExists(ghostMat):
            mc.delete(ghostMat)

        if mc.objExists(ghostName):
            mc.delete(ghostName)

    def SetGhostColor(self, ghost, r, g, b):
        ghostMat = self.GetShaderNameForGhost(ghost)
        mc.setAttr(ghostMat + ".color", r, g, b, type = "double3")

    def DeleteAllGhosts(self):
        allGhost = mc.listRelatives(self.GetGhostGrpName(), c=True)
        if not allGhost:
            return

        for ghost in allGhost:
            self.DeleteGhost(ghost)

    def InitSrcMeshFromGhostGrp(self):
        srcMeshAttr = mc.getAttr(self.GetGhostGrpName() + "." + self.GetSrcMeshAttr())
        if not srcMeshAttr:
            return
        
        meshes = srcMeshAttr.split(",")
        self.srcMeshs = set(meshes)

    def InitColorFromGhostGrp(self):
        ColorR = mc.getAttr(self.GetGhostGrpName() + "." + "ColorR")
        ColorG = mc.getAttr(self.GetGhostGrpName() + "." + "ColorG")
        ColorB = mc.getAttr(self.GetGhostGrpName() + "." + "ColorB")

        if not ColorR:
            return
        if not ColorG:
            return
        if not ColorB:
            return
        
        self.ghostColor[0] = ColorR
        self.ghostColor[1] = ColorG
        self.ghostColor[2] = ColorB

        

    def InitGhostGrpIfNotExist(self):
        if not mc.objExists(self.GetGhostGrpName()):
            mc.createNode("transform", n = self.GetGhostGrpName())
            mc.addAttr(self.GetGhostGrpName(), ln = self.GetSrcMeshAttr(), dt = "string")
            mc.addAttr(self.GetGhostGrpName(), ln = "ColorR")
            mc.addAttr(self.GetGhostGrpName(), ln = "ColorG")
            mc.addAttr(self.GetGhostGrpName(), ln = "ColorB")
            mc.addAttr(self.GetGhostGrpName(), ln = "TransBase")
            mc.addAttr(self.GetGhostGrpName(), ln = "TransRange")

    def GetColorR(self):
        return mc.getAttr(self.GetGhostGrpName() + "." + "ColorR")
    
    def GetColorG(self):
        return mc.getAttr(self.GetGhostGrpName() + "." + "ColorG")
        
    def GetColorB(self):
        return mc.getAttr(self.GetGhostGrpName() + "." + "ColorB")
    
    def GetTransBase(self):
        return mc.getAttr(self.GetGhostGrpName() + "." + "TransBase")
    
    def GetTransRange(self):
        return mc.getAttr(self.GetGhostGrpName() + "." + "TransRange")
    

    def GetSrcMeshAttr(self):
        return "src"

    def GetGhostGrpName(self):
        return "Ghost_grp"

    def GoToNextGhost(self):
        currentFrame = GetCurrentFrame()
        frames = self.GetGhostFramesSorted()
        nextFrame = frames[0]
        for frame in frames:
            if frame > currentFrame:
                nextFrame = frame
                break
        
        mc.currentTime(nextFrame, e=True)

    def GoToPrevGhost(self):
        currentFrame = GetCurrentFrame()
        frames = self.GetGhostFramesSorted()
        nextFrame = frames[-1]
        
        frames.reverse()
        for frame in frames:
            if frame < currentFrame:
                nextFrame = frame
                break

        mc.currentTime(nextFrame, e=True)

    def GetGhostFramesSorted(self):
        ghosts = mc.listRelatives(self.GetGhostGrpName(), c=True)
        frames = set() 
        for ghost in ghosts:
            frame = mc.getAttr(ghost + "." + self.GetFrameAttr())
            frames.add(frame)

        frames = list(frames)
        frames.sort()
        return frames

    def GetGhostSubfix(self):
        return "_ghost_"

    def AddGhost(self):
        for srcMesh in self.srcMeshs:
            ghostName = srcMesh + self.GetGhostSubfix() + str(GetCurrentFrame())
            if mc.objExists(ghostName):
                mc.delete(ghostName)

            mc.duplicate(srcMesh, n = ghostName)
            mc.addAttr(ghostName, ln = self.GetFrameAttr(), dv = GetCurrentFrame())
            mc.parent(ghostName, self.GetGhostGrpName())
            self.CreateMaterialForGhost(ghostName)
            self.SetGhostColor(ghostName, self.ghostColor[0], self.ghostColor[1], self.ghostColor[2])
            self.UpdateGhostTransparency()

    def GetFrameAttr(self):
        return "frame"

    def InitSrcMeshesWithSel(self):
        selection = mc.ls(sl=True)
        self.srcMeshs.clear()  
        for sel in selection:
            shapes = mc.listRelatives(sel, s=True)
            for s in shapes:
                if mc.objectType(s) == "mesh":
                    self.srcMeshs.add(sel)

        mc.setAttr(self.GetGhostGrpName() + "." + self.GetSrcMeshAttr(), ",".join(self.srcMeshs), typ="string")

    def CreateMaterialForGhost(self, ghost):        
        matName = self.GetShaderNameForGhost(ghost)
        if not mc.objExists(matName):
            mc.shadingNode("lambert", asShader = True, name = matName)
        
        setName = self.GetShaderEngineForGhost(ghost)
        if not mc.objExists(setName):
            mc.sets(name = setName, renderable = True, empty = True)

        mc.connectAttr(matName + ".outColor", setName + ".surfaceShader", force = True)
        mc.sets(ghost, edit=True, forceElement = setName)

    def GetShaderEngineForGhost(self, ghost):
        return ghost + "_sg"

    def GetShaderNameForGhost(self, ghost):
        return ghost + "_mat"

class ColorPicker(QWidget):
    colorChanged = Signal(QColor)
    def __init__(self, width = 80, height = 20):
        super().__init__()
        self.setFixedSize(width, height)
        self.color = QColor(128, 128, 128)

    def mousePressEvent(self, event):
        color = QColorDialog().getColor(self.color)
        self.color = color
        self.colorChanged.emit(self.color)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(self.color))
        painter.drawRect(0,0, self.width(), self.height())      

class GhostWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ghost = Ghost()
        self.setWindowTitle("Ghoster")
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)
        self.CreateMeshSelSection()
        self.CreateMatCtrlSection()
        self.CreateCtrlSection()

    def CreateMatCtrlSection(self):
        layout = QHBoxLayout()
        self.masterLayout.addLayout(layout)
        
        self.ghostColorPicker = ColorPicker()
        self.ghostColorPicker.color.setRedF(self.ghost.GetColorR())
        self.ghostColorPicker.color.setGreenF(self.ghost.GetColorG())
        self.ghostColorPicker.color.setBlueF(self.ghost.GetColorB())

        self.ghostColorPicker.colorChanged.connect(self.GhostColorPickerColorChanged)
        layout.addWidget(self.ghostColorPicker)

        transSlider = QSlider()
        transSlider.setOrientation(Qt.Horizontal)
        transSlider.setMinimum(0)
        transSlider.setMaximum(100)
        transSlider.setValue(self.ghost.GetTransBase())
        transSlider.valueChanged.connect(self.BaseTransparencyChanged)
        layout.addWidget(transSlider)

        visCtrlLayout = QHBoxLayout()
        self.masterLayout.addLayout(visCtrlLayout)

        rangeLabel = QLabel("Transparecy Range")
        visCtrlLayout.addWidget(rangeLabel)
        rangeSlider = QSlider()
        rangeSlider.setOrientation(Qt.Horizontal)
        rangeSlider.setMinimum(0)
        rangeSlider.setMaximum(60)
        rangeSlider.setValue(self.ghost.GetTransRange())
        rangeSlider.valueChanged.connect(self.TransparencyRangeChanged)
        visCtrlLayout.addWidget(rangeSlider)

    def BaseTransparencyChanged(self, value):
        self.ghost.UpdateBaseTranparency(value/100)        

    def TransparencyRangeChanged(self, value):
        self.ghost.UpdateTransparencyRange(value)        

    def GhostColorPickerColorChanged(self, newColor:QColor):
        self.ghost.UpdateGhostColors(newColor.redF(), newColor.greenF(), newColor.blueF())

    def CreateCtrlSection(self):
        layout = QHBoxLayout()
        self.masterLayout.addLayout(layout)

        addGhostBtn = QPushButton("Add")
        addGhostBtn.clicked.connect(self.ghost.AddGhost) 
        layout.addWidget(addGhostBtn)

        prevBtn = QPushButton("<<<")
        prevBtn.clicked.connect(self.ghost.GoToPrevGhost)
        layout.addWidget(prevBtn)

        nextBtn = QPushButton(">>>")
        nextBtn.clicked.connect(self.ghost.GoToNextGhost)
        layout.addWidget(nextBtn)

        delBtn = QPushButton("Del")
        delBtn.clicked.connect(self.ghost.DeleteSelectedGhost)
        layout.addWidget(delBtn)

        delAllBtn = QPushButton("Del All")
        delAllBtn.clicked.connect(self.ghost.DeleteAllGhosts)
        layout.addWidget(delAllBtn)

    def CreateMeshSelSection(self):
        self.SrcMeshList = QListWidget()
        self.SrcMeshList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.SrcMeshList.itemSelectionChanged.connect(self.SrcMeshListSelecionChanged)
        self.masterLayout.addWidget(self.SrcMeshList)
        setSrcMeshBtn = QPushButton("Set Selected as Source")
        setSrcMeshBtn.clicked.connect(self.SetSrcMeshBtnClicked)
        self.masterLayout.addWidget(setSrcMeshBtn)
        self.SrcMeshList.addItems(self.ghost.srcMeshs)

    def SetSrcMeshBtnClicked(self):
        self.ghost.InitSrcMeshesWithSel()
        self.SrcMeshList.clear()
        self.SrcMeshList.addItems(self.ghost.srcMeshs)

    def SrcMeshListSelecionChanged(self):
        mc.select(cl=True)
        for item in self.SrcMeshList.selectedItems():
            mc.select(item.text(), add=True)

ghostWidget = GhostWidget()
ghostWidget.show()