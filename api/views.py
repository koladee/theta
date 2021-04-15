from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .serializers import ProfileSerializer, ChatSerializer, ConfigSerializer, TimerSerializer, RewardSerializer
from .models import Profile, Chat, Config, Timer, List, Reward
import random
import string
import time
from datetime import datetime, timezone, timedelta
import requests
import json
import re
# Create your views here.


class HomeView(TemplateView):
    template_name = "index.html"


class AuthEndpoint(APIView):
    @csrf_exempt
    def post(self, request):
        # post request to create a new user
        if request.method == 'POST':
            form = request.data
            if form is not None:
                code = form['code']
                url = "https://api.theta.tv/v1/oauth/token?client_id=gxauus7bts9229e1caa7pc1rcdsiv9fq" \
                      "&client_secret=y0t4a9nqg0sq6dhajm8cjyrqn11g458k&grant_type=authorization_code&code="+str(code)
                payload = {}
                headers = ({"access_token": "z6i44ds842zfq5iivj9e5wyi84vniarp"})
                res = requests.request("POST", url, headers=headers, data=payload)
                data = json.loads(res.text)
                # print(data)

                # url = "https://mrnft.gg/api/xp/"
                # payload = {
                #     "user_id": "usrh4dwae6epttzx2kb"
                # }
                # headers = {}
                # ress = requests.request("POST", url, headers=headers, data=payload)
                # print(ress.text)

                # s = "xaz /xazx /xaxsza /zsxdaszdx zasxz /xaaz xaaaz"
                # pattern = r"/\w*\b"
                # out = re.findall(pattern, s)
                # for x in out:
                #     print(x)

                msg = ""
                if data['status'] == "SUCCESS":
                    try:
                        p = Profile.objects.get(rid=data['body']['user_id'])
                        Profile.objects.filter(rid=data['body']['user_id']).update(
                            access_token=data['body']['access_token'], refresh_token=data['body']['refresh_token'])
                        msg = "User's account exists on mrnft bot."
                        resp = {
                            "msg": msg,
                            "done": True,
                            "data": {"email": p.user.email, "password": p.rid}
                        }
                    except Profile.DoesNotExist:
                        url = "https://mrnft.gg/api/user/"
                        payload = {
                            "user_id": data['body']['user_id']
                        }
                        headers = {}
                        ress = requests.request("POST", url, headers=headers, data=payload)
                        dat = json.loads(ress.text)
                        # print(dat)
                        ndat = ""
                        for r in dat['res']:
                            ndat = ndat+r
                        dataa = json.loads(ndat)
                        if dataa['status'] == "SUCCESS":
                            username = dataa['body']['username']
                            email = username+"@mrnft.gg"
                            rid = data['body']['user_id']
                            password = rid
                            url = "https://mrnft.gg/api/xp/"
                            payload = {
                                "user_id": data['body']['user_id']
                            }
                            headers = {}
                            ress = requests.request("POST", url, headers=headers, data=payload)
                            dat = json.loads(ress.text)
                            # print(dat)
                            if len(dat.data) > 0:
                                lvl = 1
                                if len(dat.data) > 0:
                                    lvl = dat.data[0]['level']
                                try:
                                    u = User.objects.get(username=username)
                                    msg = "User's account with this username exists on this bot."
                                    resp = {
                                        "msg": msg,
                                        "done": True,
                                        "data": {"email": u.email, "password": u.profile.rid}
                                    }
                                except User.DoesNotExist:
                                    user = User.objects.create_user(username=username, email=email, password=password,
                                                                    first_name="", last_name="")
                                    user.save()
                                    theuser = User.objects.get(username=username)
                                    Profile.objects.filter(user=theuser).\
                                        update(rid=rid, level=str(lvl), access_token=data['body']['access_token'],
                                               refresh_token=data['body']['refresh_token'])
                                    msg = "New account singed up on mrnft bot."
                                    resp = {
                                        "msg": msg,
                                        "done": True,
                                        "data": {"email": email, "password": password}
                                    }
                            else:
                                msg = "You are not a follower of this channel, kindly follow this channel " \
                                      "and reattempt login."
                                resp = {
                                    "msg": msg,
                                    "done": False
                                }
                        else:
                            msg = "User's account does not exist."
                            resp = {
                                "msg": msg,
                                "done": False
                            }
                else:
                    msg = "Invalid authorization code."
                    resp = {
                        "msg": msg,
                        "done": False
                    }
                return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)


class RefreshEndpoint(APIView):
    @csrf_exempt
    def post(self, request):
        # post request to create a new user
        if request.method == 'POST':
            form = request.data
            if form is not None:
                token = form['token']
                # token = "z6i44ds842zfq5iivj9e5wyi84vniarp"
                url = "https://api.theta.tv/v1/oauth/token?client_id=gxauus7bts9229e1caa7pc1rcdsiv9fq&client_secret" \
                      "=y0t4a9nqg0sq6dhajm8cjyrqn11g458k&grant_type=refresh_token&refresh_token="+str(token)
                payload = {}
                headers = {}
                res = requests.request("POST", url, headers=headers, data=payload)
                return Response({"token": token, "res": res})
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)


class GetGiftableEndpoint(APIView):
    @csrf_exempt
    def post(self, request):
        # post request to create a new user
        if request.method == 'POST':
            form = request.data
            if form is not None:
                user_id = form['user_id']
                try:
                    p = Profile.objects.get(rid=user_id)
                    url = "https://api.theta.tv/v1/user/usrh4dwae6epttzx2kb" \
                          "/gift_items?client_id=gxauus7bts9229e1caa7pc1rcdsiv9fq" \
                          "&client_secret=y0t4a9nqg0sq6dhajm8cjyrqn11g458k"
                    payload = {}
                    headers = {
                        # "Authorization": "Bearer "+p.access_token
                        "Authorization": "Bearer v3bw8u8q055053hamsz68kxxhpuyhu95"
                    }
                    print(user_id)
                    res = requests.request("GET", url, headers=headers, data=payload)
                    data = json.loads(res.text)
                    # print(data['body']['item_forge'][1])
                    rwds = []
                    put = data['body']['item_forge']
                    for p in put:
                        rw = {
                            "id": p['id'],
                            "metadata": {
                                "name": p['metadata']['name'],
                                "image_urls": {
                                    "large": p['metadata']['image_urls']['large']
                                },
                                "code": p['creator']['username']
                            }
                        }
                        rwds.append(rw)
                    resp = {
                        "msg": "success",
                        "done": True,
                        "data": rwds
                    }
                    return Response(resp)
                except User.DoesNotExist:
                    pass
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)


class NewRewardEndpoint(APIView):
    @csrf_exempt
    def post(self, request):
        # post request to create a new user
        if request.method == 'POST':
            form = request.data
            if form is not None:
                user_id = form['user_id']
                level = form['level']
                reward = form['reward']
                reward_type = form['reward_type']
                try:
                    p = Profile.objects.get(rid=user_id)
                    try:
                        Reward.objects.get(user=p, level=level)
                        msg = "You already have a setting for the specified level, " \
                              "kindly make use of the edit function."
                        resp = {
                            "msg": msg,
                            "done": False
                        }
                    except Reward.DoesNotExist:
                        Reward.objects.create(level=level, reward=reward, reward_type=reward_type, user=p)
                        msg = "New reward setting successfully registered."
                        url = "https://mrnft.gg/api/rewards/"
                        payload = json.dumps({
                            "user_id": user_id
                        })
                        headers = {
                            'Content-Type': 'application/json'
                        }
                        res = requests.request("POST", url, headers=headers, data=payload)
                        ress = json.loads(res.text)
                        if ress['done'] is True:
                            data = ress['data']
                            resp = {
                                "msg": msg,
                                "done": True,
                                "data": data
                            }
                        else:
                            msg = msg + " \nError: " + ress['msg']
                            resp = {
                                "msg": msg,
                                "done": True
                            }
                except Profile.DoesNotExist:
                    msg = "The specified user does not exist."
                    resp = {
                        "msg": msg,
                        "done": False
                    }

                return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)


class EditRewardEndpoint(APIView):
    @csrf_exempt
    def post(self, request):
        # post request to create a new user
        if request.method == 'POST':
            form = request.data
            if form is not None:
                user_id = form['user_id']
                level = form['level']
                reward = form['reward']
                reward_type = form['reward_type']
                try:
                    p = Profile.objects.get(rid=user_id)
                    try:
                        Reward.objects.get(user=p, level=level)
                        Reward.objects.filter(user=p, level=level)\
                            .update(reward=reward, reward_type=reward_type)
                        msg = "Setting successfully edited."
                        url = "https://mrnft.gg/api/rewards/"
                        payload = json.dumps({
                            "user_id": user_id
                        })
                        headers = {
                            'Content-Type': 'application/json'
                        }
                        res = requests.request("POST", url, headers=headers, data=payload)
                        ress = json.loads(res.text)
                        if ress['done'] is True:
                            data = ress['data']
                            resp = {
                                "msg": msg,
                                "done": True,
                                "data": data
                            }
                        else:
                            msg = msg + " \nError: " + ress['msg']
                            resp = {
                                "msg": msg,
                                "done": True
                            }
                    except Reward.DoesNotExist:
                        msg = "You do not have an existing setting for the specified level to be edited.."
                        resp = {
                            "msg": msg,
                            "done": False
                        }

                except Profile.DoesNotExist:
                    msg = "The specified user does not exist."
                    resp = {
                        "msg": msg,
                        "done": False
                    }

                return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)


class DeleteRewardEndpoint(APIView):
    @csrf_exempt
    def post(self, request):
        # post request to create a new user
        if request.method == 'POST':
            form = request.data
            if form is not None:
                user_id = form['user_id']
                level = form['level']
                try:
                    p = Profile.objects.get(rid=user_id)
                    try:
                        Reward.objects.get(user=p, level=level)
                        Reward.objects.filter(user=p, level=level).delete()
                        msg = "Setting successfully deleted."
                        resp = {
                            "msg": msg,
                            "done": True
                        }
                    except Reward.DoesNotExist:
                        msg = "You do not have an existing setting for the specified level to be deleted.."
                        resp = {
                            "msg": msg,
                            "done": False
                        }

                except Profile.DoesNotExist:
                    msg = "The specified user does not exist."
                    resp = {
                        "msg": msg,
                        "done": False
                    }

                return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)


class MyRewardsEndpoint(APIView):
    @csrf_exempt
    def post(self, request):
        # post request to create a new user
        if request.method == 'POST':
            form = request.data
            if form is not None:
                user_id = form['user_id']
                try:
                    p = Profile.objects.get(rid=user_id)
                    rewards = Reward.objects.filter(user=p).order_by('level').all()
                    rwds = []
                    for r in rewards:
                        put = {
                            "level": r.level,
                            "reward_type": r.reward_type,
                            "reward": r.reward,
                            "created_date": r.created_date
                        }
                        rwds.append(put)
                    msg = "success"
                    resp = {
                        "msg": msg,
                        "done": True,
                        "data": rwds
                    }
                except Profile.DoesNotExist:
                    msg = "The specified user does not exist."
                    resp = {
                        "msg": msg,
                        "done": False
                    }
                return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)


class ShowRewardEndpoint(APIView):
    @csrf_exempt
    def post(self, request):
        # post request to create a new user
        if request.method == 'POST':
            form = request.data
            if form is not None:
                user_id = form['user_id']
                try:
                    p = Profile.objects.get(rid=user_id)
                    rewards = Reward.objects.filter(user=p, level=p.level).order_by('level').all()
                    rwds = []
                    for r in rewards:
                        put = {
                            "username": p.user.username,
                            "level": r.level,
                            "reward": r.reward,
                        }
                        rwds.append(put)
                    msg = "success"
                    resp = {
                        "msg": msg,
                        "done": True,
                        "data": rwds
                    }
                except Profile.DoesNotExist:
                    msg = "The specified user does not exist."
                    resp = {
                        "msg": msg,
                        "done": False
                    }
                return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)


class GiftGiftableEndpoint(APIView):
    @csrf_exempt
    def post(self, request):
        # post request to create a new user
        if request.method == 'POST':
            form = request.data
            if form is not None:
                channel_id = form['channel_id']
                user_id = form['user_id']
                prize_id = form['prize_id']
                url = "https://api.theta.tv/v1/channel/" \
                      ""+channel_id+"/channel_action?client_id=gxauus7bts9229e1caa7pc1rcdsiv9fq" \
                                    "&client_secret=y0t4a9nqg0sq6dhajm8cjyrqn11g458k"

                payload = json.dumps({
                    "type": "gift_item",
                    "user_id": user_id,
                    "prize_id": prize_id
                })
                headers = {
                    'Content-Type': 'application/json'
                }

                res = requests.request("POST", url, headers=headers, data=payload)
                return Response({"user_id": user_id, "channel_id": channel_id, "prize_id": prize_id, "res": res})
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)


class SendChatEndpoint(APIView):
    @csrf_exempt
    def post(self, request):
        # post request to create a new user
        if request.method == 'POST':
            form = request.data
            if form is not None:
                channel_id = "usrh4dwae6epttzx2kb"
                message = form['message']
                url = "https://api.theta.tv/v1/channel/" \
                      "" + channel_id + "/channel_action?client_id=gxauus7bts9229e1caa7pc1rcdsiv9fq" \
                                        "&client_secret=y0t4a9nqg0sq6dhajm8cjyrqn11g458k"
                payload = json.dumps({
                    "type": "chat_message",
                    "message": message
                })
                headers = {
                    'Content-Type': 'application/json',
                    "Authorization": "Bearer v3bw8u8q055053hamsz68kxxhpuyhu95"
                }
                res = requests.request("POST", url, headers=headers, data=payload)
                return Response({"channel_id": channel_id, "message": message, "res": res})
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)


class GetUserEndpoint(APIView):
    @csrf_exempt
    def post(self, request):
        # post request to create a new user
        if request.method == 'POST':
            form = request.data
            if form is not None:
                user_id = form['user_id']

                url = "https://api.theta.tv/v1/user/"+user_id
                payload = {}
                headers = {
                    "Client-ID": "gxauus7bts9229e1caa7pc1rcdsiv9fq"
                }
                res = requests.request("GET", url, headers=headers, data=payload)
                print(res)
                return Response({"user_id": user_id, "res": res})
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)


class UserChatEndpoint(APIView):
    @csrf_exempt
    def post(self, request):
        # post request to create a new user
        if request.method == 'POST':
            form = request.data
            if form is not None:
                channel_id = form['channel_id']
                token = form['token']
                user_id = form['user_id']
                message = form['message']
                url = "https://api.theta.tv/v1/channel/"+channel_id+"/channel_action"
                payload = json.dumps({
                    "type": "chat_message",
                    "message": message
                })
                headers = {
                    'x-auth-user': user_id,
                    'x-auth-token': token,
                    'Content-Type': 'application/json'
                }
                res = requests.request("POST", url, headers=headers, data=payload)
                return Response({"user_id": user_id, "channel_id": channel_id,
                                 "token": token, "message": message, "res": res})
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)


class FollowChannelEndpoint(APIView):
    @csrf_exempt
    def post(self, request):
        # post request to create a new user
        if request.method == 'POST':
            form = request.data
            if form is not None:
                channel_id = form['channel_id']
                token = form['token']
                user_id = form['user_id']
                url = "https://api.theta.tv/v1/channel/"+channel_id+"/channel_action"
                payload = json.dumps({
                    "type": "channel_follow",
                })
                headers = {
                    'x-auth-user': user_id,
                    'x-auth-token': token,
                    'Content-Type': 'application/json'
                }
                res = requests.request("POST", url, headers=headers, data=payload)
                return Response({"user_id": user_id, "channel_id": channel_id, "token": token, "res": res})
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)


class UserXPEndpoint(APIView):
    @csrf_exempt
    def post(self, request):
        if request.method == 'POST':
            form = request.data
            if form is not None:
                channel_id = "usrh4dwae6epttzx2kb"
                user_id = form['user_id']
                url = "https://api.theta.tv/v1/channel/" + channel_id + "/channel_xp/list"
                payload = {}
                headers = {}
                res = requests.request("GET", url, headers=headers, data=payload)
                xp = json.loads(res.text)
                followers = len(xp['body'])
                Profile.objects.filter(rid="usrh4dwae6epttzx2kb").update(followers=followers)
                pk = [d for d in xp['body'] if d['user_id'] == user_id]
                for x in xp['body']:
                    try:
                        Profile.objects.get(rid=x['user']['id'])
                    except Profile.DoesNotExist:
                        username = x['user']['username']
                        email = x['user']['username']+"@mrnft.gg"
                        rid = x['user']['id']
                        level = x['level']
                        try:
                            User.objects.get(username=username)
                        except User.DoesNotExist:
                            User.objects.create_user(email=email, username=username, password=rid)
                            usr = User.objects.get(username=username)
                            Profile.objects.filter(user=usr).update(rid=rid, level=level)
                resp = {
                    "msg": "success",
                    "done": True,
                    "data": pk
                }
                return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)


class ProfileEndpoint(APIView):
    # class based view for the profile endpoints and requests
    @csrf_exempt
    def get(self, request):
        if request.method == 'GET':
            # check if the get request has a query parameter(s) to know if request is to fetch for a single user or not
            if_param = request.GET.get('who')
            if if_param is not None:
                # single user request confirmed
                form = request.query_params
                if form['who'] is not None:
                    try:
                        # check if user email exist
                        data = User.objects.get(email=form['who'])
                        try:
                            # authenticate user with submitted password  and return data for single user
                            authenticate(username=data.username, password=form['pass'])
                            login(request, data)
                            resp = {'user': form['who'], 'data': {'username': data.username, 'email': data.email,
                                                                  'fname': data.first_name, 'lname': data.last_name,
                                                                  'mes': 'success'}}
                            return Response(resp)
                        except User.DoesNotExist:
                            resp = {'user': '', 'mes': 'User\'s email or password is incorrect!'}
                            return Response(resp)
                    except User.DoesNotExist:
                        resp = {'user': '', 'mes': 'User\'s email or password is incorrect!'}
                        return Response(resp)
                else:
                    resp = {'user': '', 'mes': 'Invalid request!'}
                    return Response(resp)
            else:
                # return all users as response since there is no query parameter
                profiles = Profile.objects.all()
                serializer = ProfileSerializer(profiles, many=True)
                return Response(serializer.data)
        else:
            resp = {'user': '', 'mes': 'Invalid request!'}
            return Response(resp, 400)

    @csrf_exempt
    def post(self, request):
        # post request to create a new user
        if request.method == 'POST':
            form = request.data
            if form is not None:
                email = form['email']
                username = form['username']
                p1 = form['password']
                p2 = form['password2']
                fname = form['fname']
                lname = form['lname']
                try:
                    # check if email address is a valid email address
                    validate_email(email)
                    try:
                        # check if user with the submitted email address already exist
                        User.objects.get(email=email)
                        resp = {
                            "msg": "Email address already exist!",
                            "done": False
                        }
                        return Response(resp)
                    except User.DoesNotExist:
                        # user with email does not exist, proceed
                        try:
                            # check if a user with the sumitted username exists
                            User.objects.get(username=username)
                            resp = {
                                "msg": "Username already exist!",
                                "done": False
                            }
                            return Response(resp)
                        except User.DoesNotExist:
                            # user with username does not exist, proceed
                            # check if submitted passwords are the same
                            if p1 == p2:
                                # create new user with the submitted credentials
                                user = User.objects.create_user(username=username, email=email, password=p1,
                                                                first_name=fname, last_name=lname)
                                user.save()
                                theuser = User.objects.get(username=username)
                                rand = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(20)])
                                Profile.objects.filter(user=theuser).update(rid=rand, level='1')
                                resp = {
                                    "msg": "New user successfully created!",
                                    "done": True
                                }
                                return Response(resp)
                            else:
                                resp = {
                                    "msg": "Passwords do not match!",
                                    "done": False
                                }
                                return Response(resp)
                except ValidationError:
                    resp = {
                        "msg": "Email address is invalid!",
                        "done": False
                    }
                    return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp, 400)

    @csrf_exempt
    def put(self, request):
        # put request to update user's details
        if request.method == 'PUT':
            form = request.data
            if form is not None:
                idd = form['id']
                email = form['email']
                fname = form['fname']
                lname = form['lname']
                try:
                    # check if user exists
                    User.objects.filter(id=idd, email=email)
                    try:
                        # update user's details
                        User.objects.filter(id=idd).update(first_name=fname, last_name=lname)
                        resp = {
                            "msg": "User's details successfully updated!",
                            "done": True
                        }
                        return Response(resp)
                    except User.DoesNotExist:
                        resp = {
                            "msg": "This category does not exit or belongs to you!",
                            "done": False
                        }
                        return Response(resp)
                except User.DoesNotExist:
                    resp = {
                        "msg": "The specified user dose not exist.",
                        "done": False
                    }
                    return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp)


class ConfigEndpoint(APIView):
    # List class based view for list endpoints
    @csrf_exempt
    def get(self, request):
        # get request to fetch records a single user record or all records
        if request.method == 'GET':
            # check if query parameter is present in the request to identify if request is for a sinle user
            if_param = request.GET.get('who')
            if if_param is not None:
                # single user confirmed
                form = request.query_params
                if form['who'] is not None:
                    config = {'alias': 'ThetaBot'}
                    try:
                        # check if user exist
                        udd = User.objects.get(email=form['who']).profile
                        # fetch all lists for specified user
                        try:
                            c = Config.objects.get(user=udd)
                            config[c.key] = c.content
                            config['username'] = udd.user.username
                            config['level'] = udd.level
                            config['hidden_toggle'] = udd.hidden_toggle
                            config['public_toggle'] = udd.public_toggle
                            config['mod_permission'] = udd.mod_permission
                            config['bot_pause'] = udd.bot_pause
                            config['language'] = udd.language
                        except Config.DoesNotExist:
                            config['username'] = udd.user.username
                            config['level'] = udd.level
                            config['hidden_toggle'] = udd.hidden_toggle
                            config['public_toggle'] = udd.public_toggle
                            config['mod_permission'] = udd.mod_permission
                            config['bot_pause'] = udd.bot_pause
                            config['language'] = udd.language
                        except Config.MultipleObjectsReturned:
                            cs = Config.objects.filter(user=udd).all()
                            for c in cs:
                                config[c.key] = c.content
                            config['username'] = udd.user.username
                            config['level'] = udd.level
                            config['hidden_toggle'] = udd.hidden_toggle
                            config['public_toggle'] = udd.public_toggle
                            config['mod_permission'] = udd.mod_permission
                            config['bot_pause'] = udd.bot_pause
                            config['language'] = udd.language
                        resp = {'done': True, 'mes': '', 'data': config}
                        return Response(resp)
                    except User.DoesNotExist:
                        resp = {'done': False, 'mes': 'User credentials not found!', 'data': {}}
                        return Response(resp)
                else:
                    resp = {'done': False, 'mes': 'Invalid request!', 'data': {}}
                    return Response(resp)
            else:
                # no query parameter, return all lists on the system
                confs = Config.objects.all().order_by('-id')[:100]
                serializer = ConfigSerializer(confs, many=True)
                return Response(serializer.data)
        else:
            resp = {'done': False, 'mes': 'Invalid request!', 'data': {}}
            return Response(resp)


class TimerEndpoint(APIView):
    # List class based view for list endpoints
    @csrf_exempt
    def get(self, request):
        # get request to fetch records a single user record or all records
        if request.method == 'GET':
            # check if query parameter is present in the request to identify if request is for a sinle user
            if_param = request.GET.get('who')
            if if_param is not None:
                # single user confirmed
                form = request.query_params
                if form['who'] is not None:
                    tms = []
                    try:
                        # check if user exist
                        udd = User.objects.get(email=form['who']).profile
                        # fetch all lists for specified user
                        try:
                            t = Timer.objects.get(user=udd, fire_time__lte=int(time.time()), fired=False)
                            vws = t.viewers.split('//')
                            if udd.user.username not in vws:
                                tms.append({'sender': udd.user.username, 'content': t.content})
                                # print(tms)
                                vws.append(udd.user.username)
                                nvws = "//".join(vws)
                                # Timer.objects.filter(id=t.id).update(viewers=nvws)
                        except Timer.DoesNotExist:
                            pass
                        except Timer.MultipleObjectsReturned:
                            # fire_time__gte = (int(time.time()) - 60)
                            ts = Timer.objects.filter(user=udd, fire_time__lte=int(time.time()), fired=False).all()
                            for t in ts:
                                vws = t.viewers.split('//')
                                if udd.user.username not in vws:
                                    tms.append({'sender': udd.user.username, 'content': t.content})
                                    vws.append(udd.user.username)
                                    nvws = "//".join(vws)
                                    # Timer.objects.filter(id=t.id).update(viewers=nvws)
                        exps = Timer.objects.filter(user=udd, fire_time__lte=(int(time.time())), fired=False).all()
                        for exp in exps:
                            fire_time = (int(time.time())+(int(exp.minutes)*60))
                            Timer.objects.filter(id=exp.id).update(fire_time=fire_time)
                            # print('expired')
                        for tm in tms:
                            if "{Bot.Alias}" in tm['content']:
                                try:
                                    strma = Profile.objects.get(rid="usrh4dwae6epttzx2kb")
                                    try:
                                        c = Config.objects.get(user=strma, key="alias")
                                        tm['content'] = tm['content'].replace("{Bot.Alias}", c.content)
                                    except Config.DoesNotExist:
                                        tm['content'] = tm['content'].replace("{Bot.Alias}", "MrNFTBot")
                                except Profile.DoesNotExist:
                                    tm['content'] = tm['content'].replace("{Bot.Alias}", "MrNFTBot")

                            if "{Streamer.Username}" in tm['content']:
                                try:
                                    strma = Profile.objects.get(rid="usrh4dwae6epttzx2kb")
                                    tm['content'] = tm['content'].replace("{Streamer.Username}", strma.user.username)
                                except Profile.DoesNotExist:
                                    pass

                            if "{Streamer.Uptime}" in tm['content']:
                                try:
                                    strma = Profile.objects.get(rid="usrh4dwae6epttzx2kb")
                                    tm['content'] = tm['content'].replace("{Streamer.Uptime}",
                                                                          str(strma.uptime)+" minutes")
                                except Profile.DoesNotExist:
                                    pass

                            if "{Streamer.Followers}" in tm['content']:
                                try:
                                    strma = Profile.objects.get(rid="usrh4dwae6epttzx2kb")
                                    tm['content'] = tm['content'].replace("{Streamer.Followers}",
                                                                          str(strma.followers)+" followers")
                                except Profile.DoesNotExist:
                                    tm['content'] = tm['content'].replace("{Streamer.Followers}", "0 followers")

                            if "{Streamer.Viewers}" in tm['content']:
                                tm['content'] = tm['content'].replace("{Streamer.Viewers}", "0 streamers")

                            if "{Sender.Username}" in tm['content']:
                                tm['content'] = tm['content'].replace("{Sender.Username}", tm['sender'])

                            if "{Target.Username}" in tm['content']:
                                tm['content'] = tm['content'].replace("{Target.Username}", "Username")

                            if "{Amount}" in tm['content']:
                                tm['content'] = tm['content'].replace("{Amount}", "$0.00")

                            if "{Note}" in tm['content']:
                                tm['content'] = tm['content'].replace("{Note}", "A long note goes here")

                            if "{Level}" in tm['content']:
                                try:
                                    strma = Profile.objects.get(rid="usrh4dwae6epttzx2kb")
                                    tm['content'] = tm['content'].replace("{Level}", str(strma.level))
                                except Profile.DoesNotExist:
                                    tm['content'] = tm['content'].replace("{Level}", "1")

                            if "{Text}" in tm['content']:
                                tm['content'] = tm['content'].replace("{Text}", "Some random text goes here...")

                            if "!" in tm['content'] or "/" in tm['content']:
                                di = ""
                                s = tm['content']
                                out1 = []
                                out2 = []
                                if "!" in tm['content']:
                                    di = "!"
                                    pattern = r"!\w*\b"
                                    out1 = re.findall(pattern, s)

                                if "/" in tm['content']:
                                    di = "/"
                                    pattern = r"/\w*\b"
                                    out2 = re.findall(pattern, s)

                                out = out1 + out2
                                for x in out:
                                    k = x[1:].split('.')
                                    kk = ''.join(k)
                                    try:
                                        com = Config.objects.get(key=kk)
                                        tm['content'] = tm['content'].replace(di + kk, com.content)
                                    except Config.DoesNotExist:
                                        try:
                                            li = List.objects.get(key=kk)
                                            if "!" in li.content or "/" in li.content:
                                                di1 = ""
                                                s = li.content
                                                out1 = []
                                                out2 = []
                                                if "!" in li.content:
                                                    di1 = "!"
                                                    pattern = r"!\w*\b"
                                                    out1 = re.findall(pattern, s)

                                                if "/" in li.content:
                                                    di1 = "/"
                                                    pattern = r"/\w*\b"
                                                    out2 = re.findall(pattern, s)

                                                out = out1 + out2
                                                for j in out:
                                                    k1 = j[1:].split('.')
                                                    kk1 = ''.join(k1)
                                                    try:
                                                        com = Config.objects.get(key=kk1)
                                                        li.content = li.content.replace(di1 + kk1, com.content)
                                                        content = li.content.split("{:||:}")
                                                        cont = []
                                                        mx = len(content) - 1
                                                        if li.order == "order":
                                                            con = content[int(li.index)]
                                                            nindex = 1
                                                            if int(li.index) < mx:
                                                                nindex = int(li.index) + 1
                                                            cont.append(con)
                                                            List.objects.filter(key=li.key, user=li.user)\
                                                                .update(index=nindex)
                                                        if li.order == "random":
                                                            ind = random.choice(list(range(1, mx)))
                                                            con = content[ind]
                                                            cont.append(con)
                                                        content = cont
                                                        i = 1
                                                        ncontent = []
                                                        for c in content:
                                                            if c != "<br><br>" and c != "":
                                                                ncontent.append(c)
                                                                i = i + 1
                                                        li.content = "".join(ncontent)
                                                        tm['content'] = tm['content'].replace(di + kk, li.content)
                                                    except Config.DoesNotExist:
                                                        pass
                                        except List.DoesNotExist:
                                            pass
                        # perform level_up  algorithm here
                        users = Profile.objects.filter().all()
                        for user in users:
                            if user.rid[0:3] == "usr":
                                url = "https://mrnft.gg/api/xp/"
                                payload = {
                                    "user_id": user.rid
                                }
                                headers = {}
                                ress = requests.request("POST", url, headers=headers, data=payload)
                                dat = json.loads(ress.text)
                                # print(dat)
                                if len(dat['data']) > 0:
                                    level = dat['data'][0]['level']
                                    uptime = dat['data'][0]['xp']
                                    Profile.objects.filter(rid=user.rid).update(uptime=uptime)
                                    if int(level) > int(user.level):
                                        # print(dat['data'])
                                        # update level
                                        Profile.objects.filter(rid=user.rid).update(level=level)
                                        # send nft (Not available)
                                        # send level up message to Theta tv chat
                                        rwds = [
                                            {
                                                "id": 'tmp0000000000000045',
                                                "metadata": {
                                                    "name": 'Happy Toast',
                                                    "image_urls": {
                                                        "large": 'https://user-beta-slivertv.imgix.net/usrw6zhxdeqt9r'
                                                                 '57wnq/avatar/emotes/4cfdf973-96a4-4bf9-988a-c24e8fa'
                                                                 'd0cff.png'
                                                    },
                                                    "code": ':SubwaySubshappytoast:'
                                                }
                                            },
                                            {
                                                "id": 'tmp0000000000000122',
                                                "metadata": {
                                                    "name": 'classyozlove',
                                                    "image_urls": {
                                                        "large": 'https://user-beta-slivertv.imgix.net/usrw6zhxdeqt9r'
                                                                 '57wnq/avatar/emotes/bd73434f-24a9-4a23-bc08-71b1796'
                                                                 'f01d3.png'
                                                    },
                                                    "code": ':SubwaySubsozlove:'
                                                }
                                            },
                                            {
                                                "id": 'tmp0000000000000046',
                                                "metadata": {
                                                    "name": 'Heart Eyes Toast',
                                                    "image_urls": {
                                                        "large": 'https://user-beta-slivertv.imgix.net/usrw6zhxdeqt9r57'
                                                                 'wnq/avatar/emotes/9fafa613-2db4-4204-97cc-706d5c4d'
                                                                 'f4c5.png'
                                                    },
                                                    "code": ':SubwaySubshearteyes:'
                                                }
                                            },
                                            {
                                                "id": 'tmp0000000000000047',
                                                "metadata": {
                                                    "name": 'Heart',
                                                    "image_urls": {
                                                        "large": 'https://user-beta-slivertv.imgix.net/usrw6zhxdeqt9r'
                                                                 '57wnq/avatar/emotes/cd705520-71ca-4a22-b705-a5d3a65'
                                                                 '65f21.png'
                                                    },
                                                    "code": ':SubwaySubsheart:'
                                                }
                                            }
                                        ]
                                        url = "https://mrnft.gg/api/giftable/get/"
                                        payload = {
                                            "user_id": user.rid
                                        }
                                        headers = {}
                                        ress = requests.request("POST", url, headers=headers, data=payload)
                                        dat = json.loads(ress.text)
                                        if dat['done']:
                                            if len(dat['data']) > 0:
                                                rwds = dat['data']
                                        rwd = rwds[0]
                                        try:
                                            reward = Reward.objects.get(level=level, user=user)
                                            pk = [d for d in rwds if d['id'] == reward.reward]
                                            rwd = pk[0]
                                        except Reward.DoesNotExist:
                                            pass
                                        chatmsg = "Congrats "+\
                                                  user.user.username+", you reached Level " +\
                                                  str(level) + " and earned a " +\
                                                  rwd['metadata']['name'] + " "+rwd['metadata']['code']\
                                                  + " ! Go check it out here: https://mrnft.gg/?ref="\
                                                  + str(user.rid)[3:]
                                        print(chatmsg)
                                        url = "https://mrnft.gg/api/send/chat/"
                                        payload = {
                                            "message": chatmsg
                                        }
                                        headers = {}
                                        ress = requests.request("POST", url, headers=headers, data=payload)
                                        dat = json.loads(ress.text)
                                        print(dat)
                        for tm in tms:
                            url = "https://mrnft.gg/api/send/chat/"
                            payload = {
                                "message": tm['content']
                            }
                            headers = {}
                            ress = requests.request("POST", url, headers=headers, data=payload)
                            dat = json.loads(ress.text)
                            print(dat)
                        resp = {'done': True, 'mes': '', 'data': tms}
                        return Response(resp)
                    except User.DoesNotExist:
                        resp = {'done': False, 'mes': 'User credentials not found!', 'data': {}}
                        return Response(resp)
                else:
                    resp = {'done': False, 'mes': 'Invalid request!', 'data': {}}
                    return Response(resp)
            else:
                # no query parameter, return all lists on the system
                timers = Timer.objects.all().order_by('-id')[:100]
                serializer = TimerSerializer(timers, many=True)
                return Response(serializer.data)
        else:
            resp = {'done': False, 'mes': 'Invalid request!', 'data': {}}
            return Response(resp)


class ChatEndpoint(APIView):
    # List class based view for list endpoints
    @csrf_exempt
    def get(self, request):
        # get request to fetch records a single user record or all records
        if request.method == 'GET':
            # check if query parameter is present in the request to identify if request is for a sinle user
            if_param = request.GET.get('who')
            if if_param is not None:
                # single user confirmed
                form = request.query_params
                if form['who'] is not None:
                    try:
                        # check if user exist
                        udd = User.objects.get(email=form['who']).profile
                        # fetch all lists for specified user
                        try:
                            chats = Chat.objects.filter(sender=udd).all().order_by('-id')
                            # return fetched data
                            serializer = ChatSerializer(chats, many=True)
                            return Response(serializer.data)
                        except Chat.DoesNotExist:
                            resp = {'user': '', 'mes': 'Oops! No record found.'}
                            return Response(resp)
                    except User.DoesNotExist:
                        resp = {'user': '', 'mes': 'User credentials not found!'}
                        return Response(resp)
                else:
                    resp = {'user': '', 'mes': 'Invalid request!'}
                    return Response(resp)
            else:
                # no query parameter, return all lists on the system
                chats = Chat.objects.all().order_by('-id')[:100]
                serializer = ChatSerializer(chats, many=True)
                return Response(serializer.data)
        else:
            resp = {'user': '', 'mes': 'Invalid request!'}
            return Response(resp)

    # This is the function to performs the commands algorithm
    @csrf_exempt
    def process(self, ob):
        # validate data
        command = ob['command']
        sender = ob['sender']
        config = ob['config']
        rand = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(20)])
        coms = ['add', 'remove', 'test', 'alias', 'hellomsg', 'followmsg', 'donationmsg', 'hellomsgsub', 'hellomsgmod',
                'submsg', 'levelupmsg', 'removefollowmsg', 'removedonationmsg', 'removehellomsg', 'removesubmsg',
                'removelevelupmsg', 'commands', 'subonly', 'modonly', 'streameronly', 'minlvl', 'maxlvl',
                'publiccommands', 'hiddencommands', 'history', 'togglemodpermissions', 'pause', 'resetbot', 'addtimer',
                'listtimers', 'removetimer', 'changetimer', 'list', 'suffix', 'prefix']
        langs = ['english', 'french', 'german', 'polish', 'serbian']
        try:
            profile = Profile.objects.get(id=sender)
            chat = Chat.objects.create(command=command, sender=profile, rid=rand, remark="",
                                       created_date=datetime.now(timezone.utc))
            # chat.save()
        #     do command's algorithm here and return the appropriate response
            cmds = command.split()
            showmes = True
            msg = "Oops! Invalid command entered."
            if command[:1] == "!":
                if profile.hidden_toggle is True:
                    showmes = False
                elif profile.hidden_toggle is False:
                    msg = "Hidden commands has been disabled, you can only use public commands."
                    showmes = True
            elif command[:1] == "/":
                if profile.public_toggle is True:
                    showmes = True
                elif profile.public_toggle is False:
                    msg = "The use of public commands has been disabled, you can only use hidden commands."
                    showmes = True
            if msg == "Oops! Invalid command entered.":
                if profile.bot_pause is not True or command == "/pause":
                    if len(cmds) >= 1:
                        if cmds[0][1:] == "alias":
                            if len(cmds) > 1:
                                try:
                                    Config.objects.get(user=profile, key='alias')
                                    Config.objects.filter(user=profile, key='alias').update(content=command[7:],
                                                                                            modified_date=datetime.
                                                                                            now(timezone.utc))
                                except Config.DoesNotExist:
                                    do = Config.objects.create(user=profile, key='alias', content=command[7:],
                                                               modified_date=datetime.now(timezone.utc),
                                                               created_date=datetime.now(timezone.utc))
                                    do.save()
                                msg = config['alias']+" is now called "+command[7:]
                                config['alias'] = command[7:]
                            else:
                                msg = "Invalid alias supplied!"

                        if cmds[0][1:] == "followmsg":
                            if len(cmds) > 1:
                                try:
                                    Config.objects.get(user=profile, key='followmsg')
                                    Config.objects.filter(user=profile, key='followmsg').\
                                        update(content=command[11:], modified_date=datetime.now(timezone.utc))
                                    msg = "Your follow message was successfully updated."
                                except Config.DoesNotExist:
                                    do = Config.objects.create(user=profile, key='followmsg', content=command[11:],
                                                               modified_date=datetime.now(timezone.utc),
                                                               created_date=datetime.now(timezone.utc))
                                    do.save()
                                    msg = "Your follow message was successfully configured."
                                config['followmsg'] = command[11:]
                            else:
                                msg = "Invalid follow message supplied!"

                        if cmds[0][1:] == "hellomsg":
                            if len(cmds) > 1:
                                try:
                                    Config.objects.get(user=profile, key='hellomsg')
                                    Config.objects.filter(user=profile, key='hellomsg').update(content=command[10:],
                                                                                               modified_date=datetime.
                                                                                               now(timezone.utc))
                                    msg = "Your hello message was successfully updated."
                                except Config.DoesNotExist:
                                    do = Config.objects.create(user=profile, key='hellomsg', content=command[10:],
                                                               modified_date=datetime.now(timezone.utc),
                                                               created_date=datetime.now(timezone.utc))
                                    do.save()
                                    msg = "Your hello message was successfully configured."
                                config['hellomsg'] = command[10:]
                            else:
                                msg = "Invalid hello message supplied!"

                        if cmds[0][1:] == "hellomsgsub":
                            if len(cmds) > 1:
                                try:
                                    Config.objects.get(user=profile, key='hellomsgsub')
                                    Config.objects.filter(user=profile, key='hellomsgsub').\
                                        update(content=command[13:], modified_date=datetime.now(timezone.utc))
                                    msg = "Your hello message for sub was successfully updated."
                                except Config.DoesNotExist:
                                    do = Config.objects.create(user=profile, key='hellomsgsub', content=command[13:],
                                                               modified_date=datetime.now(timezone.utc),
                                                               created_date=datetime.now(timezone.utc))
                                    do.save()
                                    msg = "Your hello message for sub was successfully configured."
                                config['hellomsgsub'] = command[13:]
                            else:
                                msg = "Invalid hello message for sub supplied!"

                        if cmds[0][1:] == "hellomsgmod":
                            if len(cmds) > 1:
                                try:
                                    Config.objects.get(user=profile, key='hellomsgmod')
                                    Config.objects.filter(user=profile, key='hellomsgmod').\
                                        update(content=command[13:], modified_date=datetime.now(timezone.utc))
                                    msg = "Your hello message for mod was successfully updated."
                                except Config.DoesNotExist:
                                    do = Config.objects.create(user=profile, key='hellomsgmod', content=command[13:],
                                                               modified_date=datetime.now(timezone.utc),
                                                               created_date=datetime.now(timezone.utc))
                                    do.save()
                                    msg = "Your hello message for mod was successfully configured."
                                config['hellomsgmod'] = command[13:]
                            else:
                                msg = "Invalid hello message for mod supplied!"

                        if cmds[0][1:] == "donationmsg":
                            if len(cmds) > 1:
                                try:
                                    Config.objects.get(user=profile, key='donationmsg')
                                    Config.objects.filter(user=profile, key='donationmsg').\
                                        update(content=command[13:], modified_date=datetime.now(timezone.utc))
                                    msg = "Your donation message was successfully updated."
                                except Config.DoesNotExist:
                                    do = Config.objects.create(user=profile, key='donationmsg', content=command[13:],
                                                               modified_date=datetime.now(timezone.utc),
                                                               created_date=datetime.now(timezone.utc))
                                    do.save()
                                    msg = "Your donation message was successfully configured."
                                config['donationmsg'] = command[13:]
                            else:
                                msg = "Invalid donation message for mod supplied!"

                        if cmds[0][1:] == "submsg":
                            if len(cmds) > 1:
                                try:
                                    Config.objects.get(user=profile, key='submsg')
                                    Config.objects.filter(user=profile, key='submsg').update(content=command[8:],
                                                                                             modified_date=datetime.
                                                                                             now(timezone.utc))
                                    msg = "Your sub message was successfully updated."
                                except Config.DoesNotExist:
                                    do = Config.objects.create(user=profile, key='submsg', content=command[8:],
                                                               modified_date=datetime.now(timezone.utc),
                                                               created_date=datetime.now(timezone.utc))
                                    do.save()
                                    msg = "Your sub message was successfully configured."
                                config['submsg'] = command[8:]
                            else:
                                msg = "Invalid sub message for mod supplied!"

                        if cmds[0][1:] == "levelupmsg":
                            if len(cmds) > 1:
                                try:
                                    Config.objects.get(user=profile, key='levelupmsg')
                                    Config.objects.filter(user=profile, key='levelupmsg').update(content=command[12:],
                                                                                                 modified_date=datetime.
                                                                                                 now(timezone.utc))
                                    msg = "Your level up message was successfully updated."
                                except Config.DoesNotExist:
                                    do = Config.objects.create(user=profile, key='levelupmsg', content=command[12:],
                                                               modified_date=datetime.now(timezone.utc),
                                                               created_date=datetime.now(timezone.utc))
                                    do.save()
                                    msg = "Your level up message was successfully configured."
                                config['levelupmsg'] = command[8:]
                            else:
                                msg = "Invalid level up message for mod supplied!"

                        if command[1:7] == "remove" and command[7:8] != " ":
                            try:
                                Config.objects.get(user=profile, key=command[8:])
                                Config.objects.filter(user=profile, key=command[8:]).delete()
                                msg = "Your "+cmds[0][7:]+" configuration was successfully deleted."
                                config[cmds[0][7:]] = ''
                            except Config.DoesNotExist:
                                msg = "You do not have "+cmds[0][7:]+" setting configured."

                        if cmds[0][1:] == "test":
                            try:
                                conf = Config.objects.get(user=profile, key=command[6:])
                                msg = "Your "+command[6:]+" configuration is:<br><br>"+conf.content
                            except Config.DoesNotExist:
                                msg = "You do not have "+command[6:]+" setting configured."

                        if cmds[0][1:] == "add":
                            if len(cmds) > 1:
                                st = 5 + len(cmds[1]) + 1
                                if command[st:] != "":
                                    if cmds[1] not in coms:
                                        try:
                                            Config.objects.get(user=profile, key=cmds[1])
                                            Config.objects.filter(user=profile, key=cmds[1]).\
                                                update(content=command[st:], modified_date=datetime.now(timezone.utc))
                                            msg = "Command successfully updated."
                                        except Config.DoesNotExist:
                                            do = Config.objects.create(user=profile, key=cmds[1], content=command[st:],
                                                                       modified_date=datetime.now(timezone.utc),
                                                                       created_date=datetime.now(timezone.utc))
                                            do.save()
                                            msg = "Command "+cmds[1]+" was successfully " \
                                                                     "added to your configuration list."
                                        config[cmds[1]] = command[st:]
                                    else:
                                        msg = "The specified command is a reserved command for the system."
                                else:
                                    msg = "Command message is required."
                            else:
                                msg = "Command name must be specified."

                        if command[1:8] == "remove ":
                            try:
                                Config.objects.get(user=profile, key=command[8:])
                                Config.objects.filter(user=profile, key=command[8:]).delete()
                                msg = "Your "+command[8:]+" configuration was successfully deleted."
                            except Config.DoesNotExist:
                                msg = "You do not have "+command[8:]+" setting configured."
                            config[command[8:]] = ''

                        if command[1:9] == "commands":
                            try:
                                Config.objects.get(user=profile)
                                comz = Config.objects.filter(user=profile).all()
                                msg = ""
                                i = 1
                                for con in comz:
                                    if con.key not in coms:
                                        msg = msg + str(i) + ". " + con.key + " { permission : " \
                                              + con.permission + ", minlvl : " + str(con.minlvl) + ", maxlvl : " \
                                              + str(con.maxlvl) + " }<br>"
                                        i = i + 1
                                if msg == "":
                                    msg = "You do not have any personalised command configured."
                            except Config.MultipleObjectsReturned:
                                comz = Config.objects.filter(user=profile).all()
                                msg = ""
                                i = 1
                                for con in comz:
                                    if con.key not in coms:
                                        msg = msg + str(i) + ". " + con.key + " { permission : " \
                                              + con.permission + ", minlvl : " + str(con.minlvl) + ", maxlvl : " \
                                              + str(con.maxlvl) + " }<br>"
                                        i = i + 1
                                if msg == "":
                                    msg = "You do not have any personalised command configured."
                            except Config.DoesNotExist:
                                msg = "You do not have any personalised command configured."

                        if command[1:9] == "subonly ":
                            if command[9:] not in coms:
                                if profile.rid == "usrh4dwae6epttzx2kb":
                                    try:
                                        Config.objects.get(user=profile, key=command[9:])
                                        Config.objects.filter(user=profile, key=command[9:]).update(permission="subonly")
                                        msg = "The permission of "+command[9:]+" was successfully changed to subonly."
                                    except Config.DoesNotExist:
                                        msg = "You do not have "+command[9:]+" setting configured."
                                else:
                                    msg = "You do not have enough permission to use this command!"
                            else:
                                msg = "You're not allowed to perform this operation on this command name."

                        if command[1:9] == "modonly ":
                            if command[9:] not in coms:
                                try:
                                    Config.objects.get(user=profile, key=command[9:])
                                    Config.objects.filter(user=profile, key=command[9:]).update(permission="modonly")
                                    msg = "The permission of "+command[9:]+" was successfully changed to modonly."
                                except Config.DoesNotExist:
                                    msg = "You do not have "+command[9:]+" setting configured."
                            else:
                                msg = "You're not allowed to perform this operation on this command name."

                        if command[1:14] == "streameronly ":
                            if command[14:] not in coms:
                                try:
                                    Config.objects.get(user=profile, key=command[14:])
                                    Config.objects.filter(user=profile, key=command[14:]).\
                                        update(permission="streameronly")
                                    msg = "The permission of "+command[14:]+" was successfully changed to streameronly."
                                except Config.DoesNotExist:
                                    msg = "You do not have "+command[14:]+" setting configured."
                            else:
                                msg = "You're not allowed to perform this operation on this command name."

                        if command[1:8] == "minlvl ":
                            if cmds[1] not in coms:
                                if 0 <= int(cmds[2]) <= 100:
                                    try:
                                        con = Config.objects.get(user=profile, key=cmds[1])
                                        if con.maxlvl > int(cmds[2]):
                                            Config.objects.filter(user=profile, key=cmds[1]).update(minlvl=cmds[2])
                                            msg = "The minimum level of "+cmds[1]+" was " \
                                                                                  "successfully changed to "+cmds[2]+"."
                                        else:
                                            msg = "The newly specified minimum level can not be greater than the" \
                                                  " existing maximum level configured for this command."
                                    except Config.DoesNotExist:
                                        msg = "You do not have "+cmds[1]+" setting configured."
                                else:
                                    msg = "Level supplied is invalid, minimum level must be between 0 and 100."
                            else:
                                msg = "You're not allowed to perform this operation on this command name."

                        if command[1:8] == "maxlvl ":
                            if cmds[1] not in coms:
                                if 0 <= int(cmds[2]) <= 100:
                                    try:
                                        con = Config.objects.get(user=profile, key=cmds[1])
                                        if con.minlvl < int(cmds[2]):
                                            Config.objects.filter(user=profile, key=cmds[1]).update(maxlvl=cmds[2])
                                            msg = "The maximum level of "+cmds[1]+" was " \
                                                                                  "successfully changed to "+cmds[2]+"."
                                        else:
                                            msg = "The newly specified maximum level can not be lesser than " \
                                                  "the existing minimum level configured for this command."

                                    except Config.DoesNotExist:
                                        msg = "You do not have "+cmds[1]+" setting configured."
                                else:
                                    msg = "Level supplied is invalid, maximum level must be between 0 and 100."
                            else:
                                msg = "You're not allowed to perform this operation on this command name."

                        if command[1:] == "hiddencommands":
                            if not profile.hidden_toggle:
                                Profile.objects.filter(id=sender).update(hidden_toggle=True)
                                msg = "Firing hidden commands now enabled."
                                config['hiddencommands'] = True
                            else:
                                Profile.objects.filter(id=sender).update(hidden_toggle=False)
                                msg = "Firing hidden commands now disabled."
                                config['hiddencommands'] = False

                        if command[1:] == "publiccommands":
                            if not profile.public_toggle:
                                Profile.objects.filter(id=sender).update(public_toggle=True)
                                msg = "Firing public commands now enabled."
                                config['publiccommands'] = True
                            else:
                                Profile.objects.filter(id=sender).update(public_toggle=False)
                                Profile.objects.filter(id=sender).update(hidden_toggle=True)
                                msg = "Firing public commands has been disabled and " \
                                      "firing of hidden commands has now been enabled."
                                config['publiccommands'] = False
                                config['hiddencommands'] = True

                        if command[1:] == "history":
                            chts = Chat.objects.all().order_by('-id')[:5]
                            msg = ""
                            for cht in chts:
                                msg = msg+"[@"+cht.sender.user.username+"] >>> "+cht.command+"<br><br>"

                        if command[1:] == "togglemodpermissions":
                            if not profile.mod_permission:
                                Profile.objects.filter(id=sender).update(mod_permission=True)
                                msg = "Other users now have access to add/edit/remove any of your commands"
                            else:
                                Profile.objects.filter(id=sender).update(mod_permission=False)
                                msg = "Other users no longer have access to add/edit/remove any of your commands"

                        if command[1:] == "pause":
                            if not profile.bot_pause:
                                Profile.objects.filter(id=sender).update(bot_pause=True)
                                msg = "Bot paused, no chat/timers/events will appear until un-paused"
                            else:
                                Profile.objects.filter(id=sender).update(bot_pause=False)
                                msg = "Bot un-paused, chat/timers/events will begin to appear."

                        if cmds[0][1:] == "resetbot":
                            if cmds[1] != "" and cmds[1] is not None:
                                try:
                                    us = User.objects.get(username=cmds[1].lower())
                                    try:
                                        Config.objects.get(user=us.profile)
                                        Config.objects.filter(user=profile).delete()
                                        Profile.objects.filter(user=us).update(hidden_toggle=True, public_toggle=True,
                                                                               mod_permission=False, bot_pause=False,
                                                                               language="english")
                                        msg = "Your bot configurations was successfully reset to default."
                                    except Config.DoesNotExist:
                                        Profile.objects.filter(user=us).update(hidden_toggle=True, public_toggle=True,
                                                                               mod_permission=False, bot_pause=False,
                                                                               language="english")
                                        msg = "Your bot configurations was successfully reset to default."
                                    except Config.MultipleObjectsReturned:
                                        Config.objects.filter(user=profile).delete()
                                        Profile.objects.filter(user=us).update(hidden_toggle=True, public_toggle=True,
                                                                               mod_permission=False, bot_pause=False,
                                                                               language="english")
                                        msg = "Your bot configurations was successfully reset to default."
                                except User.DoesNotExist:
                                    msg = "Specified username does not exist."
                            else:
                                msg = "Username is required with the resetbot command."

                        if cmds[0][1:] == "setlanguage":
                            if cmds[1].lower() in langs:
                                Profile.objects.filter(id=sender).update(language=cmds[1].lower())
                                msg = "Language setting changed from \""+profile.language+\
                                      "\" to \""+cmds[1].lower()+"\"."
                            else:
                                msg = "The specified language is not supported."

                        if cmds[0][1:] == "addtimer":
                            if int(cmds[1]) > 0 and cmds[2] is not None:
                                if cmds[2] != "" and cmds[2] is not None:
                                    if cmds[3] != "" and cmds[3] is not None:
                                        # time=(datetime.now(timezone.utc) + timedelta(minutes=2))
                                        # con.time >= datetime.now(timezone.utc)
                                        pre = cmds[0]+" "+str(cmds[1])+" "+cmds[2]+" "
                                        txt = command[len(pre):]
                                        try:
                                            t = Timer.objects.get(user=profile, key=cmds[2])
                                            if t.fired is False:
                                                msg = "You have an active timer with this same specified timer name."
                                            else:
                                                Timer.objects.create(key=cmds[2], user=profile, content=txt,
                                                                     minutes=cmds[1],
                                                                     fire_time=(int(time.time())+(int(cmds[1])*60)))
                                                msg = "New timer message successfully scheduled."
                                        except Timer.DoesNotExist:
                                            Timer.objects.create(key=cmds[2], user=profile, content=txt,
                                                                 minutes=cmds[1],
                                                                 fire_time=(int(time.time())+(int(cmds[1])*60)))
                                            msg = "New timer message successfully scheduled."
                                    else:
                                        msg = "Message to be timed is required."
                                else:
                                    msg = "Timer name must be specified."
                            else:
                                msg = "Invalid time specified in this command."

                        if cmds[0][1:] == "enabletimer":
                            if cmds[1] != "" and cmds[1] is not None:
                                try:
                                    t = Timer.objects.get(user=profile, key=cmds[1])
                                    if t.fired is False:
                                        Timer.objects.filter(id=t.id).update(status=True)
                                        msg = "Timer successfully enabled."
                                    else:
                                        msg = "This timed message has been fired, this operation cannot be executed."
                                except Timer.DoesNotExist:
                                    msg = "The timer with this timer name does not exist on your timer list."

                        if cmds[0][1:] == "disabletimer":
                            if cmds[1] != "" and cmds[1] is not None:
                                try:
                                    t = Timer.objects.get(user=profile, key=cmds[1])
                                    if t.fired is False:
                                        Timer.objects.filter(id=t.id).update(status=False)
                                        msg = "Timer successfully disabled."
                                    else:
                                        msg = "This timed message has been fired, this operation cannot be executed."
                                except Timer.DoesNotExist:
                                    msg = "The timer with this timer name does not exist on your timer list."

                        if command[1:] == "listtimers":
                            msg = ""
                            try:
                                t = Timer.objects.get(user=profile)
                                if t.status is True:
                                    status = "enabled"
                                else:
                                    status = "disabled"

                                if t.fired is True:
                                    fired = "Yes"
                                else:
                                    fired = "No"
                                msg = msg + ">>> " + t.key + " [minutes :" + t.minutes + ", status : " + status\
                                      + ", fired :" + fired + "]<br><br>"
                            except Timer.DoesNotExist:
                                msg = "You do not have any timed message on your list."
                            except Timer.MultipleObjectsReturned:
                                ts = Timer.objects.filter(user=profile).order_by('-id').all()
                                for t in ts:
                                    if t.status is True:
                                        status = "enabled"
                                    else:
                                        status = "disabled"

                                    if t.fired is True:
                                        fired = "Yes"
                                    else:
                                        fired = "No"
                                    msg = msg + ">>> " + t.key + " [ minutes :" + t.minutes + ", status : " + status \
                                          + ", fired :" + fired + " ]<br><br>"

                        if cmds[0][1:] == "changetime":
                            if cmds[1] != "" and cmds[1] is not None:
                                if int(cmds[2]) > 0 and cmds[2] is not None:
                                    try:
                                        t = Timer.objects.get(user=profile, key=cmds[1])
                                        vws = t.viewers.split("//")
                                        if profile.user.username in vws:
                                            vws.remove(profile.user.username)
                                        if "" in vws:
                                            vws.remove("")
                                        nvws = "//".join(vws)
                                        Timer.objects.filter(user=profile, key=cmds[1]).\
                                            update(minutes=cmds[2],
                                                   fire_time=(int(time.time())+(int(cmds[2])*60)),
                                                   viewers=nvws, fired=False)
                                        msg = "Timer message time successfully updated and " \
                                              "ready to be fired in "+cmds[2]+" minutes time."
                                    except Timer.DoesNotExist:
                                        msg = "The specified timer name does not exist or belongs to you."
                                else:
                                    msg = "Timer's new time in minutes must be specified."
                            else:
                                msg = "Timer name is missing in this command."

                        if cmds[0][1:] == "removetimer":
                            if cmds[1] != "" and cmds[1] is not None:
                                try:
                                    Timer.objects.get(user=profile, key=cmds[1])
                                    Timer.objects.filter(user=profile, key=cmds[1]).delete()
                                    msg = "Timer message successfully deleted."
                                except Timer.DoesNotExist:
                                    msg = "There is no timer message with this name on your list."
                            else:
                                msg = "Timer name must be specified."

                        if cmds[0][1:] == "list":
                            if cmds[1] == "create":
                                if cmds[2] != "" and cmds[2] is not None:
                                    try:
                                        List.objects.get(user=profile, key=cmds[2])
                                        msg = "You already have an existing list with the specified list name."
                                    except List.DoesNotExist:
                                        List.objects.create(key=cmds[2], user=profile)
                                        msg = "List successfully created."
                                else:
                                    msg = "List name must be specified."

                            if cmds[1] == "add" or cmds[1] == "suffix":
                                if cmds[2] != "" and cmds[2] is not None:
                                    try:
                                        lst = List.objects.get(user=profile, key=cmds[2])
                                        if cmds[3] != "" and cmds[3] is not None:
                                            start = 5 + 1 + len(cmds[1]) + 1 + len(cmds[2]) + 1
                                            mes = command[start:]
                                            content = lst.content.split("{:||:}")
                                            content.append(mes)
                                            ncontent = "{:||:}".join(content)
                                            List.objects.filter(user=profile, key=cmds[2]).update(content=ncontent)
                                            if cmds[1] == "suffix":
                                                msg = "Message successfully appended to the end of the list."
                                            else:
                                                msg = "Message successfully added to list."
                                        else:
                                            msg = "Message to be added to list must be specified."
                                    except List.DoesNotExist:
                                        msg = "Specified list name does not exist."
                                else:
                                    msg = "List name must be specified."

                            if cmds[1] == "remove":
                                if cmds[2] != "" and cmds[2] is not None:
                                    try:
                                        lst = List.objects.get(user=profile, key=cmds[2])
                                        if cmds[3] != "" and cmds[3] is not None:
                                            if cmds[3].isdigit():
                                                if int(cmds[3]) >= 1:
                                                    content = lst.content.split("{:||:}")
                                                    if int(cmds[3]) <= (len(content) - 1):
                                                        content.remove(content[int(cmds[3])])
                                                        ncontent = "{:||:}".join(content)
                                                        List.objects.filter(user=profile, key=cmds[2])\
                                                            .update(content=ncontent)
                                                        msg = "Item successfully removed from list."
                                                    else:
                                                        msg = "Specified ID number is out of range, there are only " \
                                                              "" + str((len(content) - 1)) + " items is this list."
                                                else:
                                                    msg = "ID number must be greater than zero (0)."
                                            else:
                                                msg = "Specified ID number must be numeric."
                                        else:
                                            msg = "ID number of the item to be removed " \
                                                  "from this list must be specified."
                                    except List.DoesNotExist:
                                        msg = "Specified list name does not exist."
                                else:
                                    msg = "List name must be specified."

                            if cmds[1] == "mode":
                                if cmds[2] != "" and cmds[2] is not None:
                                    try:
                                        lst = List.objects.get(user=profile, key=cmds[2])
                                        if cmds[3] != "" and cmds[3] is not None:
                                            if cmds[3] == "order" or cmds[3] == "random":
                                                content = lst.content.split("{:||:}")
                                                if cmds[3] == "order":
                                                    List.objects.filter(user=profile, key=cmds[2])\
                                                        .update(order="order", index="1")
                                                    i = 1
                                                    ncontent = [""]
                                                    for c in content:
                                                        if c != "":
                                                            ncontent.append(str(i) + ". " + c + "<br><br>")
                                                            i = i + 1
                                                    ncontent[0] = "<div style=\"text-align: center;\">" \
                                                                  "<b style=\"font-weight: bolder\">"\
                                                                  + lst.key + "<b></div><br><br>"
                                                    msg = "".join(ncontent)
                                                elif cmds[3] == "random":
                                                    List.objects.filter(user=profile, key=cmds[2]) \
                                                        .update(order="random", index="1")
                                                    i = 1
                                                    nncontent = []
                                                    ncontent = [""]
                                                    for c in content:
                                                        if c != "":
                                                            nncontent.append(str(i) + ". " + c + "<br><br>")
                                                            i = i + 1
                                                    ncontent[0] = "<div style=\"text-align: center;\">" \
                                                                  "<b style=\"font-weight: bolder\">" \
                                                                  + lst.key + "<b></div><br><br>"
                                                    random.shuffle(nncontent)
                                                    for n in nncontent:
                                                        ncontent.append(n)
                                                    msg = "".join(ncontent)
                                            else:
                                                msg = "The fourth parameter can only be \"order\" or \"random\"."
                                        else:
                                            msg = "A fourth parameter is required for this command."
                                    except List.DoesNotExist:
                                        msg = "Specified list name does not exist."
                                else:
                                    msg = "List name must be specified."

                            if cmds[1] == "prefix":
                                if cmds[2] != "" and cmds[2] is not None:
                                    try:
                                        lst = List.objects.get(user=profile, key=cmds[2])
                                        if cmds[3] != "" and cmds[3] is not None:
                                            start = 5 + 1 + len(cmds[1]) + 1 + len(cmds[2]) + 1
                                            mes = command[start:]
                                            content = lst.content.split("{:||:}")
                                            content[0] = mes
                                            content.insert(0, "")
                                            ncontent = "{:||:}".join(content)
                                            List.objects.filter(user=profile, key=cmds[2]).update(content=ncontent)
                                            msg = "Message successfully added to the beginning of the list."
                                        else:
                                            msg = "Message to be added to list must be specified."
                                    except List.DoesNotExist:
                                        msg = "Specified list name does not exist."
                                else:
                                    msg = "List name must be specified."

                            if cmds[1] == "showall" or cmds[1] == "showallcontents":
                                if cmds[2] != "" and cmds[2] is not None:
                                    try:
                                        lst = List.objects.get(user=profile, key=cmds[2])
                                        content = lst.content.split("{:||:}")
                                        i = 1
                                        ncontent = [""]
                                        for c in content:
                                            if c != "":
                                                if cmds[1] == "showallcontents":
                                                    ncontent.append(str(i) + ". " + c + "<br><br>")
                                                    i = i + 1
                                                if cmds[1] == "showall":
                                                    ncontent.append( c + "<br><br>")
                                        if cmds[1] == "showallcontents":
                                            ncontent[0] = "<div style=\"text-align: center;\">" \
                                                          "<b style=\"font-weight: bolder\">"\
                                                          + lst.key + "<b></div><br><br>"
                                        msg = "".join(ncontent)
                                    except List.DoesNotExist:
                                        msg = "Specified list name does not exist."
                                else:
                                    msg = "List name must be specified."

                            if cmds[1] is not None and len(cmds) == 2:
                                try:
                                    li = List.objects.get(key=cmds[1], user=profile)
                                    content = li.content.split("{:||:}")
                                    cont = []
                                    mx = len(content) - 1
                                    if li.order == "order":
                                        con = content[int(li.index)]
                                        nindex = 1
                                        if int(li.index) < mx:
                                            nindex = int(li.index) + 1
                                        cont.append(con)
                                        List.objects.filter(key=li.key, user=li.user) \
                                            .update(index=nindex)
                                    if li.order == "random":
                                        ind = random.choice(list(range(1, mx)))
                                        con = content[ind]
                                        cont.append(con)
                                    content = cont
                                    i = 1
                                    ncontent = []
                                    for c in content:
                                        if c != "<br><br>" and c != "":
                                            ncontent.append(c)
                                            i = i + 1
                                    msg = "".join(ncontent)
                                except List.DoesNotExist:
                                    msg = "You do not have any list configured with the specified name!"

                        if msg == "Oops! Invalid command entered.":
                            try:
                                cm = Config.objects.get(user=profile, key=command[1:])
                                msg = cm.content
                            except Config.DoesNotExist:
                                pass

                        resp = {
                            "msg": msg,
                            "done": True,
                            "showmes": showmes,
                            "config": config
                        }
                    else:
                        resp = {
                            "msg": msg,
                            "done": True,
                            "showmes": showmes,
                            "config": config
                        }
                else:
                    config['pause'] = True
                    resp = {
                        "msg": "Bot is currently paused, un-pause bot to continue sending commands.",
                        "done": True,
                        "showmes": showmes,
                        "config": config
                    }
            else:
                resp = {
                    "msg": msg,
                    "done": True,
                    "showmes": showmes,
                    "config": config
                }
            return resp
        except Profile.DoesNotExist:
            resp = {
                "msg": "User dose not exist.",
                "done": False
            }
            return resp

    @csrf_exempt
    def post(self, request):
        # post request to create a new list record
        if request.method == 'POST':
            form = request.data
            if form is not None:
                email = form['email']
                command = form['command']
                config = form['config']
                try:
                    # check if user exists
                    usr = User.objects.get(email=email)
                    ud = usr.profile.id
                    ob = {'command': command, 'sender': ud, 'config': config}
                    # run the process() method above and return response from it.
                    return Response(self.process(ob))
                except User.DoesNotExist:
                    resp = {
                        "msg": "User dose not exist.",
                        "done": False
                    }
                    return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            return Response(resp)

    @csrf_exempt
    def put(self, request):
        # put request to update chat record
        if request.method == 'PUT':
            form = request.data
            if form is not None:
                email = form['email']
                idd = form['id']
                viewed = form['viewed']
                remark = form['remark']
                try:
                    # check if user exist
                    usr = User.objects.get(email=email)
                    ud = usr.profile.id
                    try:
                        # check if specified chat exist
                        Chat.objects.get(id=idd, sender=ud)
                        if viewed == "Y":
                            # update records of the specified chat
                            Chat.objects.filter(id=idd, sender=ud).update(viewed=datetime.now(timezone.utc))
                        if remark != "":
                            # update records of the specified chat
                            Chat.objects.filter(id=idd, sender=ud).update(remark=remark)
                        resp = {"msg": 'Chat record successfully updated.', 'done': True}
                        return Response(resp)
                    except Chat.DoesNotExist:
                        resp = {
                            "msg": "Item does not exist in your chat history.",
                            "done": False
                        }
                        return Response(resp)
                except User.DoesNotExist:
                    resp = {
                        "msg": "User dose not exist.",
                        "done": False
                    }
                    return Response(resp)
            else:
                resp = {
                    "msg": "All fields are required",
                    "done": False
                }
                return Response(resp)
        else:
            resp = {
                "msg": "Invalid request",
                "done": False
            }
            Response(resp)
