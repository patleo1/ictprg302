log_file_path = '/home/ec2-user/environment/ictprg302/backup.log'

jobs={'job50':['/home/ec2-user/environment/ictprg302/file1.dat','/home/ec2-user/environment/ictprg302/file50.dat'],
'job20':['/home/ec2-user/environment/ictprg302/fly']
}


destinations={'desti_path1':'/home/ec2-user/environment/ictprg302/backups/'}


smtp={"sender": "30025606p@gmail.com",                          #elasticemail.com verified sender
        "recipient": "30025606@students.sunitafe.edu.au",       # elasticemail.com verified recipient
        "server": "smtp.elasticemail.com",                      # elasticemail.com SMTP server
        "port": 2525,                                           # elasticemail.com SMTP port
        "user": "30025606p@gmail.com",                          # elasticemail.com user
        "password": "A2D2794FA1BBECAF14038F54B5E176D8A57B"}     # elasticemail.com password