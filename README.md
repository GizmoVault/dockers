# dockers

1. 安装`python`或`python3`
2. 安装最新版本 `docker`，`docker compose`插件
3. 安装项目依赖的`python`库

    ```bash
    pip install -r requirements.txt
    #or 
    pip3 install -r requirements.txt
    ```

4. 拷贝`.modules.sample`为`.modules`, 修改文件去除不需要的服务
5. 拷贝`.local.vars.sample`为`.local.vars`。如果有必要，则修改。变量参考`scripts/vars.py`
6. 启动`docker`镜像

    ```bash
    make update-all
    ```
