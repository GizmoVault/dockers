import os
import time
from helper import xlog
import defines
import importlib

os.chdir(defines.scriptPath)

time.sleep(5)

docker_compose_dir = os.path.join("..")
abs_docker_compose_dir = os.path.abspath(docker_compose_dir)


def abs_base_docker_compose(s):
    if os.path.isabs(s):
        return s
    return os.path.join(abs_docker_compose_dir, s)


for m in defines.modules:
    data_dir = abs_base_docker_compose(eval('defines.' + m.upper() + '_DIR'))
    image = eval('defines.' + m.upper() + '_IMAGE')

    if os.path.isfile(os.path.join(data_dir, 'new')):
        xlog.info('new dir {}'.format(data_dir))
        d = importlib.import_module('init_' + m)
        d.post_init(data_dir, image)
        os.remove(os.path.join(data_dir, 'new'))
