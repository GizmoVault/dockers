import fileinput
import os


scriptPath = os.path.split(os.path.realpath(__file__))[0]
cfgFile = os.path.join(scriptPath, "..", "local.cfg")

if os.path.isfile(cfgFile):
    for line in fileinput.input(cfgFile):
        if len(line) == 0 or line.startswith('#'):
            continue
        parts = line.split('=', 2)
        if len(parts) != 2:
            continue
        exec(parts[0] + ' = ' + parts[1].capitalize())

