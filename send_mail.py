"""
send_mail.py
author: Jack Evitts
"""
import os
import smtplib
from email.message import EmailMessage
import imghdr


def send_mail():
    """Function to send an email with or without attachments.
    =========================================================
    This function is able to send an email from the users
    gmail account to one or many recipients via the smtplib
    module. It may contain several attachments.

    The users email address and password are stored as system
    variables and are called through the os module.

    The message recipients, subject and body are all input via
    the user within the function and are not passed as
    arguments.

    The required modules for this function are as follows:
    os
    smtplib
    email.message.EmailMessage
    imghdr
    =========================================================
    """

    user_address = os.environ.get("EMAIL_USER")
    user_password = os.environ.get("EMAIL_PASS")

    recipients = []
    recipients.append(input("Please enter the email address of the recipient. Press ENTER to send to self.\n"))
    if recipients[0] == "":
        recipients[0] = user_address
    choice = "Y"
    while choice.upper() == "Y":
        choice = input("Would you like to add another recipient? Please input Y or N.\n")
        if choice.upper() == "Y":
            recipients.append(input("Please enter the email address of an additional recipient.\n"))
    
    
    msg = EmailMessage()
    msg["Subject"] = input("Please write the email subject here.\n")
    msg["From"] = user_address
    msg["To"] = recipients
    msg.set_content(input("Please write the body of the email here.\n").replace('\\n', '\n'))

    images = []
    choice = input("Do you want to attach an image? Please input Y or N.\n")
    if choice.upper() == "Y":
        images.append(input("Please enter the full path to the image file.\n"))
        while choice.upper() == "Y":
            choice = input("Would you like to add another image? Please input Y or N.\n")
            if choice.upper() == "Y":
                images.append(input("Please enter the full path to the new image file.\n"))
        for im in images:
            with open(im, "rb") as f:
                im_data = f.read()
                im_type = imghdr.what(f.name)
                im_name = f.name
            msg.add_attachment(im_data, maintype="image", subtype=im_type, filename=im_name)

    files = []
    choice = input("Do you want to attach a file? Please input Y or N.\n")
    if choice.upper() == "Y":
        files.append(input("Please enter the full path to the file.\n"))
        while choice.upper() == "Y":
            choice = input("Would you like to add another file? Please input Y or N.\n")
            if choice.upper() == "Y":
                files.append(input("Please enter the full path to the new file.\n"))
        for file in files:
            with open(file, "rb") as f:
                file_data = f.read()
                file_name = f.name
            msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(user_address, user_password)
            smtp.send_message(msg)
            print("Message sent.")
    except:
        print("Failure. Message not sent.")

send_mail()