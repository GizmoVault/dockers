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

for line in fileinput.input(os.path.join(scriptPath, "..", ".env")):
    line = line.strip()
    if len(line) == 0 or line.startswith('#'):
        continue
    parts = line.split('=', 2)
    if len(parts) != 2:
        continue
    setter = parts[0] + ' = "' + parts[1] + '"'
    exec(setter)

if os.getenv('REDIS_PASSWORD') is None:
    print("NO REDIS_PASSWORD, use the default")
    os.environ['REDIS_PASSWORD'] = 'redis_default_pass'
if os.getenv('INFLUXDB_ADMIN_PASSWORD') is None:
    print("NO INFLUXDB_ADMIN_PASSWORD, use the default")
    os.environ['INFLUXDB_ADMIN_PASSWORD'] = 'influx_admin_default_pass'
if os.getenv('MYSQL_ROOT_PASSWORD') is None:
    print("NO MYSQL_ROOT_PASSWORD, use the default")
    os.environ['MYSQL_ROOT_PASSWORD'] = 'mysql_root_default_pass'
