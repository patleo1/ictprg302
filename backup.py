"""
Patrick
email: 30025606@students.sunitafe.edu.au
program name: backup
Version:1.0
"""

import sys
import os
from backupcfg import jobs
from backupcfg import destinations
import time
import pathlib
import shutil
from datetime import datetime
import smtplib
from backupcfg import smtp


def error_handling(error_messages, dateTimeStamp):
    print(error_messages)
    sendEmail(error_messages, dateTimeStamp)
    logging(error_messages, dateTimeStamp,True)
    pass
    
def sendEmail(message, dateTimeStamp): 
    """ 
    Send an email message to the specified recipient. 
    Parameters: 
    message (string): message to send. 
    dateTimeStamp (string): Date and time when program was run. 
    """ 
# create email message 
    email = 'To: ' + smtp["recipient"] + '\n' + 'From: ' + smtp["sender"] + '\n' + 'Subject: Backup Error\n\n' + dateTimeStamp +' ' + message + '\n' 
# connect to email server and send email
    try:
        smtp_server = smtplib.SMTP(smtp["server"], smtp["port"])
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(smtp["user"], smtp["password"])
        smtp_server.sendmail(smtp["sender"], smtp["recipient"], email)
        smtp_server.close()
    except Exception as e:
        print("ERROR: Send email failed: " + str(e), file=sys.stderr)

def logging(error_messages, dateTimeStamp,iserror):
    try:
        file = open("/home/ec2-user/environment/ictprg302/backup.log", "a")
        if iserror:
            file.write(f"FAILURE {dateTimeStamp} {error_messages} .\n")
            file.close()
        else:
            file.write(f"SUCCESS {dateTimeStamp} {error_messages} .\n")
            file.close()
    except FileNotFoundError:
        print("ERROR: File does not exist.")
    except IOError:
        print("ERROR: File is not accessible.")
    pass


def main():
    
    """
    Your module description
    """

    try:
        dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        argCount = len(sys.argv)
        if argCount != 2:
            error_handling("ERROR: Argument count is not 2", dateTimeStamp)
        else:
            jobname = sys.argv[1]
            if jobname not in jobs:
                error_handling(f"ERROR: {jobname} is not in job", dateTimeStamp)
            else:
                source = jobs[jobname]
                if not os.path.exists(source):
                    error_handling("ERROR: file " + source + " does not exist.", dateTimeStamp)
                else:
                    des = destinations['desti_path1']
                    if not os.path.exists (des): 
                        error_handling("ERROR: destination " + des + " does not exist.", dateTimeStamp)
                    else:
                        #pathlib.PurePath is a tool for simplifying cross-platform path operations..
                        srcPath = pathlib.PurePath(source)
                        dstLoc = des  + srcPath.name + "-" + dateTimeStamp
                        if pathlib.Path(source).is_dir():
                            shutil.copytree(source, dstLoc)
                        else:
                            shutil.copy2(source, dstLoc)
                            logging(f" backedup{source} to {dstLoc}", dateTimeStamp,False)

    except Exception as err:
        print(f"ERROR: GAME OVER: {err}")



 


if __name__ == "__main__":
    main()    