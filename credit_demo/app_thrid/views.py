
import uuid,time
from django.core.paginator import Paginator

import os
from django.shortcuts import render, HttpResponse, redirect
from app.models import Auth_user,Blacklist,Log,Reply,Apply_progress,Emp,Information,Auth_user_emp_information,Auth_user_emp_reply,Announcement,News,User_credit,Credit_reporting,Blacklist,Laundry_list,user_Product
# Create your views here.

'''获取当前用户的对象'''
def getSession(request):
	u = request.user.username  #获取当前用户的session值
	employee_obj = Emp.objects.filter(username = u )[0]  #根据session值获取当前用户对象——客服的对象（‘kaiaki’需要改成account）
	return employee_obj



'''咨询信息返回页面'''
def chat(request):
	employee_obj = getSession(request)#获取当前用户对象
	mess_obj = Auth_user_emp_information.objects.filter(Eid = employee_obj)  #消息中间表——需要在页面显示消息
	uid_id = []
	for obj in mess_obj:
		if obj.Iid.i_read == 0:
			uid_id.append(obj.Uid_id)
		# print(uid_id)
	uid_list = set(uid_id)
	# print(uid_list)
	uid_mess =[]
	# uid_dmess = []
	for id in uid_list:
		u_obj = Auth_user_emp_information.objects.filter(Uid_id=id,Eid=employee_obj)
		# print(u_obj)
		uid_mess.append(u_obj[0])
	context = {}  #定义返回对象
	# context['dmess'] = uid_dmess
	context['mess'] = uid_mess   # 中间表对象——页面遍历获取发送者和接受者以及消息内容
	return render(request,'chat.html',context)

from django.http import HttpResponse, JsonResponse

def show_mess(request,id):
	employee_obj = getSession(request)  # 获取当前用户对象
	u_obj = Auth_user_emp_information.objects.filter(Uid_id=id, Eid=employee_obj)
	u_list = []
	for u in u_obj:
		read = u.Iid.i_read
		i_id = u.Iid.id
		if read ==0:
			Information.objects.filter(id=i_id).update(i_read=1)
			u_list.append(u)
	context = {}
	context['per_usermess'] = u_list
	return render(request, 'aaa.html', context)




	# rows = dict(zip(range(len(mess_obj)),mess_obj))
	# rows.sort(key=lambda r: r['date'])
	# for date, items in groupby(rows, key=lambda r: r['date']):
	# 	print(date)
	# 	for i in items:



'''回复'''
def reply_user(request):   #id —— 传入用户的ID接收者
	try:
		id = int(request.POST.get('reply_content'))
	except:
		return redirect('/chat/')
	print(id,type(id))
	reply_mess = request.POST.get('msg-box')           # 获取回复内容
	reply_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())     #回复时间
	reply_obj = Reply.objects.create(r_talk=reply_mess,r_time = reply_time,r_read = 0)   #回复表添加数据
	employee_obj = getSession(request)   #回复者对象——当前客服对象
	# user_obj = Auth_user.objects.get(id = id ).id  #用户对象
	Auth_user_emp_reply.objects.create(Uid_id = id,Eid = employee_obj,Rid = reply_obj)  # 中间表数据添加
	context = {}  # 定义回显页面信息
	context['msg'] = reply_mess   #回显回复消息
	context['reply_obj'] = employee_obj  #客服对象
	return render(request,'chat.html',context)


#轮播图
def addbanner(request):
	if request.POST:
		file = request.FILES.get('picture_banner')   #获取文件对象
		try:
			filename = file.name     #获取文件名
		except:
			return redirect('/pic/')
		filetype = filename.split('.')[-1]
		alltype = ['jpg','png','jpeg','bmp','gif']
		if filetype not in alltype:
			return render(request,'gallery.html',{'msg':'图片格式不正确'})
		filepath = 'app_thrid/static/img/banner/'
		if not os.path.exists(filepath):
			os.makedirs(filepath)
		with open(filepath+filename,mode='wb')as f:
			for chunk in file.chunks():
				f.write(chunk)
		newfilepath = 'img/banner/' + filename
		Announcement.objects.create(banner = newfilepath)
		return HttpResponse('<script>location.href = "/pic/";</script>')
		pass
	else:
		try:
			banner = Announcement.objects.all().order_by('-id')
		except:
			return render(request,'gallery.html')
		paginator = Paginator(banner, 6)
		try:
			page = int(request.GET.get('page'))
		except:
			return redirect('/pic/?page=1')
		banner_list = paginator.page(page)
		context = {}
		context['banners'] = banner_list
		return render(request,'gallery.html',context)

def del_pic(request,id):
	pic_obj = Announcement.objects.filter(id=id)
	pic_obj.delete()
	return redirect('/pic/')

def news(request):
	new_obj = News.objects.all()
	paginator = Paginator(new_obj, 13)
	try:
		page = int(request.GET.get('page'))
	except:
		return redirect('/news/?page=1')
	news_list = paginator.page(page)
	context = {}
	context['paginator'] = paginator
	context['news_list'] = news_list
	return render(request,'news.html',context)

def add_news(request):
	if request.POST:
		title = request.POST.get('title_new')
		content = request.POST.get('content_news')
		time_add = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		news_obj = News.objects.create(title=title, content=content, ntime=time_add)
		return HttpResponse('<script>alert("添加成功");location.href = "/news/";</script>')
	else:
		return render(request,'add_news.html')

def update_news(request,id):
	if request.POST:
		title = request.POST.get('title_new')
		content = request.POST.get('content_news')
		time_add = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		news_obj = News.objects.filter(id=id).update(title=title,content =content,ntime=time_add)
		return HttpResponse('<script>alert("修改成功");location.href = "/news/";</script>')
		pass
	else:
		news_obj = News.objects.get(id = id)
		context = {}
		context['upd_obj'] = news_obj
		return render(request,'update_news.html',context)

def del_news(request,id):
	news_obj = News.objects.filter(id = id).delete()
	return redirect('/news/')


def log(request):
	u = request.user.username
	user_id = Emp.objects.get(username=u).id
	ip = request.META['REMOTE_ADDR']
	t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	Log.objects.create(time=t, operation=ip, Uid_id=user_id)

def show_log(request):
	log_list = Log.objects.all()
	paginator = Paginator(log_list, 3)
	try:
		page = int(request.GET.get('page'))
	except:
		return redirect('/show_login/?page=1')
	login_list = paginator.page(page)
	context = {}
	context['login_list'] = login_list
	return render(request,'log_manage.html',context)


def update_log(request,id):
	if request.POST:
		ip = request.POST.get('update_ip')
		# u = request.POST.get('update_user')
		t = request.POST.get('update_time')
		log_list = Log.objects.filter(id = id).update(time = t,operation = ip )
		return redirect('/show_login/')
		pass
	else:
		login_obj = Log.objects.get(id = id)
		context = {}
		context['login'] = login_obj
		return render(request,'update_log.html',context)

def del_login(request,id):
	Log.objects.filter(id = id).delete()
	return redirect('/show_login/')

def manage_creid(request):
	u = User_credit.objects.all()
	paginator = Paginator(u, 1)
	try:
		page = int(request.GET.get('page'))
	except:
		return redirect('/manage_creid/?page=1')
	all_credit = paginator.page(page)
	# for uid_obj in all_credit:
	# 	user_name = uid_obj.Uid.name
	# 	uid_id = uid_obj.Cid_id
	# 	usercobj = Credit_reporting.objects.get(id= uid_id)
	context = {}
	context['all_clist'] = all_credit
	return render(request,'managecred.html',context)

# def add_credit(request,id):
#
# 	return

def add_credit_b(request,id):
	obj = Blacklist.objects.filter(Uid_id=id )
	if obj.count()>0:
		return redirect('/manage_creid/')
	else:
		result = Blacklist.objects.create(Uid_id=id)
		u_id = User_credit.objects.filter(Uid_id=id)[0].Cid.id
		Credit_reporting.objects.filter(id=u_id).update(rate=0)
		return redirect('/manage_creid/')

def show_u(request,id):
	u = user_Product.objects.filter(Uid_id=id)
	u_obj = Laundry_list.objects.filter(Uid_id=id)

	context = {}
	context['users'] = u_obj
	context['pr']=u
	return render(request,'addcredit.html',context)

# def credit_user_show(request):
# 	all_user = Auth_user.objects.all()
# 	m_credit = User_credit.objects.all()
# 	for u in all_user:
# 		if u.name != 'null':
# 			for m in m_credit:
# 				if m.Uid_id != u.id:
# 					C = Credit_reporting.objects.create(c_credit = 0,higher = 0,overdue =0,three_parties = 0,rate = 80)
# 					User_credit.objects.create(Uid = u,Cid = C)
# 			return redirect('/pic/')













