import os
from helper import execute_or_fatal


def pre_init(data_root, image):
    execute_or_fatal('docker run -d --user root --name=grafana_tmp ' + image)
    execute_or_fatal('docker cp -a grafana_tmp:/etc/grafana/ ' + data_root + '/etc')
    execute_or_fatal('docker cp -a grafana_tmp:/var/lib/grafana/ ' + data_root + '/data')
    execute_or_fatal('docker cp -a grafana_tmp:/var/log/grafana/ ' + data_root + '/log')
    execute_or_fatal('docker rm -f grafana_tmp')


def post_init(data_root, image):
    execute_or_fatal('docker exec -it grafana /bin/bash -c "grafana-cli plugins install grafana-piechart-panel"')
    execute_or_fatal('docker exec -it grafana /bin/bash -c "grafana-cli plugins install alexanderzobnin-zabbix-app"')
    execute_or_fatal('docker exec -it grafana /bin/bash -c "grafana-cli plugins install grafana-clock-panel"')
    execute_or_fatal('docker exec -it grafana /bin/bash -c "grafana-cli plugins install snuids-radar-panel"')
    execute_or_fatal('docker exec -it grafana /bin/bash -c "grafana-cli plugins install redis-datasource"')
    execute_or_fatal('docker restart grafana')

