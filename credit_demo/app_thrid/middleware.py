#python\
#-*-coding:utf-8-*-
'''
credit_demo	middleware
@Author:Mr.Liang
@Date:2020-11-18
@Version:1.0
@Descript:
'''
import time

from django.http import HttpResponseForbidden
from django.conf import settings
from app.models import Log
class Md2:
	def __init__(self,get_response = None):
		self.get_response = get_response

	def __call__(self,request):
		#相当于process_request
		# user_obj = request.user
		ip = request.META['REMOTE_ADDR']
		t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
		if ip in getattr(settings,'IPLIST',[]):
			return HttpResponseForbidden('<h3 style = "color:red">你的ip暂时无法使用</h3>')
		response = self.get_response(request)#固定语法，上面是请求，下面是响应
		# Log.objects.create(time = t,operation = 'get', Uid = user_obj)
		return response