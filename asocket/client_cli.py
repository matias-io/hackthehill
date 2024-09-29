from client_obj import Client

def help():
    print("""
All commands
          
Upload a chunk to a host
    `s-upchunk filename number host`
          
Upload a file to a host
    `s-upfile filename host
          
Download a file from a host
    `s-down filename host    

Get all chunks
    `cls host
    

List all available files in network
    `ls`
        
Distributed upload
Will split the chunks accross hosts
    `upfile filename

Distributed download
# Will find chunks from everywhere
    `down filename

Delete file from network
    `del filename
          
Reconnect to hosts
    `recon`

Update path
    `path path`
          
Add user to network
    `add name ip port

Explore all network to discover users
    `explore`

""")
    
c = Client()
    
while True:
    command = input('> ')
    s = command.split(' ')

    if s[0] == "q":
        exit()
    elif s[0] == "s-upchunk":
        c.upload_chunk_to_host(s[1], s[2], s[3])
    elif s[0] ==  "s-upfile":
        c.upload_file_to_host(s[1], s[2])
    elif s[0] ==  "s-down":
        c.download_file_host(s[1], s[2])
    elif s[0] ==  "cls":
        c.chunk_list(s[1])
    elif s[0] ==  "ls":
        c.ls()
    elif s[0] ==  "upfile":
        c.upload_file_distributed(s[1])
    elif s[0] ==  "down":
        c.download_file(s[1])
    elif s[0] ==  "del":
        c.delete_file(s[1])
    elif s[0] == "recon":
        c.connect_to_hosts()
    elif s[0] == "path":
        c.update_path(s[1])
    elif s[0] == "add":
        c.add_user(s[1], s[2], s[3])
    elif s[0] == "explore":
        c.user_table_update()
    else:
        help()