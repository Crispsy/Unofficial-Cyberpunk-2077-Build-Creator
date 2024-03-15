from pathlib import Path
path = Path.cwd()

def readfile(filename):
    perkfile = str(path) + "/perkFiles/" + filename
    file = open(perkfile, "r")
    allperks = []
    while True:
        perkentry = []
        line = file.readline()
        if not line:
            break
        if "entry" in line.lower():
            perkentry = []
            perklvl = 1
            line = file.readline()

            words = line.split(",")
            for char in words[0]:
                match char:
                    case "1":
                        perklvl = 1
                    case "2":
                        perklvl = 2
                    case "3":
                        perklvl = 3
            if len(line) > 5:
                perkentry.append(line)
            else:
                perkentry.append(perklvl)

            for i in range (1+3*perklvl+2):
                line = file.readline().strip()
                perkentry.append(line)
            allperks.append(perkentry)
        if "//" in line:
            allperks.append("//")
    file.close()
    return allperks

            
        
