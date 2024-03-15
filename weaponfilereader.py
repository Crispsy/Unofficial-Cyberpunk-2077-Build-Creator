from pathlib import Path
path = Path.cwd()

def readfile(filename):
    if filename in "bladeblunt":
        weapons = readmeleefile(filename)
    elif filename in "throwable":
        weapons = readthrowablefile(filename)
    else:
        weapons = readrangedfile(filename)
    return weapons

def readrangedfile(filename1):
    perkfile = str(path) + "\equipmentFiles" + f"\{filename1}" + ".txt"
    file = open(perkfile, "r")
    weapons = []
    index = 0
    while True:
        line = file.readline()
        if not line:
            break
        if "entry" in line.lower():
            name = file.readline().strip()
            type = file.readline().strip()
            iconic = file.readline().strip()
            intrinsic = file.readline().strip()
            actEff = file.readline().strip()
            condition = file.readline().strip()
            firerate = file.readline().strip()
            damage = file.readline().strip()
            reloadSpeed = file.readline().strip()
            range = file.readline().strip()
            handling = file.readline().strip()
            magSize = file.readline().strip()
            headshot = file.readline().strip()
            armorPen = file.readline().strip()
            weaponType = filename1
            entry = rangedWeapon(name, type, iconic, intrinsic, actEff, condition, firerate, damage, reloadSpeed, range, handling, magSize, headshot, armorPen, weaponType, index)
            weapons.append(entry)
            index += 1
    file.close()
    return weapons
                
class rangedWeapon():
    def __init__(self, name, type, iconic, intrinsic, actEff, condition, firerate, damage, reloadSpeed, range, handling, magSize, headshot, armorPen, weaponType, index):
        self.name = name
        self.type = type
        self.iconic = iconic
        self.intrinsic = intrinsic
        self.actEff = actEff
        self.condition = condition
        self.firerate = float(firerate)
        self.damage = float(damage)
        self.reloadSpeed = float(reloadSpeed)
        self.range = float(range)
        self.handling = float(handling)
        self.magSize = int(magSize)
        self.headshot = float(headshot)
        self.index = index
        if armorPen != "":
            self.armorPen = int(armorPen)
        else:
            self.armorPen = 0
        self.weaponType = weaponType

        imgname = ""
        for char in name.lower():
            if char not in ":":
                imgname += char
        
        self.imgname = imgname

        self.attributes = [self.name, self.type, self.iconic, self.intrinsic, self.actEff, self.condition, self.firerate, self.damage, self.reloadSpeed, self.range, self.range, self.handling, self.magSize, self.headshot, self.armorPen, self.imgname, self.index]

    def __iter__(self):
        yield from self.attributes
    
    def __getitem__(self, index):
        return self.attributes[index]
    
    def __repr__(self):
        return f"{self.weaponType}&{self.name}&{self.type}"
    


from pathlib import Path
path = Path.cwd()

def readmeleefile(filename):
    perkfile = str(path) + "\equipmentFiles" + f"\{filename}" + ".txt"
    file = open(perkfile, "r")
    weapons = []
    index = 0
    while True:
        line = file.readline()
        if not line:
            break
        if "entry" in line.lower():
            name = file.readline().strip()
            type = file.readline().strip().title()
            iconic = file.readline().strip()
            intrinsic = file.readline().strip()
            actEff = file.readline().strip()
            condition = file.readline().strip()
            firerate = file.readline().strip()
            damage = file.readline().strip()
            staminaCost = file.readline().strip()
            armorPen = file.readline().strip()
            weaponType = filename
            entry = meleeWeapon(name, type, iconic, intrinsic, actEff, condition, firerate, damage, staminaCost, armorPen, weaponType, index)
            weapons.append(entry)
            index += 1
    file.close()
    return weapons
                
class meleeWeapon():
    def __init__(self, name, type, iconic, intrinsic, actEff, condition, firerate, damage, staminaCost, armorPen, weaponType, index):
        self.name = name
        self.type = type
        self.iconic = iconic
        self.intrinsic = intrinsic
        self.actEff = actEff
        self.condition = condition
        self.firerate = float(firerate)
        self.damage = float(damage)
        self.staminaCost = float(staminaCost)
        self.index = index
        if armorPen != "":
            self.armorPen = int(armorPen)
        else:
            self.armorPen = 0
        self.weaponType = weaponType

        imgname = ""
        for char in name.lower():
            if char not in ":":
                imgname += char
        
        self.imgname = imgname

        self.attributes = [self.name, self.type, self.iconic, self.intrinsic, self.actEff, self.condition, self.firerate, self.damage, self.staminaCost, self.armorPen, self.imgname, self.index]

    def __iter__(self):
        yield from self.attributes
    
    def __getitem__(self, index):
        return self.attributes[index]
    
    def __repr__(self):
        return f"{self.weaponType}&{self.name}&{self.type}"
    

def readthrowablefile(filename):
    perkfile = str(path) + "\equipmentFiles" + f"\{filename}" + ".txt"
    file = open(perkfile, "r")
    weapons = []
    index = 0
    while True:
        line = file.readline()
        if not line:
            break
        if "entry" in line.lower():
            name = file.readline().strip()
            type = file.readline().strip().title()
            iconic = file.readline().strip()
            intrinsic = file.readline().strip()
            actEff = file.readline().strip()
            condition = file.readline().strip()
            firerate = file.readline().strip()
            damage = file.readline().strip()
            range = file.readline().strip()
            staminaCost = file.readline().strip()
            returnTime = file.readline().strip()
            headshot = file.readline().strip()
            armorPen = file.readline().strip()
            weaponType = filename
            entry = throwableWeapon(name, type, iconic, intrinsic, actEff, condition, firerate, damage, range, staminaCost, returnTime, headshot, armorPen, weaponType, index)
            weapons.append(entry)
            index += 1
    file.close()
    return weapons
                
class throwableWeapon():
    def __init__(self, name, type, iconic, intrinsic, actEff, condition, firerate, damage, range, staminaCost, returnTime, headshot, armorPen, weaponType, index):
        self.name = name
        self.type = type
        self.iconic = iconic
        self.intrinsic = intrinsic
        self.actEff = actEff
        self.condition = condition
        self.firerate = float(firerate)
        self.damage = float(damage)
        self.range = float(range)
        self.staminaCost = float(staminaCost)
        self.returnTime = float(returnTime)
        self.index = index
        self.headshot = float(headshot)
        if armorPen != "":
            self.armorPen = int(armorPen)
        else:
            self.armorPen = 0
        self.weaponType = weaponType

        imgname = ""
        for char in name.lower():
            if char not in ":":
                imgname += char
        
        self.imgname = imgname

        self.attributes = [self.name, self.type, self.iconic, self.intrinsic, self.actEff, self.condition, self.firerate, self.damage, self.range, self.staminaCost, self.returnTime, self.headshot, self.armorPen, self.imgname, self.index]

    def __iter__(self):
        yield from self.attributes
    
    def __getitem__(self, index):
        return self.attributes[index]
    
    def __repr__(self):
        return f"{self.weaponType}&{self.name}&{self.type}"