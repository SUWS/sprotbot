
from datetime import datetime, timedelta
import os
from sprotbot.notify import send_email

def determine_meeting_details(date):
    """
    The purpose of this function is to determine what the date
    of the next SUWS event is going to be, and to figure out
    whether it will be a meeting or a workshop.
    """

    cur_day = date.weekday()

    if cur_day == 3:
        # Today is a Thursday...
        days_to_thur = 0
    elif cur_day < 3:
        # Today is Mon - Wed
        days_to_thur = 3 - cur_day
    else:
        # Today is Fri - Sun
        days_to_thur = 7 + 3 - cur_day

    td = timedelta(days=days_to_thur)

    meeting_day = date + td
    week = (meeting_day.day - 1) // 7
    event_type = "meeting" if week % 2 == 0 else "workshop"
    
    return meeting_day.strftime("%Y-%m-%d"), event_type

def load_email_details():
    """
    Pulls the email details out of the environment variables.

    Note: the sender needs to be verified in AWS SES.
    """

    try:
        sender = os.environ["SPROTBOT_SENDER"]
        recipient = os.environ["SPROTBOT_RECIPIENT"]
    except KeyError as ex:
        raise SprotBotEnvironmentError("The sprotbot email environment variables are not set correctly.")

    return sender, recipient

class SprotBotEnvironmentError(Exception):
    pass

def send_meeting_reminder():
    """
    Sends out the meeting reminder to the SUWS mailing list.

    Loads the template from ./templates/meeting.txt
    """

    with open(os.path.join(os.path.dirname(__file__), "templates", "meeting.txt"), "r") as template_file:
        template = template_file.read()

    e_date, e_type = determine_meeting_details(datetime.now())

    sender, recipient = load_email_details()

    subject = "📅 SUWS {}: {} @ Zepler CLS".format(e_type, e_date)

    message = template.replace("{EVENT_TYPE}", e_type)
    message = message.replace("{EVENT_DATE}", e_date)

    send_email(sender, recipient, subject, message)

def run_applet():
    send_meeting_reminder()

