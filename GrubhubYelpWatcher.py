#!/usr/bin/env python3
# The above line allows tells the computer which interpreter/language is being 
#   used in this script.

"""
AUTHOR

    Bofan Chen :)
--------------------------------------------------------------------------------
DESCRIPTION

    This script will check a Yelp webpage and notify via email if the listed 
    phone number changes to one provided by a third party, like Grubhub.
        When paired with a <.bat> file in the same directory, a Windows program 
    can be scheduled to run at set times.
"""

#   - "requests" downloads a webpage's HTML code.
#   - "bs4" (Beautiful Soup 4) parses HTML (and XML) documents.
#   - "smtplib" defines an email client session.
#   - "sys" will be used to terminate the script should an error be found.
import requests, bs4, smtplib, sys

# TODO - The URL of the Yelp page you want to monitor.
yelp_page = "https://www.yelp.com/biz/XXXXXXXXXX"
# TODO - Format the phone number as 10 digits with no dashes, parentheses, or spaces.
correct_phone = "XXXXXXXXXX"
# If reading lines from a info_list.txt file....
#   phonenumber
#   email1
#   email2
#   email3
with open("contact-info.txt") as file:
    info_list = file.readlines()
info_list = [info.strip() for info in info_list]
correct_phone = info_list[0]
email_list = info_list[1:]

# Download the page's HTML code.
webpage_html = requests.get(yelp_page)
# Check to see if there were any download issues with
webpage_html.raise_for_status()
# If there was an error, the above line will output an error message and
#   stop the script.

# Parse the metadata for the listed phone number.
# Create a new object that will contain the HTML code.
info = bs4.BeautifulSoup(webpage_html.text, "html.parser")
# Isolate the currently-listed phone number by using HTML tags and knowledge 
#   of Yelp's page formatting.
phone_number = info.find("span", itemprop = "telephone")
# Isolate the phone number string from the overall BS4 tag element.
phone_number = phone_number.string
# Remove all whitespace, parentheses, and dashes from the formatted phone number.
for char in ["\n", " ", "(", ")", "-"]:
    phone_number = phone_number.replace(char, "")
# Check to see if the listed phone number is correct.
if phone_number != correct_phone:
    # If not, send a warning email.
    try:
        # Set up a connection to email by using the correct address and port.
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        # Start the connection.
        connection.ehlo()
        # Encrypt the TLS protocol connection.
        connection.starttls()
        # TODO - Login and send the email.
	# Note that the password is an app-specific key.
        connection.login("XXXXXXXXXX@gmail.com", "XXXXXXXXXX")
	for email in email_list:
            connection.sendmail("XXXXXXXXXX@gmail.com", email, \
              "Subject: Your Yelp Phone Number Has Been Changed.\n" + \
              "You can contact Yelp customer service at (877) 767-9357.")
        connection.quit()
    except SMTPException:
        print("Error encountered.")
