import smtplib, ssl
import logging
import sys
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="./logs/send_mail.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="w", )
logger = logging.getLogger()

subject = "An email with attachment from Python by snehal"
body = """
 Hi Krupa,  
       Attached files are generated from fakestore api.  
       There are 4 files :- 
       1.CSV - Generated using pandas dataframe df_csv() method  
       2.HTML - Generated using pandas dataframe df_html() method  
       3.XML - Generated using pandas dataframe df_xml() method  
       4.PDF - Generated using pdfkit package from_file() method  
 Thanks & Regards
"""


sender_email = os.environ["Email"]
receiver_email = "snehal@codeops.tech"
password = os.environ['Emailpassword']
# password = "tpurolawxhmnfvdz"

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain "))  # In same directory as script
filename = "Zip_Generated_files.zip"
# Open PDF file in binary mode
try:
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        logger.info("Successfully read %s",filename)
except (FileNotFoundError, OSError) as ex:
    logger.error("%s-%s", ex.__class__.__name__, ex)
    sys.exit(1)


# Encode file in ASCII characters to send by email
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        logger.info("Email Sent Success !")
except smtplib.SMTPAuthenticationError as ex :
    logger.error("%s-%s", ex.__class__.__name__, ex)
    sys.exit(1)
#
