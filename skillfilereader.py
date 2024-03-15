from pathlib import Path

path = Path.cwd()

def readfile():
    perkfile = str(path) + "/skill-info.txt"
    file = open(perkfile, "r")
    fullList = []
    skillEntry = None  # Initialize skillEntry to None

    for line in file:
        line = line.strip()

        if "#" in line:
            if skillEntry is not None:
                fullList.append(skillEntry)
            skillEntry = {'name': line[1:], 'levels': [], 'progressedBy': None, 'effects': []}

        elif line[0] in "012345679":
            levels = line.split(";")
            level = f"{levels[0]}. {levels[1]}"
            skillEntry['levels'].append(level)

        elif line[0] == "@":
            skillEntry['progressedBy'] = line[1:]

        elif "?" in line:
            skillEffects = []
            line = file.readline().strip()
            while "END" not in line:
                skillEffects.append(line)
                line = file.readline().strip()
                if not line:
                    break
            skillEntry['effects'] = skillEffects

    if skillEntry is not None:
        fullList.append(skillEntry)

    file.close()
    return fullList
