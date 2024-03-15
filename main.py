# Made by AnybodyC / Crips

import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QScrollArea,
    QLabel, QAction, QApplication, QInputDialog, QLineEdit,
    QMenuBar, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QGridLayout, QSizePolicy
)
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QPalette, QFontDatabase
from PyQt5.QtCore import QSize, Qt, QCoreApplication
import perks
import skillfilereader
import cyberwarefilereader
import weaponfilereader
from pathlib import Path
import functools
import string
import os

# FIX THIS TO GET A PROPER PATH FOR ALL USERS (do at the end, maybe .exe will fix it all (probably not but well see))
path = Path.cwd()
PATH = Path.cwd()
FILE_LIST = os.listdir(f"{path}/Saves/")
imagespath = str(path) + "/images/"
app = QApplication(sys.argv)

global_attributes = {
    "BODY": 3,
    "REFLEXES": 3,
    "TECH": 3,
    "INTELLIGENCE": 3,
    "COOL": 3,
    "TOTAL": 66
}

headerfontid = QFontDatabase.addApplicationFont(fr"{path}\SAIBA-45.ttf")
HEADERFONT = QFont(QFontDatabase.applicationFontFamilies(headerfontid)[0])
HEADERFONT.setPointSize(20)

numfontid = QFontDatabase.addApplicationFont(fr"{path}\GlitchGoblin-2O87v.ttf")
NUMFONT = QFont(QFontDatabase.applicationFontFamilies(numfontid)[0])
NUMFONT.setPointSize(30)

textfontid = QFontDatabase.addApplicationFont(fr"{path}\Play-Regular.ttf")
TEXTFONT = QFont(QFontDatabase.applicationFontFamilies(textfontid)[0])
TEXTFONT.setPointSize(10)

app.setFont(TEXTFONT)

global PERKPOINTS
PERKPOINTS = 80

PERKCOLOREVEN = "31181e"
PERKCOLORUNEVEN = "2c141a"

SKILLLIST = skillfilereader.readfile()

SPECIALPERKS = []

BODYPERKS = perks.createPerkList("bodyPerks.txt")
for perk in BODYPERKS[len(BODYPERKS) - 1]:
    SPECIALPERKS.append(perk)

REFLEXESPERKS = perks.createPerkList("reflexesPerks.txt")
for perk in REFLEXESPERKS[len(REFLEXESPERKS) - 1]:
    SPECIALPERKS.append(perk)

TECHPERKS = perks.createPerkList("techPerks.txt")
for perk in TECHPERKS[len(TECHPERKS) - 1]:
    SPECIALPERKS.append(perk)

INTELLIGENCEPERKS = perks.createPerkList("intelligencePerks.txt")
for perk in INTELLIGENCEPERKS[len(INTELLIGENCEPERKS) - 1]:
    SPECIALPERKS.append(perk)

COOLPERKS = perks.createPerkList("coolPerks.txt")
for perk in COOLPERKS[len(COOLPERKS) - 1]:
    SPECIALPERKS.append(perk)

CWBUTTONLIST = []
ACTIVECYBERWARE = []

WEAPONSELECTION = []
SELECTEDWEAPONFILES = []

WEAPONTOSELECT = 1

WEAPON1 = None
WEAPON2 = None
WEAPON3 = None
WEAPON4 = None

SELECTEDSORT = 0

STATBUTTONLIST = [1, 1, 1, 1, 1] 

CYBERWARECOST = 0


def mergesort(lst, key):
    if len(lst) <= 1:
        return lst

    midpoint = len(lst) // 2
    lst1 = lst[:midpoint]
    lst2 = lst[midpoint:]

    lst1 = mergesort(lst1, key)
    lst2 = mergesort(lst2, key)

    return merge(lst1, lst2, key)

def merge(lst1, lst2, key):
    resultList = []
    i1 = 0
    i2 = 0

    while i1 < len(lst1) and i2 < len(lst2):
        if hasattr(lst1[i1], key):
            if hasattr(lst2[i2], key):
                if getattr(lst1[i1], key) > getattr(lst2[i2], key):
                    resultList.append(lst1[i1])
                    i1 += 1
                else:
                    resultList.append(lst2[i2])
                    i2 += 1
            else:
                i2 += 1
        else:
            i1 += 1

    resultList.extend(lst1[i1:])
    resultList.extend(lst2[i2:])
    return resultList


class MainWindow(QMainWindow):
    # main app
    def __init__(self):
        super().__init__()
        self.attribute_labels = {}
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(19,9,12))  # Adjust RGB values as needed
        self.setPalette(palette)
        self.setWindowTitle("Unofficial, Fanmade Build Creator for Cyberpunk 2077")
        self.setWindowIcon(QIcon(imagespath + "titlepic.png"))
        self.resize(QSize(1920, 1080))
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint | Qt.WindowMaximizeButtonHint)
        self.showMaximized()
        self.createActions()
        self.createMenuBar()
        self.createMainToolBar()
        self.attributeScreen()


        # MAIN MENU BAR, SAVING, OPENING FILES OR SHARING
    def createMenuBar(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)
        menuBar.setStyleSheet("background-color: #ffffff; color: #2e2e2e")
        saveMenu = menuBar.addMenu("Save")
        openMenu = menuBar.addMenu("Open")
        shareMenu = menuBar.addMenu("Share")
        saveMenu.addAction(self.saveFileAction)
        saveMenu.addAction(self.copyCodeAction)
        openMenu.addAction(self.openFileAction)
        openMenu.addAction(self.enterCodeAction)
        shareMenu.addAction(self.copyCodeAction)
        shareMenu.addAction(self.enterCodeAction)

    # MAIN TOOL BAR, ATTR & PERK POINTS LEFT, CATEGORIES
    def createMainToolBar(self):
        fileToolBar = self.addToolBar("MainToolBar")
        fileToolBar.setMovable(False)
        fileToolBar.addSeparator()
        perkpoints_label = QLabel(f"{PERKPOINTS}/80 ", self)
        global_attributes_label = QLabel(f"{global_attributes['TOTAL']}/66 ", self)

        perkpoints_label.setFont(NUMFONT)
        global_attributes_label.setFont(NUMFONT)
        global_attributes_label.setStyleSheet("color: #29ffff")
        self.perklabel = perkpoints_label
        self.attrlabel = global_attributes_label

        # fileToolBar.addWidget(global_attributes_label)
        # fileToolBar.addSeparator()
        # fileToolBar.addWidget(perkpoints_label)
        # fileToolBar.addSeparator()
        
        infoLayout = QHBoxLayout()
        infoLayout.addWidget(global_attributes_label)
        infoLayout.addWidget(perkpoints_label)
        infoLabel = QLabel()
        infoLabel.setLayout(infoLayout)
        infoLabel.setMinimumWidth(300)
        infoLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        fileToolBar.addWidget(infoLabel)

        fileToolBar.addAction(self.attributeAction)
        fileToolBar.addAction(self.cyberwareAction)
        fileToolBar.addAction(self.equipmentAction)
        fileToolBar.addAction(self.statsAction)

        fileToolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        fileToolBar.setIconSize(QSize(50,50))
        fileToolBar.setFixedHeight(65)
        fileToolBar.setStyleSheet("background-color: #4c1015; color: #ffd540; border: none")

        # FUNCTIONALITY THAT UPDATES THE TOOLBAR LABELS WHEN ATTR OR PERK POINTS ARE SPENT
    def updateLabels(self):
        self.perklabel.setText(f"{PERKPOINTS}/80 ")
        self.attrlabel.setText(f"{global_attributes['TOTAL']}/66 ")

        # ACTIONS FOR THE MENU/TOOLBAR BUTTONS
    def createActions(self):
        # Menu bar actions
        self.saveFileAction = QAction("Save File", self)
        self.saveFileAction.triggered.connect(self.save)
        self.openFileAction = QAction("Open File", self)
        self.openFileAction.triggered.connect(self.openFile)
        self.enterCodeAction = QAction("Enter Code", self)
        self.enterCodeAction.triggered.connect(self.enterCodePopup)
        self.copyCodeAction = QAction("Copy Code", self)
        self.copyCodeAction.triggered.connect(self.save)

        # Tool bar actions
        self.attributeAction = QAction(QIcon(imagespath + "attribute-icon.png"), "Attributes", self)
        self.attributeAction.setIconText(" Attributes")
        self.attributeAction.setFont(HEADERFONT)
        self.attributeAction.triggered.connect(self.attributeScreen)

        self.cyberwareAction = QAction(QIcon(imagespath + "cyberware-icon.png"), "Cyberware", self)
        self.cyberwareAction.setIconText(" Cyberware")
        self.cyberwareAction.setFont(HEADERFONT)
        self.cyberwareAction.triggered.connect(self.cyberwareScreen)

        self.equipmentAction = QAction(QIcon(imagespath + "equipment-icon.png"), "Equipment", self)
        self.equipmentAction.setIconText(" Equipment")
        self.equipmentAction.setFont(HEADERFONT)
        self.equipmentAction.triggered.connect(self.equipmentScreen)

        self.statsAction = QAction(QIcon(imagespath + "stat-icon.png"), "Stats", self)
        self.statsAction.setIconText(" Stats Overview")
        self.statsAction.setFont(HEADERFONT)
        self.statsAction.triggered.connect(self.statScreen)


                                                                                # ATTRIBUTES
        # THE SCREEN USED FOR THE ATTRIBUTE SELECTION
    def attributeScreen(self):
        attrWidget = QWidget(self)
        attrWidget.setStyleSheet("background-color: #31181e")
        attrLayout = QGridLayout(attrWidget)

        body = self.aScreenattr("body", "BODY")
        refl = self.aScreenattr("refl", "REFLEXES")
        tech = self.aScreenattr("tech", "TECH")
        inte = self.aScreenattr("inte", "INTELLIGENCE")
        cool = self.aScreenattr("cool", "COOL")
        attrLayout.addWidget(body, 0, 0)
        attrLayout.addWidget(refl, 0, 1)
        attrLayout.addWidget(tech, 0, 2)
        attrLayout.addWidget(inte, 0, 3) 
        attrLayout.addWidget(cool, 0, 4)

        skillList = SKILLLIST
        c1 = 0
        for dictionary in skillList:
            label = QLabel()
            label.setWordWrap(True)
            label.setAlignment(Qt.AlignTop)
            name = dictionary.get('name', '')
            levels = dictionary.get('levels', {})
            progressedBy = dictionary.get('progressedBy', '')

            namestr = f"<font color = #29ffff><h1><b>{name}</b></h1></font>"
            skillsstr = ""
            skillsstr += namestr
            c2 = 0
            for skill in levels:
                evenColor = "#fdd83f"
                unevenColor = "#a68a2a"
                color = unevenColor
                if c2 % 2 == 0:
                    color = evenColor
                tempstr = f"<b><font color = {color}>{levels[c2].strip()}"
                skillsstr += tempstr
                c2 += 1


            progBystr = f"<font color = #ff6158><h3>Progressed By: {progressedBy}"
            skillsstr += progBystr
            textfont = TEXTFONT
            textfont.setPointSize(8)
            label.setText(skillsstr)
            label.setFont(textfont)
            label.setStyleSheet("background-color: #1d0e12")
            label.setContentsMargins(10,10,10,10)
            attrLayout.addWidget(label, 1, c1)
            c1 += 1


        attrWidget.setLayout(attrLayout)
        self.setCentralWidget(attrWidget)

        # FUNC THAT FILLS IN THE TOP LABELS WITH THE CORRECT ATTRIBUTES
    def aScreenattr(self, attributestr, attribute):
        attributeList = ["body", "refl", "tech", "inte", "cool"]
        screenList = [self.bodyPerkScreen, self.reflexesPerkScreen, self.techPerkScreen, self.intelligencePerkScreen, self.coolPerkScreen]

        mALayout = QVBoxLayout()

        topWidget = QLabel()
        attributeCode = attributestr[:4].lower()
        self.addImageToWidget(topWidget, f"{attributeCode}-attr-button.png")
        topWidget.setMinimumHeight(100)

        midWidget1 = QLabel()
        midWidget1.setText(f"<h1>{global_attributes[attribute]}</h1>")
        self.attribute_labels[attribute] = midWidget1
        midWidget1.setStyleSheet("color: #29ffff")
        midWidget1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        numfont = NUMFONT
        numfont.setPointSize(40)
        midWidget1.setFont(numfont)

        midWidgetLeft = QVBoxLayout()
        attrPointDown = QPushButton()
        attrPointDown.setText(f"-")
        attrPointDown.setStyleSheet("background-color: #31181e; color: #29ffff")
        attrPointDown.clicked.connect(lambda: self.updateAttribute(attribute, self.attrDownClick))
        attrPointDown.setFont(HEADERFONT)
        midWidgetLeft.addWidget(attrPointDown)
        midWidgetLeftContainer = QWidget()
        midWidgetLeftContainer.setLayout(midWidgetLeft)

        attrPointUp = QPushButton()
        attrPointUp.setText(f"+")
        attrPointUp.setStyleSheet("background-color: #31181e; color: #29ffff")
        attrPointUp.clicked.connect(lambda: self.updateAttribute(attribute, self.attrUpClick))
        attrPointUp.setFont(HEADERFONT)

        midWidgetRight = QVBoxLayout()
        midWidgetRight.addWidget(attrPointUp)
        midWidgetRightContainer = QWidget()
        midWidgetRightContainer.setLayout(midWidgetRight)

        midWidget2 = QHBoxLayout()
        midWidget2.addWidget(midWidgetLeftContainer)
        midWidget2.addWidget(midWidgetRightContainer)
        midWidget2Container = QWidget()
        midWidget2Container.setLayout(midWidget2)

        screen = None 
        c = 0
        for element in attributeList:
            if attributestr == element:
                screen = screenList[c]
                break 
            c += 1

        if screen is None:
            screen = self.attributeScreen()

        bottomWidget = QPushButton()
        icon = QIcon(imagespath+"perk-points.png")
        bottomWidget.setIcon(icon)
        bottomWidget.setIconSize(QSize(150,40))
        bottomWidget.clicked.connect(functools.partial(screen))

        QApplication.processEvents()
        
        mALayout.addWidget(topWidget)
        mALayout.addWidget(midWidget1)
        mALayout.addWidget(midWidget2Container)
        mALayout.addWidget(bottomWidget)
        label = QLabel()
        label.setLayout(mALayout)
        label.setStyleSheet("background-color: #271318")
        return label
    

        # FUNCTION THAT UPDATES THE ATTRIBUTES (AND THE TOOLBAR LABELS) WHEN ADJUSTING A VAL
    def updateAttribute(self, attribute, update_function):
        global global_attributes
        current_value = global_attributes[attribute]
        updated_value = update_function(current_value)
        global_attributes[attribute] = updated_value
        spent_attr = 0
        attributeList = ["BODY", "REFLEXES", "TECH", "INTELLIGENCE", "COOL"]
        for i in range(5):
            points = global_attributes[attributeList[i]] - 3
            spent_attr += points
        global_attributes["TOTAL"] = 66 - spent_attr
        self.updateLabels()
        self.attribute_labels[attribute].setText(f"<h1>{global_attributes[attribute]}</h1>")
        QApplication.processEvents()

        # FUNC FOR PRESSING THE + BUTTON
    def attrUpClick(self, current_value):
        if current_value != 20 and global_attributes["TOTAL"] > 0:
            return current_value + 1
        return current_value
        
        # FUN FOR PRESSING THE - BUTTON
    def attrDownClick(self, current_value):
        if current_value != 3:
            return current_value - 1
        return current_value

        # ADDS AN IMAGE TO A WIDGET
    def addImageToWidget(self, widget, imageName):
        pixmap = QPixmap(imagespath + imageName)
        label = QLabel()
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignBottom) 
        widget.setLayout(QVBoxLayout())
        widget.layout().addWidget(label) 
        

        # FUNCTION FOR THE BODY PERKS
    def bodyPerkScreen(self):
        bodyPerkWidget = QWidget(self)
        bodyPerkWidget.setStyleSheet("background-color: #1c0005")
        bodyPerkLayout = QGridLayout(bodyPerkWidget)

        perks = [
            ("shotgunDDD", 5, BODYPERKS[0]),
            ("shotgunSO", 5, BODYPERKS[1]),
            ("healthPK", 5, BODYPERKS[2]),
            ("healthAR", 5, BODYPERKS[3]),
            ("meleeWB", 5, BODYPERKS[4]),
            ("meleeQ", 5, BODYPERKS[5]),
            ("bodySpecial", 5, BODYPERKS[6])
        ]
        column = 1
        for perkName, cellNum, perkList in perks:
            perkLabel = QLabel()
            perkLabel.setStyleSheet(f"background-color: #31181e")
            self.perkLabelFill(perkLabel, cellNum, perkList, global_attributes["BODY"], BODYPERKS, column, "body")
            column += 1
            bodyPerkLayout.addWidget(perkLabel, column % 2, int(column/2))

        bodyPerkWidget.setLayout(bodyPerkLayout)
        self.setCentralWidget(bodyPerkWidget)

        # FUNCTION FOR THE REFLEXES PERK (NEARLY IDENTICAL TO THE ONE FOR THE BODY PERKS)
    def reflexesPerkScreen(self):
        reflexPerkWidget = QWidget(self)
        reflexPerkWidget.setStyleSheet("background-color: #1c0005")
        reflexPerkLayout = QGridLayout(reflexPerkWidget)

        perks = [
            ("arsmgRRR", 5, REFLEXESPERKS[0]),
            ("arsmgSS", 5, REFLEXESPERKS[1]),
            ("movementS", 5, REFLEXESPERKS[2]),
            ("movementD", 5, REFLEXESPERKS[3]),
            ("movementAD", 5, REFLEXESPERKS[4]),
            ("bladesLaS", 5, REFLEXESPERKS[5]),
            ("bladesFB", 5, REFLEXESPERKS[6]),
            ("reflexesSpecial", 5, REFLEXESPERKS[7])
        ]
        column = 1
        for perkName, cellNum, perkList in perks:
            perkLabel = QLabel()
            perkLabel.setStyleSheet(f"background-color: #31181e")
            self.perkLabelFill(perkLabel, cellNum, perkList, global_attributes["REFLEXES"], REFLEXESPERKS, column, "refl")
            column += 1
            reflexPerkLayout.addWidget(perkLabel, column % 2, int(column/2))

        reflexPerkWidget.setLayout(reflexPerkLayout)
        self.setCentralWidget(reflexPerkWidget)

    def techPerkScreen(self):
        techPerkWidget = QWidget(self)
        techPerkWidget.setStyleSheet("background-color: #1c0005")
        techPerkLayout = QGridLayout(techPerkWidget)

        perks = [
            ("itemsGFW", 5, TECHPERKS[0]),
            ("itemsHF", 5, TECHPERKS[1]),
            ("itemsP", 5, TECHPERKS[2]),
            ("cyberwareATC", 6, TECHPERKS[3]),
            ("cyberwareLTC", 5, TECHPERKS[4]),
            ("techB", 5, TECHPERKS[5]),
            ("techSpecial", 5, TECHPERKS[6])
        ]
        column = 1
        for perkName, cellNum, perkList in perks:
            perkLabel = QLabel()
            perkLabel.setStyleSheet(f"background-color: #31181e")
            self.perkLabelFill(perkLabel, cellNum, perkList, global_attributes["TECH"], TECHPERKS, column, "tech")
            column += 1
            techPerkLayout.addWidget(perkLabel, column % 2, int(column/2))

        techPerkWidget.setLayout(techPerkLayout)
        self.setCentralWidget(techPerkWidget)

    def intelligencePerkScreen(self):
        intelligencePerkWidget = QWidget(self)
        intelligencePerkWidget.setStyleSheet("background-color: #1c0005")
        intelligencePerkLayout = QGridLayout(intelligencePerkWidget)

        perks = [
            ("queueEitS", 5, INTELLIGENCEPERKS[0]),
            ("queueHQ", 5, INTELLIGENCEPERKS[1]),
            ("queueQA", 5, INTELLIGENCEPERKS[2]),
            ("quickhacksO", 5, INTELLIGENCEPERKS[3]),
            ("quickhacksEE", 5, INTELLIGENCEPERKS[4]),
            ("quickhacksO", 5, INTELLIGENCEPERKS[5]),
            ("smartAS", 7, INTELLIGENCEPERKS[6]),
            ("intelligenceSpecial", 5, INTELLIGENCEPERKS[7])
        ]
        column = 1
        for perkName, cellNum, perkList in perks:
            perkLabel = QLabel()
            perkLabel.setStyleSheet(f"background-color: #31181e")
            self.perkLabelFill(perkLabel, cellNum, perkList, global_attributes["INTELLIGENCE"], INTELLIGENCEPERKS, column, "inte")
            column += 1
            intelligencePerkLayout.addWidget(perkLabel, column % 2, int(column/2))

        intelligencePerkWidget.setLayout(intelligencePerkLayout)
        self.setCentralWidget(intelligencePerkWidget)
        
    def coolPerkScreen(self):
        coolPerkWidget = QWidget(self)
        coolPerkWidget.setStyleSheet("background-color: #1c0005")
        coolPerkLayout = QGridLayout(coolPerkWidget)

        perks = [
            ("precisionF", 5, COOLPERKS[0]),
            ("precisionD", 5, COOLPERKS[1]),
            ("stealthFF", 5, COOLPERKS[2]),
            ("stealthN", 5, COOLPERKS[3]),
            ("stealthKI", 5, COOLPERKS[4]),
            ("throwableSS", 5, COOLPERKS[5]),
            ("throwableJ", 5, COOLPERKS[6]),
            ("coolSpecial", 5, COOLPERKS[7])
        ]
        column = 1
        for perkName, cellNum, perkList in perks:
            perkLabel = QLabel()
            perkLabel.setStyleSheet(f"background-color: #31181e")
            self.perkLabelFill(perkLabel, cellNum, perkList, global_attributes["COOL"], COOLPERKS, column, "cool")
            column += 1
            coolPerkLayout.addWidget(perkLabel, column % 2, int(column/2))

        coolPerkWidget.setLayout(coolPerkLayout)
        self.setCentralWidget(coolPerkWidget)

        # FILL EACH OF THE PERK LABELS WITH THE CORRECT PERK INFO
    def perkLabelFill(self, label, cellNum, perkList, attr, attrPerks, column, name):
        labelLayout = QGridLayout()
        subPerkLayout = QGridLayout()
        subPerkLayout.setContentsMargins(0,0,0,0)

        for i in range(cellNum):
            try:
                strList = self.perkStrList(str(perkList[i]))
                cell = QPushButton()
                inBlabel = QLabel()
                sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
                cell.setSizePolicy(sizePolicy)
                if i == 0:
                    inBlabel.setText(f"<font color = #29ffff><h1><b>{strList[0]}</b></h1><b><font color = #34cacd>Requires: {strList[3]}</b><br><b><font color = #ff5e55>{strList[1]}</font></b><h4><font color = #ffffff>{strList[2]}</font></h4>")
                elif len(strList) > 3 and "none" not in strList[3].lower():
                    inBlabel.setText(f"<font color = #ffd540><h2><b>{strList[0]}</b></h2><b><font color = #34cacd>Requires: {strList[3]}")
                else:
                    inBlabel.setText(f"<font color = #ffd540><h2><b>{strList[0]}")
                for perk in SPECIALPERKS:
                    if strList[0] in perk:
                        inBlabel.setText(f"<font color = #bef75a><h2><b>{strList[0]}</b></h2><b><font color = #34cacd>Requires: {strList[3]}")
                string = ""
                if "none" not in strList[3].lower():
                    string = f"<body style = margin: 5px><body style = background-color: #31181e><font color = #29ffff><h1><b>{strList[0]}</b></h1><b><font color = #34cacd>Requires: {strList[3]}</b><br><b><font color = #ff5e55>{strList[1]}</font></b><h4><font color = #ffffff>{strList[2]}</font></h4>"
                else:
                    string = f"<body style = margin: 5px><body style = background-color: #31181e><font color = #29ffff><h1><b>{strList[0]}</b></h1><b><font color = #ff5e55>{strList[1]}</font></b><h4><font color = #ffffff>{strList[2]}</font></h4>"
  

                for perk in SPECIALPERKS:
                    if strList[0] in perk:
                        string = f"<font color = #bef75a><h2><b>{strList[0]}</b></h2><b><font color = #34cacd>Requires: {strList[3]}</b><br><b><font color = #ff5e55>{strList[1]}</font></b><h4><font color = #ffffff>{strList[2]}</font></h4>"


                inBlabel.setToolTip(string)
                valid = False
                if attr >= perkList[i].unlocklvl:
                    if "none" in perkList[i].precedingperk.lower():
                        if perkList[0].level == perkList[0].maxlvl or i == 0:
                            valid = True
                    else:
                        for perks in attrPerks:
                            for perk in perks:
                                if perkList[i].precedingperk in perk.name or perk.name in perkList[i].precedingperk:
                                    if perk.level == perk.maxlvl:
                                        valid = True
                if valid == False:
                    cell.setStyleSheet("background-color: #1c0005")

                inBlabel.setStyleSheet("QToolTip { background-color: #31181e; border: 1px solid #271318} ")
                inBlabel.setAlignment(Qt.AlignCenter)
                inBlabel.setWordWrap(True)

                layout = QVBoxLayout(cell)
                layout.addWidget(inBlabel)
                cell.setLayout(layout)

                if perkList[i].level == perkList[i].maxlvl:
                    cell.setStyleSheet(f"background-color: #df9b2f")
                elif perkList[i].level == 2:
                    cell.setStyleSheet(f"background-color: #744d1d")
                elif perkList[i].level == 1:
                    cell.setStyleSheet(f"background-color: #631b1e")
                
                cell.clicked.connect(functools.partial(self.perkButtonClick, perkList[i], perkList, cell, attr, attrPerks, name))
                inBlabel.mousePressEvent = functools.partial(self.inBlabelClick, perkList[i], perkList, cell, attr, attrPerks, name)

                QApplication.processEvents()
            except IndexError:
                cell = QLabel()

            if i == 0:
                labelLayout.addWidget(cell, 0, 0)
            else:
                subPerkLayout.addWidget(cell, int((i-1)/2), ((i-1) % 2))
            subPerkLabel = QLabel()
            subPerkLabel.setLayout(subPerkLayout)
            labelLayout.addWidget(subPerkLabel, 1,0)

        label.setLayout(labelLayout)
        windowSize = WINDOW.size()
        windowHeight = windowSize.height()
        label.setMaximumHeight(int((windowHeight/2)-50))

        # FUNC FOR PRESSING IN A LABEL
    def inBlabelClick(self, perkList, cell, fullList, attr, attrPerks, name, event):
        if event.button() == Qt.LeftButton:
            self.perkButtonClick(perkList, cell, fullList, attr, attrPerks, name)

        # FUNC FOR CREATING THE PROPER STRING FOR PERK LABELS
    def perkStrList(self, perk):
        perkStrList = []
        tempstr = ""
        splits = perk.split("&")
        for i in range(len(splits)):
            tempstr = ""
            for char in splits[i]:
                if char == "#":
                    tempstr = tempstr + " \n "
                else:
                    tempstr = tempstr + char
            perkStrList.append(tempstr)
        return perkStrList
                

        # FUNC FOR WHAT HAPPENS WHEN YOU CLICK THE ACTUAL PERK BUTTON
    def perkButtonClick(self, perkData, perkList, cell, attr, attrPerks, name):
        global PERKPOINTS
        firstPerk = perkList[0]
        validPerk = False
        for list in attrPerks:
            for perk in list:
                precPerktemp = perkData.precedingperk.lower()
                precPerk = precPerktemp.strip()
                if precPerk in perk.name.lower():
                    if perk.level == perk.maxlvl:
                        validPerk = True
                elif "none" in perkData.precedingperk.lower():
                    validPerk = True
        if perkData.level < perkData.maxlvl and perkData.unlocklvl <= attr and validPerk == True and PERKPOINTS != 0:
            if firstPerk == perkData or firstPerk.level == firstPerk.maxlvl or perkData in SPECIALPERKS:
                perkData.level += 1
                PERKPOINTS = PERKPOINTS - 1
                self.updateLabels()
                if perkData.level != perkData.maxlvl:
                    if perkData.level == 2:
                        cell.setStyleSheet("background-color: #744d1d;")
                    else:
                        cell.setStyleSheet("background-color: #631b1e;")
                else:
                    cell.setStyleSheet("background-color: #df9b2f;")
        elif perkData.level == perkData.maxlvl:
            if firstPerk == perkData and firstPerk not in SPECIALPERKS:
                perkScore = 0
                for perk in perkList:
                    if perk.level > 0 and perk != perkList[0]:
                        perkScore = 1
                if perkScore == 0:
                    perkData.level = 0
                    cell.setStyleSheet("background-color: #31181e;")  
                    PERKPOINTS = PERKPOINTS + perkData.maxlvl
                    self.updateLabels()       
            else:
                perkData.level = 0
                PERKPOINTS = PERKPOINTS + perkData.maxlvl
                self.updateLabels()
                cell.setStyleSheet("background-color: #31181e;")

        match name:
            case "body":
                self.bodyPerkScreen()
            case "refl":
                self.reflexesPerkScreen()
            case "tech":
                self.techPerkScreen()
            case "inte":
                self.intelligencePerkScreen()
            case "cool":
                self.coolPerkScreen()
                                                                                                #CYBERWARE
                
    def cyberwareScreen(self):
        global CYBERWARECOST
        CWLayout = QGridLayout()

        cyberwareLeft = QVBoxLayout()
        cyberwareLeft.setContentsMargins(0,0,0,0)
        windowSize = WINDOW.size()
        windowWidth = windowSize.width()
        
        frontalcortex = QVBoxLayout()
        frontalcortex.addWidget(self.cyberwareLabelFill(3,"left", "frontal-cortex.txt"))
        frontalcortexLabel = QLabel()
        frontalcortexLabel.setLayout(frontalcortex)
        cyberwareLeft.addWidget(frontalcortexLabel)

        arms = QVBoxLayout()
        arms.addWidget(self.cyberwareLabelFill(1,"left", "arms.txt"))
        armsLabel = QLabel()
        armsLabel.setLayout(arms)
        cyberwareLeft.addWidget(armsLabel)

        skeleton = QVBoxLayout()
        skeleton.addWidget(self.cyberwareLabelFill(3,"left", "skeleton.txt"))
        skeletonLabel = QLabel()
        skeletonLabel.setLayout(skeleton)
        cyberwareLeft.addWidget(skeletonLabel)

        nervousSystem = QVBoxLayout()
        nervousSystem.addWidget(self.cyberwareLabelFill(3,"left", "nervous-system.txt"))
        nervousSystemLabel = QLabel()
        nervousSystemLabel.setLayout(nervousSystem)
        cyberwareLeft.addWidget(nervousSystemLabel)

        integumentary = QVBoxLayout()
        integumentary.addWidget(self.cyberwareLabelFill(3,"left", "integumentary-system.txt"))
        integumentaryLabel = QLabel()
        integumentaryLabel.setLayout(integumentary)
        cyberwareLeft.addWidget(integumentaryLabel)

        infoWidget = QHBoxLayout()
        cyberwareArmor = 0
        cyberwareCost = 0
        cyberwarePercentIncrease = 1
        for cyberware in ACTIVECYBERWARE:
            cyberwareArmor += int(cyberware.armor)
            cyberwareCost += int(cyberware.cost)
            if hasattr(cyberware, "pasEff") and "armor" in cyberware.pasEff.lower():
                effects = cyberware.pasEff.split(",")
                for effect in effects:
                    if "armor" in effect.lower():
                        numstr = ""
                        for char in effect:
                            if char in "0123456789":
                                numstr += char
                        if numstr == "":
                            cyberwareArmor += 0
                        elif "%" in effect:
                            cyberwarePercentIncrease += (int(numstr)/100)
                        else:
                            cyberwareArmor += int(numstr)
        cyberwareArmor = round(cyberwareArmor * cyberwarePercentIncrease)
        CYBERWARECOST = cyberwareCost
        costWidget = QLabel(f"<font color = #ffd741><h1>{cyberwareCost}")
        costWidget.setToolTip(f"Your Cyberware Cost.")
        costWidget.setStyleSheet("background-color: #31181e")
        costWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        numFont = NUMFONT
        numFont.setPointSize(30)
        costWidget.setFont(numFont)
        self.costWidget = costWidget
        armorWidget = QLabel(f"<font color = #29ffff><h1>{cyberwareArmor}")
        armorWidget.setToolTip(f"Your Cyberware Armor.<br>Only base Armor from Cyberware is added to this stat.<br>Check the Stats screen to see your total Armor.")
        armorWidget.setStyleSheet("background-color: #31181e")
        armorWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        armorWidget.setFont(numFont)
        self.armorWidget = armorWidget
        infoWidget.addWidget(costWidget)
        infoWidget.addWidget(armorWidget)
        infoWidgetLabel = QLabel()
        infoWidgetLabel.setMaximumHeight(200)
        infoWidgetLabel.setLayout(infoWidget)

        cyberwareLeftLabel = QLabel()
        cyberwareLeftLabel.setStyleSheet("background-color: #271318")
        cyberwareLeftLabel.setLayout(cyberwareLeft)
        cyberwareLeftLabel.setMinimumWidth(int(windowWidth/4.5))

        cyberwareMidWidget = QVBoxLayout()
        cyberwareMiddle = QLabel()
        cyberwareMiddle.setContentsMargins(0,0,0,0)
        icon = QIcon(imagespath + "edgerunner-upscaled.png")
        windowSize = WINDOW.size()
        cyberwareMiddle.setPixmap(icon.pixmap(int(windowSize.width()/4.5), windowSize.height()))
        cyberwareMiddle.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter) 
        cyberwareMidWidget.addWidget(cyberwareMiddle)
        cyberwareMidWidget.addWidget(infoWidgetLabel)
        cyberwareMidLabel = QLabel()
        cyberwareMidLabel.setMinimumWidth(int(windowSize.width()/4.5))
        cyberwareMidLabel.setLayout(cyberwareMidWidget)
        
        cyberwareRight = QVBoxLayout()
        cyberwareRight.setContentsMargins(0,0,0,0)
        
        operatingSystem = QVBoxLayout()
        operatingSystem.addWidget(self.cyberwareLabelFill(1,"right", "operating-system.txt"))
        operatingSystemLabel = QLabel()
        operatingSystemLabel.setLayout(operatingSystem)
        cyberwareRight.addWidget(operatingSystemLabel)

        face = QVBoxLayout()
        face.addWidget(self.cyberwareLabelFill(1,"right", "face.txt"))
        faceLabel = QLabel()
        faceLabel.setLayout(face)
        cyberwareRight.addWidget(faceLabel)

        hands = QVBoxLayout()
        hands.addWidget(self.cyberwareLabelFill(1,"right", "hands.txt"))
        handsLabel = QLabel()
        handsLabel.setLayout(hands)
        cyberwareRight.addWidget(handsLabel)

        circulatory = QVBoxLayout()
        circulatory.addWidget(self.cyberwareLabelFill(3,"right", "circulatory-system.txt"))
        circulatoryLabel = QLabel()
        circulatoryLabel.setLayout(circulatory)
        cyberwareRight.addWidget(circulatoryLabel)

        legs = QVBoxLayout()
        legs.addWidget(self.cyberwareLabelFill(1,"right", "legs.txt"))
        legsLabel = QLabel()
        legsLabel.setLayout(legs)
        cyberwareRight.addWidget(legsLabel)

        cyberwareRightLabel = QLabel()
        cyberwareRightLabel.setStyleSheet("background-color: #271318")
        cyberwareRightLabel.setMinimumWidth(int(windowWidth/4.5))
        cyberwareRightLabel.setLayout(cyberwareRight)

        cyberwareSelection = QVBoxLayout()
        self.cyberwareSelection = cyberwareSelection
        cyberwareSelection.setContentsMargins(0,0,0,0)
        cyberwareSelectionLabel = QLabel()
        cyberwareSelectionLabel.setText("")
        cyberwareSelectionLabel.setStyleSheet("background-color: #271318")
        cyberwareSelectionLabel.setLayout(cyberwareSelection)
        

        CWLayout.addWidget(cyberwareLeftLabel, 0, 0)
        CWLayout.addWidget(cyberwareMidLabel, 0, 1)
        CWLayout.addWidget(cyberwareRightLabel, 0, 2)
        CWLayout.addWidget(cyberwareSelectionLabel, 0, 3)

        cyberware = QLabel()
        cyberware.setStyleSheet("background-color: #31181e")
        cyberware.setLayout(CWLayout)
        self.setCentralWidget(cyberware)

    def updateCWValues(self):
        cyberwareArmor = 0
        cyberwareCost = 0
        for cyberware in ACTIVECYBERWARE:
            cyberwareArmor += int(cyberware.armor)
            CybNode = TECHPERKS[3]
            if CybNode[0].level == 2 and ("skeleton" in cyberware.filename or "integumentary" in cyberware.filename):
                cyberwareCost += int(round(float(cyberware.cost) * 0.8))
            else:
                cyberwareCost += int(cyberware.cost)

        self.costWidget.setText(f"<font color = #ffd741><h1>{cyberwareCost}")
        self.armorWidget.setText(f"<font color = #29ffff><h1>{cyberwareArmor}")
        
    def cyberwareLabelFill(self, slots, alignment, file, preselected=ACTIVECYBERWARE):
        preselected = ACTIVECYBERWARE
        buttonLayout = QHBoxLayout()
        if "skeleton" in file:
            LTCNode = TECHPERKS[4]
            if LTCNode[0].level == LTCNode[0].maxlvl:
                slots = 3
            else:
                slots = 2
        if "hand" in file:
            LTCNode = TECHPERKS[4]
            if LTCNode[3].level == LTCNode[3].maxlvl:
                slots = 2
            else:
                slots = 1
        if alignment:
            alreadyEntered = []
            for i in alreadyEntered:
                alreadyEntered.remove(i)
            for c in range(slots):
                buttonFound = False
                # Check if the current file matches any preselected cyberware
                for preselect in preselected:
                    if preselect.filename == file and preselect.name not in alreadyEntered:
                        button = QPushButton()
                        icon = QIcon(f"{imagespath}cyberware/{preselect.imgname}")
                        button.setIcon(icon)
                        windowSize = WINDOW.size()
                        iconSize = QSize(int(windowSize.width() / 14), int(windowSize.width() / 14))
                        button.setIconSize(iconSize)
                        button.setStyleSheet("background-color: #391c23; border: 5px solid #5c211f")
                        if "Iconic" in preselect.description:
                            button.setStyleSheet("background-color: #6f510b; border: 5px solid #ffd842")
                            tempdescription = preselect.description.split(";")[1]
                        else:
                            button.setStyleSheet("background-color: #391c23; border: 5px solid #5c211f")
                            tempdescription = preselect.description
                        description = ""
                        description = ""
                        if file != "arms.txt" and "," in preselect.attunement:
                            attunementTexts = preselect.attunement.split(",")
                            attunementNum = 0
                            counter = 0
                            attunementStr = ""
                            for char in attunementTexts[1]:
                                if char in "0123456789.":
                                    attunementStr += char
                                    lastNum = counter
                                if char in "%":
                                    lastNum == counter
                                counter += 1
                            attunementNum += float(attunementStr)
                            match attunementTexts[0]:
                                case 'body':
                                    attunementNum = attunementNum * global_attributes["BODY"]
                                case 'refl':
                                    attunementNum = attunementNum * global_attributes["REFLEXES"]
                                case 'tech':
                                    attunementNum = attunementNum * global_attributes["TECH"]
                                case 'int':
                                    attunementNum = attunementNum * global_attributes["INTELLIGENCE"]
                                case 'cool':
                                    attunementNum = attunementNum * global_attributes["COOL"]
                            attunementNumText = ""
                            if '+' in attunementTexts[1]:
                                attunementNumText += "+"
                            elif '-' in attunementTexts[1]:
                                attunementNumText += "-"
                            attunementNumText += str(round(attunementNum, 2))
                            if '%' in attunementTexts[1]:
                                attunementNumText += '%'
                            tempdescription += f"<br><br><font color = #e0ff5e>Attunement:<br><b>{preselect.attunement.title()} per Attribute point.<br>Current: {attunementNumText}</b></font>"
                        validchar = True
                        for char in tempdescription:
                            if char in "<":
                                validchar = False
                            elif char in ">":
                                validchar = True
                            if char in " 1234567890%+-" and validchar == True:
                                description += f"<font color = #29ffff>{char}</font>"
                            else:
                                description += char
                        CWArmorText = ""
                        if preselect.armor != 0:
                            CWArmorText = f"<font color = #ffffff> / <font color = #29ffff>Armor: {preselect.armor}</font>"
                        cyberdeckText = ""
                        if "cyberdeck" in preselect.name.lower():
                            cyberdeckText = f"<font color = #ffffff> / <font color = #29ffff>RAM: {preselect.ram}<font color = #ffffff> / <font color = #29ffff>Slots: {preselect.QHslots}<font color = #ffffff> / <font color = #dbfa5c>Buffer: {preselect.buffer}</font></font>"
                        button.setToolTip(f"<body style = margin: 10px;><font color = #ff6158><h2>{preselect.name}</h2></font><font color = #ffd642><h3>Cost: {preselect.cost}{CWArmorText}{cyberdeckText}</h3><font color = #ffffff><b>{description}")
                        buttonFound = True
                        alreadyEntered.append(preselect.name)
                        break
                if buttonFound != True:
                    # Create buttons for non-preselected cyberware
                    button = QPushButton()
                    icon = QIcon(f"{imagespath}cyberware/cyberwareicon")
                    button.setIcon(icon)
                    buttonSize = button.size()
                    button.setIconSize(QSize(int(buttonSize.width()*0.9), int(buttonSize.height()*0.9)))
                    button.setStyleSheet("background-color: #1d0e11")
                    currentCW = None
                    CWBUTTONLIST.append([button, file, c, currentCW])
                button.clicked.connect(functools.partial(self.cyberwareButtonColor, file, c, button))
                buttonLayout.addWidget(button)
        label = QLabel()
        label.setLayout(buttonLayout)
        return label

    def cyberwareButtonColor (self, file, index, button):
        exceptionList = []
        for b in CWBUTTONLIST:
            try:
                if b[3]:
                    if "iconic" in b[3].description.lower():
                        b[0].setStyleSheet("background-color: #6f510b; border: 5px solid #ffd842")
                    else:
                        b[0].setStyleSheet("background-color: #391c23; border: 5px solid #5c211f")
                else:
                    button.setStyleSheet("background-color: #1d0e11; border: 1px solid #29ffff")
            except Exception as e:
                exceptionList.append(e)
                # Print the list when checking for errors

        self.cyberwareSelectionScreen(file, index, button)
                
    def cyberwareSelectionScreen(self, file, index, button):
        for i in reversed(range(self.cyberwareSelection.count())):
            widgetToRemove = self.cyberwareSelection.itemAt(i).widget()
            self.cyberwareSelection.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setStyleSheet("border: none")

        layout = QVBoxLayout()

        cyberwareList = cyberwarefilereader.readfile(file)
        for cyberware in cyberwareList:
            CWlayout = QHBoxLayout()
            imageButton = QPushButton()
            icon = QIcon(f"{imagespath}cyberware/{cyberware.imgname}")
            imageButton.setIcon(icon)
            imageButton.setIconSize(QSize(150,150))
            imageButton.setFixedSize(QSize(150,150))
            if "Iconic" in cyberware.description:
                imageButton.setStyleSheet("background-color: #6f510b; border: 5px solid #ffd842")
                tempdescription = cyberware.description.split(";")[1]
            else:
                imageButton.setStyleSheet("background-color: #391c23; border: 5px solid #5c211f")
                tempdescription = cyberware.description
            description = ""
            if file != "arms.txt" and "," in cyberware.attunement:
                attunementTexts = cyberware.attunement.split(",")
                attunementNum = 0
                counter = 0
                attunementStr = ""
                for char in attunementTexts[1]:
                    if char in "0123456789.":
                        attunementStr += char
                        lastNum = counter
                    if char in "%":
                        lastNum == counter
                    counter += 1
                attunementNum += float(attunementStr)
                match attunementTexts[0]:
                    case 'body':
                        attunementNum = attunementNum * global_attributes["BODY"]
                    case 'refl':
                        attunementNum = attunementNum * global_attributes["REFLEXES"]
                    case 'tech':
                        attunementNum = attunementNum * global_attributes["TECH"]
                    case 'int':
                        attunementNum = attunementNum * global_attributes["INTELLIGENCE"]
                    case 'cool':
                        attunementNum = attunementNum * global_attributes["COOL"]
                attunementNumText = ""
                if '+' in attunementTexts[1]:
                    attunementNumText += "+"
                elif '-' in attunementTexts[1]:
                    attunementNumText += "-"
                attunementNumText += str(round(attunementNum, 2))
                if '%' in attunementTexts[1]:
                    attunementNumText += '%'
                tempdescription += f"<br><br><font color = #e0ff5e>Attunement:<br><b>{cyberware.attunement.title()} per Attribute point.<br>Current: {attunementNumText}</b></font>"
            validchar = True
            for char in tempdescription:
                if char in "<":
                    validchar = False
                elif char in ">":
                    validchar = True
                if char in " 1234567890%+-" and validchar == True:
                    description += f"<font color = #29ffff>{char}</font>"
                else:
                    description += char
            if "cellular" in cyberware.name.lower():
                LTCNode = TECHPERKS[4]
                if LTCNode[1].level != LTCNode[1].maxlvl:
                    s = "<font color = #ff6158><h3>THIS CYBERWARE CAN ONLY BE USED IF THE 'Built Different' PERK IS ACTIVE.</font></h3>"
                    description = s + description
                
            CWlayout.addWidget(imageButton)
            CWArmorText = ""
            if cyberware.armor != 0:
                CWArmorText = f"<font color = #ffffff> / <font color = #29ffff>Armor: {cyberware.armor}</font>"
            cyberdeckText = ""
            if "cyberdeck" in cyberware.name.lower():
                cyberdeckText = f"<font color = #ffffff> / <font color = #29ffff>RAM: {cyberware.ram}<font color = #ffffff> / <font color = #29ffff>Slots: {cyberware.QHslots}<font color = #ffffff> / <font color = #dbfa5c>Buffer: {cyberware.buffer}</font></font>"
            label = QLabel(f"<font color = #ff6158><h2>{cyberware.name}</h2></font><font color = #ffd642><h3>Cost: {cyberware.cost}{CWArmorText}{cyberdeckText}</h3><font color = #ffffff><b>{description}")
            label.setWordWrap(True)
            imageButton.clicked.connect(functools.partial(self.cyberwareButtonClick, file, index, button, cyberware))
            CWlayout.addWidget(label)
            coverLabel = QLabel()
            coverLabel.setStyleSheet("background-color: #31181e; color: #ffffff")
            coverLabel.setLayout(CWlayout)
            layout.addWidget(coverLabel)

        scrollWidget = QWidget()
        scrollWidget.setContentsMargins(0,0,0,0)
        scrollWidget.setLayout(layout)
        scrollArea.setWidget(scrollWidget)
        scrollArea.setStyleSheet("background-color: #1c0005; border: none")

        self.cyberwareSelection.addWidget(scrollArea)

    def cyberwareButtonClick(self, file, index, button, cyberware):

        global ACTIVECYBERWARE
        valid = True
        for cw in ACTIVECYBERWARE:
            if cw.name == cyberware.name:
                valid = False
        if valid == True:
            ACTIVECYBERWARE.append(cyberware)
            for item in CWBUTTONLIST:
                if item[1] == file and item[2] == index:
                    for i in ACTIVECYBERWARE:
                        if i == item[3]:
                            ACTIVECYBERWARE.remove(i)
                    item[3] = cyberware
                    icon = QIcon(f"{imagespath}cyberware/{item[3].imgname}")
                    button.setIcon(icon)
                    buttonSize = button.size()
                    button.setIconSize(QSize(int(buttonSize.width()*0.9), int(buttonSize.height()*0.9)))
                    button.setFixedSize(QSize(buttonSize.width(), buttonSize.height()))
                    if "Iconic" in cyberware.description:
                        button.setStyleSheet("background-color: #6f510b; border: 5px solid #ffd842")
                        tempdescription = cyberware.description.split(";")[1]
                    else:
                        button.setStyleSheet("background-color: #391c23; border: 5px solid #5c211f")
                        tempdescription = cyberware.description
                    if file != "arms.txt" and "," in cyberware.attunement:
                        attunementTexts = cyberware.attunement.split(",")
                        attunementNum = 0
                        counter = 0
                        attunementStr = ""
                        for char in attunementTexts[1]:
                            if char in "0123456789.":
                                attunementStr += char
                                lastNum = counter
                            if char in "%":
                                lastNum == counter
                            counter += 1
                        attunementNum += float(attunementStr)
                        match attunementTexts[0]:
                            case 'body':
                                attunementNum = attunementNum * global_attributes["BODY"]
                            case 'refl':
                                attunementNum = attunementNum * global_attributes["REFLEXES"]
                            case 'tech':
                                attunementNum = attunementNum * global_attributes["TECH"]
                            case 'int':
                                attunementNum = attunementNum * global_attributes["INTELLIGENCE"]
                            case 'cool':
                                attunementNum = attunementNum * global_attributes["COOL"]
                        attunementNumText = ""
                        if '+' in attunementTexts[1]:
                            attunementNumText += "+"
                        elif '-' in attunementTexts[1]:
                            attunementNumText += "-"
                        attunementNumText += str(round(attunementNum, 2))
                        if '%' in attunementTexts[1]:
                            attunementNumText += '%'
                        tempdescription += f"<br><br><font color = #e0ff5e>Attunement:<br><b>{cyberware.attunement.title()} per Attribute point.<br>Current: {attunementNumText}</b></font>"
                    validchar = True
                    description = ""
                    for char in tempdescription:
                        if char in "<":
                            validchar = False
                        elif char in ">":
                            validchar = True
                        if char in " 1234567890%+-" and validchar == True:
                            description += f"<font color = #29ffff>{char}</font>"
                        else:
                            description += char
                    CWArmorText = ""
                    if cyberware.armor != 0:
                        CWArmorText = f"<font color = #ffffff> / <font color = #29ffff>Armor: {cyberware.armor}</font>"
                    cyberdeckText = ""
                    if "cyberdeck" in cyberware.name.lower():
                        cyberdeckText = f"<font color = #ffffff> / <font color = #29ffff>RAM: {cyberware.ram}<font color = #ffffff> / <font color = #29ffff>Slots: {cyberware.QHslots}<font color = #ffffff> / <font color = #dbfa5c>Buffer: {cyberware.buffer}</font></font>"
                    button.setToolTip(f"<body style = margin: 10px;><font color = #ff6158><h2>{cyberware.name}</h2></font><font color = #ffd642><h3>Cost: {cyberware.cost}{CWArmorText}{cyberdeckText}</h3><font color = #ffffff><b>{description}")
            self.updateCWValues()

    def equipmentScreen(self):
        global WEAPONSELECTIONLIST
            
        equipmentLayout = QGridLayout()
        equipmentLayout.setContentsMargins(0,0,0,0)

        windowSize = WINDOW.size()
        windowWidth = windowSize.width()
        windowHeight = windowSize.height()
        weaponsLayout = QGridLayout()

        w1 = self.weaponWidget(1, WEAPON1)
        self.w1 = w1
        w2 = self.weaponWidget(2, WEAPON2)
        self.w2 = w2
        w3 = self.weaponWidget(3, WEAPON3)
        self.w3 = w3
        w4 = self.weaponWidget(4, WEAPON4)
        self.w4 = w4

        WEAPONSELECTIONLIST = [self.w1, self.w2, self.w3, self.w4]
        for item in WEAPONSELECTIONLIST:
            item.setMinimumHeight(int((windowHeight-75)/2-25))

        weaponsLayout.addWidget(self.w1, 0,0)
        weaponsLayout.addWidget(self.w2, 1,0)
        weaponsLayout.addWidget(self.w3, 0,1)
        weaponsLayout.addWidget(self.w4, 1,1)
        self.weaponsLayout = weaponsLayout

        weaponLabel = QLabel()
        weaponLabel.setStyleSheet("background-color: #1c0005")
        weaponLabel.setLayout(self.weaponsLayout)
        weaponLabel.setMinimumWidth(int(windowWidth/2.25))
        equipmentLayout.addWidget(weaponLabel, 0, 0)


        filterBar = self.filterBarWidget()
        self.filterBar = filterBar
        filterBar = self.filterBar
        filterBar.setMinimumWidth(150)
        equipmentLayout.addWidget(filterBar, 0, 1)
        
        self.equipmentScreenLayout = equipmentLayout

        equipmentLabel = QLabel()
        equipmentLabel.setStyleSheet("background-color: #1c0005")
        equipmentLabel.setLayout(self.equipmentScreenLayout)

        self.setCentralWidget(equipmentLabel)

    def filterBarWidget(self):
        global SORTOPTIONLIST
        global SELECTEDSORT

        filterBarLayout = QVBoxLayout()
        
        weaponFilters = QVBoxLayout()
        weaponFilters.setContentsMargins(0,0,0,0)

        optionList = [["Pistols", "pistol"],["Revolvers","revolver"],["SMGs","SMG"],["Assault Rifles", "ar"],["Precision Rifles", "precision rifle"],["Sniper Rifles", "sniper rifle"], ["Shotguns", "shotgun"],["LMGs","LMG"],["Blades","blade"],["Blunt","blunt"],["Throwable","throwable"]]

        for weaponType in optionList:
            filterButton = QPushButton()
            filterButton.setText(f"{weaponType[0]}")
            sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            filterButton.setSizePolicy(sizePolicy)
            if weaponType[1] in SELECTEDWEAPONFILES:
                filterButton.setStyleSheet("background-color: #ffd741; color: #3b1d24; font-weight: bold; font-size: 14px")
            else:    
                filterButton.setStyleSheet("background-color: #3b1d24; color: #ffd741; font-weight: bold; font-size: 14px")
            filterButton.clicked.connect(functools.partial(self.weaponFilterButtons, weaponType[1], filterButton))
            
            weaponFilters.addWidget(filterButton)

        filterButtonLabel = QLabel()
        filterButtonLabel.setLayout(weaponFilters)
        sortOptions = QVBoxLayout()
        sortOptions.setContentsMargins(0,0,0,0)

        SORTOPTIONLIST = []
        fileOptions = []
        for i in optionList:
            fileOptions.append(i[1])
        fullSortOptionList = [["Name", "name"],["Type", "type"],["Damage","damage"],["Attack Speed","firerate"],["Reload Time","reloadSpeed"],["Effective Range","range"],["Handling","handling"],["Mag Size","magSize"],["Headshot Mult.","headshot"],["Armor Pen.","armorPen"],["Stamina Cost", "staminaCost"],["Return Time", "returnTime"]]
        tempsortOptionList = [["Name", "name"],["Type", "type"],["Damage","damage"],["Attack Speed","firerate"]]
        for file in SELECTEDWEAPONFILES:
            if fileOptions.index(file) <= 7:
                for i in range(6):
                    option = fullSortOptionList[i+4]
                    if option not in tempsortOptionList:
                        tempsortOptionList.append(option)
            elif fileOptions.index(file) > 7 and fileOptions.index(file) < 10:
                for i in range(2):
                    option = fullSortOptionList[i+9]
                    if option not in tempsortOptionList:
                        tempsortOptionList.append(option)
            elif fileOptions.index(file) == 10:
                option = fullSortOptionList[5]
                if option not in tempsortOptionList:
                    tempsortOptionList.append(option)
                for i in range(4):
                    option = fullSortOptionList[8+i]
                    if option not in tempsortOptionList:
                        tempsortOptionList.append(option)
        sortOptionList = []

        for entry in fullSortOptionList:
            if entry in tempsortOptionList:
                sortOptionList.append(entry)

        for i in fullSortOptionList:
            SORTOPTIONLIST.append(i[1])
        for sortOption in sortOptionList:
            sortButton = QPushButton()
            sortButton.setText(f"{sortOption[0]}")
            if SELECTEDSORT == fullSortOptionList.index(sortOption):
                sortButton.setStyleSheet("background-color: #29ffff; color: #3b1d24; font-weight: bold; font-size: 14px")
            else:
                sortButton.setStyleSheet("background-color: #3b1d24; color: #29ffff; font-weight: bold; font-size: 14px")
            sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            sortButton.setSizePolicy(sizePolicy)
            sortButton.clicked.connect(functools.partial(self.weaponSelectScreen, sortOption[1]))
            sortOptions.addWidget(sortButton)
        sortButtonLabel = QLabel()
        sortButtonLabel.setLayout(sortOptions)  

        filterBarLayout.addWidget(filterButtonLabel)
        filterBarLayout.addWidget(sortButtonLabel)
        filterBarLayout.setContentsMargins(0,10,0,10)

        filterBarLabel = QLabel()
        filterBarLabel.setStyleSheet("background-color: #1c0005")
        filterBarLabel.setLayout(filterBarLayout)
        
        return filterBarLabel

    def weaponFilterButtons(self, fileName, sortButton):
        global WEAPONSELECTION
        global SELECTEDWEAPONFILES

        if fileName in SELECTEDWEAPONFILES:
            SELECTEDWEAPONFILES.remove(fileName)
            WEAPONSELECTION = []
            for i in SELECTEDWEAPONFILES:
                entry = weaponfilereader.readfile(i)
                WEAPONSELECTION.append(entry)
        else:
            WEAPONSELECTION.append(weaponfilereader.readfile(fileName))
            SELECTEDWEAPONFILES.append(fileName)

        sortKey = SORTOPTIONLIST[SELECTEDSORT]
        self.weaponSelectScreen(sortKey)

    def weaponWidget(self, num, weapon):

        windowSize = WINDOW.size()
        windowWidth = windowSize.width()
        weaponLayout = QGridLayout()
        weaponLayout.setContentsMargins(10,10,10,10)
        dpsLow = 0
        dpsHigh = 0
        dpsNoReload = 0

        iconButton = QPushButton()
        if weapon == None:
            weaponIcon = QIcon(f"{imagespath}weapon-icon.png")
            weaponElem = weaponfilereader.readfile("Empty Weapon")
            weapon = weaponElem[0]
        else:
            weaponIcon = QIcon(f"{imagespath}weapons/{weapon.imgname}.png")
        iconButton.setFixedSize(QSize(int(windowWidth/9.5),200))
        iconButton.setIcon(weaponIcon)
        iconButton.setToolTip(f"<font color = #ffffff>{weapon.name}")
        if len(weapon.iconic) > 8:
            iconButton.setStyleSheet("background-color: #6f510b; border: 5px solid #ffd842")
        else:
            iconButton.setStyleSheet("background-color: #31181e; border: 5px solid #5c211f")
        iconButton.setIconSize(QSize(190,190))
        iconButton.clicked.connect(functools.partial(self.weaponNumSelect, num))
        weaponLayout.addWidget(iconButton, 0, 0)

        descriptionLabel = QLabel(f"<font color = #ffd740><b>{weapon.iconic}<br><br><font color = #ff6159>{weapon.intrinsic}")
        descriptionLabel.setWordWrap(True)
        descriptionLabel.setToolTip(f"<font color = #ffd740><b>{weapon.iconic}<br><br><font color = #ff6159>{weapon.intrinsic}")
        if num != 4:
            descriptionLabel.setStyleSheet(f"background-color: #3b1d24; border: 5px solid #3b1d24")
        else:
            descriptionLabel.setStyleSheet(f"background-color: #33191f; border: 5px solid #33191f")

        weaponLayout.addWidget(descriptionLabel, 1, 0)
        meleeWeapons = ["blade","blunt"]

        mainInfo = QGridLayout()
        mainInfo.setContentsMargins(10,0,10,10)
        weaponName = QLabel(f"<font color = #29ffff><h1>{weapon.name}")
        if num == 4:
            weaponName = QLabel(f"<font color = #29ffff><h5>Comparison/Extra Slot<h2>{weapon.name}")
        weaponName.setWordWrap(True)
        weaponType = QLabel(f"<h4><font color = #d8f75a>{weapon.type} {weapon.weaponType}")
        if weapon.weaponType in meleeWeapons:
            dpsLayout = QHBoxLayout()
            dps = round(weapon.damage * weapon.firerate)
            dpsLayout.setContentsMargins(0,0,0,0)
            dpstxt = QLabel(f"<h4><font color = #ffffff>DPS:")
            dpstxt.setToolTip("DPS = DMG * ATS<br>DMG = Damage<br>ATS = Attack Speed")
            dpsNum = QLabel(f"<h3><font color = #71bd00>{dps}")
            dpsLayout.addWidget(dpstxt)
            dpsLayout.addWidget(dpsNum)            
            dpsLabel = QLabel()
            dpsLabel.setLayout(dpsLayout)
            mainInfo.addWidget(weaponName, 0, 0)
            mainInfo.addWidget(weaponType, 1, 0)
            mainInfo.addWidget(dpsLabel, 2, 0)
        elif weapon.weaponType == "throwable":
            dpsLow = round((weapon.damage / weapon.returnTime) * 1.5)
            dpsHigh = round(weapon.damage * (1 + (weapon.headshot / 100)) * 1.5)
            dpsLowLayout = QHBoxLayout()
            dpsLowLayout.setContentsMargins(0,0,0,0)
            dpsLowTxt = QLabel(f"<h4><font color = #ffffff>DPS Low:")
            dpsLowTxt.setToolTip("DPS Low = (DMG / RTT) * 1.5 <br><br>DMG = Damage<br>RTT = Return Time<br>1.5 = Estimated Thrown Multiplier")
            dpsLowNum = QLabel(f"<h4><font color = #cfff00>{dpsLow}")
            dpsLowLayout.addWidget(dpsLowTxt)
            dpsLowLayout.addWidget(dpsLowNum)
            dpsLowLabel = QLabel()
            dpsLowLabel.setLayout(dpsLowLayout)

            dpsHighLayout = QHBoxLayout()
            dpsHighLayout.setContentsMargins(0,0,0,0)
            dpsHighTxt = QLabel(f"<h4><font color = #ffffff>DPS High:")
            dpsHighTxt.setToolTip("DPS High = DMG * (1 + (HSM / 100)) * 1.5<br><br>DMG = Damage<br>HSM = Headshot Multiplier<br>1.5 = Estimated Thrown Multiplier")
            dpsHighNum = QLabel(f"<h4><font color = #71bd00>{dpsHigh}")
            dpsHighLayout.addWidget(dpsHighTxt)
            dpsHighLayout.addWidget(dpsHighNum)
            dpsHighLabel = QLabel()
            dpsHighLabel.setLayout(dpsHighLayout)

            mainInfo.addWidget(weaponName, 0, 0)
            mainInfo.addWidget(weaponType, 1, 0)
            mainInfo.addWidget(dpsLowLabel, 2, 0)
            mainInfo.addWidget(dpsHighLabel, 3, 0)
        else:
            if weapon.magSize * weapon.firerate != 0 and weapon.reloadSpeed * weapon.firerate + weapon.magSize != 0:
                dpsLow = round(weapon.damage / ((weapon.reloadSpeed * weapon.firerate + weapon.magSize) / (weapon.magSize * weapon.firerate)))
                dpsHigh = round(dpsLow * (1 + (weapon.headshot / 100)))
            else:
                dpsLow = 0.0
                dpsHigh = 0.0
            dpsNoReload = round((weapon.damage * weapon.firerate) * (1 + (weapon.headshot / 100)))
            dpsLowLayout = QHBoxLayout()
            dpsLowLayout.setContentsMargins(0,0,0,0)
            dpsLowTxt = QLabel(f"<h4><font color = #ffffff>DPS Low:")
            dpsLowTxt.setToolTip("DPS Low = DMG / ((RLT * ATS + MZS) / (MZS * ATS)<br><br>DMG = Damage<br>RLT = Reload Time<br>ATS = Attack Speed<br>MZS = Mag. Size")
            dpsLowNum = QLabel(f"<h4><font color = #cfff00>{dpsLow}")
            dpsLowLayout.addWidget(dpsLowTxt)
            dpsLowLayout.addWidget(dpsLowNum)
            dpsLowLabel = QLabel()
            dpsLowLabel.setLayout(dpsLowLayout)

            dpsHighLayout = QHBoxLayout()
            dpsHighLayout.setContentsMargins(0,0,0,0)
            dpsHighTxt = QLabel(f"<h4><font color = #ffffff>DPS High:")
            dpsHighTxt.setToolTip("DPS High = DPS Low * (1 + (HSM / 100))<br><br>HSM = Headshot Multiplier")
            dpsHighNum = QLabel(f"<h4><font color = #71bd00>{dpsHigh}")
            dpsHighLayout.addWidget(dpsHighTxt)
            dpsHighLayout.addWidget(dpsHighNum)
            dpsHighLabel = QLabel()
            dpsHighLabel.setLayout(dpsHighLayout)

            dpsNRLayout = QHBoxLayout()
            dpsNRLayout.setContentsMargins(0,0,0,0)
            dpsNRTxt = QLabel(f"<h4><font color = #ffffff>No Reload:")
            dpsNRTxt.setToolTip("DPS No Reload = DMG * ATS * (1 + (HSM / 100))")
            dpsNRNum = QLabel(f"<h4><font color = #1e8500>{dpsNoReload}")
            dpsNRLayout.addWidget(dpsNRTxt)
            dpsNRLayout.addWidget(dpsNRNum)
            dpsNRLabel = QLabel()
            dpsNRLabel.setLayout(dpsNRLayout)

            mainInfo.addWidget(weaponName, 0, 0)
            mainInfo.addWidget(weaponType, 1, 0)
            mainInfo.addWidget(dpsLowLabel, 2, 0)
            mainInfo.addWidget(dpsHighLabel, 3, 0)
            mainInfo.addWidget(dpsNRLabel, 4, 0)

        mainInfoLabel = QLabel()
        mainInfoLabel.setLayout(mainInfo)

        weaponLayout.addWidget(mainInfoLabel, 0, 1)

        weaponStats = QGridLayout()
        weaponStats.setContentsMargins(10,10,10,10)

        windowSize = WINDOW.size()
        windowHeight = windowSize.height()

        
        if windowHeight > 1200:
            texttxt = "<font size = 10px><b><font color = #ffffff>"
            dpstxt = "<h3><font color = #29ffa8>"
            rldtxt = "<h3><font color = #29ffcf>"
            othtxt = "<h3><font color = #29ffff>"
        else:
            texttxt = "<h4><b><font color = #ffffff><br>"
            dpstxt = " <font color = #29ffa8>"
            rldtxt = " <font color = #29ffcf>"
            othtxt = " <font color = #29ffff>"

        if weapon.weaponType in meleeWeapons:
            dmg = QLabel(f"{texttxt}DMG:{dpstxt}{weapon.damage}")
            firerate = QLabel(f"{texttxt}ATS:{dpstxt}{weapon.firerate}")
            staminaCost = QLabel(f"{texttxt}STC:{othtxt}{weapon.staminaCost}")
            armorPen = QLabel(f"{texttxt}APN:{othtxt}{weapon.armorPen}")
            
            weaponStats.addWidget(dmg, 0,0)
            weaponStats.addWidget(firerate, 1,0)

            weaponStats.addWidget(staminaCost, 0,1)
            weaponStats.addWidget(armorPen, 1, 1)
        elif weapon.weaponType == "throwable":
            dmg = QLabel(f"{texttxt}DMG:{dpstxt}{weapon.damage}")
            firerate = QLabel(f"{texttxt}ATS:{dpstxt}{weapon.firerate}")
            range = QLabel(f"{texttxt}EFR:{othtxt}{weapon.range}")
            
            headshot = QLabel(f"{texttxt}HSM:{dpstxt}{weapon.headshot}")
            returnTime = QLabel(f"{texttxt}RTT:{rldtxt}{weapon.returnTime}")
            stamCost = QLabel(f"{texttxt}STC:{rldtxt}{weapon.staminaCost}")
            armorPen = QLabel(f"{texttxt}APN:{othtxt}{weapon.armorPen}")
            
            weaponStats.addWidget(dmg, 0,0)
            weaponStats.addWidget(firerate, 1,0)
            weaponStats.addWidget(range, 2,0)
            weaponStats.addWidget(headshot, 3,0)

            weaponStats.addWidget(returnTime, 0,1)
            weaponStats.addWidget(stamCost, 1,1)
            weaponStats.addWidget(armorPen, 2,1)
        else:
            dmg = QLabel(f"{texttxt}DMG:{dpstxt}{weapon.damage}")
            firerate = QLabel(f"{texttxt}ATS:{dpstxt}{weapon.firerate}")
            range = QLabel(f"{texttxt}EFR:{othtxt}{weapon.range}")
            handling = QLabel(f"{texttxt}HND:{othtxt}{weapon.handling}")
            
            headshot = QLabel(f"{texttxt}HSM:{dpstxt}{weapon.headshot}")
            reload = QLabel(f"{texttxt}RLT:{rldtxt}{weapon.reloadSpeed}")
            magSize = QLabel(f"{texttxt}MZS:{rldtxt}{weapon.magSize}")
            armorPen = QLabel(f"{texttxt}APN:{othtxt}{weapon.armorPen}")
            
            weaponStats.addWidget(dmg, 0,0)
            weaponStats.addWidget(firerate, 1,0)
            weaponStats.addWidget(range, 2,0)
            weaponStats.addWidget(handling, 3,0)

            weaponStats.addWidget(headshot, 0,1)
            weaponStats.addWidget(reload, 1,1)
            weaponStats.addWidget(magSize, 2,1)
            weaponStats.addWidget(armorPen, 3,1)

        weaponStatsLabel = QLabel()
        weaponStatsLabel.setMinimumWidth(int(windowWidth/9))
        weaponStatsLabel.setLayout(weaponStats)
        weaponLayout.addWidget(weaponStatsLabel, 1,1)

        weaponLayoutLabel = QLabel()
        if num == 4:
            color = "#33191f"
        else:
            color = "#3b1d24"
        weaponLayoutLabel.setStyleSheet(f"background-color: {color}")
        weaponLayoutLabel.setLayout(weaponLayout)
        return weaponLayoutLabel

    def weaponNumSelect(self, num):
        global WEAPONTOSELECT
        WEAPONTOSELECT = num

    def weaponSelectScreen(self, sortKey):
        global SELECTEDSORT
        SELECTEDSORT = SORTOPTIONLIST.index(sortKey)
        layout = QVBoxLayout()

        self.equipmentScreenLayout.removeWidget(self.filterBar)
        self.filterBar = self.filterBarWidget()
        self.filterBar.setMinimumWidth(150)
        self.equipmentScreenLayout.addWidget(self.filterBar,0,1)

        selectedWeaponTypes = []
        for list in WEAPONSELECTION:            
            for i in list:
                selectedWeaponTypes.append(i)

        avgAttackSpeed = 0
        avgdamage = 0
        avgreloadSpeed = 0
        avgrange = 0
        avghandling = 0
        avgmagSize = 0
        avgheadshot = 0
        avgStaminaCost = 0
        avgarmorPen = 0
        avgreturnTime = 0
        rangedWeaponCounter = 0
        meleeWeaponCounter = 0
        throwableWeaponCounter = 0
        
        weaponTypes = ["ar","LMG","pistol","precision rifle","revolver","shotgun","SMG","sniper rifle", "blade", "blunt", "throwable"]
        for weapontype in weaponTypes:
            if WEAPONSELECTION == []:
                lst = weaponfilereader.readfile(f"{weapontype}")
                for w in lst:
                    selectedWeaponTypes.append(w)

        for weapon in selectedWeaponTypes:
            avgAttackSpeed += weapon.firerate
            avgdamage += weapon.damage
            if ("blade" not in weapon.weaponType) and ("blunt" not in weapon.weaponType) and ("throwable" not in weapon.weaponType):
                avgreloadSpeed += weapon.reloadSpeed
                avgrange += weapon.range
                avghandling += weapon.handling
                avgmagSize += weapon.magSize
                avgheadshot += weapon.headshot
                rangedWeaponCounter += 1
            elif "throwable" in weapon.weaponType:
                avgStaminaCost += weapon.staminaCost
                avgrange += weapon.range
                avgheadshot += weapon.headshot
                avgreturnTime += weapon.returnTime
                throwableWeaponCounter += 1
            else:
                avgStaminaCost += weapon.staminaCost
                meleeWeaponCounter += 1
            avgarmorPen += weapon.armorPen

        averageList = [avgdamage, avgAttackSpeed, avgreloadSpeed, avgrange, avghandling, avgmagSize, avgheadshot, avgarmorPen, avgStaminaCost, avgreturnTime]
        averages = []
        counter = 0
        for i in averageList:
            # if damage, attack speed or armor pen, all weapons
            if counter < 2 or counter == 7:
                i = i/(rangedWeaponCounter + meleeWeaponCounter + throwableWeaponCounter)
            # if reload speed, handling or magsize, only ranged weapons
            elif counter == 2 or counter == 4 or counter == 5:
                if rangedWeaponCounter != 0:
                    i = i/rangedWeaponCounter
            # if range or headshot, ranged and throwable
            elif counter == 3 or counter == 6:
                if rangedWeaponCounter + throwableWeaponCounter != 0:
                    i = i/(rangedWeaponCounter + throwableWeaponCounter)
            # if staminacost, melee and throwable
            elif counter == 8:
                if meleeWeaponCounter + throwableWeaponCounter != 0:
                    i = i/(meleeWeaponCounter + throwableWeaponCounter)
            elif counter == 9 and throwableWeaponCounter != 0:
                i = i/(throwableWeaponCounter)
            averages.append(i)
            counter += 1
        self.setCursor(Qt.WaitCursor)  # Change cursor to loading icon
        sortedWeapons = mergesort(selectedWeaponTypes, sortKey)
        if sortKey == "name" or sortKey == "type" or sortKey == "reloadSpeed" or sortKey == "staminaCost" or sortKey == "returnTime":
            sortedWeapons.reverse()

        wpnSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        for weapon in sortedWeapons:
            WLayout = QHBoxLayout()
            imgButton = QPushButton()
            icon = QIcon(f"{imagespath}weapons/{weapon.imgname}")
            imgButton.setIcon(icon)
            imgButton.setIconSize(QSize(200,200))
            imgButton.setFixedSize(QSize(200,200))

            imgButton.clicked.connect(functools.partial(self.replaceWeapon, weapon))
            
            imgButton.setStyleSheet("background-color: #391c23; border: 2px solid #5c211f")
            if len(weapon.iconic) > 7:
                imgButton.setStyleSheet("border: 2px solid #ffd842")
            tooltiptxt = f"{weapon.type} {weapon.weaponType}"
            imgButton.setToolTip(f"<font color = #d9fa5c>{tooltiptxt}")
            WLayout.addWidget(imgButton)

            statnameLayout = QGridLayout()
            if "blade" not in weapon.weaponType and "blunt" not in weapon.weaponType and "throwable" not in  weapon.weaponType:
                dmgLabel = QLabel(f"<font color = #ff5f59><h4>DMG:")
                ASLabel = QLabel(f"<font color = #ff5f59><h4>ATS:")
                reloadSpeedLabel = QLabel(f"<font color = #ff5f59><h4>RLD:")
                rangeLabel = QLabel(f"<font color = #ff5f59><h4>RNG:")
                handlingLabel = QLabel(f"<font color = #ff5f59><h4>HND:")
                magSizeLabel = QLabel(f"<font color = #ff5f59><h4>MZS:")
                headshotLabel = QLabel(f"<font color = #ff5f59><h4>HSM:")
                armorPenLabel = QLabel(f"<font color = #ff5f59><h4>APN:")

                labels = [dmgLabel, ASLabel, reloadSpeedLabel, rangeLabel, handlingLabel, magSizeLabel, headshotLabel, armorPenLabel]
                for label in labels:
                    label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    label.setWordWrap(True)

                statnameLayout.addWidget(dmgLabel, 0, 0)
                statnameLayout.addWidget(ASLabel, 0, 1)
                statnameLayout.addWidget(reloadSpeedLabel, 0, 2)
                statnameLayout.addWidget(rangeLabel, 0, 3)
                statnameLayout.addWidget(handlingLabel, 0, 4)
                statnameLayout.addWidget(magSizeLabel, 0, 5)
                statnameLayout.addWidget(headshotLabel, 0, 6)
                statnameLayout.addWidget(armorPenLabel, 0, 7)
            elif "blade" in weapon.weaponType or "blunt" in weapon.weaponType:
                dmgLabel = QLabel(f"<font color = #ff5f59><h4>DMG:")
                ASLabel = QLabel(f"<font color = #ff5f59><h4>ATS:")
                SCLabel = QLabel(f"<font color = #ff5f59><h4>STC:")
                armorPenLabel = QLabel(f"<font color = #ff5f59><h4>APN:")

                labels = [dmgLabel, ASLabel, SCLabel, armorPenLabel]
                for label in labels:
                    label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    label.setWordWrap(True)
                    label.setSizePolicy(wpnSizePolicy)

                statnameLayout.addWidget(dmgLabel, 0, 0)
                statnameLayout.addWidget(ASLabel, 0, 1)
                statnameLayout.addWidget(SCLabel, 0, 2)
                statnameLayout.addWidget(armorPenLabel, 0, 3)
            else:
                dmgLabel = QLabel(f"<font color = #ff5f59><h4>DMG:")
                ASLabel = QLabel(f"<font color = #ff5f59><h4>ATS:")
                rangeLabel = QLabel(f"<font color = #ff5f59><h4>RNG:")
                headshotLabel = QLabel(f"<font color = #ff5f59><h4>HSM:")
                returnTimeLabel = QLabel(f"<font color = #ff5f59><h4>RTT:")
                staminaCostLabel = QLabel(f"<font color = #ff5f59><h4>STC:")
                armorPenLabel = QLabel(f"<font color = #ff5f59><h4>APN:")

                labels = [dmgLabel, ASLabel, rangeLabel, headshotLabel, returnTimeLabel, staminaCostLabel, armorPenLabel]
                max_width = max(label.sizeHint().width() for label in labels)

                for label in labels:
                    label.setFixedWidth(max_width)
                    label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    label.setWordWrap(True)
                    label.setSizePolicy(wpnSizePolicy)


                statnameLayout.addWidget(dmgLabel, 0, 0)
                statnameLayout.addWidget(ASLabel,0,1)
                statnameLayout.addWidget(rangeLabel, 0,2)
                statnameLayout.addWidget(headshotLabel,0,3)
                statnameLayout.addWidget(returnTimeLabel,0,4)
                statnameLayout.addWidget(staminaCostLabel,0,5)
                statnameLayout.addWidget(armorPenLabel,0,6)

            statnameLabel = QLabel()
            statnameLabel.setLayout(statnameLayout)

            statNumLayout = QHBoxLayout()
                
            tier1color = "<font color = #a40000>"
            tier2color = "<font color = #a44f00>"
            tier3color = "<font color = #cdd100>"
            tier4color = "<font color = #7ad100>"
            tier5color = "<font color = #0e9202>"
            if "blade" not in weapon.weaponType and "blunt" not in weapon.weaponType and "throwable" not in weapon.weaponType:
                stats = [weapon.damage, weapon.firerate, weapon.reloadSpeed, weapon.range, weapon.handling, weapon.magSize, weapon.headshot, weapon.armorPen]
            elif "blade" in weapon.weaponType or "blunt" in weapon.weaponType:
                stats = [weapon.damage, weapon.firerate, weapon.staminaCost, weapon.armorPen]
            else:
                stats = [weapon.damage, weapon.firerate, weapon.range, weapon.headshot, weapon.returnTime, weapon.staminaCost, weapon.armorPen]
            index = 0
            for stat in stats:
                if int(stat) == stat:
                    stat = int(stat)
                if "blade" in weapon.weaponType or "blunt" in weapon.weaponType:
                    if index == 9:
                        index = 7
                    if index == 2:
                        index = 8     
                elif "throwable" in weapon.weaponType:
                    if index == 7:
                        index = 9
                    elif index == 9:
                        index = 7
                    if index == 10:
                        index = 8
                    if index == 4:
                        index = 6
                    if index == 2:
                        index = 3
                statNumLabel = QLabel("")
                stattext = ""
                color = "#ffffff"
                if index != 2 and index != 8 and index != 9:
                    if stat < averages[index]*0.25:
                        color = tier1color
                    elif stat > averages[index]*1.75:
                        color = tier5color
                    elif stat < averages[index]*0.75:
                        color = tier2color
                    elif stat > averages[index]*1.25:
                        color = tier4color 
                    else:
                        color = tier3color
                else:
                    if stat < (averages[index]*0.25):
                        color = tier5color
                    elif stat > (averages[index]*1.75):
                        color = tier1color
                    elif stat < (averages[index]*0.75):
                        color = tier4color
                    elif stat > (averages[index]*1.25):
                        color = tier2color
                    else:
                        color = tier3color
                avgColor = tier2color
                if stat > averages[index]:
                    avgColor = tier4color
                statNumLabel.setToolTip(f"{avgColor}Average: {round(averages[index], 1)}")
                if index != 6:
                    stattext = f"<h1><b>{color}{stat}"
                else:
                    stattext = f"<h1><b>{color}+{int(stat)}%"
                statNumLabel.setText(stattext)
                statNumLabel.setWordWrap(True)
                statNumLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                statNumLayout.addWidget(statNumLabel)
                index += 1
                
            
            statNums = QLabel()
            statNums.setLayout(statNumLayout)

            statLayout = QVBoxLayout()
            statLayout.addWidget(statnameLabel)
            statLayout.addWidget(statNums)

            statsLabel = QLabel()
            statsLabel.setLayout(statLayout)

            descLayout = QHBoxLayout()
            iconicstr = weapon.iconic[0].capitalize() + weapon.iconic[1:]
            iconicdesc = QLabel(f"<h4><b><font color = #ffd641>{iconicstr}")
            iconicdesc.setWordWrap(True)
            intrinsicstr = weapon.intrinsic[0].capitalize() + weapon.intrinsic[1:]
            weaponTypeStr = str(weapon.type + " " + weapon.weaponType).title()
            intrinsicdesc = QLabel(f"<font color = #29ffff><h1>{weapon.name}<h3><font color = #d9fa5c>{weaponTypeStr}<h4><font color = #ff6059><b>{intrinsicstr}")
            intrinsicdesc.setContentsMargins(20,20,20,20)
            intrinsicdesc.setWordWrap(True)
            descLayout.addWidget(intrinsicdesc)
            descLayout.addWidget(iconicdesc)


            descLabel = QLabel()
            descLabel.setLayout(descLayout)

            descstatLayout = QVBoxLayout()
            descstatLayout.addWidget(descLabel)
            descstatLayout.addWidget(statsLabel)

            descstatLabel = QLabel()
            descstatLabel.setLayout(descstatLayout)

            WLayout.addWidget(descstatLabel)

            WLabel = QLabel()
            WLabel.setLayout(WLayout)
            bgcolor = "#31181e"
            if (sortedWeapons.index(weapon) % 2) == 0:
                bgcolor = "#3b1d24"
            WLabel.setStyleSheet(f"background-color: {bgcolor}")

            layout.addWidget(WLabel)
        
        weaponSelectionWidget = QWidget()
        weaponSelectionWidget.setLayout(layout)
        weaponSelectionWidget.setMinimumSize(layout.minimumSize())
        weaponSelectionWidget.setStyleSheet("background-color: #1c0005")

        widgetSizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        weaponSelectionWidget.setSizePolicy(widgetSizePolicy)

        weaponSelection = QScrollArea()
        weaponSelection.setWidgetResizable(True)
        weaponSelection.setStyleSheet("border: none")
        weaponSelection.setWidget(weaponSelectionWidget)
        self.equipmentScreenLayout.addWidget(weaponSelection, 0, 2)
        self.setCursor(Qt.ArrowCursor)

    def replaceWeapon(self, weapon):
        global WEAPON1
        global WEAPON2
        global WEAPON3
        global WEAPON4
        match WEAPONTOSELECT:
            case 1:
                num1 = 0
                num2 = 0
                WEAPON1 = weapon
            case 2:
                num1 = 1
                num2 = 0
                WEAPON2 = weapon
            case 3:
                num1 = 0
                num2 = 1
                WEAPON3 = weapon
            case 4:
                num1 = 1
                num2 = 1
                WEAPON4 = weapon
        weaponList = [WEAPON1, WEAPON2, WEAPON3, WEAPON4]
        slotToReplace = WEAPONSELECTIONLIST[WEAPONTOSELECT-1]
        slotToReplace = self.weaponWidget(WEAPONTOSELECT, weaponList[WEAPONTOSELECT-1])
        newWeaponSlot = slotToReplace
        self.weaponsLayout.removeWidget((WEAPONSELECTIONLIST[WEAPONTOSELECT-1]))
        slotToReplace = WEAPONSELECTIONLIST[WEAPONTOSELECT-1]
        slotToReplace.deleteLater()
        WEAPONSELECTIONLIST.pop(WEAPONTOSELECT - 1)
        WEAPONSELECTIONLIST.insert(WEAPONTOSELECT - 1, newWeaponSlot)
        self.weaponsLayout.addWidget(newWeaponSlot, num1, num2)


    def statScreen(self):

        global STATBUTTONLIST 

        cybBonuses = []
        perkBonuses = []
        skillBonuses = []

        cybPassEff = []
        cybActEff = []


        if STATBUTTONLIST[2] == 1:
            for i in ACTIVECYBERWARE:
                # Passive Effects
                if hasattr(i, "pasEff") and "none" not in i.pasEff.lower():
                    affects = "all"
                    if "," in i.pasEff:
                        effList = i.pasEff.split(",")
                        for element in effList:
                            if ":" in element:
                                effectAffects = element.split(":")
                                cybPassEff.append([i.name, effectAffects[0], effectAffects[1]])
                            else:
                                cybPassEff.append([i.name, element, affects])
                    else:
                        if ":" in i.pasEff:
                            effectAffects = i.pasEff.split(":")
                            cybPassEff.append([i.name, effectAffects[0], effectAffects[1]])
                        else:
                            cybPassEff.append([i.name, i.pasEff, affects])
                
                # Active Effects
                if hasattr(i, "actEff") and "none" not in i.actEff.lower():
                    affects = "all"
                    if ";" in i.actEff:
                        effList = i.actEff.split(";")
                        for element in effList:
                            if ":" in element:
                                components = element.split(":")
                                cybActEff.append([i.name, components[0], components[2], components[1]])
                    else:
                        if "berserk" in i.name.lower():
                            affects = "blunt blade"
                        if "," in i.actEff:
                            effList = i.actEff.split(",")
                            for element in effList:
                                if ":" in element:
                                    components = element.split(":")
                                    cybActEff.append([i.name, components[0], components[2], components[1]])
                                else:
                                    cybActEff.append([i.name, element, affects])

                        elif ":" in i.actEff:
                            components = i.actEff.split(":")

                            cybActEff.append([i.name, components[0], components[1], i.condition])
                        else:
                            cybActEff.append([i.name, i.actEff, affects, i.condition])

                # attunement effects
                if hasattr(i, "attunement") and i.attunement != "none":
                    attunementsplit = i.attunement.split(",")
                    attunementattr = attunementsplit[0].strip().lower()
                    mulFactor = 0
                    match attunementattr:
                        case "body":
                            mulFactor = global_attributes["BODY"]
                        case "refl":
                            mulFactor = global_attributes["REFLEXES"]
                        case "tech":
                            mulFactor = global_attributes["TECH"]
                        case "int":
                            mulFactor = global_attributes["INTELLIGENCE"]
                        case "cool":
                            mulFactor = global_attributes["COOL"]
                    charstr = ""
                    string = ""
                    for char in attunementsplit[1]:
                        if char in "0123456789.":
                            charstr += char
                        else:
                            string += char
                    charflt = float(charstr)
                    num = charflt * mulFactor
                    string = str(num) + string
                    cybPassEff.append([i.name, string, "all"])

            cybBonuses = cybPassEff
            if STATBUTTONLIST[4] == 1:
                for i in cybActEff:
                    cybBonuses.append(i)

        perkPassEff = []
        perkActEff = []

        activePerks = []

        if STATBUTTONLIST[0] == 1:

            for i in BODYPERKS:
                for perk in i:
                    if perk.level >= 1:
                        activePerks.append(perk)

            for i in REFLEXESPERKS:
                for perk in i:
                    if perk.level >= 1:
                        activePerks.append(perk)

            for i in TECHPERKS:
                for perk in i:
                    if perk.level >= 1:
                        activePerks.append(perk)

            for i in COOLPERKS:
                for perk in i:
                    if perk.level >= 1:
                        activePerks.append(perk)

            for i in INTELLIGENCEPERKS:
                for perk in i:
                    if perk.level >= 1:
                        activePerks.append(perk) 

            for perk in activePerks:
                if perk.maxlvl == 1:
                    if "none" not in perk.pasEff.lower():
                        if "," in perk.pasEff:
                            effList = perk.pasEff.split(",")
                            for element in effList:
                                perkPassEff.append([perk.name, element, perk.affects])
                        else:
                            perkPassEff.append([perk.name, perk.pasEff, perk.affects])

                    if "none" not in perk.actEff.lower():
                        if "," in perk.actEff:
                            effList = perk.actEff.split(",")
                            for element in effList:
                                perkActEff.append([perk.name, element, perk.affects, perk.condition])
                        else:
                            perkActEff.append([perk.name, perk.actEff, perk.affects, perk.condition])
                elif perk.level >= 1:
                    if "none" not in perk.pasEff1.lower():
                        if "," in perk.pasEff1:
                            effList = perk.pasEff1.split(",")
                            for element in effList:
                                perkPassEff.append([perk.name, element, perk.affects])
                        else:
                            perkPassEff.append([perk.name, perk.pasEff1, perk.affects])

                    if "none" not in perk.actEff1.lower():
                        if "," in perk.actEff1:
                            effList = perk.pasEff1.split(",")
                            for element in effList:
                                perkActEff.append([perk.name, element, perk.affects, perk.condition1])
                        else:
                            perkActEff.append([perk.name, perk.actEff1, perk.affects, perk.condition1])

                    if perk.level >= 2:
                        if "none" not in perk.pasEff2.lower():
                            if "," in perk.pasEff2:
                                effList = perk.pasEff2.split(",")
                                for element in effList:
                                    perkPassEff.append([perk.name, element, perk.affects])
                            else:
                                perkPassEff.append([perk.name, perk.pasEff2, perk.affects])

                        if "none" not in perk.actEff2.lower():
                            if "," in perk.actEff2:
                                effList = perk.pasEff2.split(",")
                                for element in effList:
                                    perkActEff.append([perk.name, element, perk.affects, perk.condition2])
                            else:
                                perkActEff.append([perk.name, perk.actEff2, perk.affects, perk.condition2])
                        if perk.level >= 3:
                            if "none" not in perk.pasEff3.lower():
                                if "," in perk.pasEff3:
                                    effList = perk.pasEff3.split(",")
                                    for element in effList:
                                        perkPassEff.append([perk.name, element, perk.affects])
                                else:
                                    perkPassEff.append([perk.name, perk.pasEff3, perk.affects])

                            if "none" not in perk.actEff3.lower():
                                if "," in perk.actEff3:
                                    effList = perk.pasEff3.split(",")
                                    for element in effList:
                                        perkActEff.append([perk.name, element, perk.affects, perk.condition3])
                                else:
                                    perkActEff.append([perk.name, perk.actEff3, perk.affects, perk.condition3])
            
            perkBonuses = perkPassEff
            if STATBUTTONLIST[4] == 1:
                for i in perkActEff:
                    perkBonuses.append(i)

            # Bonuses from attributes
            bodyNum = global_attributes["BODY"] * 2
            reflNum = global_attributes["REFLEXES"] * 0.5
            techNum = global_attributes["TECH"] * 2
            inteNum = int(global_attributes["INTELLIGENCE"] / 4)
            coolNum = global_attributes["COOL"] * 1.25
            perkBonuses.append(["Body", f"+{bodyNum} health", "all"])
            perkBonuses.append(["Reflexes", f"+{reflNum}% crit chance", "all"])
            perkBonuses.append(["Tech", f"+{techNum} armor", "all"])
            perkBonuses.append(["Intelligence", f"+{inteNum} ram", "all"])
            perkBonuses.append(["Cool", f"+{coolNum}% crit damage", "all"])

        # skills
        skillActEff = []
        skillPassEff = []
        if STATBUTTONLIST[1] == 1:
            skillDictionaries = skillfilereader.readfile()
            for dictionary in skillDictionaries:
                for effect in dictionary['effects']:
                    affects = "all"
                    if ":" in effect:
                        splitSkills = effect.split(":")
                        affects = splitSkills[1]
                        if "melee" in affects:
                            affects = "blunt,blade"
                    if ',' in effect:
                        actCond = effect.split(",")
                        skillActEff.append([dictionary['name'], actCond[0], affects, actCond[1]])
                    else:
                        skillPassEff.append([dictionary['name'], effect, affects])
        
            skillBonuses = skillPassEff
            if STATBUTTONLIST[4] == 1:
                for i in skillActEff:
                    skillBonuses.append(i)
        


        weaponIntrinsicEff = []

        if STATBUTTONLIST[3] == 1 and STATBUTTONLIST[4] == 1:
            for weapon in [WEAPON1, WEAPON2, WEAPON3]:
                if weapon != None:
                    if "all" in weapon.condition:
                        weaponIntrinsicEff.append([weapon.name, weapon.actEff, "all", f"{weapon.condition},{weapon.name}"])
                    if "movspeed" in weapon.actEff:
                        if "," in weapon.actEff:
                            split = weapon.actEff.split()
                            for element in split:
                                if "movspeed" in element:
                                    weaponIntrinsicEff.append([weapon.name, element, "all", weapon.condition])
                        else:
                            weaponIntrinsicEff.append([weapon.name, weapon.actEff, "all", weapon.condition])
                

        # weapon effects can be done within the weapon itself, as they often only affect that weapon
        
        statLayout = QHBoxLayout()
        statLayout.setContentsMargins(0,0,0,0)

        genOverviewLayout = QVBoxLayout()
        genOverviewLayout.setContentsMargins(0,0,0,0)

        buttonLayout = QGridLayout()
        buttonLayout.setContentsMargins(0,0,0,0)
        buttonLayout.setSpacing(0)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        perkButton = QPushButton()
        perkButtonL = QLabel()
        tempLayout = QHBoxLayout()
        if STATBUTTONLIST[0] == 1:
            perkButtonL.setText("Perks On")
            perkButton.setStyleSheet("background-color: #29ffff; color: #31181e; font-weight: bold")
        else:
            perkButtonL.setText("Perks Off")
            perkButton.setStyleSheet("background-color: #31181e; color: #29ffff; font-weight: bold")
        perkButtonL.setWordWrap(True)
        perkButtonL.setSizePolicy(sizePolicy)
        perkButton.setSizePolicy(sizePolicy)
        tempLayout.addWidget(perkButtonL)
        perkButton.setLayout(tempLayout)
        perkButton.clicked.connect(functools.partial(self.statButton, 0))

        skillButton = QPushButton()
        skillButtonL = QLabel()
        tempLayout = QHBoxLayout()
        if STATBUTTONLIST[1] == 1:
            skillButtonL.setText("Skills On")
            skillButton.setStyleSheet("background-color: #dbfb5c; color: #31181e; font-weight: bold")
        else:
            skillButtonL.setText("Skills Off")
            skillButton.setStyleSheet("background-color: #31181e; color: #dbfb5c; font-weight: bold")
        skillButtonL.setWordWrap(True)
        skillButtonL.setSizePolicy(sizePolicy)
        skillButton.setSizePolicy(sizePolicy)
        tempLayout.addWidget(skillButtonL)
        skillButton.setLayout(tempLayout)
        skillButton.clicked.connect(functools.partial(self.statButton, 1))
        
        cyberwareButton = QPushButton()
        cyberwareButtonL = QLabel()
        tempLayout = QHBoxLayout()
        if STATBUTTONLIST[2] == 1:
            cyberwareButtonL.setText("Cyberware On")
            cyberwareButton.setStyleSheet("background-color: #ffd741; color: #31181e; font-weight: bold")
        else:
            cyberwareButtonL.setText("Cyberware Off")
            cyberwareButton.setStyleSheet("background-color: #31181e; color: #ffd741; font-weight: bold")
        cyberwareButtonL.setWordWrap(True)
        cyberwareButtonL.setSizePolicy(sizePolicy)
        cyberwareButton.setSizePolicy(sizePolicy)
        tempLayout.addWidget(cyberwareButtonL)
        cyberwareButton.setLayout(tempLayout)
        cyberwareButton.clicked.connect(functools.partial(self.statButton, 2))

        IconicIntrinsicButton = QPushButton()
        IconicIntrinsicButtonL = QLabel()
        tempLayout = QHBoxLayout()
        if STATBUTTONLIST[3] == 1:
            IconicIntrinsicButtonL.setText("Weapon Icon./Intrin. On")
            IconicIntrinsicButton.setStyleSheet("background-color: #ff6158; color: #31181e; font-weight: bold")
        else:
            IconicIntrinsicButtonL.setText("Weapon Icon. / Intrin. Off")
            IconicIntrinsicButton.setStyleSheet("background-color: #31181e; color: #ff6158; font-weight: bold")
        IconicIntrinsicButtonL.setWordWrap(True)
        IconicIntrinsicButtonL.setSizePolicy(sizePolicy)
        IconicIntrinsicButton.setSizePolicy(sizePolicy)
        tempLayout.addWidget(IconicIntrinsicButtonL)
        IconicIntrinsicButton.setLayout(tempLayout)
        IconicIntrinsicButton.clicked.connect(functools.partial(self.statButton, 3))

        buttonLayout.addWidget(perkButton, 0, 0)
        buttonLayout.addWidget(skillButton, 1, 0)
        buttonLayout.addWidget(cyberwareButton, 0, 1)
        buttonLayout.addWidget(IconicIntrinsicButton, 1, 1)
        buttonLabel = QLabel()
        buttonLabel.setLayout(buttonLayout)
        buttonLabel.setFixedSize(300,100)

        genOverviewLayout.addWidget(buttonLabel)
        genOverviewLayout.setSpacing(2)
        
        cyberwareLayout1 = QVBoxLayout()
        cyberwareLayout2 = QVBoxLayout()
        cyberwareLayout1.setContentsMargins(0,0,0,0)
        cyberwareLayout1.setSpacing(2)
        cyberwareLayout2.setContentsMargins(0,0,0,0)
        cyberwareLayout2.setSpacing(2)

        windowSize = WINDOW.size()
        windowWidth = windowSize.width()
        windowHeight = windowSize.height()
        if len(ACTIVECYBERWARE) != 0:
            maxImgSize = int((windowHeight - 300) / (len(ACTIVECYBERWARE) / 2))
        else:
            maxImgSize = 150
        imgSize = min(150,maxImgSize)

        for cyberware in ACTIVECYBERWARE:
            cyberwareLabel = QLabel()
            cyberwareLabel.setContentsMargins(0,0,0,0)
            pixmap = QPixmap(f"{imagespath}/cyberware/{cyberware.imgname}")

            pixmap = pixmap.scaled(imgSize, imgSize)
            cyberwareLabel.setPixmap(pixmap)
            cyberwareLabel.setMaximumSize(150,150)
            cyberwareLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            if "Iconic" in cyberware.description:
                cyberwareLabel.setStyleSheet("background-color: #6f510b; border: 5px solid #ffd842")
                tempdescription = cyberware.description.split(";")[1]
            else:
                cyberwareLabel.setStyleSheet("background-color: #391c23; border: 5px solid #5c211f")
                tempdescription = cyberware.description
            if hasattr(cyberware, "attunement") and "," in cyberware.attunement:
                attunementTexts = cyberware.attunement.split(",")
                attunementNum = 0
                counter = 0
                attunementStr = ""
                for char in attunementTexts[1]:
                    if char in "0123456789.":
                        attunementStr += char
                        lastNum = counter
                    if char in "%":
                        lastNum == counter
                    counter += 1
                attunementNum += float(attunementStr)
                match attunementTexts[0]:
                    case 'body':
                        attunementNum = attunementNum * global_attributes["BODY"]
                    case 'refl':
                        attunementNum = attunementNum * global_attributes["REFLEXES"]
                    case 'tech':
                        attunementNum = attunementNum * global_attributes["TECH"]
                    case 'int':
                        attunementNum = attunementNum * global_attributes["INTELLIGENCE"]
                    case 'cool':
                        attunementNum = attunementNum * global_attributes["COOL"]
                attunementNumText = ""
                if '+' in attunementTexts[1]:
                    attunementNumText += "+"
                elif '-' in attunementTexts[1]:
                    attunementNumText += "-"
                attunementNumText += str(round(attunementNum, 2))
                if '%' in attunementTexts[1]:
                    attunementNumText += '%'
                tempdescription += f"<br><br><font color = #e0ff5e>Attunement:<br><b>{cyberware.attunement.title()} per Attribute point.<br>Current: {attunementNumText}</b></font>"
            validchar = True
            description = ""
            for char in tempdescription:
                if char in "<":
                    validchar = False
                elif char in ">":
                    validchar = True
                if char in " 1234567890%+-" and validchar == True:
                    description += f"<font color = #29ffff>{char}</font>"
                else:
                    description += char
            CWArmorText = ""
            if cyberware.armor != 0:
                CWArmorText = f"<font color = #ffffff> / <font color = #29ffff>Armor: {cyberware.armor}</font>"
            cyberdeckText = ""
            if "cyberdeck" in cyberware.name.lower():
                cyberdeckText = f"<font color = #ffffff> / <font color = #29ffff>RAM: {cyberware.ram}<font color = #ffffff> / <font color = #29ffff>Slots: {cyberware.QHslots}<font color = #ffffff> / <font color = #dbfa5c>Buffer: {cyberware.buffer}</font></font>"
            cyberwareLabel.setToolTip(f"<body style = margin: 10px;><font color = #ff6158><h2>{cyberware.name}</h2></font><font color = #ffd642><h3>Cost: {cyberware.cost}{CWArmorText}{cyberdeckText}</h3><font color = #ffffff><b>{description}")
            
            if ACTIVECYBERWARE.index(cyberware) < (len(ACTIVECYBERWARE) / 2):
                cyberwareLayout1.addWidget(cyberwareLabel)
            else:
                cyberwareLayout2.addWidget(cyberwareLabel)
        cyberware1Label = QLabel()
        cyberware1Label.setContentsMargins(0,0,0,0)
        cyberware1Label.setLayout(cyberwareLayout1)
        cyberware2Label = QLabel()
        cyberware2Label.setContentsMargins(0,0,0,0)
        cyberware2Label.setLayout(cyberwareLayout2)
        cyberwareTotalLayout = QHBoxLayout()
        cyberwareTotalLayout.setSpacing(2)
        cyberwareTotalLayout.setContentsMargins(0,0,0,0)
        if len(ACTIVECYBERWARE) > 0:
            cyberwareTotalLayout.addWidget(cyberware1Label)
            cyberwareTotalLayout.addWidget(cyberware2Label)
        cyberwareTotalLabel = QLabel()
        if len(ACTIVECYBERWARE) == 0:
            cyberwareTotalLabel.setText("<h2><font color = #29ffff>Cyberware will show up here")
            cyberwareTotalLabel.setWordWrap(True)
            cyberwareTotalLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        cyberwareTotalLabel.setLayout(cyberwareTotalLayout)
        cyberwareTotalLabel.setStyleSheet("background-color: #1d0005")        

        genOverviewLayout.addWidget(cyberwareTotalLabel)

        highLowLayout = QHBoxLayout()
        highLowLayout.setSpacing(0)
        highLowLayout.setContentsMargins(0,0,0,0)

        lowButton = QPushButton()
        lowButton.setText(f"Low Stats")
        if STATBUTTONLIST[4] == 0:
            lowButton.setStyleSheet("background-color: #ff6158; color: #1d0005; font-weight: bold; font-size: 23px")
        else:
            lowButton.setStyleSheet("background-color: #1d0005; color: #ff6158; font-weight: bold; font-size: 23px")
        lowButton.clicked.connect(functools.partial(self.statButton, 4))
        lowButton.setSizePolicy(sizePolicy)

        highButton = QPushButton()
        highButton.setText(f"High Stats")
        if STATBUTTONLIST[4] == 1:
            highButton.setStyleSheet("background-color: #e0ff5e; color: #1d0005; font-weight: bold; font-size: 23px")
        else:
            highButton.setStyleSheet("background-color: #1d0005; color: #e0ff5e; font-weight: bold; font-size: 23px")
        highButton.clicked.connect(functools.partial(self.statButton, 4))
        highButton.setSizePolicy(sizePolicy)
        highLowLayout.addWidget(lowButton)
        highLowLayout.addWidget(highButton)

        highLowLabel = QLabel()
        highLowLabel.setMaximumHeight(100)
        highLowLabel.setLayout(highLowLayout)

        genOverviewLayout.addWidget(highLowLabel)
        genOverviewLabel = QLabel()
        genOverviewLabel.setLayout(genOverviewLayout)
        genOverviewLabel.setMaximumWidth(300)
        statLayout.addWidget(genOverviewLabel)

        bonuses = perkBonuses.copy()
        for x in cybBonuses:
            bonuses.append(x)
        for y in skillBonuses:
            bonuses.append(y)
        for z in weaponIntrinsicEff:
            bonuses.append(z)

        for item in bonuses:
            if len(item) > 3:
                if "sandevistan" in item[3].lower() or "sandy" in item[3].lower():
                    valid = False
                    for cyberware in ACTIVECYBERWARE:
                        if "sandevistan" in cyberware.name.lower():
                            valid = True
                    if valid == False:
                        bonuses.remove(item)
                if "berserk" in item[3].lower():
                    valid = False
                    for cyberware in ACTIVECYBERWARE:
                        if "berserk" in cyberware.name.lower():
                            valid = True
                    if valid == False:
                        bonuses.remove(item)
                if "optical camo" in item[3].lower():
                    valid = False
                    for cyberware in ACTIVECYBERWARE:
                        if "optical camo" in cyberware.name.lower():
                            valid = True
                    if valid == False:
                        bonuses.remove(item)


        counter = 0
        weaponLayout = QVBoxLayout()
        weapons = [WEAPON1, WEAPON3, WEAPON2]
        
        for w in weapons:
            if w == None:
                weaponList = weaponfilereader.readfile("Empty Weapon")
                w = weaponList[0]
            weaponStatLayout = QHBoxLayout()

            mainInfoLayout = QVBoxLayout()
            imgButton = QPushButton()
            icon = QIcon(f"{imagespath}weapons/{w.imgname}")
            imgButton.setIcon(icon)
            imgButton.setIconSize(QSize(200,200))
            imgButton.setFixedSize(QSize(200,200))

            imgButton.clicked.connect(functools.partial(self.equipmentScreen))
            
            imgButton.setStyleSheet("background-color: #391c23; border: 5px solid #5c211f")
            if len(w.iconic) > 7:
                imgButton.setStyleSheet("background-color: #684d1e ;border: 5px solid #ffd842")
            tooltiptxt = f"<h1><font color = #29ffff>{w.name}<h3><font color = #dbfa5d>Base Damage: {w.damage}<br>Base Attack Speed: {w.firerate}<h4><font color = #ff5e55>{w.iconic}<br>{w.intrinsic}"
            imgButton.setToolTip(f"<font color = #d9fa5c>{tooltiptxt}")
            imgButton.setMinimumHeight(200)

            mainInfoLayout.addWidget(imgButton)

            nameLabel = QLabel(f"<font color = #29ffff><h2>{w.name}")
            nameLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            nameLabel.setWordWrap(True)
            mainInfoLayout.addWidget(nameLabel)

            if windowHeight > 1000:
                typeLabel = QLabel(f"<font color = #d8f75a><h4>{w.type.title()} - {w.weaponType.title()}")
                typeLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                typeLabel.setWordWrap(True)
            
                mainInfoLayout.addWidget(typeLabel)

            mainInfoLabel = QLabel()
            mainInfoLabel.setMaximumWidth(230)
            mainInfoLabel.setLayout(mainInfoLayout)
            weaponWrapper = QHBoxLayout()
            weaponWrapper.addWidget(mainInfoLabel)

            addedDMG = 0
            dmgSources = []
            addedATS = 0
            atsSources = []
            addedcritC = 0
            critCSources = []
            addedcritD = 0
            critDSources = []
            addedHSM = 0
            hsmSources = []

            weaponBonuses = []

            if w.actEff != "none" and STATBUTTONLIST[3] == 1:
                effects = w.actEff.strip()
                conditions = w.condition.strip()
                if "headhunter" not in w.name.lower():
                    if ";" in w.actEff:
                        effects = w.actEff.split(";")
                        conditions = w.condition.split(";")
                        for e in effects:
                            weaponBonuses.append([w.name, e, w.name, conditions[effects.index(e)]])
                    else:
                        weaponBonuses.append([w.name, effects, w.name, conditions])
                
            for b in weaponBonuses:
                if len(b) > 3:
                    if "sandevistan" in b[3].lower() or "sandy" in b[3].lower():
                        valid = False
                        for cyberware in ACTIVECYBERWARE:
                            if "sandevistan" in cyberware.name.lower():
                                valid = True
                        if valid == False:
                            weaponBonuses.remove(b)
                    if "berserk" in b[3].lower():
                        valid = False
                        for cyberware in ACTIVECYBERWARE:
                            if "berserk" in cyberware.name.lower():
                                valid = True
                        if valid == False:
                            weaponBonuses.remove(b)
                    if "optical camo" in b[3].lower():
                        valid = False
                        for cyberware in ACTIVECYBERWARE:
                            if "optical camo" in cyberware.name.lower():
                                valid = True
                        if valid == False:
                            weaponBonuses.remove(b)
                if STATBUTTONLIST[4] == 0:
                    if "none" not in b[3]:
                        weaponBonuses.remove(b)

            for bon in weaponBonuses:
                bonuses.append(bon)

            for bonus in bonuses:
                bonusEff = bonus[1].lower()
                if (("damage" in bonusEff) and ("q" not in bonusEff) and ("ricochet" not in bonusEff) and ("reduction" not in bonusEff) and ("crit" not in bonusEff) and ("headshot" not in bonusEff) and ("+" in bonusEff)) or (("ricochet" in bonusEff) and ("power" in w.type.lower())):
                    if w.type.lower() in bonus[2].lower() or w.weaponType.lower() in bonus[2].lower() or "all" in bonus[2].lower() or w.name in bonus[2]:
                        if "," in bonusEff:
                            bonusEffects = bonusEff.split(",")
                            for eff in bonusEffects:
                                if ("damage" in eff) and ("q" not in eff) and ("ricochet" not in eff) and ("reduction" not in eff) and ("crit" not in eff) and ("headshot" not in eff) and ("+" in eff):
                                    tempStr = ""
                                    for char in eff:
                                        if char in "0123456789.":
                                            tempStr += char
                                    addedDMG += float(tempStr)
                                    dmgSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {effect}")
                        else:
                            tempStr = ""
                            for char in bonusEff:
                                if char in "0123456789.":
                                    tempStr += char
                            addedDMG += float(tempStr)
                            dmgSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")

                if ("attack speed" in bonusEff or "firerate" in bonusEff or "fire rate" in bonusEff):
                    if w.type.lower() in bonus[2].lower() or w.weaponType.lower() in bonus[2].lower() or "all" in bonus[2].lower() or w.name in bonus[2]:
                        if "," in bonusEff:
                            bonusEffects = bonusEff.split(",")
                            for eff in bonusEffects:
                                if ("attack speed" in eff or "firerate" in eff or "fire rate" in eff):
                                    tempStr = ""
                                    for char in eff:
                                        if char in "0123456789.":
                                            tempStr += char
                                    addedATS += float(tempStr)
                                    atsSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {effect}")
                        else:
                            tempStr = ""
                            for char in bonusEff:
                                if char in "0123456789.":
                                    tempStr += char
                            addedATS += float(tempStr)
                            atsSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")

                if "crit" in bonusEff:
                    if "crit chance" in bonusEff and "q" not in bonusEff:
                        if w.type.lower() in bonus[2].lower() or w.weaponType.lower() in bonus[2].lower() or "all" in bonus[2].lower() or w.name in bonus[2]:
                            if "," in bonusEff:
                                bonusEffects = bonusEff.split(",")
                                for eff in bonusEffects:
                                    if "crit chance" in eff:
                                        tempStr = ""
                                        for char in eff:
                                            if char in "0123456789.":
                                                tempStr += char
                                        addedcritC += float(tempStr)
                                        critCSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {effect}")
                            else:
                                tempStr = ""
                                for char in bonusEff:
                                    if char in "0123456789.":
                                        tempStr += char
                                addedcritC += float(tempStr)
                                critCSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")
                    if "crit damage" in bonusEff:
                        if w.type.lower() in bonus[2].lower() or w.weaponType.lower() in bonus[2].lower() or "all" in bonus[2].lower() or w.name in bonus[2]:
                            if "," in bonusEff:
                                bonusEffects = bonusEff.split(",")
                                for eff in bonusEffects:
                                    if "crit damage" in eff:
                                        tempStr = ""
                                        for char in eff:
                                            if char in "0123456789.":
                                                tempStr += char
                                        addedcritD += float(tempStr)
                                        critDSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {effect}")
                            else:
                                tempStr = ""
                                for char in bonusEff:
                                    if char in "0123456789.":
                                        tempStr += char
                                addedcritD += float(tempStr)
                                critDSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")
                
                if "headshot" in bonusEff:
                    if w.type.lower() in bonus[2].lower() or w.weaponType.lower() in bonus[2].lower() or "all" in bonus[2].lower() or w.name in bonus[2]:
                        if "," in bonusEff:
                            bonusEffects = bonusEff.split(",")
                            for eff in bonusEffects:
                                if "headshot" in bonusEff :
                                    tempStr = ""
                                    for char in eff:
                                        if char in "0123456789.":
                                            tempStr += char
                                    addedHSM += float(tempStr)
                                    hsmSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {effect}")
                        else:
                            tempStr = ""
                            for char in bonusEff:
                                if char in "0123456789.":
                                    tempStr += char
                            addedHSM += float(tempStr)
                            hsmSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")
            
            weaponStatLayout = QGridLayout()
            if w != None:
                dmgTitle = QLabel("<font color = #dffe5e>Damage")
                dmgTitle.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                dmgTitle.setWordWrap(True)
                dmgPLabel = QLabel(f"<font color = #ff6158><h3>+{round(addedDMG,2)}%")
                dmgPLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                dmgPLabel.setToolTip(self.getToolTip(dmgSources))
                dmgTLabel = QLabel(f"<font color = #29ffff><h2>{round(w.damage*(1+(addedDMG/100)),2)}")
                dmgTLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                weaponStatLayout.addWidget(dmgTitle, 0, 0)
                weaponStatLayout.addWidget(dmgPLabel, 1, 0)
                weaponStatLayout.addWidget(dmgTLabel, 2, 0)

                atsTitle = QLabel("<font color = #dffe5e>Attack Speed")
                atsTitle.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                atsTitle.setWordWrap(True)
                atsPLabel = QLabel(f"<font color = #ff6158><h3>+{round(addedATS,2)}%")
                atsPLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                atsPLabel.setToolTip(self.getToolTip(atsSources))
                atsTLabel = QLabel(f"<font color = #29ffff><h2>{round(w.firerate*(1+(addedATS/100)),2)}")
                atsTLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                weaponStatLayout.addWidget(atsTitle, 3, 0)
                weaponStatLayout.addWidget(atsPLabel, 4, 0)
                weaponStatLayout.addWidget(atsTLabel, 5, 0)

                critCTitle = QLabel("<font color = #dffe5e>Crit Chance")
                critCTitle.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter) 
                critCTitle.setWordWrap(True)
                critCPLabel = QLabel(f"<font color = #ff6158><h3>+{round(addedcritC,2)}%")
                critCPLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                critCPLabel.setToolTip(self.getToolTip(critCSources))
                critCTLabel = QLabel(f"<font color = #29ffff><h2>{round(min(100,addedcritC),2)}%")
                critCTLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                weaponStatLayout.addWidget(critCTitle, 0, 1)
                weaponStatLayout.addWidget(critCPLabel, 1, 1)
                weaponStatLayout.addWidget(critCTLabel, 2, 1)

                critDTitle = QLabel("<font color = #dffe5e>Crit Damage")
                critDTitle.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                critDTitle.setWordWrap(True)
                critDPLabel = QLabel(f"<font color = #ff6158><h3>+{round(addedcritD,2)}%")
                critDPLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                critDPLabel.setToolTip(self.getToolTip(critDSources))
                critDTLabel = QLabel(f"<font color = #29ffff><h2>{round((addedcritD + 50),2)}%")
                critDTLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                weaponStatLayout.addWidget(critDTitle, 3, 1)
                weaponStatLayout.addWidget(critDPLabel, 4, 1)
                weaponStatLayout.addWidget(critDTLabel, 5, 1)

                if "blunt" not in w.weaponType and "blade" not in w.weaponType:
                    hsmTitle = QLabel("<font color = #dffe5e>Headshot Multiplier")
                    hsmTitle.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    hsmTitle.setWordWrap(True)
                    hsmPLabel = QLabel(f"<font color = #ff6158><h3>+{round(addedHSM,2)}%")
                    hsmPLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    hsmPLabel.setToolTip(self.getToolTip(hsmSources))
                    hsmTLabel = QLabel(f"<font color = #29ffff><h2>+{round(w.headshot + addedHSM,2)}%")
                    hsmTLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    weaponStatLayout.addWidget(hsmTitle, 0, 2)
                    weaponStatLayout.addWidget(hsmPLabel, 1, 2)
                    weaponStatLayout.addWidget(hsmTLabel, 2, 2)

                dpsTitle = QLabel("<font color = #dffe5e>Peak DPS (No HS / HS)")
                dpsTitle.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                dpsTitle.setWordWrap(True)
                if w.weaponType not in "blunt blade ":
                    hsm = (w.headshot + addedHSM + 100)/100
                else:
                    hsm = 1
                if "throwable" not in w.weaponType:
                    if addedcritC != 0: 
                        dpsNoHS = QLabel(f"<font color = #ff6158><h2>{round( (w.damage * (1+(addedDMG/100)) ) * (w.firerate * (1+(addedATS/100)) ) * (1+ ((min(addedcritC,100))/100) * ((addedcritD+50)/100) ) )}")
                        dpsHS = QLabel(f"<font color = #29ffff><h2>{round(((w.damage*(1+(addedDMG/100)))*(w.firerate*(1+(addedATS/100)))*(1+(((min(addedcritC,100))/100)*((addedcritD + 50)/100))) * hsm))}")
                        dmgpershot = round(((w.damage*(1+(addedDMG/100)))*(1+(((min(addedcritC,100))/100)*((addedcritD + 50)/100))) * hsm))
                    else:
                        dpsNoHS = QLabel(f"<font color = #ff6158><h2>{round((w.damage*(1+(addedDMG/100)))*(w.firerate*(1+(addedATS/100))))}")
                        dpsHS = QLabel(f"<font color = #29ffff><h2>{round(((w.damage*(1+(addedDMG/100)))*(w.firerate*(1+(addedATS/100)))) * hsm)}")
                        dmgpershot = round((w.damage*(1+(addedDMG/100))) * hsm)
                    dpsNoHS.setToolTip("Calculated As:<br>(New DMG) * (New ATS) *(1+((min(Crit Chance, 100) / 100) * (1+(Crit Damage / 100 ))))")
                    dpsHS.setToolTip(f"Peak Damage per hit:<br>{dmgpershot}<br><br>Calculated As:<br>DPS No Headshot * (1+(HSM) / 100)")
                else:
                    if addedcritC != 0: 
                        dpsNoHS = QLabel(f"<font color = #ff6158><h2>{round( (w.damage * (1+(addedDMG/100)) ) * (1) * (1+ ((min(addedcritC,100))/100) * ((addedcritD+50)/100)) * 1.5)}")
                        dpsHS = QLabel(f"<font color = #29ffff><h2>{round(((w.damage*(1+(addedDMG/100)))*(1)*(1+(((min(addedcritC,100))/100)*((addedcritD + 50)/100))) * hsm) * 1.5)}")
                        dmgpershot = round(((w.damage*(1+(addedDMG/100)))*(1+(((min(addedcritC,100))/100)*((addedcritD + 50)/100))) * hsm) * 1.5)
                    else:
                        dpsNoHS = QLabel(f"<font color = #ff6158><h2>{round((w.damage*(1+(addedDMG/100)))*(1))}")
                        dpsHS = QLabel(f"<font color = #29ffff><h2>{round(((w.damage*(1+(addedDMG/100)))*(1)) * hsm)}")
                        dmgpershot = round((w.damage*(1+(addedDMG/100))) * hsm * 1.5)
                    dpsNoHS.setToolTip("Calculated As:<br>(New DMG) * (1) *(1+((min(Crit Chance, 100) / 100) * (1+(Crit Damage / 100 )))) * 1.5<br>1.5 is the estimated thrown multiplier<br>1 is taken as a general attack speed estimate of 1 throwing attack per second")
                    dpsHS.setToolTip(f"Peak Damage per throw:<br>{dmgpershot}<br><br>Calculated As:<br>DPS No Headshot * (1+(HSM) / 100)")
                dpsNoHS.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                dpsHS.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                weaponStatLayout.addWidget(dpsTitle, 3, 2)
                weaponStatLayout.addWidget(dpsNoHS, 4, 2)
                weaponStatLayout.addWidget(dpsHS, 5, 2)


                weaponLabel = QLabel()
                weaponLabel.setLayout(weaponStatLayout)
                weaponWrapper.addWidget(weaponLabel)
                wrapperLabel = QLabel()
                if counter == 1:
                    wrapperLabel.setStyleSheet("background-color: #2c151b")
                else:
                    wrapperLabel.setStyleSheet("background-color: #31181e")

                if windowWidth > 1920:
                    iconicLabel = QLabel(f"<font color = #ffd740>{w.iconic}<br><font color = #ff615a>{w.intrinsic}")
                    iconicLabel.setWordWrap(True)
                    iconicLabel.setMaximumWidth(250)
                    weaponWrapper.addWidget(iconicLabel)          
                wrapperLabel.setLayout(weaponWrapper)
                weaponLayout.addWidget(wrapperLabel)
                counter += 1

        addedHealthPerc = 0
        addedHealthNum = 0
        healthPercSources = []
        healthNumSources = []

        addedHealthRegen = 0
        healthRegenSources = []

        addedMovSpeed = 0
        movSpeedSources = []


        addedArmorPerc = 0
        addedArmorNum = 0
        armorPercSources = []
        armorNumSources = []

        addedDmgRed = 0
        DmgRedSources = []

        addedMitChance = 0
        mitChanceSources = []

        addedMitStrength = 0
        mitStrengthSources = []


        addedRam = 0
        ramSources = []

        addedRamRec = 0
        ramRecSources = []

        addedQHdmg = 0
        QHdmgSources = []


        for bonus in bonuses:
            bonusEff = bonus[1].lower()
            if "health" in bonusEff and "regen" not in bonusEff and "item" not in bonusEff:
                if "," in bonusEff:
                    bonusEffects = bonusEff.split(",")
                    for eff in bonusEffects:
                        if "health" in eff:
                            if "%" in eff:
                                tempStr = ""
                                for char in eff:
                                    if char in "0123456789.":
                                        tempStr += char
                                if tempStr == "":
                                    tempStr = "0"
                                addedHealthPerc += float(tempStr)
                                healthPercSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {eff}")
                            else:
                                tempStr = ""
                                for char in eff:
                                    if char in "0123456789.":
                                        tempStr += char
                                if tempStr == "":
                                    tempStr = "0"
                                addedHealthNum += float(tempStr)
                                healthNumSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {eff}")
                else:
                    if "%" in bonusEff:
                        tempStr = ""
                        for char in bonusEff:
                            if char in "0123456789.":
                                tempStr += char
                        if tempStr == "":
                            tempStr = "0"
                        addedHealthPerc += float(tempStr)
                        healthPercSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")
                    else:
                        tempStr = ""
                        for char in bonusEff:
                            if char in "0123456789.":
                                tempStr += char
                        if tempStr == "":
                            tempStr = "0"
                        addedHealthNum += float(tempStr)
                        healthNumSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")


            if "regen" in bonusEff and "health" in bonusEff:
                if "," in bonusEff:
                    bonusEffects = bonusEff.split(",")
                    for eff in bonusEffects:
                        if "regen" in eff:
                            tempStr = ""
                            for char in eff:
                                if char in "0123456789.":
                                    tempStr += char
                            if tempStr == "":
                                tempStr = "0"
                            addedHealthRegen += float(tempStr)
                            healthRegenSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {eff}")
                else:
                    tempStr = ""
                    for char in bonusEff:
                        if char in "0123456789.":
                            tempStr += char
                    if tempStr == "":
                        tempStr = "0"
                    addedHealthRegen += float(tempStr)
                    healthRegenSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")

            if ("movspeed" in bonusEff or "movement speed" in bonusEff) and "crouch" not in bonusEff and "crouch" not in bonus[len(bonus)-1]:
                if "," in bonusEff:
                    bonusEffects = bonusEff.split(",")
                    for eff in bonusEffects:
                        if "movspeed" in eff:
                            tempStr = ""
                            for char in eff:
                                if char in "0123456789.":
                                    tempStr += char
                            if tempStr == "":
                                tempStr = "0"
                            addedMovSpeed += float(tempStr)
                            movSpeedSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {eff}")
                else:
                    tempStr = ""
                    for char in bonusEff:
                        if char in "0123456789.":
                            tempStr += char
                    if tempStr == "":
                        tempStr = "0"
                    addedMovSpeed += float(tempStr)
                    movSpeedSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")

                
            if "armor" in bonusEff and "pen" not in bonusEff and "enemy" not in bonusEff:
                if "," in bonusEff:
                    bonusEffects = bonusEff.split(",")
                    for eff in bonusEffects:
                        if "armor" in eff:
                            if "%" in eff:
                                tempStr = ""
                                for char in eff:
                                    if char in "0123456789.":
                                        tempStr += char
                                if tempStr == "":
                                    tempStr = "0"
                                addedArmorPerc += float(tempStr)
                                armorPercSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {eff}")
                            else:
                                tempStr = ""
                                for char in eff:
                                    if char in "0123456789.":
                                        tempStr += char
                                if tempStr == "":
                                    tempStr = "0"
                                addedArmorNum += float(tempStr)
                                armorNumSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {eff}")
                else:
                    if "%" in bonusEff:
                        tempStr = ""
                        for char in bonusEff:
                            if char in "0123456789.":
                                tempStr += char
                        if tempStr == "":
                            tempStr = "0"
                        addedArmorPerc += float(tempStr)
                        armorPercSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")
                    else:
                        tempStr = ""
                        for char in bonusEff:
                            if char in "0123456789.":
                                tempStr += char
                        if tempStr == "":
                            tempStr = "0"
                        addedArmorNum += float(tempStr)
                        armorNumSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")

            if ("inc" in bonusEff and ("dmg" in bonusEff or "damage" in bonusEff)) or (("damage" in bonusEff or "dmg" in bonusEff) and "reduction" in bonusEff):
                if "," in bonusEff:
                    bonusEffects = bonusEff.split(",")
                    for eff in bonusEffects:
                        if ("inc" in eff and ("dmg" in eff or "damage" in eff)) or (("damage" in eff or "dmg" in eff) and "reduction" in eff):
                            tempStr = ""
                            for char in eff:
                                if char in "0123456789.":
                                    tempStr += char
                            if tempStr == "":
                                tempStr = "0"
                            addedDmgRed += float(tempStr)
                            DmgRedSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {eff}")
                else:
                    tempStr = ""
                    for char in bonusEff:
                        if char in "0123456789.":
                            tempStr += char
                    if tempStr == "":
                        tempStr = "0"
                    addedDmgRed += float(tempStr)
                    DmgRedSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")

            if "mit" in bonusEff:
                if ("mit chance" in bonusEff or "mitigation chance" in bonusEff) and "q" not in bonusEff:
                    if "," in bonusEff:
                        bonusEffects = bonusEff.split(",")
                        for eff in bonusEffects:
                            if ("mit chance" in bonusEff or "mitigation chance" in bonusEff) in eff:
                                tempStr = ""
                                for char in eff:
                                    if char in "0123456789.":
                                        tempStr += char
                                addedMitChance += float(tempStr)
                                mitChanceSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {effect}")
                    else:
                        tempStr = ""
                        for char in bonusEff:
                            if char in "0123456789.":
                                tempStr += char
                        addedMitChance += float(tempStr)
                        mitChanceSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")
                if ("mit strength" in bonusEff or "mitigation strength" in bonusEff):
                        if "," in bonusEff:
                            bonusEffects = bonusEff.split(",")
                            for eff in bonusEffects:
                                if "crit damage" in eff:
                                    tempStr = ""
                                    for char in eff:
                                        if char in "0123456789.":
                                            tempStr += char
                                    addedcritD += float(tempStr)
                                    critDSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {effect}")
                        else:
                            tempStr = ""
                            for char in bonusEff:
                                if char in "0123456789.":
                                    tempStr += char
                            addedMitStrength += float(tempStr)
                            mitStrengthSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")

            if " ram" in bonusEff and "regen" not in bonusEff and "recovery" not in bonusEff:
                if "," in bonusEff:
                    bonusEffects = bonusEff.split(",")
                    for eff in bonusEffects:
                        if " ram" in eff:
                            tempStr = ""
                            for char in eff:
                                if char in "0123456789.":
                                    tempStr += char
                            if tempStr == "":
                                tempStr = "0"
                            if "-" in eff:
                                addedRam -= float(tempStr)
                            else:
                                addedRam += float(tempStr)
                            ramSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {eff}")
                else:
                    tempStr = ""
                    for char in bonusEff:
                        if char in "0123456789.":
                            tempStr += char
                    if tempStr == "":
                        tempStr = "0"
                    if "-" in bonusEff:
                        addedRam -= float(tempStr)
                    else:
                        addedRam += float(tempStr)
                    ramSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")
            
            if " ram" in bonusEff and ("regen" in bonusEff or "recovery" in bonusEff):
                if "," in bonusEff:
                    bonusEffects = bonusEff.split(",")
                    for eff in bonusEffects:
                        if "regen" in eff:
                            tempStr = ""
                            for char in eff:
                                if char in "0123456789.":
                                    tempStr += char
                            if tempStr == "":
                                tempStr = "0"
                            addedRamRec += float(tempStr)
                            ramRecSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {eff}")
                else:
                    tempStr = ""
                    for char in bonusEff:
                        if char in "0123456789.":
                            tempStr += char
                    if tempStr == "":
                        tempStr = "0"
                    addedRamRec += float(tempStr)
                    ramRecSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")
        
            if ("quickh" in bonusEff or "qh" in bonusEff) and ("damage" in bonusEff or "dmg" in bonusEff):
                if "," in bonusEff:
                    bonusEffects = bonusEff.split(",")
                    for eff in bonusEffects:
                        if "q" in eff:
                            tempStr = ""
                            for char in eff:
                                if char in "0123456789.":
                                    tempStr += char
                            if tempStr == "":
                                tempStr = "0"
                            addedQHdmg += float(tempStr)
                            QHdmgSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {eff}")
                else:
                    tempStr = ""
                    for char in bonusEff:
                        if char in "0123456789.":
                            tempStr += char
                    if tempStr == "":
                        tempStr = "0"
                    addedQHdmg += float(tempStr)
                    QHdmgSources.append(f"<font color = #ff6158>{bonus[0]}</font> - {bonusEff}")

        otherStatLayout = QVBoxLayout()

        generalStats = QGridLayout()
        
        healthLabel = QLabel(f"<font color = #29ffff><h3>Health")
        healthLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        healthaddedLabel = QLabel(f"<font color = #29ffff><h2>+{addedHealthPerc}%<br><font color = #29ffff>+{addedHealthNum}")
        healthaddedLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        healthaddedLabel.setToolTip(f"Base = 100<br>lvl 60 = +300<br>lvl 60 Base = 400<br><br>Percentages = <br>{self.getToolTip(healthPercSources)}<br><br>Addition = <br>{self.getToolTip(healthNumSources)}")
        newHealthNum = round((400 + addedHealthNum) * (1+addedHealthPerc/100))
        totalHealthLabel = QLabel(f"<font color = #29ffff><h1>{newHealthNum} HP")
        totalHealthLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        generalStats.addWidget(healthLabel, 0,0)
        generalStats.addWidget(healthaddedLabel, 0,1)
        generalStats.addWidget(totalHealthLabel, 0,2)


        healthRegenLabel = QLabel(f"<font color = #29ffff><h3>Health Regen")
        healthRegenLabel.setWordWrap(True)
        healthRegenLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        healthRegenaddedLabel = QLabel(f"<font color = #29ffff><h2>+{addedHealthRegen}%")
        healthRegenaddedLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        healthRegenaddedLabel.setToolTip(f"{self.getToolTip(healthRegenSources)}")
        healthPerSecond = 0
        if activePerks != None:
            for perk in activePerks:
                if "Painkiller" in perk.name:
                    healthPerSecond = round((1 + (addedHealthRegen/100))/100 * newHealthNum, 2)
        totalHealthRegenLabel = QLabel(f"<font color = #29ffff><h1>{healthPerSecond} HP/s")
        totalHealthRegenLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        generalStats.addWidget(healthRegenLabel, 1,0)
        generalStats.addWidget(healthRegenaddedLabel, 1,1)
        generalStats.addWidget(totalHealthRegenLabel, 1,2)


        movementSpeedlabel = QLabel(f"<font color = #ff5e55><h3>Movement Speed")
        movementSpeedlabel.setWordWrap(True)
        movementSpeedlabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        movementSpeedaddedLabel = QLabel(f"<font color = #ff5e55><h2>+{addedMovSpeed}%")
        movementSpeedaddedLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        movementSpeedaddedLabel.setToolTip(f"{self.getToolTip(movSpeedSources)}")
        totalMovementSpeedLabel = QLabel(f"<font color = #ff5e55><h1>x {(addedMovSpeed+100)/100}")
        totalMovementSpeedLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        generalStats.addWidget(movementSpeedlabel, 2,0)
        generalStats.addWidget(movementSpeedaddedLabel, 2,1)
        generalStats.addWidget(totalMovementSpeedLabel, 2,2)

        generalStatLabel = QLabel()
        generalStatLabel.setMaximumHeight(int(windowHeight/4))
        generalStatLabel.setStyleSheet("background-color: #2c151b")
        generalStatLabel.setLayout(generalStats)

        otherStatLayout.addWidget(generalStatLabel)

        for cyberware in ACTIVECYBERWARE:
            addedArmorNum += int(cyberware.armor)
            armorNumSources.append(cyberware.name)

        defense = QVBoxLayout()

        defenseTitle = QLabel("<font color = #29ffff><h1>Defense")
        defenseTitle.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        defenseTitle.setMaximumHeight(50)
        defense.addWidget(defenseTitle)

        defenseStats = QGridLayout()

        armorName = QLabel("<h3><font color = #29ffff>Armor")
        armorName.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        armorAdded = QLabel(f"<h2><font color = #29ffff>+{addedArmorPerc}%<br>+{addedArmorNum}")
        armorAdded.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        armorAdded.setToolTip(f"Percentages = <br>{self.getToolTip(armorPercSources)}<br><br>Addition = <br>{self.getToolTip(armorNumSources)}")
        finalArmor = round(addedArmorNum * (1+(addedArmorPerc/100)))
        totalArmor = QLabel(f"<h2><font color = #29ffff>{finalArmor}")
        totalArmor.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        defenseStats.addWidget(armorName,0,0)
        defenseStats.addWidget(armorAdded,0,1)
        defenseStats.addWidget(totalArmor,0,2)

        dmgredName = QLabel(f"<h3><font color = #29ffff>Damage Reduction")
        dmgredName.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        dmgredName.setWordWrap(True)
        dmgredAdded = QLabel(f"<h2><font color = #29ffff>+{addedDmgRed}%")
        dmgredAdded.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        dmgredAdded.setToolTip(self.getToolTip(DmgRedSources))
        totalDmgRed = QLabel(f"<h2><font color = #29ffff>+{addedDmgRed}%")
        totalDmgRed.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        defenseStats.addWidget(dmgredName,1,0)
        defenseStats.addWidget(dmgredAdded,1,1)
        defenseStats.addWidget(totalDmgRed,1,2)
        
        mitCName = QLabel("<h3><font color = #ff5e55>Mitigation Chance")
        mitCName.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        mitCName.setWordWrap(True)
        mitCAdded = QLabel(f"<h2><font color = #ff5e55>+{addedMitChance}%")
        mitCAdded.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        mitCAdded.setToolTip(self.getToolTip(mitChanceSources))
        totalMitC = QLabel(f"<h2><font color = #ff5e55>{addedMitChance + 10}%")
        totalMitC.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        totalMitC.setToolTip(f"Total Mitigation Chance is capped at 100% in game")

        defenseStats.addWidget(mitCName,2,0)
        defenseStats.addWidget(mitCAdded,2,1)
        defenseStats.addWidget(totalMitC,2,2)

        mitSName = QLabel("<h3><font color = #ff5e55>Mitigation Strength")
        mitSName.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        mitSName.setWordWrap(True)
        mitSAdded = QLabel(f"<h2><font color = #ff5e55>+{addedMitStrength}%")
        mitSAdded.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        mitSAdded.setToolTip(self.getToolTip(mitStrengthSources))
        totalMitS = QLabel(f"<h2><font color = #ff5e55>{addedMitStrength + 50}%")
        totalMitS.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        totalMitS.setToolTip(f"Total Mitigation Strength is capped at 90% in game")

        defenseStats.addWidget(mitSName,3,0)
        defenseStats.addWidget(mitSAdded,3,1)
        defenseStats.addWidget(totalMitS,3,2)

        defenseStatsLabel = QLabel()
        defenseStatsLabel.setLayout(defenseStats)

        defense.addWidget(defenseStatsLabel)
        defenseLabel = QLabel()
        defenseLabel.setStyleSheet("background-color: #31181e")
        defenseLabel.setLayout(defense)
        otherStatLayout.addWidget(defenseLabel)

        qhWrapper = QVBoxLayout()
        qhTitle = QLabel("<font color = #dbfb5d><h1>Quickhacks")
        qhTitle.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        qhTitle.setMaximumHeight(50)

        totalRam = 0
        for c in ACTIVECYBERWARE:
            if hasattr(c,"ram") == True:
                totalRam = float(c.ram)
                break
        
        totalRam += addedRam

        qhStatsWrapper = QGridLayout()

        ram = QLabel(f"<font color = #dbfb5d><h3>RAM<h2>{totalRam}")
        ram.setToolTip(self.getToolTip(ramSources))
        ram.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        ramRegen = QLabel(f"<font color = #dbfb5d><h3>RAM Regen<h2>{addedRamRec}%")
        ramRegen.setToolTip(f"Estimated:<br>+{addedRamRec/100} RAM/sec.<br><br>{self.getToolTip(ramRecSources)}")
        ramRegen.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        ramRegen.setWordWrap(True)

        qhdmg = QLabel(f"<font color = #dbfb5d><h3>Quickhack<br>Damage<h2>+{addedQHdmg}%")
        qhdmg.setToolTip(self.getToolTip(QHdmgSources))
        qhdmg.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        qhdmg.setWordWrap(True)

        qhStatsWrapper.addWidget(ram,0,0)
        qhStatsWrapper.addWidget(ramRegen,0,1)
        qhStatsWrapper.addWidget(qhdmg,0,2)

        qhStatsLabel = QLabel()
        qhStatsLabel.setLayout(qhStatsWrapper)

        qhWrapper.addWidget(qhTitle)
        qhWrapper.addWidget(qhStatsLabel)

        qhLabel = QLabel()
        qhLabel.setLayout(qhWrapper)
        qhLabel.setMaximumHeight(int(windowHeight/5))
        qhLabel.setStyleSheet("background-color: #2c151b")

        otherStatLayout.addWidget(qhLabel)

        windowSize = WINDOW.size()
        windowWidth = windowSize.width()

        otherStatLabel = QLabel()
        otherStatLabel.setMaximumWidth(int(windowWidth/4))
        otherStatLabel.setLayout(otherStatLayout)

        weaponLayoutLabel = QLabel()
        weaponLayoutLabel.setLayout(weaponLayout)
        statLayout.setContentsMargins(5,5,5,5)
        statLayout.addWidget(weaponLayoutLabel)
        statLayout.addWidget(otherStatLabel)
        statLabel = QLabel()
        statLabel.setStyleSheet("background-color: #1d0005")
        statLabel.setLayout(statLayout)

        self.setCentralWidget(statLabel)


    def statButton(self, num):
        global STATBUTTONLIST
        match STATBUTTONLIST[num]:
            case 1:
                STATBUTTONLIST[num] = 0
            case 0:
                STATBUTTONLIST[num] = 1
        self.statScreen()

    def getToolTip(self, list):
        string = "Sources:"
        for item in list:
            string += f"<br>- {item}"
        return string

    def binToB32(self, binary_str):
        base32_chars = string.digits + string.ascii_uppercase
        base32_val = 0
        power = 0
        
        for bit in reversed(binary_str):
            if bit == '1':
                base32_val += 2 ** power
            power += 1
        
        base32_str = ''
        while base32_val > 0:
            base32_str = base32_chars[base32_val % 32] + base32_str
            base32_val //= 32
        
        return base32_str.lower() if base32_str else '0'
    
    def decToB32(self,decNum):
        base32_digits = "0123456789abcdefghijklmnopqrstuv"
        result = ""
        
        while int(decNum) > 0:
            remainder = decNum % 32
            result = base32_digits[remainder] + result
            decNum = decNum // 32
        if result == "":
            result = "0"
        return result
    
    def b32ToDec(self, b32Num):
        base32_digits = "0123456789abcdefghijklmnopqrstuv"
        result = 0

        # Reverse the input string to start processing from the least significant digit
        b32Num = b32Num[::-1]

        for i in range(len(b32Num)):
            digit = base32_digits.index(b32Num[i])
            result += digit * (32 ** i)

        return result
    
    def b32ToBinary(self, b32Num):
        result_dec = self.b32ToDec(b32Num)
        # Convert decimal to binary
        result_bin = bin(result_dec)[2:]  # Convert decimal to binary string
        return result_bin

    def save(self):
        FullSaveCode = ""

        # creating the code for the perks
        attributeCode = ""
        perkCounter = 0
        for perkList in [BODYPERKS,REFLEXESPERKS,TECHPERKS,INTELLIGENCEPERKS,COOLPERKS]:
            # 3 strings per attribute, 1 for all the full nodes, 1 for the empty and 1 for the nonfull and nonempty
            nodeAmount = len(perkList)
            fullNodes = []
            emptyNodes = []
            for i in range(nodeAmount):
                fullNodes.append("0")
                emptyNodes.append("0")
            otherNodes = ""
            for node in perkList:
                nodeList = ""
                for perk in node:
                    s = "ERROR"
                    if perk.maxlvl > 1:
                        match perk.level:
                            case 1:
                                s = "01"
                            case 2:
                                if perk.maxlvl == 2:
                                    s = "11"
                                else:
                                    s = '10'
                            case 3:
                                s = "11"
                            case 0:
                                s = "00"
                        nodeList += s
                    else:
                        nodeList += str(perk.level)
                i = perkList.index(node)
                if "1" not in nodeList:
                    emptyNodes[i] = "1"
                elif "0" not in nodeList:
                    fullNodes[i] = "1"
                else:
                    base32 = self.binToB32(nodeList)
                    if len(base32) > 1:
                        base32 = f"+{base32}"
                    otherNodes += base32
            # attributeCodeList.append([fullNodes, emptyNodes, otherNodes])
            fullNodesStr = ""
            emptyNodesStr = ""
            for item in fullNodes:
                fullNodesStr += str(item)
            for item in emptyNodes:
                emptyNodesStr += str(item)
            fullNodesB32 = self.binToB32(fullNodesStr) 
            emptyNodesB32 = self.binToB32(emptyNodesStr)
            string = "ERROR"
            match perkCounter:
                case 0:
                    string = "B"+self.decToB32(global_attributes["BODY"])
                case 1:
                    string = "R"+self.decToB32(global_attributes["REFLEXES"])
                case 2:
                    string = "T"+self.decToB32(global_attributes["TECH"])
                case 3:
                    string = "I"+self.decToB32(global_attributes["INTELLIGENCE"])
                case 4:
                    string = "C"+self.decToB32(global_attributes["COOL"])
            perkCounter += 1
            string += f"{fullNodesB32}/{emptyNodesB32}/{otherNodes}"
            attributeCode += string
            
        fileList = [["arms",1],["circulatory-system",3],["face",1],["frontal-cortex",3],["hands",2],["integumentary-system",3],["legs",1],["nervous-system",3],["operating-system",1],["skeleton",3]]
        orderedCybList = []
        for x in fileList:
            orderedCybList.append([])

        for c in ACTIVECYBERWARE:
            for file in fileList:
                if file[0] in c.filename:
                    orderedCybList[fileList.index(file)].append(c.index + 1)

        for list in orderedCybList:
            index = fileList[orderedCybList.index(list)]
            while len(list) < index[1]:
                list.append("0")

        cyberwareCode = ""

        for l in orderedCybList:
            if l == []:
                l = ["0"]
            for entry in l:
                entryB32 = self.decToB32(entry)
                cyberwareCode += entryB32

        weaponFileList = ["ar","blade","blunt","Empty Weapon","LMG","pistol","precision rifle","revolver","shotgun","SMG","sniper rifle","throwable"]
        wIndexList = []
        weaponsList = [WEAPON1, WEAPON2, WEAPON3]
        weaponCode = ""
        for weapon in weaponsList:
            if weapon != None:
                for wfl in weaponFileList:
                    if wfl in weapon.weaponType:
                        wIndexList.append([weaponFileList.index(wfl)+1,weapon.index+1])
            else:
                wIndexList.append(["0","0"])
        for list in wIndexList:
            for indexNum in list:
                weaponCode += f"{self.decToB32(indexNum)}"

        FullSaveCode = f"{attributeCode}-{cyberwareCode}-{weaponCode}"

        self.savePopup(FullSaveCode)

    def savePopup(self, code):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Save/Copy Menu")
        dialog.setLabelText(f"Your copyable code:\n\n{code}\n\nEnter a Save Filename and press 'Ok' to save.\nPress 'Cancel' to exit this window without saving.")
        label = dialog.findChild(QLabel)
        if label:
            label.setTextInteractionFlags(label.textInteractionFlags() | Qt.TextSelectableByMouse)
        okPressed = dialog.exec_()
        if okPressed == QInputDialog.Accepted:
            filename, ok = dialog.textValue(), True
            if filename.strip():
                try:
                    with open(f"Saves/{filename}.txt", "w") as file:
                        file.write(str(code))
                except Exception as e:
                    ok = False
                    print(f"Error saving file: {e}")
            else:
                ok = False
            if not ok:
                self.savePopup(code)

    def enterCodePopup(self, code):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Enter Code")
        dialog.setLabelText(f"Please enter your code:")
        label = dialog.findChild(QLabel)
        if label:
            label.setTextInteractionFlags(label.textInteractionFlags() | Qt.TextSelectableByMouse)
        okPressed = dialog.exec_()
        if okPressed == QInputDialog.Accepted:
            code, ok = dialog.textValue(), True
            try:
                self.openBuild(code)
            except Exception as e:
                print(e)
                self.enterCodePopup(code)


    def openBuild(self, code):
        global global_attributes
        global BODYPERKS
        global REFLEXESPERKS
        global TECHPERKS
        global INTELLIGENCEPERKS
        global COOLPERKS
        global PERKPOINTS
        global ACTIVECYBERWARE

        global CWBUTTONLIST

        global WEAPON1
        global WEAPON2
        global WEAPON3

        ACTIVECYBERWARE = []
        CWBUTTONLIST = []
        for i in ACTIVECYBERWARE:
            ACTIVECYBERWARE.remove(i)
        for i in CWBUTTONLIST:
            CWBUTTONLIST.remove(i)
        
        
        codeSegments = code.split("-")
        perkCode = codeSegments[0]
        cybCode = codeSegments[1]
        wpnCode = codeSegments[2]
        attributeList = ["BODY", "REFLEXES","TECH","INTELLIGENCE","COOL"]
        attributeCodeList = [[],[],[],[],[]]
        for attribute in attributeList:
            attrCodes = []
            perkCode = perkCode[1:]
            global_attributes[attribute] = int(self.b32ToDec(perkCode[0]))
            if len(perkCode) > 1 and perkCode[1] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                perkCode = perkCode[1:]
                # fullNodes
                fullNodes = ""
                for char in perkCode:
                    if char != "/":
                        fullNodes += char
                    else:
                        break
                perkCode = perkCode[(len(fullNodes) + 1):]
                attrCodes.append(fullNodes)
                # Empty Nodes
                emptyNodes = ""
                for char in perkCode:
                    if char != "/":
                        emptyNodes += char
                    else:
                        break
                perkCode = perkCode[(len(emptyNodes) + 1):]
                attrCodes.append(emptyNodes)
                # Non full or empty Nodes
                otherPerks = []
                while (len(perkCode) > 0) and perkCode[0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    if perkCode[0] != "+":
                        otherPerks.append(perkCode[0])
                        perkCode = perkCode[1:]
                    else:
                        perkCode = perkCode[1:]
                        otherPerks.append(perkCode[:2])
                        perkCode = perkCode[2:]
                attrCodes.append(otherPerks)
                attributeCodeList[attributeList.index(attribute)] = attrCodes
            else:
                perkCode = perkCode[1:]
        
        counter = 0
        for l in attributeCodeList:
            if l != []:
                l[0] = self.b32ToBinary(l[0]) 
                l[1] = self.b32ToBinary(l[1])
                perkList = [BODYPERKS, REFLEXESPERKS, TECHPERKS, INTELLIGENCEPERKS, COOLPERKS]
                convertedList = []
                for i in range(len(perkList[counter])):
                    convertedList.append("")
                while len(l[0]) < len(convertedList):
                    l[0] = "0" + l[0]
                c1 = 0
                for char in l[0]:
                    if char == "1":
                        convertedList[c1] = "F"
                    c1 += 1
                while len(l[1]) < len(convertedList):
                    l[1] = "0" + l[1]
                c2 = 0
                for char in l[1]:
                    if char == "1":
                        convertedList[c2] = "E"
                    c2 += 1
                
                c3 = 0
                otherPerkList = l[2]
                newconvertedList = []
                for entry in convertedList:
                    if entry == "":
                        entry = otherPerkList[c3]
                        c3 += 1
                    newconvertedList.append(entry)
                convertedList = newconvertedList
                
                currentPerkList = perkList[counter]
                for node in range(len(currentPerkList)):
                    if convertedList[node] == "F":
                        for perk in currentPerkList[node]:
                            if perk != 0:
                                perk.level = perk.maxlvl
                    elif convertedList[node] == "E":
                        for perk in currentPerkList[node]:
                            if perk != 0:
                                perk.level = 0
                    else:
                        binRep = self.b32ToBinary(convertedList[node])
                        listOfPerks = currentPerkList[node]
                        if listOfPerks[0].maxlvl > 1:
                            while len(binRep) < (len(listOfPerks) + 1):
                                binRep = "0" + binRep
                            val = int(binRep[:2], 2)
                            if val == 3:
                                listOfPerks[0].level = listOfPerks[0].maxlvl
                            elif val == 2:
                                listOfPerks[0].level = 2
                            else:
                                listOfPerks[0].level = 1
                            for p in listOfPerks[1:]:
                                try:
                                    p.level = int(binRep[listOfPerks.index(p)+1])
                                except IndexError:
                                    print(IndexError)
                        else:
                            try:
                                for p in listOfPerks:
                                    while len(binRep) < len(listOfPerks):
                                        binRep = "0" + binRep
                                    p.level = int(binRep[listOfPerks.index(p)])
                            except Exception as e:
                                print(e)
                        currentPerkList[node] = listOfPerks
                    match counter:
                        case 0:
                            BODYPERKS[node] = currentPerkList[node]
                        case 1:
                            REFLEXESPERKS[node] = currentPerkList[node]
                        case 2:
                            TECHPERKS[node] = currentPerkList[node]
                        case 3:
                            INTELLIGENCEPERKS[node] = currentPerkList[node]
                        case 4:
                            COOLPERKS[node] = currentPerkList[node]
            counter += 1
        
        totalPerkPointsSpent = 0
        for perkList in [BODYPERKS, REFLEXESPERKS, TECHPERKS, INTELLIGENCEPERKS, COOLPERKS]:
            for node in perkList:
                for perk in node:
                    totalPerkPointsSpent += perk.level
        PERKPOINTS = 80 - totalPerkPointsSpent
        global_attributes['TOTAL'] = 66 - global_attributes["BODY"] - global_attributes["REFLEXES"] - global_attributes["TECH"] - global_attributes["INTELLIGENCE"] - global_attributes["COOL"] + 15
        self.updateLabels()


        Originalfiles = [["arms",1],["circulatory-system",3],["face",1],["frontal-cortex",3],["hands",2],["integumentary-system",3],["legs",1],["nervous-system",3],["operating-system",1],["skeleton",3]]
        files = Originalfiles.copy()
        cyberwareList = []
        cybCodeList = []
        for char in cybCode:
            cybCodeList.append(char)
        for file in files:
            fileList = []
            while file[1] > 0 and len(cybCodeList) > 0:
                file[1] -= 1
                index = cybCodeList.pop(0)
                if index == "0":
                    fileList.append("E")
                else:
                    indexDec = self.b32ToDec(index)
                    fileList.append(indexDec)
            cyberwareList.append(fileList)
        
        c = 0
        for lst in cyberwareList:
            file = Originalfiles[c]
            cyberwareL = cyberwarefilereader.readfile(f"{file[0]}.txt")
            c2 = 0
            for cyberware in cyberwareL:
                if (cyberware.index + 1) in lst:
                    ACTIVECYBERWARE.append(cyberware)
                    CWBUTTONLIST.append([None, cyberware.filename, c2, cyberware])
                    c2 += 1
            c += 1
        
        weaponFileList = ["ar","blade","blunt","Empty Weapon","LMG","pistol","precision rifle","revolver","shotgun","SMG","sniper rifle","throwable"]
        
        weaponList = []
        wpnCodeList = []
        for char in wpnCode:
            wpnCodeList.append(char)
        wpnCode = wpnCodeList
        for i in range(3):
            wpnFileIndex = (self.b32ToDec(wpnCode.pop(0)) - 1)
            weapons = weaponfilereader.readfile(weaponFileList[wpnFileIndex])
            for weapon in weapons:
                if wpnCode[0] != "0" and (weapon.index + 1) == self.b32ToDec(wpnCode[0]):
                    weaponList.append(weapon)
                    wpnCode.pop(0)
                    break
        
        while len(weaponList) < 3:
            emptywpnList = weaponfilereader.readfile("Empty Weapon")
            weaponList.append(emptywpnList[0])

        WEAPON1 = weaponList[0]
        WEAPON2 = weaponList[1]
        WEAPON3 = weaponList[2]


        self.statScreen()

    def openFile(self):
        dialog = MyDialog()
        okPressed = dialog.exec_()
        okPressed = dialog.exec_()
        if okPressed == QInputDialog.Accepted:
            num = dialog.intValue()
            if num == 0 or len(FILE_LIST) == 0:
                code = "B30/3v/R30/7v/T30/3v/I30/7v/C30/7v/-000000000000000000000-000000"
            else:
                if len(FILE_LIST) > num:
                    chosenFile = open(f"{PATH}\Saves\{FILE_LIST[num-1]}", "r")
                    code = chosenFile.readline().strip()
                    print(code)
                    chosenFile.close()
                else:
                    chosenFile = open(f"{PATH}\Saves\{FILE_LIST[len(FILE_LIST)-1]}", "r")
                    code = chosenFile.readline().strip()
                    print(code)
                    chosenFile.close()
            try:
                self.openBuild(code)
            except:
                self.openFile(self)

class MyDialog(QInputDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Open File")
        self.setWindowIcon(QIcon(imagespath + "titlepic.png"))
        string = "0. New File\n"
        c = 1
        FILE_LIST = os.listdir(f"{PATH}/Saves/") 
        for file in FILE_LIST:
            string += f"{c}. {file[:-4]}\n"
            c += 1
        self.setLabelText(f"{string}\n\nPlease enter the number of the file:")
        self.setInputMode(QInputDialog.IntInput)
        self.setIntRange(0, c-1)

# TRYOUT CODES: Bkm/30/+1t3Rk1i/60/u+1rjTk20/i/+1i+3u+3o2I30/7v/Ci0/7p/+1g+1p-114a319b2023b527a3237-34c924
# Bf0/37/p+1gR3T3I3C3-40003000400000000000-93131c


window = MainWindow()
WINDOW = window
window.show()
sys.exit(app.exec())

# Made by AnybodyC / Crips