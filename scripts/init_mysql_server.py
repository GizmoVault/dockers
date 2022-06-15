import os
from posixpath import split
import time
from tempfile import NamedTemporaryFile
from helper import execute_or_fatal, execute
import modules


def pre_init(data_root, image, docker_vars):
    execute_or_fatal('docker rm -f mysql_tmp')
    execute_or_fatal('docker run -d --name=mysql_tmp ' + image)

    os.makedirs(data_root+'/config')
    os.makedirs(data_root+'/data')
    execute_or_fatal('docker cp -a mysql_tmp:/etc/my.cnf ' + data_root + '/config/my.cnf')
    execute_or_fatal('docker cp -a mysql_tmp:/etc/my.cnf.d ' + data_root + '/config/my.cnf.d')
    execute_or_fatal('docker rm -f mysql_tmp')


def post_init(data_root, image, docker_vars):
    rootPass = ''
    for i in range(30):
        time.sleep(1)
        msg = execute('docker logs mysql_server 2>&1 | grep GENERATED')
        print(msg)
        ps = msg.split('PASSWORD:')
        if len(ps) != 2:
            continue
        rootPass = ps[1].strip()
        break
    print("password: [" + rootPass + ']')

    f = NamedTemporaryFile(mode="w+")
    f.write("ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '"+docker_vars['MYSQL_ROOT_PASSWORD']
            + "';\n")
    f.write("CREATE USER 'root'@'%' IDENTIFIED BY '"+docker_vars['MYSQL_ROOT_PASSWORD']+"';\n")
    f.write("GRANT ALL ON *.* TO 'root'@'%';\n")
    f.write('FLUSH PRIVILEGES;')
    f.flush()
    execute_or_fatal('docker cp ' + f.name + ' mysql_server:/tmp/do.sql')
    time.sleep(5)
    execute_or_fatal('docker exec -it mysql_server /bin/bash -c "' + 'mysql -uroot -p\''+rootPass+'\' --connect-expired-password  </tmp/do.sql' + '"')
    f.close()
