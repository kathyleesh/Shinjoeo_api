from urllib import request
from django.shortcuts import redirect
import requests
from shinjoeo.settings import KAKAO_CONFIG
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

@api_view(['GET'])
@permission_classes([AllowAny, ])
def kakaoGetLogin(request):
    CLIENT_ID = KAKAO_CONFIG['KAKAO_REST_API_KEY']
    REDIRET_URL = KAKAO_CONFIG['KAKAO_REDIRECT_URI']
    url = "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}".format(
        CLIENT_ID, REDIRET_URL)
    res = redirect(url)
    return res

@api_view(['GET'])
@permission_classes([AllowAny, ])
def getUserInfo(request):
    CODE = request.query_params['code']
    url = "https://kauth.kakao.com/oauth/token"
    res = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_CONFIG['KAKAO_REST_API_KEY'],
        'redirect_url': KAKAO_CONFIG['KAKAO_REDIRECT_URI'],
        'client_secret': KAKAO_CONFIG['KAKAO_CLIENT_SECRET_KEY'],
        'code': CODE
    }
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    response = requests.post(url, data=res, headers=headers)
    token_json = response.json()

    user_url = "https://kapi.kakao.com/v2/user/me"
    access_token =  token_json['access_token']
    auth = "Bearer " + token_json['access_token']

    HEADER = {
        "Authorization": auth,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    res = requests.get(user_url, headers=HEADER)
    json_data = res.json()
    user_id = json_data["id"]
    nickname = json_data["properties"]["nickname"]

    # print("=========="+str(json_data["id"]))
    if User.objects.filter(username = user_id).exists():
        user = User.objects.get(username = user_id)
    else:
        user = User.objects.create_user(
            username = user_id,
            first_name = nickname,
        )
        user.set_unusable_password()

    my_res = {
        'id' : user.id,
        'user_id' : user_id,
        'user_name' : nickname,
        'access_token': access_token,
    }

    print(response.json())
    login(request,user=user)
    return Response(my_res)

@login_required
def logoutView(request):
    logout(request)
    url = str('https://accounts.kakao.com/logout?continue=http%3A%2F%2Fshinjoeo.s3-website.ap-northeast-2.amazonaws.com%2Fmain%3Fclient_id%3Dfad3300d7c33374e2bb2bab358bcbec3%26logout_redirect_uri%3Dhttp%3A%2F%2Fec2-54-180-8-2.ap-northeast-2.compute.amazonaws.com%3A8000%2Faccounts%2Flogin')
    return redirect(url)
'''
logout은 frontend에서 아래 링크를 바로 연결시킬 예정
https://accounts.kakao.com/logout?continue=https://kauth.kakao.com/oauth/logout/callback?logout_redirect_url=http://ec2-54-180-8-2.ap-northeast-2.compute.amazonaws.com:8000/accounts/login&client_id=fad3300d7c33374e2bb2bab358bcbec3
'''

