import os
import time
from tempfile import NamedTemporaryFile
from helper import execute_or_fatal
import modules


def pre_init(data_root, image, docker_vars):
    execute_or_fatal('docker run -d --name=mysql_tmp ' + image)
    execute_or_fatal('docker cp -a mysql_tmp:/var/lib/mysql/ ' + data_root + '/data')
    execute_or_fatal('docker cp -a mysql_tmp:/etc/mysql/conf.d/ ' + data_root + '/config')
    execute_or_fatal('docker rm -f mysql_tmp')


def post_init(data_root, image, docker_vars):
    f = NamedTemporaryFile(mode="w+")
    f.write("ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '"+docker_vars['MYSQL_ROOT_PASSWORD']
            + "';\n")
    f.write('FLUSH PRIVILEGES;')
    f.flush()
    execute_or_fatal('docker cp ' + f.name + ' mysql:/tmp/do.sql')
    time.sleep(5)
    execute_or_fatal('docker exec -it mysql /bin/bash -c "' + 'mysql -uroot -p${MYSQL_ROOT_PASSWORD}</tmp/do.sql' + '"')
    f.close()
