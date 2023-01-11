from django.shortcuts import render
from TRS import models
from django.db.models import Q
import json
from datetime import date

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from TRS.forms import *
from TRS.models import *

# Create your views here.


def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])


def login(request):
    return render(request, 'index.html')


@csrf_exempt
@require_http_methods("POST")
def cust_login(request):
    response = {}
    if request.session.get('is_login', None):
        response['msg'] = 'this employee has logined'
        response['error_num'] = 0
        response['position'] = request.session.get('position')
        return JsonResponse(response)

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        response['msg'] = 'please check '
        print(login_form)
        id = login_form.cleaned_data['id']
        password = login_form.cleaned_data['password']
        position = login_form.cleaned_data['position']
        if position=='customer':
            try:
                user = CUSTOMERS.objects.get(custID=id)
                if user.custPassword == password:
                    request.session['is_login'] = True
                    request.session['custName'] = user.custName
                    request.session['position'] = "customer"
                    response['msg'] = '登陆成功'
                    response['error_num'] = 0
                    response['position'] = "customer"
                    return JsonResponse(response)
                else:
                    response['msg'] = '登录失败：密码错误'
                    response['error_num'] = 1
                    return JsonResponse(response)
            except:
                response['msg'] = '登录失败：账号不存在'
                response['error_num'] = 1
                return JsonResponse(response)
        else:
            try:
                user = Administrator.objects.get(adminID=id)
                if user.adminPassword == password:
                    request.session['is_login'] = True
                    request.session['id'] = user.adminID
                    request.session['position'] = "administrator"
                    response['msg'] = 'login successfully'
                    response['error_num'] = 0
                    response['position'] = "administrator"
                    return JsonResponse(response)
                else:
                    response['msg'] = '登录失败：密码错误'
                    response['error_num'] = 1
            except:
                response['msg'] = '登录失败：账号不存在'
                response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods("POST")
def logout(request):
    response = {}

    if not request.session.get('is_login'):
        response['msg'] = 'have not login'
        response['error_num'] = 0
        return JsonResponse(response)
    request.session.flush()
    response['msg'] = 'logout successfully'
    response['error_num'] = 1
    # except Exception as e:
    #     response['msg'] = str(e)
    #     response['error_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods("POST")
def register(request):
    response = {}
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        print("here")
        if register_form.is_valid():
            custID = register_form.cleaned_data['custID']
            custPassword = register_form.cleaned_data['custPassword']
            custName = register_form.cleaned_data['custName']
            age = register_form.cleaned_data['age']
            sex = register_form.cleaned_data['sex']
            balance = register_form.cleaned_data['balance']

            try:
                same_cust = CUSTOMERS.objects.get(custName=custName)
                response['msg'] = '该用户已注册！'
                response['error_num'] = 2
                return JsonResponse(response)

            except Exception as e:
                new_cust = CUSTOMERS(
                    custName=custName,
                    custID=custID,
                    custPassword=custPassword,
                    age=age,
                    sex=sex,
                    balance=balance
                )
                response['msg'] = '注册成功'
                response['error_num'] = 0
                new_cust.save()
        else:
            response['msg'] = '表单格式有误'
            response['error_num'] = 1

    return JsonResponse(response)


# 管理员部分

# 用户管理
@csrf_exempt
@require_http_methods(["POST"])
def add_one_customer(request):
    response = {}
    try:
        customer_form = CUSTOMERSForm(request.POST)
        if customer_form.is_valid():
            customer_name = customer_form.cleaned_data['custName']
            try:
                CUSTOMERS.objects.get(custName=customer_name)
                response['msg'] = '该用户已添加'
                response['error_num'] = 1
            except:

                customer = CUSTOMERS(custName=customer_name,
                                    custID=customer_form.cleaned_data['custID'],
                                    custPassword=customer_form.cleaned_data['custPassword'],
                                    age=customer_form.cleaned_data['age'],
                                    sex=customer_form.cleaned_data['sex'],
                                    balance=customer_form.cleaned_data['balance']
                                    )
                customer.save()
                response['msg'] = '添加用户成功'
                response['error_num'] = 0
        else:
            response['msg'] = '表单格式有误'
            response['error_num'] = 1
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_customer(request):
    response = {}
    try:
        if request.GET.get('custName') != '':
            print(( request.GET.get('custName')))
            customer = CUSTOMERS.objects.get(custName=request.GET.get('custName'))
            response['list'] = object_to_json(customer)
            total = 1
            response['total'] = total
            response['error_num'] = -1
        else:
            # 返回值增加了分页，把数据分成每页pagesize个数据
            customer = CUSTOMERS.objects.all()
            listall =  json.loads(serializers.serialize("json", customer))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize>total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum-1]
            response['error_num'] = 0
        response['msg'] = '显示用户成功'
        response['total'] = total
    except  Exception as e:
        if str(e) == "range() arg 3 must not be zero":
            response['error_num'] = 0
            response['msg'] = 'successfully'
        else:
            response['msg'] = str(e)
            response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def change_one_customer(request):
    response = {}
    try:
        customer_form = CUSTOMERSForm(request.POST)
        if customer_form.is_valid():
            customer_name = customer_form.cleaned_data['custName']
            try:
                customer = CUSTOMERS.objects.get(custName=customer_name)
                customer.custID = customer_form.cleaned_data['custID']
                customer.custPassword = customer_form.cleaned_data['custPassword']
                customer.age = customer_form.cleaned_data['age']
                customer.sex = customer_form.cleaned_data['sex']
                customer.balance = customer_form.cleaned_data['balance']
                customer.save()
                response['msg'] = '修改成功'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = '该用户不存在！'
                response['error_num'] = 1
        else:
            response['msg'] = '表单格式有误！'
            response['error_num'] = 1

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def delete_one_customer(request):
    response = {}
    try:
        customer_form = CUSTOMERSForm(request.POST)
        if customer_form.is_valid():
            customer_name = customer_form.cleaned_data['custName']
            try:
                customer = CUSTOMERS.objects.get(custName=customer_name)
                customer.delete()
                response['msg'] = '删除成功'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = '该用户不存在，删除失败！'
                response['error_num'] = 1
        else:
            response['msg'] = '表单格式有误！'
            response['error_num'] = 1

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


# 航班管理
@csrf_exempt
@require_http_methods(["POST"])
def add_one_flight(request):
    response = {}
    try:
        flight_form = FLIGHTSForm(request.POST)
        if flight_form.is_valid():
            flight_num = flight_form.cleaned_data['flightNum']
            try:
                FLIGHTS.objects.get(flightNum=flight_num)
                response['msg'] = '该航班已添加'
                response['error_num'] = 1
            except:

                flight = FLIGHTS(flightNum=flight_num,
                                    price=flight_form.cleaned_data['price'],
                                    numSeats=flight_form.cleaned_data['numSeats'],
                                    numAvail=flight_form.cleaned_data['numAvail'],
                                    FromCity=flight_form.cleaned_data['FromCity'],
                                    ArivCity=flight_form.cleaned_data['ArivCity']
                                    )
                flight.save()
                response['msg'] = '添加航班成功'
                response['error_num'] = 0
        else:
            response['msg'] = '表单格式有误'
            response['error_num'] = 1
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_flight(request):
    response = {}
    try:
        if request.GET.get('flightNum') != '':
            print(( request.GET.get('flightNum')))
            flight = FLIGHTS.objects.get(flightNum=request.GET.get('flightNum'))
            print(flight)
            response['list'] = object_to_json(flight)
            total = 1
            response['total'] = total
            response['error_num'] = -1
        elif request.GET.get('FromCity') != '' and request.GET.get('ArivCity') != '':
            flight = FLIGHTS.objects.get(Q(Q(FromCity=request.GET.get('FromCity')) & Q(ArivCity=request.GET.get('ArivCity'))))
            print(flight)
            response['list'] = object_to_json(flight)
            total = 1
            response['total'] = total
            response['error_num'] = -1
            # 将get改成filter  使用 json.loads(serializers.serialize("json", flight))可能更加统一！！后续更改
        else:
            # 返回值增加了分页，把数据分成每页pagesize个数据
            flight = FLIGHTS.objects.all()
            listall =  json.loads(serializers.serialize("json", flight))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize>total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum-1]
            response['error_num'] = 0
        response['msg'] = '显示航班成功'
        response['total'] = total
    except  Exception as e:
        if str(e) == "range() arg 3 must not be zero":
            response['error_num'] = 0
            response['msg'] = 'successfully'
        else:
            response['msg'] = str(e)
            response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def change_one_flight(request):
    response = {}
    try:
        flight_form = FLIGHTSForm(request.POST)
        if flight_form.is_valid():
            flight_num = flight_form.cleaned_data['flightNum']
            try:
                flight = FLIGHTS.objects.get(flightNum=flight_num)
                flight.price = flight_form.cleaned_data['price']
                flight.numSeats = flight_form.cleaned_data['numSeats']
                flight.numAvail = flight_form.cleaned_data['numAvail']
                flight.FromCity = flight_form.cleaned_data['FromCity']
                flight.ArivCity = flight_form.cleaned_data['ArivCity']
                flight.save()
                response['msg'] = '修改成功'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = '该航班不存在！'
                response['error_num'] = 1
        else:
            response['msg'] = '表单格式有误！'
            response['error_num'] = 1

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def delete_one_flight(request):
    response = {}
    try:
        flight_form = FLIGHTSForm(request.POST)
        if flight_form.is_valid():
            flight_num = flight_form.cleaned_data['flightNum']
            try:
                flight = FLIGHTS.objects.get(flightNum=flight_num)
                flight.delete()
                response['msg'] = '删除成功'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = '该航班不存在，删除失败！'
                response['error_num'] = 1
        else:
            response['msg'] = '表单格式有误！'
            response['error_num'] = 1

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


# 大巴管理
@csrf_exempt
@require_http_methods(["POST"])
def add_one_bus(request):
    response = {}
    try:
        bus_form = BUSForm(request.POST)
        if bus_form.is_valid():
            location = bus_form.cleaned_data['location']
            try:
                BUS.objects.get(location=location)
                response['msg'] = '该大巴已添加'
                response['error_num'] = 1
            except:

                bus = BUS(location=location,
                                    price=bus_form.cleaned_data['price'],
                                    numBus=bus_form.cleaned_data['numBus'],
                                    numAvail=bus_form.cleaned_data['numAvail'],
                                    )
                bus.save()
                response['msg'] = '添加航班成功'
                response['error_num'] = 0
        else:
            response['msg'] = '表单格式有误'
            response['error_num'] = 1
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_bus(request):
    response = {}
    try:
        if request.GET.get('location') != '':
            print(( request.GET.get('location')))
            bus = BUS.objects.get(location=request.GET.get('location'))
            print(bus)
            response['list'] = object_to_json(bus)
            total = 1
            response['total'] = total
            response['error_num'] = -1
        else:
            # 返回值增加了分页，把数据分成每页pagesize个数据
            bus = BUS.objects.all()
            listall =  json.loads(serializers.serialize("json", bus))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize>total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum-1]
            response['error_num'] = 0
        response['msg'] = '显示大巴成功'
        response['total'] = total
    except  Exception as e:
        if str(e) == "range() arg 3 must not be zero":
            response['error_num'] = 0
            response['msg'] = 'successfully'
        else:
            response['msg'] = str(e)
            response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def change_one_bus(request):
    response = {}
    try:
        bus_form = BUSForm(request.POST)
        if bus_form.is_valid():
            location = bus_form.cleaned_data['location']
            try:
                bus = BUS.objects.get(location=location)
                bus.price = bus_form.cleaned_data['price']
                bus.numBus = bus_form.cleaned_data['numBus']
                bus.numAvail = bus_form.cleaned_data['numAvail']
                bus.save()
                response['msg'] = '修改成功'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = '该大巴不存在！'
                response['error_num'] = 1
        else:
            response['msg'] = '表单格式有误！'
            response['error_num'] = 1

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def delete_one_bus(request):
    response = {}
    try:
        bus_form = BUSForm(request.POST)
        if bus_form.is_valid():
            location = bus_form.cleaned_data['location']
            try:
                bus = BUS.objects.get(location=location)
                bus.delete()
                response['msg'] = '删除成功'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = '该大巴不存在，删除失败！'
                response['error_num'] = 1
        else:
            response['msg'] = '表单格式有误！'
            response['error_num'] = 1

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


# 旅店管理
@csrf_exempt
@require_http_methods(["POST"])
def add_one_hotel(request):
    response = {}
    try:
        hotel_form = HOTELSForm(request.POST)
        if hotel_form.is_valid():
            location = hotel_form.cleaned_data['location']
            try:
                HOTELS.objects.get(location=location)
                response['msg'] = '该大旅店已添加'
                response['error_num'] = 1
            except:

                hotel = HOTELS(location=location,
                                    price=hotel_form.cleaned_data['price'],
                                    numRooms=hotel_form.cleaned_data['numRooms'],
                                    numAvail=hotel_form.cleaned_data['numAvail'],
                                    )
                hotel.save()
                response['msg'] = '添加航班成功'
                response['error_num'] = 0
        else:
            response['msg'] = '表单格式有误'
            response['error_num'] = 1
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_hotel(request):
    response = {}
    try:
        if request.GET.get('location') != '':
            print(( request.GET.get('location')))
            hotel = HOTELS.objects.get(location=request.GET.get('location'))
            print(hotel)
            response['list'] = object_to_json(hotel)
            total = 1
            response['total'] = total
            response['error_num'] = -1
        else:
            # 返回值增加了分页，把数据分成每页pagesize个数据
            hotel = HOTELS.objects.all()
            listall =  json.loads(serializers.serialize("json", hotel))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize>total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum-1]
            response['error_num'] = 0
        response['msg'] = '显示旅店成功'
        response['total'] = total
    except  Exception as e:
        if str(e) == "range() arg 3 must not be zero":
            response['error_num'] = 0
            response['msg'] = 'successfully'
        else:
            response['msg'] = str(e)
            response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def change_one_hotel(request):
    response = {}
    try:
        hotel_form = HOTELSForm(request.POST)
        if hotel_form.is_valid():
            location = hotel_form.cleaned_data['location']
            try:
                hotel = HOTELS.objects.get(location=location)
                hotel.price = hotel_form.cleaned_data['price']
                hotel.numRooms = hotel_form.cleaned_data['numRooms']
                hotel.numAvail = hotel_form.cleaned_data['numAvail']
                hotel.save()
                response['msg'] = '修改成功'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = '该旅店不存在！'
                response['error_num'] = 1
        else:
            response['msg'] = '表单格式有误！'
            response['error_num'] = 1

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def delete_one_hotel(request):
    response = {}
    try:
        hotel_form = HOTELSForm(request.POST)
        if hotel_form.is_valid():
            location = hotel_form.cleaned_data['location']
            try:
                hotel = HOTELS.objects.get(location=location)
                hotel.delete()
                response['msg'] = '删除成功'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = '该大旅店不存在，删除失败！'
                response['error_num'] = 1
        else:
            response['msg'] = '表单格式有误！'
            response['error_num'] = 1

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


#用户


@csrf_exempt
@require_http_methods(['POST'])
def add_reservation(request):
    response = {}
    try:
        reservation_form = RESERVATIONSForm(request.POST)
        if reservation_form.is_valid():
            resvKey = reservation_form.cleaned_data['resvKey']
            try:
                RESERVATIONS.objects.get(resvKey=request.session.get('custName')+resvKey)
                response['msg'] = '该订单已存在'
                response['error_num'] = 1
            except:

                reservation = RESERVATIONS(resvKey=request.session.get('custName')+resvKey,
                               resvType=reservation_form.cleaned_data['resvType'],
                               custName=request.session.get('custName'),
                               resvInfo = reservation_form.cleaned_data['resvInfo']
                               )


                if reservation_form.cleaned_data['resvType'] == 1:
                    flight = FLIGHTS.objects.get(flightNum=resvKey)

                    if flight.numAvail==0:
                        response['msg'] = '无座'
                        response['error_num'] = 2
                        return JsonResponse(response)
                    else:
                        flight.numAvail = flight.numAvail-1
                        flight.save()
                        reservation.save()
                        response['msg'] = '添加订单成功'
                        response['error_num'] = 0
                        return JsonResponse(response)
                elif reservation_form.cleaned_data['resvType'] == 3:

                    print("+++++++++++++++++",resvKey[1:])
                    bus = BUS.objects.get(location = resvKey[1:])

                    if bus.numAvail == 0:
                        response['msg'] = '无座'
                        response['error_num'] = 2
                        return JsonResponse(response)
                    else:
                        bus.numAvail = bus.numAvail - 1
                        bus.save()
                        reservation.save()
                        response['msg'] = '添加订单成功'
                        response['error_num'] = 0
                        return JsonResponse(response)
                elif reservation_form.cleaned_data['resvType'] == 2:
                    hotel = HOTELS.objects.get(location = resvKey[1:])

                    if hotel.numAvail == 0:
                        response['msg'] = '无房'
                        response['error_num'] = 2
                        return JsonResponse(response)
                    else:
                        hotel.numAvail = hotel.numAvail - 1
                        hotel.save()
                        reservation.save()
                        response['msg'] = '添加订单成功'
                        response['error_num'] = 0
                        return JsonResponse(response)


        else:
            response['msg'] = '表单格式有误'
            response['error_num'] = 1
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_reservation(request):
    response = {}
    try:
        if request.session.get('position') == 'administrator':
            reservation = RESERVATIONS.objects.all()
            listall = json.loads(serializers.serialize("json", reservation))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize > total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum - 1]
            response['error_num'] = 0
            response['msg'] = '显示订单成功'
            response['total'] = total
        else:
            reservation = RESERVATIONS.objects.filter(custName = request.session.get('custName'))
            listall = json.loads(serializers.serialize("json", reservation))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize > total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum - 1]
            response['error_num'] = 0
            response['msg'] = '显示订单成功'
            response['total'] = total
    except  Exception as e:
        if str(e) == "range() arg 3 must not be zero":
            response['error_num'] = 0
            response['msg'] = 'successfully'
        else:
            response['msg'] = str(e)
            response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def delete_one_reservation(request):
    response = {}
    try:
        reservation_form = RESERVATIONSForm(request.POST)
        if reservation_form.is_valid():
            resvKey = reservation_form.cleaned_data['resvKey']
            try:
                reservation = RESERVATIONS.objects.get(resvKey=resvKey)
                reservation.delete()
                print(resvKey[len(request.session.get('custName')):])
                print(resvKey[len(request.session.get('custName'))+1:])
                if reservation_form.cleaned_data['resvType'] == 1:
                    flight = FLIGHTS.objects.get(flightNum=resvKey[len(request.session.get('custName')):])
                    flight.numAvail = flight.numAvail + 1
                    flight.save()

                elif reservation_form.cleaned_data['resvType'] == 3:
                    bus = BUS.objects.get(location=resvKey[len(request.session.get('custName'))+1:])
                    bus.numAvail = bus.numAvail + 1
                    bus.save()

                elif reservation_form.cleaned_data['resvType'] == 2:
                    hotel = HOTELS.objects.get(location=resvKey[len(request.session.get('custName'))+1:])
                    hotel.numAvail = hotel.numAvail + 1
                    hotel.save()
                response['msg'] = '删除成功'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = '该订单不存在，删除失败！'
                response['error_num'] = 1
        else:
            response['msg'] = '表单格式有误！'
            response['error_num'] = 1

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


def show_travel_route(request):
    response = {}
    try:
        if request.session.get('position') == 'administrator':
            reservation = RESERVATIONS.objects.filter(resvType = 1)
            listall = json.loads(serializers.serialize("json", reservation))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize > total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum - 1]
            response['error_num'] = 0
            response['msg'] = '显示订单成功'
            response['total'] = total
        else:
            reservation = RESERVATIONS.objects.filter(Q(Q(custName=request.session.get('custName')) & Q(resvType=1)))
            listall = json.loads(serializers.serialize("json", reservation))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize > total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum - 1]
            response['error_num'] = 0
            response['msg'] = '显示订单成功'
            response['total'] = total
    except  Exception as e:
        if str(e) == "range() arg 3 must not be zero":
            response['error_num'] = 0
            response['msg'] = 'successfully'
        else:
            response['msg'] = str(e)
            response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def check_route(request):
    response = {}
    try:
        check_form = CHECKForm(request.POST)
        if check_form.is_valid():
            FromCity = check_form.cleaned_data['FromCity']
            ArivCity = check_form.cleaned_data['ArivCity']

            from_bus = len( RESERVATIONS.objects.filter(
                Q(Q(custName=request.session.get('custName')) & Q(resvKey=request.session.get('custName')+'B' + FromCity))))
            arrive_bus = len(RESERVATIONS.objects.filter(
                Q(Q(custName=request.session.get('custName')) & Q(resvKey=request.session.get('custName')+'B' + ArivCity))))
            arrive_hotel = len(RESERVATIONS.objects.filter(
                Q(Q(custName=request.session.get('custName')) & Q(resvKey=request.session.get('custName')+'H' + ArivCity))))

            if(from_bus > 0 and arrive_bus > 0 and arrive_hotel > 0):
                response['from_bus'] = 'true'
                response['arrive_bus'] = 'true'
                response['arrive_hotel'] = 'true'
            elif (from_bus > 0 and arrive_bus > 0 and arrive_hotel == 0):
                response['from_bus'] = 'true'
                response['arrive_bus'] = 'true'
                response['arrive_hotel'] = 'false'
            elif (from_bus > 0 and arrive_bus == 0 and arrive_hotel > 0):
                response['from_bus'] = 'true'
                response['arrive_bus'] = 'false'
                response['arrive_hotel'] = 'true'
            elif (from_bus > 0 and arrive_bus == 0 and arrive_hotel == 0):
                response['from_bus'] = 'true'
                response['arrive_bus'] = 'false'
                response['arrive_hotel'] = 'false'
            elif (from_bus == 0 and arrive_bus > 0 and arrive_hotel > 0):
                response['from_bus'] = 'false'
                response['arrive_bus'] = 'true'
                response['arrive_hotel'] = 'true'
            elif (from_bus == 0 and arrive_bus > 0 and arrive_hotel == 0):
                response['from_bus'] = 'false'
                response['arrive_bus'] = 'true'
                response['arrive_hotel'] = 'false'
            elif (from_bus == 0 and arrive_bus == 0 and arrive_hotel > 0):
                response['from_bus'] = 'false'
                response['arrive_bus'] = 'false'
                response['arrive_hotel'] = 'true'
            elif (from_bus == 0 and arrive_bus == 0 and arrive_hotel == 0):
                response['from_bus'] = 'false'
                response['arrive_bus'] = 'false'
                response['arrive_hotel'] = 'false'

            response['msg'] = '检查成功'
            response['error_num'] = 0
        else:
            response['msg'] = '表单格式有误！'
            response['error_num'] = 1

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)