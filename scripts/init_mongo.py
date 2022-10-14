import os,stat

def pre_init(data_root, image, docker_vars):
    os.makedirs(os.path.join(data_root, 'data'))
    os.makedirs(os.path.join(data_root, 'scrips'))
    initSh = os.path.join(data_root, 'scrips', 'mongo-init.sh')
    with open(initSh, 'w') as file_writer:
      file_writer.write('''
mongosh -- "$MONGO_INITDB_DATABASE" <<EOF
db = db.getSiblingDB('admin')
db.auth('$MONGO_INITDB_ROOT_USERNAME', '$MONGO_INITDB_ROOT_PASSWORD')
db = db.getSiblingDB('$MONGO_INITDB_DATABASE')
db.createUser({
  user: "$MONGO_USERNAME",
  pwd: "$MONGO_PASSWORD",
  roles: [
  { role: 'readWrite', db: '$MONGO_INITDB_DATABASE' }
  ]
})
EOF
      ''')
    os.chmod(initSh, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)


def post_init(data_root, image, docker_vars):
    pass
