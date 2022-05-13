from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .alipay import AliPay
import uuid
from urllib.parse import parse_qs
from accounts.models import *

# Create your views here.
def index(request):
    return render(request,'index.html')
 

"""
Bitten Coin charge (0.1 rmb)
""" 
def bill1(request):
    alipay = AliPay(
        appid="2021000119666477",
        app_notify_url='https://have-you-eaten.herokuapp.com/alipay/check/',
        return_url='https://have-you-eaten.herokuapp.com/alipay/show/',
        app_private_key_path=r'alipay/keys/private2048.txt', 
        alipay_public_key_path=r'alipay/keys/alipaypublic.txt', 
        debug=True,  
    )
    res=alipay.direct_pay(
        subject='Bittencoin',  
        out_trade_no=str(uuid.uuid4()), 
        total_amount='0.1',
    )
    cli = Client.objects.get(user = request.user.id)
    cli.coin_num += 1
    cli.save()
    url='https://openapi.alipaydev.com/gateway.do?{0}'.format(res)
    return redirect(url)

"""
Bitten Coin charge (0.5 rmb)
"""  
def bill2(request):
    alipay = AliPay(
        appid="2021000119666477",
        app_notify_url='https://have-you-eaten.herokuapp.com/alipay/check/',
        return_url='https://have-you-eaten.herokuapp.com/alipay/show/',
        app_private_key_path=r'alipay/keys/private2048.txt', 
        alipay_public_key_path=r'alipay/keys/alipaypublic.txt', 
        debug=True,  
    )
    res=alipay.direct_pay(
        subject='Bittencoin',  
        out_trade_no=str(uuid.uuid4()), 
        total_amount='0.5',
    )
    cli = Client.objects.get(user = request.user.id)
    cli.coin_num += 6
    cli.save()
    url='https://openapi.alipaydev.com/gateway.do?{0}'.format(res)
    return redirect(url)

"""
Bitten Coin charge (328 rmb)
"""  
def bill3(request):
    alipay = AliPay(
        appid="2021000119666477",
        app_notify_url='https://have-you-eaten.herokuapp.com/alipay/check/',
        return_url='https://have-you-eaten.herokuapp.com/alipay/show/',
        app_private_key_path=r'alipay/keys/private2048.txt', 
        alipay_public_key_path=r'alipay/keys/alipaypublic.txt', 
        debug=True, 
    )
    res=alipay.direct_pay(
        subject='Bittencoin',  
        out_trade_no=str(uuid.uuid4()), 
        total_amount='328',
    )
    cli = Client.objects.get(user = request.user.id)
    cli.coin_num += 648
    cli.save()
    url='https://openapi.alipaydev.com/gateway.do?{0}'.format(res)
    return redirect(url)
 
"""
Redirect after paying is complete (method == 'GET')
"""  
def show(request):
    if request.method == 'GET':
        alipay = AliPay(
            appid="2021000119666477",  
            app_notify_url='https://have-you-eaten.herokuapp.com/alipay/check/',
            return_url='https://have-you-eaten.herokuapp.com/alipay/show/',
            app_private_key_path=r'alipay/keys/private2048.txt', 
            alipay_public_key_path=r'alipay/keys/alipaypublic.txt', 
            debug=True, 
        )
        param=request.GET.dict() 
        sign=param.pop('sign', None)  
        statu = alipay.verify(param,sign)
        if statu: # payment success
            return redirect("Profile")
        else: # payment failed
            return render(request, 'show.html', {'msg': 'Payment Failed'})
    else:
        return render(request, 'show.html', {'msg': 'Accept GET method only.'})
 
"""
Redirect after paying is complete (method == 'POST')
"""  
def check(request):
    if request.method=='POST':
        alipay=AliPay(appid="2021000119666477",
            app_notify_url='https://have-you-eaten.herokuapp.com/alipay/check/', 
            return_url='https://have-you-eaten.herokuapp.com/show_msg/', 
            app_private_key_path=r'alipay/keys/private2048.txt', 
            alipay_public_key_path=r'alipay/keys/alipaypublic.txt',  
            debug=True,
        )
        body=request.body.decode('utf-8')
        post_data = parse_qs(body)
        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        if status:  # payment success
            return HttpResponse('Payment Success')
        else: # payment failed
            return HttpResponse('Payment Failed')
    else:
        return HttpResponse('Accept POST method only')