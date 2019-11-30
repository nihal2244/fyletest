from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Banks, Branches
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.http import JsonResponse, HttpResponse, Http404
import datetime
import calendar
import time
import jwt
import json

# Create your views here.


def jwtGenerator(request):
    exp = datetime.datetime.utcnow() + datetime.timedelta(days=5)
    exp = calendar.timegm(exp.timetuple())

    payload = {
        # issued at time
        'iat': int(time.time()),
        # expiration time
        'exp': exp
    }
    jwt_token = {'jwt_token': jwt.encode(
        payload, "SECRET_KEY").decode('utf-8')}
    print(type(jwt_token))

    return HttpResponse(json.dumps(jwt_token), status=200, content_type="application/json")


def authenticate_jwt(token):
    try:
        payload = jwt.decode(token, "SECRET_KEY")
        experation = payload['exp']
        issued = payload['iat']
        # if int(time.time()) < experation and token:
        #     return True
        # else:
        #     return False
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.' 


def getifsc(request):
    try:
        if authenticate_jwt(request.META.get('HTTP_AUTHORIZATION', '')):
            ifsc_code = Branches.objects.get(pk=request.GET['ifsc'])
            data = {"ifsc": ifsc_code.ifsc,
                    "bank_name": ifsc_code.bank.name,
                    "branch": ifsc_code.branch,
                    "address": ifsc_code.address,
                    "city": ifsc_code.city,
                    "district": ifsc_code.district,
                    "state": ifsc_code.state
                    }
    except ObjectDoesNotExist:
        raise Http404
    return JsonResponse({"data": data})


def filterbyname(request):
    try:
        if authenticate_jwt(request.META.get('HTTP_AUTHORIZATION', '')):
            data_list = []
            offset = int(request.GET['offset'])
            limit = int(request.GET['limit'])
            bank_name = request.GET['name']
            city = request.GET['city']
            name = Banks.objects.get(name=bank_name)
            for branch in name.branch.all().filter(city=city)[offset:limit+1]:
                data_list.append({"ifsc": branch.ifsc,
                                "bank_name": branch.bank.name,
                                "branch": branch.branch,
                                "address": branch.address,
                                "city": branch.city,
                                "district": branch.district,
                                "state": branch.state
                                })

    except ObjectDoesNotExist:
        raise Http404
    return JsonResponse(data_list, safe=False)
