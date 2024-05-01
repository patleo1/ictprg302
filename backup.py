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
from backupcfg import smtp,log_file_path

# error handling process
def error_handling(error_messages, dateTimeStamp):
    """
    Handle errors by printing error messages, sending emails, and logging.
    
    Parameters:
        error_messages (str): Error message to handle.
        dateTimeStamp (str): Date and time when the error occurred.
    """
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
    """
    Log messages to a file.
    
    Parameters:
        error_messages (str): Message to log.
        dateTimeStamp (str): Date and time when the message was logged.
        iserror (bool): Indicates whether the message is an error message.
    """
    try:
        file = open(log_file_path, "a")
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
   Main function to perform backup operations.
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
                for source in  jobs[jobname]:
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
        print(f"ERROR: System Failure: {err}")
        
        # logging function


# Execute the main function when the script is run
if __name__ == "__main__":
    main()    