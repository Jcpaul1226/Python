# Importing libraries
import imaplib
import email
import os
import pandas as pd
import time

start= time.time()
#pip install pyyaml
import yaml  #To load saved login credentials from a yaml file

with open("credentials.yml") as f:
    content = f.read()
    
# from credentials.yml import user name and password
my_credentials = yaml.load(content, Loader=yaml.FullLoader)

#Load the user name and passwd from yaml file
user, password = my_credentials["user"], my_credentials["password"]

#URL for IMAP connection
imap_url = 'imap.gmail.com'

# Connection with GMAIL using SSL
my_mail = imaplib.IMAP4_SSL(imap_url)

# Log in using your credentials
my_mail.login(user, password)

# Select the Inbox to fetch messages
my_mail.select('inbox')

#Define Key and Value for email search
#For other keys check out imap_keys.txt document
_, data1 = my_mail.search(None, "BODY","application")  
print("Found ", len(data1[0].split()), " emails containing application")

_, data2 = my_mail.search(None, "BODY","screen")  
print("Found ", len(data2[0].split()), " emails containing screen")

_, data3 = my_mail.search(None, "SUBJECT","interview")  
_, data4 = my_mail.search(None, "BODY","interview")  
print("Found ", len(data3[0].split()) + len(data4[0].split()), " emails containing interview")

datai = data1 + data2 + data3 + data4
datai = datai[0].split()
dataf = list(set(datai) )   #remove duplicate emails
print("Removing duplicate emails and extracting the rest")

mail_id_list = dataf  #IDs of all emails that we want to fetch 
msgs = [] # empty list to capture all messages

#Iterate through messages and extract data into the msgs list
for num in mail_id_list:
    typ, data = my_mail.fetch(num, '(RFC822)') #RFC822 returns whole message (BODY fetches just body)
    msgs.append(data)

print("retrieved ", len(mail_id_list), " emails")

#words to remove from sender
remove = ["com","online", "apply","workday","career","talent","data","jobs","apply","alert","Indeed","Linkedin"
          ,"my","linkedin","indeed","no","reply","talent","recruiting","message","wayup","applicant","talent","aqcuisition",
          "Workday","mail"]

#check if excel sheet already exists
path = 'C:\\Users\\jcpau\\OneDrive\\Desktop\\coding stuff\\Email\\applications1.xlsx'
exists = os.path.isfile(path)

#create the excel sheet
if(exists == True):
       print("excel found, creating new sheet")
       os.remove("applications1.xlsx")
else:
    print("Creating excel sheet")

sender= []
application = []
subject1 = []

for msg in msgs[::-1]: 
    step = 'application'
    body = "none"
    subject = "none"
    for response_part in msg:
        if type(response_part) is tuple:
            my_msg=email.message_from_bytes((response_part[1]))
            #Remove special characters from subject and sender
            subject = ''.join(letter for letter in my_msg["subject"] if letter.isalnum())
            f = ''.join(letter for letter in my_msg['from'] if letter.isalnum())
            for i in remove:
                f = f.replace(i,'')
            #clean up the body portion of email
            for part in my_msg.walk():  
                #print(part.get_content_type())
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload()
                    #categorize what step of application each email is
                    if "interview" in subject or "Interview" in subject:
                        step = "interview"   
                    elif "screen" in body or "screen" in subject:
                        step =  "screen"
    sender.append(f)
    application.append(step)
    subject1.append(subject)
                
print("Applications: ", application.count("application"))
print("screenings: ", application.count("interview") + application.count("screen"))
print("interviews: ", application.count("interview"))
d = {'sender': sender, 'step': application, 'subject': subject1}
df = pd.DataFrame(data = d)
print("--- %s seconds ---" % (time.time() - start))
df.to_excel("applications1.xlsx")

#In a multipart e-mail, email.message.Message.get_payload() returns a 
# list with one item for each part. The easiest way is to walk the message 
# and get the payload on each part:
# https://stackoverflow.com/questions/1463074/how-can-i-get-an-email-messages-text-content-using-python

