MONGODB = {
    'host': '10.134.103.241',
    'port': '27017',
    'user': 'HCC_DB02',
    'pwd': 'foxconn0525',
    'db': '',
    'replicaSet': {
        'name': '',
        "members": [
            {
                "host": "localhost",
                "port": "27017"
            },
            {
                "host": "localhost",
                "port": "27027"
            },
            {
                "host": "localhost",
                "port": "27037"
            }
        ]
    }
}