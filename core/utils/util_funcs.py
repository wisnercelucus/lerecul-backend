import maya
from celery import shared_task
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
import tempfile
from django.utils.translation import (
    gettext as _,
)
# from django_tenants.utils import schema_context

from core.utils.emails import email_account_info
import os


 
def correct_timeline(start, end):
    if end < start:
        return False
    return True


def str_to_date(str_date):
    try:
        return maya.parse(str_date).datetime()
    except Exception as e:
        print(e)

def str_to_time(str_time):
    try:
        return maya.parse(str_time).datetime().time()
    except:
        pass


def generate_randowm_password(length):
    import random
    if not isinstance(length, int):
        raise TypeError("Length should be an integer")

    possible_characters = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789"
    random_character_list = [random.choice(possible_characters) for i in range(length)]
    random_password = "".join(random_character_list)
    return random_password

def generate_randowm_code(length):
    import random
    if not isinstance(length, int):
        raise TypeError("Length should be an integer")

    possible_characters = "ABCDEFGHIJKLMNOPQRSTUVWX123456789"
    random_character_list = [random.choice(possible_characters) for i in range(length)]
    random_password = "".join(random_character_list)
    return random_password

def get_schema_from_host_url(url):
    if not url:
        raise ValueError("You must provide a url")

    if not isinstance(url, str):
        raise TypeError("url must be a string")

    parts = url.split('.')
    instance = parts[0]
    return instance
    

def get_schema_name(request):
    http_host = request.META['HTTP_HOST']
    schema_name = get_schema_from_host_url(str(http_host))
    return schema_name

def get_language_from_request_header(request):
    if not request:
        return 'en'
    language = request.headers.get("Accept-Language", None)
    return language


def getShortFromName(name):
    name_parts = name.split(' ')
    short = ''
    name_parts_fisrt_chars = []
    for part in name_parts:
        fisrt_char = part[0]
        name_parts_fisrt_chars.append(fisrt_char)
    short = ''.join(name_parts_fisrt_chars)
    return short.lower()


def normalize_username(username):
    username = slugify(username)
    username = username.split("-")
    username = "".join(username)

    return "".join(username)


    
def getTenantDomainOnProd(site_domain):
    return site_domain

#@shared_task
#def check_membership_expired():
#    # check if current_date >= expired_date
#    print("Tasks run")

def get_temp_file_path(filename):
    return os.path.join(tempfile.gettempdir(), filename)


def get_email_csv_errors_context(to_email):
    return {"mail_subject": "Import error", "to_email": to_email,
            "message": "Please find enclosed a CSV file with your imports errors."}


def get_month(n):
    if not type(n) == int:
        try:
            n = int(n)
        except:
            return None
    if n == 1:
        return 'January'
    elif n == 2:
        return 'February'
    elif n == 3:
        return 'March'
    elif n == 4:
        return 'April'
    elif n == 5:
        return 'May'
    elif n == 6:
        return 'June'
    elif n == 7:
        return 'July'
    elif n == 8:
        return 'August'
    elif n == 9:
        return 'September'
    elif n == 10:
        return 'October'
    elif n == 11:
        return 'November'
    elif n == 12:
        return 'December'
    else:
        return None

def add(a, b):
    return a + b


from operator import itemgetter
from itertools import groupby 

def group2(arr, by):
    groups = {}
    arr = sorted(arr,
                key = itemgetter(by))
    # Display data grouped by grade
    for key, value in groupby(arr, key = itemgetter(by)):
        if key in groups.keys():
            groups[key]['values'].append(list(value))
        else:
            groups[key]= {"values": list(value), by: key}
            
    return groups


def compute_totals(dict_results, agg_fac, val_key, agg_critegria):
    for key in dict_results.keys():
        result = 0
        values = dict_results[key][val_key]
        for value in values:
            result = result + value[agg_fac]
        dict_results[key]['total_' + agg_fac]= result
    return dict_results