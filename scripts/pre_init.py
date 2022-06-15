import sys
import os
import time
import shutil
from helper import xlog
import modules
import yaml
import importlib

import prepare
import vars

REINSTALL_FLAG = True
if len(sys.argv) >= 2:
    if sys.argv[1] == 'false':
        REINSTALL_FLAG = False

vars.root_dir = prepare.abs_base_docker_compose(vars.root_dir)

if REINSTALL_FLAG:
    if os.path.exists(prepare.abs_base_docker_compose(vars.root_dir)):
        shutil.rmtree(prepare.abs_base_docker_compose(vars.root_dir))

with open('docker-compose.yml', 'r') as f:
    yaml_info = yaml.safe_load(f)

networks = []
for key in yaml_info['networks']:
    networks.append(key)

yaml_info['services'] = {}


def sure_var(var_key, def_value):
    if var_key not in vars.docker_vars.keys():
        if os.getenv(var_key) is not None:
            vars.docker_vars[var_key] = os.getenv(var_key)
            print('NO ' + var_key + ', use the environment value: ' + vars.docker_vars[var_key])
        else:
            vars.docker_vars[var_key] = def_value
            print('NO ' + var_key + ', use the default value: ' + vars.docker_vars[var_key])


sure_var('REDIS_PASSWORD', 'redis_default_pass')
sure_var('INFLUXDB_ADMIN_PASSWORD', 'influx_admin_default_pass')
sure_var('MYSQL_ROOT_PASSWORD', 'mysql_root_default_pass')

for m in modules.modules:
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
    if 'image' not in yaml_info['services'][m].keys():
        yaml_info['services'][m]['image'] = "${" + m.upper() + "_IMAGE}"
    if '-name' in yaml_info['services'][m].keys():
        mID = yaml_info['services'][m]['-name']
        del yaml_info['services'][m]['-name']
        yaml_info['services'][mID] = yaml_info['services'][m]
        del yaml_info['services'][m]

    data_dir_key = m.upper() + '_DIR'
    data_dir = vars.docker_vars.get(data_dir_key)
    if data_dir is None:
        data_dir = os.path.join(vars.root_dir, m.lower())
        vars.docker_vars[data_dir_key] = data_dir

    image_key = m.upper() + '_IMAGE'
    image = vars.docker_vars[image_key]

    if not os.path.exists(data_dir):
        xlog.info('new dir {}'.format(data_dir))
        os.makedirs(data_dir)
        with open(os.path.join(data_dir, 'new'), 'w') as file_writer:
            file_writer.write(time.asctime(time.localtime(time.time())))
        try:
            d = importlib.import_module('init_' + m)
            d.pre_init(data_dir, image, vars.docker_vars)
        except ModuleNotFoundError:
            pass

with open(prepare.abs_base_docker_compose('.env'), 'w', encoding='utf-8') as f:
    for k, v in vars.docker_vars.items():
        f.write(k + '=' + str(v) + '\n')

with open(prepare.abs_base_docker_compose('docker-compose.yaml'), 'w', encoding='utf-8') as f:
    yaml.dump(yaml_info, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
