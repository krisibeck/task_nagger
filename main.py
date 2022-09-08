import pandas
from datetime import datetime
import smtplib
from random import choice
from os import listdir, environ

FROM_EMAIL = environ.get('FROM_EMAIL')
APP_PASSWORD = environ.get('APP_PASSWORD')

print(FROM_EMAIL)
print(APP_PASSWORD)

NAG_LETTER_DIR = './nagging_templates'

def find_people_to_nag(nag_frame):
    now = datetime.now()
    nagged_people_rows = []
    for index, row in nag_frame.iterrows():
        start_nag_date = datetime(year=row.year, month=row.month, day=row.day)
        delta_days = (now - start_nag_date).days
        if delta_days % row.frequency == 0:
            nagged_people_rows.append(row)
    return nagged_people_rows


def get_random_nag_message(name, chore):
    message_filename = choice(listdir(NAG_LETTER_DIR))
    with open(f'{NAG_LETTER_DIR}/{message_filename}') as f:
        message = f.read().replace('[NAME]', name).replace('[CHORE]', chore)
    return message


def send_nagging_emails(nagged_people):
    for row in nagged_people:
        to_email = row.email
        message_body = get_random_nag_message(row['name'], row['chore'])
        connection = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        print('attempting to send email')
        connection.login(user=FROM_EMAIL, password=APP_PASSWORD)
        connection.sendmail(FROM_EMAIL, to_addrs=to_email, msg=f"subject: Hello\n\n{message_body}")
        connection.close()


nag_frame = pandas.read_csv('nags.csv')
nagged_people = find_people_to_nag(nag_frame)
if nagged_people:
    send_nagging_emails(nagged_people)

