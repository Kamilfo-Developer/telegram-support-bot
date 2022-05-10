from urllib.parse import quote_plus as quote

#You can download the certificate from this url: https://storage.yandexcloud.net/cloud-certs/CA.pem
CERTIFICATE_PATH = "ca-certificates\Yandex\CA.pem"

MONGO_DB_URI_FOR_CLIENT = "mongodb://localhost:27017"
#MONGO_DB_URI_FOR_CLIENT = 'mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}'.format(
#    user=quote('Admin'),
#    pw=quote('Alice-skill!'),
#    hosts=','.join([
#        'rc1b-k9pia9hucf7abn95.mdb.yandexcloud.net:27018'
#    ]),
#    rs='rs01',
#    auth_src='yandex-helper-database')

MONGO_DB_NAME = "yandex-helper-database"
MONGO_DB_QUESTIONS_COLLECTION_NAME = "questions"
MONGO_DB_ADMINS_COLLECTION_NAME = "admins"
MONGO_DB_USERS_COLLECTION_NAME = "users"