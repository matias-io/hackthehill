# TODO: Modify this for you machine
TABLE_PATH = 'C:/Users/Reima/Documents/Notes/Competitive Programming/hackthehill/asocket/user_table.tx'

LOCAL_IP='127.0.0.1'
LOCAL_PORT='12345'
LOCAL_NAME='antoine'

def findUser(all, name):
    for u in all:
        if u['name'] == name:
            return u

class UserTable:

    users = []

    def read(self):
        with open(TABLE_PATH, 'r') as f:
            for l in f.readlines():
                s = l.split(':')
                name = s[0]
                ip = s[1]
                port = s[2]
                self.users.append({
                    'name': name,
                    'ip': ip,
                    'port': port[:-1]
                })

    def write(self):
        lines = ''

        for user in self.users:
            lines = lines + user['name'] + ':' + user['ip'] + ':' + user['port'] + '\n'

        with open(TABLE_PATH, 'w') as f:
            f.write(lines)
    
    def __init__(self) -> None:
        self.read()

    def addUser(self, name, ip, port):
        self.users.append({
            'name': name,
            'ip': ip,
            'port': port
        })
        self.write()

    def checkUser(self, name):
        for u in self.users:
            if u['name'] == name:
                return True

        return False