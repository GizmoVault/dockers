import fileinput
import prepare

docker_vars = {}

for line in fileinput.input(prepare.abs_base_docker_compose('.env')):
    line = line.strip()
    if len(line) == 0 or line.startswith('#'):
        continue
    parts = line.split('=', 2)
    if len(parts) != 2:
        continue
    docker_vars[parts[0]] = parts[1]

