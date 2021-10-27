from requests import Session
import json
from re import search
from faker import Faker
from random import randint

ref_link = 'here'  # your link 'https://invite.duolingo.com/xxxxx' here


def reg_acc():

    s = Session()
    fake = Faker()
    name = fake.first_name()
    email = name + str(randint(1000, 99999)) + '@gmail.com'
    password = str(randint(1000000000, 9999999999))
    data_1 = {"timezone": "Europe",
              "fromLanguage": "ru",
              "learningLanguage": "en",
              "inviteCode": search('(?<=https://invite\.duolingo\.com/).*', ref_link)[0],
              "landingUrl": ref_link,
              "initialReferrer": "$direct",}

    data_2 = {"age": "22", "email": email, "identifier": "", "name": name, "password": password, "username": ''}

    req1 = s.get(ref_link,
                 headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'})
    req2 = s.post('https://www.duolingo.com/2017-06-30/users?fields=id',
                  headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
                           'content-type': 'application/json'}, data=json.dumps(data_1))
    bearer = search('(?<=<Cookie\ jwt_token=).*(?=\ for\ \.duolingo\.com/>,\ <Cookie)', str(req2.cookies))
    user_id = search('(?<=\{"id":).*(?=})', str(req2.content))
    token = 'Bearer ' + bearer[0]

    req3 = s.patch('https://www.duolingo.com/2017-06-30/users/{}?fields=adsConfig,email,identifier,name,privacySettings,trackingProperties,username'.format(user_id[0]),
                   headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
                            'content-type': 'application/json', 'Authorization': token}, data=json.dumps(data_2))

    if 'SESSION_END' in str(req3.content):
        print('Ok')
