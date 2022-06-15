import os

scriptPath = os.path.split(os.path.realpath(__file__))[0]
os.chdir(scriptPath)

docker_compose_dir = os.path.join("..")
abs_docker_compose_dir = os.path.abspath(docker_compose_dir)


def abs_base_docker_compose(s):
    if os.path.isabs(s):
        return s
    return os.path.join(abs_docker_compose_dir, s)
