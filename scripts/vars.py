import fileinput
import prepare
import os

root_dir = 'datas'

docker_vars = {
    'REDIS_EXPORT_PORT': 8300,
    'REDIS_STAT_EXPORT_PORT': 8301,
    'MYSQL_EXPORT_PORT': 8302,
    'MYSQL_SERVER_EXPORT_PORT': 8302,
    'GRAFANA_EXPORT_PORT': 8303,
    'PROMETHEUS_EXPORT_PORT': 8304,
    'PROMETHEUS_PUSH_GATEWAY_EXPORT_PORT': 8305,
    'PROMETHEUS_ALERT_MANAGER_EXPORT_PORT': 8306,
    'PROMETHEUS_NODE_EXPORTER_EXPORT_PORT': 8307,
    'PROMETHEUS_MYSQL_EXPORTER_EXPORT_PORT': 8308,
    'NGINX_HTTP_EXPORT_PORT': 80,
    'NGINX_HTTPS_EXPORT_PORT': 443,

    'GRAFANA_IMAGE': 'grafana/grafana',
    'REDIS_IMAGE': 'redis',
    'REDIS_STAT_IMAGE': 'insready/redis-stat',
    'MYSQL_IMAGE': 'mysql',
    'MYSQL_SERVER_IMAGE': 'mysql/mysql-server',
    'PROMETHEUS_IMAGE': 'prom/prometheus',
    'PROMETHEUS_PUSH_GATEWAY_IMAGE': 'prom/pushgateway',
    'PROMETHEUS_ALERT_MANAGER_IMAGE': 'prom/alertmanager',
    'PROMETHEUS_NODE_EXPORTER_IMAGE': 'prom/node-exporter',
    'PROMETHEUS_MYSQL_EXPORTER_IMAGE': 'prom/mysqld-exporter',
    'PROMETHEUS_ALERT_MANAGER_WEBHOOK_FEISHU_IMAGE': 'johnxu1989/alertmanager-webhook-feishu',
    'NGINX_IMAGE': 'nginx',
    'PHP_IMAGE': 'php:7.2-fpm',
}

try:
    for line in fileinput.input(prepare.abs_base_docker_compose('.local.vars')):
        line = line.strip()
        if len(line) == 0 or line.startswith('#'):
            continue
        parts = line.split('=', 2)
        if len(parts) != 2:
            continue
        docker_vars[parts[0]] = parts[1]
except FileNotFoundError:
    pass


def sure_var(var_key, def_value):
    if var_key not in docker_vars.keys():
        if os.getenv(var_key) is not None:
            docker_vars[var_key] = os.getenv(var_key)
            print('NO ' + var_key + ', use the environment value: ' + docker_vars[var_key])
        else:
            docker_vars[var_key] = def_value
            print('NO ' + var_key + ', use the default value: ' + docker_vars[var_key])


sure_var('REDIS_PASSWORD', 'redis_default_pass')
sure_var('INFLUXDB_ADMIN_PASSWORD', 'influx_admin_default_pass')
sure_var('MYSQL_ROOT_PASSWORD', 'mysql_root_default_pass')

if docker_vars.get('FEISHU_WEBHOOK') is None:
    print('WARNING: NO FEISHU_WEBHOOK, you can set it on .local.vars file or environment')
    ctn = input("Continue(Y/n):")
    if ctn == "Y" or ctn == 'y' or ctn == '':
        pass
    else:
        raise Exception("User Cancelled")
