from django.conf import settings
import hashlib
import re
import requests
import json
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

MAILCHIMP_API_KEY = getattr(settings, "MAILCHIMP_API_KEY", None)
MAILCHIMP_DATA_CENTER = getattr(settings, "MAILCHIMP_DATA_CENTER", None)
MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)


def get_subscriber_hash(member_email):
    #check email
    member_email = member_email.lower().encode()
    m = hashlib.md5(member_email)
    return m.hexdigest()


class Mailchimp(object):
    def __init__(self):
        super(Mailchimp, self).__init__()
        self.key = MAILCHIMP_API_KEY
        self.api_url = 'https://{dc}.api.mailchimp.com/3.0/'.format(dc=MAILCHIMP_DATA_CENTER)
        self.list_id = MAILCHIMP_EMAIL_LIST_ID
        self.list_endpoint = '{api_url}/lists/{list_id}'.format(api_url=self.api_url, list_id=self.list_id)

    def get_members_endpoint(self):
        return self.list_endpoint + "/members"

    def change_subscription_status(self, email, status="unsubscribed"):  #Add or update list member
        # PUT/lists/{list_id}/members/{subscriber_hash}
        hashed_email = get_subscriber_hash(email)
        print(hashed_email)
        endpoint = self.get_members_endpoint() + "/" + hashed_email
        data = {"status": self.check_valid_status(status)}
        r = requests.put(endpoint, auth=("", self.key), data=json.dumps(data))
        return r.status_code, r.json()

    def check_subscription_status(self, email):  #Get member info
        # GET/lists/{list_id}/members/{subscriber_hash}
        hashed_email = get_subscriber_hash(email)
        print(hashed_email)
        endpoint = self.get_members_endpoint() + "/" + hashed_email
        r = requests.get(endpoint, auth=("", self.key))
        return r.status_code, r.json()

    def check_valid_status(self, status):
        choices = ["subscribed", "unsubscribed", "cleaned", "pending", "transactional"]
        if status not in choices:
            raise ValueError("Not a valid choice for email status")
        return status

    def add_email(self, email):  #Add member
        # POST//lists/{list_id}/members
        status = "subscribed"
        self.check_valid_status(status)
        data = {"email_address": email, "status": status}
        endpoint = self.get_members_endpoint()
        r = requests.post(endpoint, auth=("", self.key), data=json.dumps(data))
        return r.status_code, r.json()

    def delete_email(self, email):
        hashed_email = get_subscriber_hash(email)
        print(hashed_email)
        endpoint = self.get_members_endpoint() + "/" + hashed_email
        requests.delete(endpoint, auth=("", self.key))

    def unsubscribe(self, email):
        return self.change_subscription_status(email, status='unsubscribed')

    def subscribe(self, email):
        return self.change_subscription_status(email, status='subscribed')

    def pending(self, email):
        return self.change_subscription_status(email, status='pending')

    def add(self, email):
        try:
            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": MAILCHIMP_API_KEY,
                "server": MAILCHIMP_DATA_CENTER,
            })
            response = client.lists.add_list_member(self.list_id, {"email_address": email, "status": "subscribed"})
            print(response)
        except ApiClientError as error:
            print("Error: {}".format(error.text))
