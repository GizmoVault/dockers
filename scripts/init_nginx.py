import os
from helper import execute_or_fatal, execute


def pre_init(data_root, image, docker_vars):
    os.makedirs(os.path.join(data_root, 'conf.d'))
    os.makedirs(os.path.join(data_root, 'ssl'))
    execute('docker rm -f nginx_tmp')
    execute_or_fatal('docker run -d --name=nginx_tmp ' + image)
    execute_or_fatal('docker cp -a nginx_tmp:/etc/nginx/nginx.conf ' + data_root + '/nginx.conf')
    execute_or_fatal('docker cp -a nginx_tmp:/usr/share/nginx/html/ ' + data_root + '/html')
    execute_or_fatal('docker cp -a nginx_tmp:/var/log/nginx/ ' + data_root + '/logs')
    execute_or_fatal('docker rm -f nginx_tmp')


def post_init(data_root, image, docker_vars):
    with open(os.path.join(data_root, 'html', 'info.php'), 'w') as file_writer:
        file_writer.write('<?php phpinfo(); ?>')
    with open(os.path.join(data_root, 'conf.d', 'default.conf'), 'w') as file_writer:
        file_writer.write('''
server {
    listen       80;
    listen  [::]:80;
    server_name  localhost;

    #charset koi8-r;
    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #
    #location ~ \.php$ {
    #    proxy_pass   http://127.0.0.1;
    #}

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    location ~ \.php$ {
        root           html;
        fastcgi_pass   php:9000;
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME  /www/$fastcgi_script_name;
        include        fastcgi_params;
    }

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}
        ''')

