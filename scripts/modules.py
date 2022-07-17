import fileinput
import os

modules = []

scriptPath = os.path.split(os.path.realpath(__file__))[0]
cfgFile = os.path.join(scriptPath, "..", ".modules")

if os.path.isfile(cfgFile):
    for line in fileinput.input(cfgFile):
        if len(line) == 0 or line.startswith('#'):
            continue
        m = line.strip()
        if m.startswith('\'') and m.endswith('\''):
            m = m.strip('\'')
        if m.startswith('"') and m.endswith('"'):
            m = m.strip('"')
        if m == '':
            continue
        modules.append(m)
else:
    modules = ['nginx', 'php', 'redis', 'mysql_server']
