### User Directory ###
USERS = [
    {
        'ip': '127.0.0.1',
        'port': 12343,
        'name': 'Antoine'
    },
    {
        'ip': '127.0.0.1',
        'port': 12398,
        'name': 'Lucas'
    }
]

def findUser(name):
    for u in USERS:
        if u['name'].lower() == name.lower():
            return u
    print('Could not find user')