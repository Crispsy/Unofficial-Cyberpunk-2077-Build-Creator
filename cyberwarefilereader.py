from pathlib import Path
path = Path.cwd()

def readfile(filename):
    perkfile = str(path) + "/cyberware files/" + filename
    file = open(perkfile, "r")
    cyberware = []
    index = 0
    if filename == "arms.txt":
        while True:
            line = file.readline()
            if not line:
                break
            if "entry" in line.lower():
                name = file.readline().strip()
                cost = file.readline().strip()
                affectedBy = file.readline().strip()
                for i in range(5):
                    dmgType = file.readline().strip()
                    description = file.readline().strip()
                    if "none" not in dmgType.lower():
                        cyberware.append(armCyberware(name, cost, affectedBy, dmgType, description, filename, index))
                        index += 1
    while True:
        line = file.readline()
        if not line:
            break
        if "entry" in line.lower():
            line = file.readline().strip()
            name = line
            line = file.readline().strip()
            if "sandevistan" in line.lower() or "berserk" in line.lower() or line == "":
                type = line
                cost = file.readline().strip()
                actEff = file.readline().strip()
                description = file.readline().strip()
                attunement = file.readline().strip()
                cyberware.append(sandyberserkCyberware(name, type, cost, actEff, description, attunement, filename, index))
            elif "cyberdeck" in line.lower():
                type = line
                cost = file.readline().strip()
                ram = file.readline().strip()
                QHslots = file.readline().strip()
                buffer = file.readline().strip()
                effects = file.readline().strip()
                description = file.readline().strip()
                cyberware.append(cyberdeckCyberware(name, type, cost, ram, QHslots, buffer, effects, description, filename, index))
            else:
                cost = line
                pasEff = file.readline().strip()
                actEff = file.readline().strip()
                condition = file.readline().strip()
                description = file.readline().strip()
                armor = file.readline().strip()
                attunement = file.readline().strip()
                if attunement == "":
                    attunement = armor
                    armor = ""
                cyberware.append(regularCyberware(name, cost, pasEff, actEff, condition, description, armor, attunement, filename, index))
            index += 1
    file.close()
    return cyberware
                
class regularCyberware():
    def __init__(self, name, cost, pasEff, actEff, condition, description, armor, attunement, filename, index):
        self.name = name
        self.cost = cost
        self.pasEff = pasEff
        self.actEff = actEff
        self.condition = condition
        self.description = description
        if armor == "":
            armor = 0
        self.armor = armor
        imgfile = ""
        if "Iconic" in description:
            match name.lower():
                case "axolotl":
                    imgfile = "newtonmodule"
                case "cox-2 cybersomatic optimizer":
                    imgfile = "bioconductor"
                case "ram reallocator":
                    imgfile = "camillorammanager"
                case "rara avis":
                    imgfile = "parabellum"
                case "adreno-trigger":
                    imgfile = "adrenalineconverter"
                case "deep-field visual interface":
                    imgfile = "visualcortexsupport"
                case "revulsor":
                    imgfile = "reflextuner"
                case "electromag recycler":
                    imgfile = "feedbackcircuit"
                case "isometric stabilizer":
                    imgfile = "clutchpadding"
                case "peripheral inverse":
                    imgfile = "proxishield"
        if imgfile == "":
            imgname = ""
            for char in name.lower():
                if char in "abcdefghijklmnopqrstuvwxyz-'":
                    imgname += char
            imgfile = imgname
        self.imgname = imgfile
        self.attunement = attunement
        self.filename = filename
        self.index = index

        self.attributes = [self.name, self.cost, self.pasEff, self.actEff, self.condition, self.description, self.armor, self.imgname, self.attunement, self.filename, self.index]

    def __iter__(self):
        yield from self.attributes
    
    def __getitem__(self, index):
        return self.attributes[index]
    
    def __str__(self):
        return f"{self.name}&{self.cost}&{self.armor}&{self.description}"
    
    def __repr__(self):
        return f"{self.name}&{self.cost}&{self.armor}&{self.description}"
    

class sandyberserkCyberware():
    def __init__(self, name, type, cost, actEff, description, attunement, filename, index):
        self.name = f"{name} {type}"
        self.cost = cost
        self.pasEff = "None"
        self.actEff = actEff
        self.condition = type.lower()
        self.description = description
        self.armor = 0
        imgname = ""
        for char in name.lower():
            if char in "abcdefghijklmnopqrstuvwxyz-'":
                imgname += char
        self.imgname = imgname
        self.attunement = attunement
        self.filename = filename
        self.index = index
        self.attributes = [self.name, self.cost, self.pasEff, self.actEff, self.condition, self.description, self.armor, self.imgname, self.attunement, self.filename, self.index]

    def __iter__(self):
        yield from self.attributes
    
    def __getitem__(self, index):
        return self.attributes[index]
    
    def __str__(self):
        return f"{self.name}&{self.cost}&{self.armor}&{self.description}"
    
    def __repr__(self):
        return f"{self.name}&{self.cost}&{self.armor}&{self.description}"
    

class cyberdeckCyberware():
    def __init__(self, name, type, cost, ram, QHslots, buffer, effects, description, filename, index):
        self.name = f"{name}   {type}"
        self.cost = cost
        self.ram = ram
        self.QHslots = QHslots
        self.buffer = buffer
        pasEff = ""
        actEff = ""
        self.condition = "cyberdeck"
        if ";" in effects:
            effectList = effects.split(";")
            for effect in effectList:
                s = effect.split(":")
                if "none" in s[1].lower():
                    pasEff += f"{s[0]}:{s[2]};"
                else:
                    actEff += effect
        
        if pasEff != "":
            self.pasEff = pasEff
        else:
            self.pasEff = "None"
        if actEff != "":
            self.actEff = actEff
        else:
            self.actEff = "None"

        self.description = description
        self.armor = 0
        imgname = ""
        for char in name.lower():
            if char in "abcdefghijklmnopqrstuvwxyz-'":
                imgname += char
        self.imgname = imgname
        self.attunement = "none"
        self.filename = filename
        self.index = index

        self.attributes = [self.name, self.cost, self.ram, self.QHslots, self.buffer, self.pasEff, self.actEff, self.description, self.armor, self.imgname, self.attunement, self.filename, self.index]

    def __iter__(self):
        yield from self.attributes
    
    def __getitem__(self, index):
        return self.attributes[index]
    
    def __str__(self):
        return f"{self.name}&{self.cost}&{self.ram}&{self.QHslots}&{self.buffer}&{self.armor}&{self.description}"
    
    def __repr__(self):
        return f"{self.name}&{self.cost}&{self.ram}&{self.QHslots}&{self.buffer}&{self.armor}&{self.description}"
    
class armCyberware():
    def __init__(self, name, cost, affectedBy, dmgType, description, filename, index):
        self.name = f"{dmgType} {name}"
        self.cost = cost
        self.type = affectedBy
        self.description = description
        self.armor = 0
        imgname = ""
        for char in name.lower():
            if char in "abcdefghijklmnopqrstuvwxyz-'":
                imgname += char
        self.imgname = imgname
        self.filename = filename
        self.index = index
        self.attributes = [self.name, self.cost, self.type, self.description, self.armor, self.imgname, self.filename, self.index]

    def __iter__(self):
        yield from self.attributes
    
    def __getitem__(self, index):
        return self.attributes[index]
    
    def __str__(self):
        return f"{self.name}&{self.cost}&{self.armor}&{self.description}"
    
    def __repr__(self):
        return f"{self.name}&{self.cost}&{self.armor}&{self.description}"