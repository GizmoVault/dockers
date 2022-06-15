import os
from helper import execute, execute_or_fatal


def pre_init(data_root, image):
    execute('docker rm -f prometheus_tmp')
    execute_or_fatal('docker run -d --name=prometheus_tmp ' + image)
    execute_or_fatal('docker cp -a prometheus_tmp:/etc/prometheus/ ' + data_root + '/etc')
    with open(os.path.join(data_root, 'etc', 'prometheus.yml'), 'w') as file_writer:
        file_writer.write('''
# A scrape configuration containing exactly one endpoint to scrape:
scrape_configs:
  - job_name: 'node_exporter'
    scrape_interval: 10s
    static_configs:
      - targets: ['prometheus_node_exporter:9100']
  - job_name: 'prometheus_push_gateway'
    scrape_interval: 10s
    honor_labels: true
    static_configs:
      - targets: ['prometheus_push_gateway:9091']
  - job_name: 'prometheus_mysql_exporter'
    scrape_interval: 10s
    honor_labels: true
    static_configs:
      - targets: ['prometheus_mysql_exporter:9104']
      
alerting:
  alertmanagers:
  - scheme: http
    static_configs:
    - targets: 
      - alertmanager:9092

rule_files:
  - "rule_test.yml"
        ''')
    with open(os.path.join(data_root, 'etc', 'rule_test.yml'), 'w') as file_writer:
        file_writer.write('''
groups:
  - name: QPS
    rules:
      - alert: QPSAlertLow
        expr: sum(rate(test_request[1m])) < 100
        for: 10m
        labels:
          severity: warning
        annotations:
          description: "QPS 当前值为: {{ $value }}"
      - alert: QPSAlertHigh
        expr: sum(rate(test_request[1m])) > 1000
        for: 10m
        labels:
          severity: warning
        annotations:
          description: "QPS 当前值为: {{ $value }}"        
        ''')

    os.makedirs(data_root + '/prometheus_data')
    execute_or_fatal('docker rm -f prometheus_tmp')


def post_init(data_root, image):
    pass
