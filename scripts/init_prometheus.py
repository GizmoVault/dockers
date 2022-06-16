import os
from helper import execute, execute_or_fatal


def pre_init(data_root, image, docker_vars):
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
  - job_name: 'file_ds'
    # metrics_path: '/actuator/prometheus'
    file_sd_configs:
    - files:
      - /prometheus_sd_files/*.yml
      - /prometheus_sd_files/*.yaml
      - /prometheus_sd_files/*.json
      
alerting:
  alertmanagers:
  - scheme: http
    static_configs:
    - targets: 
      - prometheus_alert_manager:9093

rule_files:
  - "rule_test.yml"
        ''')

    os.makedirs(data_root + '/sd/files')
    with open(os.path.join(data_root, 'sd', 'files', 'rule_test.yml'), 'w') as file_writer:
        file_writer.write('''
- labels:
    service: test
  targets:
  - 192.168.249.11:9000
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
      - alert: LicenceCheckDown
        expr: > 
            increase(stw_licence_licence_check_success[2h]) <= 0 and 
            increase(stw_licence_licence_check_success[2h] offset 2h) > 0
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "licence檢測丟失: {{ $value }}"
          description: "{{ $labels.ip }}"
        ''')

    os.makedirs(data_root + '/prometheus_data')
    execute_or_fatal('docker rm -f prometheus_tmp')


def post_init(data_root, image, docker_vars):
    pass
