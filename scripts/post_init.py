import os
import time
from helper import xlog
import modules
import importlib
import env_r_vars

time.sleep(5)

for m in modules.modules:
    data_dir = env_r_vars.docker_vars[m.upper() + '_DIR']
    image = env_r_vars.docker_vars[m.upper() + '_IMAGE']

    if os.path.isfile(os.path.join(data_dir, 'new')):
        xlog.info('new dir {}'.format(data_dir))
        try:
            d = importlib.import_module('init_' + m)
            d.post_init(data_dir, image, env_r_vars.docker_vars)
        except ModuleNotFoundError:
            pass
        os.remove(os.path.join(data_dir, 'new'))
