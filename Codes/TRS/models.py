from django.db import models

from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.shortcuts import render
from django.db.models import Q
import json
from datetime import date

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from TRS.forms import *

# Create your models here.


class FLIGHTS(models.Model):
    flightNum = models.CharField(primary_key=True, unique=True, max_length=50, null=False)
    price = models.IntegerField(null=False)
    numSeats = models.IntegerField(null=False)
    numAvail = models.IntegerField(null=False)
    FromCity = models.CharField(max_length=50, null=False)
    ArivCity = models.CharField(max_length=50, null=False)


class HOTELS(models.Model):
    location = models.CharField(primary_key=True, unique=True, max_length=50, null=False)
    price = models.IntegerField(null=False)
    numRooms = models.IntegerField(null=False)
    numAvail = models.IntegerField(null=False)


class BUS(models.Model):
    location = models.CharField(primary_key=True, unique=True, max_length=50, null=False)
    price = models.IntegerField(null=False)
    numBus = models.IntegerField(null=False)
    numAvail = models.IntegerField(null=False)


class CUSTOMERS(models.Model):
    custName = models.CharField(primary_key=True, unique=True, max_length=50, null=False)
    custID = models.CharField(null=False, unique=True, max_length=20)
    custPassword = models.CharField(null=False, max_length=20)
    age = models.IntegerField(null=True)
    sex = models.CharField(null=True, max_length=5)
    balance = models.IntegerField(null=True, default=0)


class RESERVATIONS(models.Model):
    custName = models.CharField(max_length=50, null=False)
    resvType = models.IntegerField(null=False)
    resvKey = models.CharField(primary_key=True, unique=True, null=False, max_length=50)
    resvInfo = models.CharField(max_length=50, null=False)
    # resvType：1为预订航班；2为预订宾馆房间；3为预订大巴车。


class Administrator(models.Model):
    adminID = models.CharField(primary_key=True, null=False, unique=True, max_length=20)
    adminPassword = models.CharField(null=False, max_length=20)
    balance = models.IntegerField(null=True, default=0)


# @receiver(pre_delete, sender=FLIGHTS)
# def before_delete_blog(sender, instance, **kwargs):
#
#     response = {}
#     try:
#         reservation_form = RESERVATIONSForm(request.POST)
#         if reservation_form.is_valid():
#             resvKey = reservation_form.cleaned_data['resvKey']
#             try:
#                 reservation = RESERVATIONS.objects.get(resvKey=resvKey)
#                 reservation.delete()
#                 print(resvKey[len(request.session.get('custName')):])
#                 print(resvKey[len(request.session.get('custName'))+1:])
#                 if reservation_form.cleaned_data['resvType'] == 1:
#                     flight = FLIGHTS.objects.get(flightNum=resvKey[len(request.session.get('custName')):])
#                     flight.numAvail = flight.numAvail + 1
#                     flight.save()
#
#                 elif reservation_form.cleaned_data['resvType'] == 3:
#                     bus = BUS.objects.get(location=resvKey[len(request.session.get('custName'))+1:])
#                     bus.numAvail = bus.numAvail + 1
#                     bus.save()
#
#                 elif reservation_form.cleaned_data['resvType'] == 2:
#                     hotel = HOTELS.objects.get(location=resvKey[len(request.session.get('custName'))+1:])
#                     hotel.numAvail = hotel.numAvail + 1
#                     hotel.save()
#                 response['msg'] = '删除成功'
#                 response['error_num'] = 0
#             except Exception as e:
#                 response['msg'] = '该订单不存在，删除失败！'
#                 response['error_num'] = 1
#         else:
#             response['msg'] = '表单格式有误！'
#             response['error_num'] = 1
#
#     except Exception as e:
#         response['msg'] = str(e)
#         response['error_num'] = 2
#     print(instance.flightNum + " has been deleted ")
