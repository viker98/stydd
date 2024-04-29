from PySide2.QtCore import Signal
import maya.cmds as mc
from PySide2.QtWidgets import QCheckBox, QLineEdit, QMessageBox, QWidget, QPushButton, QListWidget, QAbstractItemView, QLabel, QHBoxLayout, QVBoxLayout, QDialog

class AnimEntry():
    def __init__(self):
        self.subfix = ""
        self.frameMin = mc.playbackOptions(q = True, min = True)
        self.frameMax = mc.playbackOptions(q = True, max = True)
        self.shouldExport = True



class MayaToUE:
    def __init__(self):
        self.rootJnt = ""
        self.models = set()
        self.animations = []


    def RemoveEntry(self, entryToRemove):
        self.animations.remove(entryToRemove)

    def AddRootJnt(self):

        if not self.rootJnt:
            return False, "No Root Joint Assigned"
    
        if self.rootJnt and mc.objExists(self.rootJnt):
            #q = querying  t = Transform  ws = WorldSpace
            currentRootPos = mc.xform(self.rootJnt, q=True,t=True,ws=True)
            if currentRootPos[0] == 0 and currentRootPos[1] == 0 and currentRootPos[2] == 0:
                return False, "Root Joint Already Exists"

        mc.select(cl=True)
        rootJntName = self.rootJnt + "_root"
        mc.joint(n = rootJntName)
        mc.parent(self.rootJnt,rootJntName)
        self.rootJnt = rootJntName
        return True, ""



    def GetSelectionAsRootJnt(self):
        selection = mc.ls(sl=True, type = "joint")
        if not selection:
            return False, "No Joint Selected"
        
        self.rootJnt = selection[0]
        return True, ""
    
    def AddSelectedMeshes(self):
        selection = mc.ls(sl=True)
        if not selection:
            return False,"No Mesh Selected"
        
        meshes = set()

        for sel in selection:
            shapes = mc.listRelatives(sel, s=True)
            for s in shapes:
                if mc.objectType(s) == "mesh":
                    meshes.add(sel)

        if len(meshes) == 0:
            return False, "No Mesh Selected"
        self.models = meshes
        return True, ""

    def AddNewAnimEntry(self):
        self.animations.append(AnimEntry())
        return self.animations[-1]




class AnimEntryWidget(QWidget):
    entryRemoved = Signal(AnimEntry)


    def __init__(self, entry:AnimEntry):
        super().__init__()
        self.entry = entry
        self.masterLayout = QHBoxLayout()
        self.setLayout(self.masterLayout)

        enableCheckbox = QCheckBox()
        enableCheckbox.setChecked(self.entry.shouldExport)
        self.masterLayout.addWidget(enableCheckbox)
        enableCheckbox.toggled.connect(self.EnableCheckboxToggled)

        subfixLabel = QLabel("SubFix: ")
        self.masterLayout.addWidget(subfixLabel)
        subfixLineEdit = QLineEdit()
        subfixLineEdit.setText(self.entry.subfix)
        subfixLineEdit.textChanged.connect(self.subfixTextChanged)
        self.masterLayout.addWidget(subfixLineEdit)

        minFrameLabel = QLabel("Min: ")
        self.masterLayout.addWidget(minFrameLabel)
        minFrameLineEdit = QLineEdit()
        minFrameLineEdit.setText(str(self.entry.frameMin))
        minFrameLineEdit.textChanged.connect(self.MinFrameTextChanged)
        self.masterLayout.addWidget(minFrameLineEdit)
        
        maxFrameLabel = QLabel("Max: ")
        self.masterLayout.addWidget(maxFrameLabel)
        maxFrameLineEdit = QLineEdit()
        maxFrameLineEdit.setText(str(self.entry.frameMax))
        maxFrameLineEdit.textChanged.connect(self.MaxFrameTextChanged)
        self.masterLayout.addWidget(maxFrameLineEdit)

        setRangeBtn = QPushButton("[-]")
        setRangeBtn.clicked.connect(self.SetRangeBtnClicked)
        self.masterLayout.addWidget(setRangeBtn)

        DeleteBtn = QPushButton("X")
        self.close()
        DeleteBtn.clicked.connect(self.DeleteBtnClicked)
        self.masterLayout.addWidget(DeleteBtn)
        

    def DeleteBtnClicked(self):
        self.entryRemoved.emit(self.entry)
        self.deleteLater()

    def SetRangeBtnClicked(self):
        mc.playbackOptions(e=True,min=self.entry.frameMin,max = self.entry.frameMax)
        mc.playbackOptions(e=True,ast=self.entry.frameMin,aet = self.entry.frameMax)


    def MinFrameTextChanged(self, newVal):
        self.entry.frameMin = int(newVal)

    def MaxFrameTextChanged(self, newVal):
        self.entry.frameMax = int(newVal)

    def subfixTextChanged(self, newVal):
        self.entry.subfix = newVal

    def EnableCheckboxToggled(self):
        self.entry.shouldExport = not self.entry.shouldExport

class MayaToUEWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.mayaToUE = MayaToUE()
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.rootJntText = QLineEdit()
        self.rootJntText.setEnabled(False)
        self.masterLayout.addWidget(self.rootJntText)
    
        setSelectionAsRootJntBtn = QPushButton("Set Root Joint")
        setSelectionAsRootJntBtn.clicked.connect(self.SetSelectionAsRootJntBTnClicked)
        self.masterLayout.addWidget(setSelectionAsRootJntBtn)

        addRootJntBtn = QPushButton("Add Root Joint")
        addRootJntBtn.clicked.connect(self.AddRootJntBtnClicked)
        self.masterLayout.addWidget(addRootJntBtn)

        self.meshList = QListWidget()
        self.meshList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.masterLayout.addWidget(self.meshList)
        self.meshList.setFixedHeight(80)
        addMeshBtn = QPushButton("Add Mesh")
        addMeshBtn.clicked.connect(self.AddMeshBtnClicked)
        self.masterLayout.addWidget(addMeshBtn)

        
        addNewAnimEntryBtn = QPushButton("Add Animation clip")
        addNewAnimEntryBtn.clicked.connect(self.AddNewAnimEntryBtnClicked)
        self.masterLayout.addWidget(addNewAnimEntryBtn)

        self.setFixedWidth(500)
        self.resize(self.minimumSizeHint())

    
    
    def AddNewAnimEntryBtnClicked(self):
        newEntry = self.mayaToUE.AddNewAnimEntry()
        newAnimEntryWidget = AnimEntryWidget(newEntry)
        newAnimEntryWidget.entryRemoved.connect(self.EntryRemoved)
        self.masterLayout.addWidget(newAnimEntryWidget)


    def EntryRemoved(self, entry):
        self.resize(self.minimumSizeHint())
        self.mayaToUE.RemoveEntry(entry)

    def AddMeshBtnClicked(self):
        success, msg = self.mayaToUE.AddSelectedMeshes()
        if not success:
            QMessageBox.warning(self, "Warning",msg)
        else:
            self.meshList.clear()
            self.meshList.addItems(self.mayaToUE.models)

    def AddRootJntBtnClicked(self):
        success, msg = self.mayaToUE.AddRootJnt()

        if not success:
            QMessageBox.warning(self,"Warning",msg)
        else:
            self.rootJntText.setText(self.mayaToUE.rootJnt)

    def SetSelectionAsRootJntBTnClicked(self):
        success, msg = self.mayaToUE.GetSelectionAsRootJnt()
        if not success:
            QMessageBox().warning(self,"Warning",msg)

        else:
            self.rootJntText.setText(self.mayaToUE.rootJnt)


MayaToUEWidget = MayaToUEWidget()
MayaToUEWidget.show()