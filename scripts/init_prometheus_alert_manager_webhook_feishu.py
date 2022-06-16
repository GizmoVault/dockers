import os


def pre_init(data_root, image, docker_vars):
    with open(os.path.join(data_root, 'config.yml'), 'w') as file_writer:
        file_writer.write('''
bots:
  webhook: # webhook 是 group name
    url: ''' + docker_vars['FEISHU_WEBHOOK'] + '''
    metadata:
      "链接地址": "https://www.baidu.com"
        ''')


def post_init(data_root, image, docker_vars):
    pass
