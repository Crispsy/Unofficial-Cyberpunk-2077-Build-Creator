import perkfilereader

class singleLevelPerk():

    def __init__(self, lvlinfo, name, pasEff, actEff, condition, description, affects):
        self.name = name
        self.pasEff = pasEff
        self.actEff = actEff
        self.condition = condition
        self.description = description
        self.affects = affects
        
        self.level = 0
        self.maxlvl = 1

        if len(lvlinfo) > 8:
            words = lvlinfo.split(",")
            if words[1].isnumeric() == True:
                words[1] = int(words[1])
            self.unlocklvl = words[1]
            self.precedingperk = words[2]
        else:
            self.unlocklvl = 0
            self.precedingperk = "None"


        self.attributes = [self.name, self.pasEff, self.actEff, self.condition, self.description, self.affects, self.level, self.unlocklvl, self.precedingperk]


    def __iter__(self):
        yield from self.attributes
    
    def __getitem__(self, index):
        return self.attributes[index]
    
    def __str__(self):
        returnstr = f"{self.name}&{self.affects}&{self.description}"
        if self.precedingperk != "none":
            returnstr = returnstr + f"&Level {self.unlocklvl} - {self.precedingperk}"
        return returnstr
    
    def __repr__(self):
        returnstr = f"{self.name}&{self.affects}&{self.description}"
        if self.precedingperk != "none":
            returnstr = returnstr + f"&Level {self.unlocklvl} - {self.precedingperk}"
        return returnstr

class multiLevelPerk():

    def __init__(self, lvlinfo, name, pasEff1, actEff1, condition1, pasEff2, actEff2, condition2, pasEff3, actEff3, condition3, description, affects, maxlvl):
        self.name = name

        self.pasEff1 = pasEff1
        self.actEff1 = actEff1
        self.condition1 = condition1

        self.pasEff2 = pasEff2
        self.actEff2 = actEff2
        self.condition2 = condition2

        self.pasEff3 = pasEff3
        self.actEff3 = actEff3
        self.condition3 = condition3
        self.description = description

        self.affects = affects

        self.level = 0
        self.maxlvl = maxlvl

        if len(lvlinfo) > 8:
            words = lvlinfo.split(",")
            if words[1].isnumeric() == True:
                words[1] = int(words[1])
            self.unlocklvl = words[1]
            self.precedingperk = words[2]
        else:
            self.unlocklvl = 0
            self.precedingperk = "none"
        
        self.attributes = [self.name, self.pasEff1, self.actEff1, self.condition1, self.pasEff2, self.actEff2, self.condition2, self.pasEff3, self.actEff3, self.condition3, self.description, self.affects, self.level, self.unlocklvl, self.precedingperk]

    def __iter__(self):
        yield from self.attributes
    
    def __getitem__(self, index):
        return self.attributes[index]
    
    def __str__(self):
        returnstr = f"{self.name}&{self.affects}&{self.description}"
        if self.precedingperk != "none":
            returnstr = returnstr + f"&Level {self.unlocklvl} - {self.precedingperk}"
        return returnstr
    
    def __repr__(self):
        returnstr = f"{self.name}&{self.affects}&{self.description}"
        if self.precedingperk != "none":
            returnstr = returnstr + f"&Level {self.unlocklvl} - {self.precedingperk}"
        return returnstr
    

def createSLPerk(name, lvlinfo, pasEff, actEff, condition, description, affects):
    perkEntry = singleLevelPerk(name, lvlinfo, pasEff, actEff, condition, description, affects)
    return perkEntry

def createMLPerk(name, lvlinfo, pasEff1, actEff1, condition1, pasEff2, actEff2, condition2, pasEff3, actEff3, condition3, description, affects, maxlvl):
    perkEntry = multiLevelPerk(name, lvlinfo, pasEff1, actEff1, condition1, pasEff2, actEff2, condition2, pasEff3, actEff3, condition3, description, affects, maxlvl)
    return perkEntry
    

def createPerkList(filename):
    attrPerkList = []
    nodePerkList = []
    parsedperks = perkfilereader.readfile(filename)
    for i in parsedperks:
        if i == "//":
            attrPerkList.append(nodePerkList)
            nodePerkList = []
        else:

            lvl = i[0].split(",")
            if "1" in lvl[0]:
                nodePerkList.append(createSLPerk(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
            elif "2" in lvl[0]:
                nodePerkList.append(createMLPerk(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], 'None', 'None', 'None', i[8], i[9], 2))
            elif "3" in lvl[0]:
                nodePerkList.append(createMLPerk(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], 3))
    attrPerkList.append(nodePerkList)
    return attrPerkList
