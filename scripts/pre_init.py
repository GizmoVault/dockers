import sys
import os
import time
import shutil
from helper import xlog
import defines
import yaml
import importlib

os.chdir(defines.scriptPath)

REINSTALL_FLAG = True
if len(sys.argv) >= 2:
    if sys.argv[1] == 'false':
        REINSTALL_FLAG = False

docker_compose_dir = os.path.join("..")
abs_docker_compose_dir = os.path.abspath(docker_compose_dir)


def abs_base_docker_compose(s):
    if os.path.isabs(s):
        return s
    return os.path.join(abs_docker_compose_dir, s)


if REINSTALL_FLAG:
    if os.path.exists(abs_base_docker_compose(defines.ROOT_DIR)):
        shutil.rmtree(abs_base_docker_compose(defines.ROOT_DIR))

with open('docker-compose.yml', 'r') as f:
    yaml_info = yaml.safe_load(f)

networks = []
for key in yaml_info['networks']:
    networks.append(key)

yaml_info['services'] = {}

for m in defines.modules:
    with open('config_' + m + '.yaml', 'r') as f:
        yaml_info['services'][m] = yaml.safe_load(f)
    if 'restart' not in yaml_info['services'][m].keys():
        yaml_info['services'][m]['restart'] = 'always'
    if 'container_name' not in yaml_info['services'][m].keys():
        yaml_info['services'][m]['container_name'] = m
    if 'hostname' not in yaml_info['services'][m].keys():
        yaml_info['services'][m]['hostname'] = m
    if 'networks' not in yaml_info['services'][m].keys():
        yaml_info['services'][m]['networks'] = networks

    data_dir = abs_base_docker_compose(eval('defines.' + m.upper() + '_DIR'))
    image = eval('defines.' + m.upper() + '_IMAGE')

    if not os.path.exists(data_dir):
        xlog.info('new dir {}'.format(data_dir))
        os.makedirs(data_dir)
        with open(os.path.join(data_dir, 'new'), 'w') as file_writer:
            file_writer.write(time.asctime(time.localtime(time.time())))
        d = importlib.import_module('init_' + m)
        d.pre_init(data_dir, image)

with open(abs_base_docker_compose('docker-compose.yaml'), 'w', encoding='utf-8') as f:
    yaml.dump(yaml_info, f, allow_unicode=True, default_flow_style=False,sort_keys=False)
