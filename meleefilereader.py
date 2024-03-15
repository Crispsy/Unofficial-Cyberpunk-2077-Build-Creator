from pathlib import Path
path = Path.cwd()

def readfile(filename):
    perkfile = str(path) + "\equipmentFiles" + f"\{filename}" + ".txt"
    file = open(perkfile, "r")
    weapons = []

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
            print(weaponType)
            entry = weapon(name, type, iconic, intrinsic, actEff, condition, firerate, damage, staminaCost, armorPen, weaponType)
            weapons.append(entry)
    return weapons
                
class weapon():
    def __init__(self, name, type, iconic, intrinsic, actEff, condition, firerate, damage, staminaCost, armorPen, weaponType):
        self.name = name
        self.type = type
        self.iconic = iconic
        self.intrinsic = intrinsic
        self.actEff = actEff
        self.condition = condition
        self.firerate = float(firerate)
        self.damage = float(damage)
        self.staminaCost = float(staminaCost)
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

        self.attributes = [self.name, self.type, self.iconic, self.intrinsic, self.actEff, self.condition, self.firerate, self.damage, self.staminaCost, self.armorPen, self.imgname]

    def __iter__(self):
        yield from self.attributes
    
    def __getitem__(self, index):
        return self.attributes[index]
    
    def __repr__(self):
        return f"{self.weaponType}&{self.name}&{self.type}"