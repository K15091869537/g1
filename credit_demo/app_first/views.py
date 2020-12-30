from django.shortcuts import render,HttpResponse,redirect
# 导入登录/登出模块
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import Auth_user
import xlwt,os,uuid,time,datetime
# 导入分页器对象
from django.core.paginator import Paginator
# 导入员工表
from app.models import Emp,Job,Apply_progress,user_Product,Breaks,Product,Product_type
# Create your views here.
@login_required(login_url='/login/')
def index(request):
    grant_money = 0
    orders_money = 0
    # 待审核数
    audit_no = Apply_progress.objects.filter(audit=0).count()
    # 已经审核数量
    audit_pass = Apply_progress.objects.filter(audit=1).count()
    # 待放款数
    grant_no = Apply_progress.objects.filter(grant=0, approval=1).count()
    # 已放款
    grant_pass = Apply_progress.objects.filter(grant=1, approval=1).count()
    # 已逾期
    yq = Apply_progress.objects.filter(yq=1).count()
    # 已经结算清楚
    # ok =
    # 需催收的订单
    ll = Laundry_list.objects.all().count()
    # 累计用户
    user = Auth_user.objects.all().count()
    # 累计申请订单
    orders = Apply_progress.objects.all().count()
    # 累计放款金额
    grant_list = Apply_progress.objects.filter(grant=1, approval=1)
    for g in grant_list:
        grant_money += g.Pid.range
    # 累计通过订单金额
    for m in Apply_progress.objects.filter(grant=0, approval=1):
        orders_money += m.Pid.range
    context = {}
    context['audit_pass'] = audit_pass
    context['audit_no'] = audit_no
    context['grant_no'] = grant_no
    context['grant_pass'] = grant_pass
    context['yq'] = yq
    context['ll'] = ll
    context['au'] = user
    context['orders'] = orders
    context['grant_money'] = grant_money
    context['orders_money'] = orders_money + grant_money
    return render(request, 'index.html', context)

# 新员工初始化信息
@login_required(login_url='/login/')
def newemp(request):
    if request.POST:
        name = request.POST.get('name')
        password =request.POST.get('password')
        worknum = time.strftime('%Y%m%d%H%M%S',time.localtime())
        emp = Emp.objects.create(username=name,password=password,work_num=worknum,Uid_id=1,e_work_id=1)
        emp.set_password(password)
        emp.save()
        return redirect('/index/')
    else:
        return render(request,'newemp.html')

# 登录
from app_thrid.views import log

def gologin(request):
    if request.POST:
        name = request.POST.get('name')
        password =request.POST.get('password')
        empobj = authenticate(username=name, password=password)
        # 读取数据库
        # 判断账号是否存在
        if empobj:
            # 写入session
            login(request,empobj)
            # log(request)
            return redirect('/index/')
        else:
            return render(request,'login.html',{'error':'账号或密码错误'})
    else:
        return render(request,'login.html')

# 修改个人信息
@login_required(login_url='/login/')
def updatamesage(request):
    if request.POST:
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        emp = authenticate(password=oldpassword,username=request.user.username)
        if emp:
            emp.set_password(newpassword)
            emp.save()
            return redirect('/login/')
        else:
            return render(request,'updata.html',{'msg':'旧密码输入不正确'})
    else:
        return render(request,'updata.html')

# 部门人员管理
@login_required(login_url='/login/')
def administration(request):
    emp = Emp.objects.all()
    page_num = 15
    pr = Paginator(emp, page_num)
    # 接收客户端传递的页数
    page = request.GET.get('page')
    # 判断页码是否存在
    if page is None:
        page = 1
    # 将页数传递给分页对象获取内容响应客户端
    emp = pr.get_page(page)
    return render(request,'administration.html',{'emp':emp})

# 添加员工
@login_required(login_url='/login/')
def addemp(request):
    if request.POST:
        username = request.POST.get('name')
        empnum = request.POST.get('job_num')
        empjob = request.POST.get('job')
        # 查询职位对应的id
        jid = Job.objects.get(Job_name=empjob).id
        # 存入姓名和编号
        Emp.objects.create(username=username,work_num=empnum,e_work_id=jid,Uid_id=1)
        return redirect('/administration/')
    else:
        empjob = Job.objects.all()
        return render(request,'addemp.html',{'empjob':empjob})
# 修改员工信息
@login_required(login_url='/login/')
def updateemp(request,id):
    if request.POST:
        empnum = request.POST.get('job_num')
        empjob = request.POST.get('job')
        # 查询职位对应的id
        jid = Job.objects.get(Job_name=empjob).id
        # 存入姓名和编号
        Emp.objects.filter(id=id).update(work_num=empnum, e_work_id=jid)
        return redirect('/administration/')
        pass
    else:
        empobj = Emp.objects.filter(id=id)
        empjob = Job.objects.all()
        return render(request,'updateemp.html',{'empobj':empobj,'empjob':empjob})

# 删除员工
@login_required(login_url='/login/')
def daleemp(request,id):
    Emp.objects.filter(id=id).delete()
    return redirect('/administration/')

# 退出登录
def exit(request):
    logout(request)
    return redirect('/index/')

from app.models import Laundry_list
# 财务资金管理--三方支付流水
@login_required(login_url='/login/')
def thirdpay(request):
    payobj = Laundry_list.objects.all()
    # 建立分页器对象设定每页条数
    page_num = 15
    pr = Paginator(payobj, page_num)
    # 接收客户端传递的页数
    page = request.GET.get('page')
    # 判断页码是否存在
    if page is None:
        page = 1
    # 将页数传递给分页对象获取内容响应客户端
    payobj = pr.get_page(page)
    return render(request,'thirdpay.html',{'payobj':payobj})
# 现金支付
@login_required(login_url='/login/')
def cashpay(request):
    payobj = Laundry_list.objects.all()
    list_data = []
    for pay in payobj:
        list=[]
        if pay.Pid.pay_way == '现金':
            list.append(pay)
            list_data.append(list)
    # 建立分页器对象设定每页条数
    page_num = 15
    pr = Paginator(list_data, page_num)
    # 接收客户端传递的页数
    page = request.GET.get('page')
    # 判断页码是否存在
    if page is None:
        page = 1
    # 将页数传递给分页对象获取内容响应客户端
    list_data = pr.get_page(page)
    return render(request,'cashpay.html',{'list_data':list_data})
# 封装文件写入excel
def toexcel(filename,header,list_data):
    # 写入excel
    path = 'app_first/static/xls/' + filename
    wk = xlwt.Workbook(encoding='utf-8')
    sheet = wk.add_sheet('sheet1')
    for i in range(len(header)):
        sheet.write(0, i, header[i])
    for row in range(1, len(list_data) + 1):
        for col in range(len(header)):
            sheet.write(row, col, list_data[row - 1][col])
    wk.save(path)
    with open(path, mode='rb') as f:
        content = f.read()
    # 删除文件
    os.remove(path)
    return content
# excel导出功能
@login_required(login_url='/login/')
def downloadexcel(request,filename):
    payobj = Laundry_list.objects.all()
    header =['用户姓名','贷款日期','贷款金额','还款日期','还款金额','应还金额','支付方式']
    list_data =[]
    for pay in payobj:
        list =[]
        username = pay.Uid.name
        p_date = pay.Aid.lendtime.strftime('%Y-%m-%d %H:%M:%S')
        p_money = pay.Aid.Pid.range
        h_date = pay.repaid_time.strftime('%Y-%m-%d %H:%M:%S')
        h_money = pay.repaid
        money = pay.surplus
        pay_type = pay.Pid.pay_way
        list.append(username)
        list.append(p_date)
        list.append(p_money)
        list.append(h_date)
        list.append(h_money)
        list.append(money)
        list.append(pay_type)
        list_data.append(list)
    # print(list_data)
    # 写入excel
    content = toexcel(filename,header,list_data)
    return HttpResponse(content,content_type=True)

# 现金流导出
@login_required(login_url='/login/')
def carshload(request,filename):
    payobj = Laundry_list.objects.all()
    header =['用户姓名','贷款日期','贷款金额','还款日期','还款金额','应还金额','支付方式']
    list_data =[]
    for pay in payobj:
        list = []
        if pay.Pid.pay_way == '现金':
            username = pay.Uid.name
            p_date = pay.time.strftime('%Y-%m-%d %H:%M:%S')
            p_money = pay.sum_money
            h_date = pay.repaid_time.strftime('%Y-%m-%d %H:%M:%S')
            h_money = pay.repaid
            money = pay.surplus
            pay_type = pay.Pid.pay_way
            list.append(username)
            list.append(p_date)
            list.append(p_money)
            list.append(h_date)
            list.append(h_money)
            list.append(money)
            list.append(pay_type)
            list_data.append(list)
    # print(list_data)
    # 写入excel
    content = toexcel(filename, header, list_data)
    return HttpResponse(content,content_type=True)

# 客户还款台账
@login_required(login_url='/login/')
def repayment(request):
    Lobj = Laundry_list.objects.all()
    # 对查询到的数据进行分页
    # 建立分页器对象设定每页条数
    page_num = 15
    pr = Paginator(Lobj, page_num)
    # 接收客户端传递的页数
    page = request.GET.get('page')
    # 判断页码是否存在
    if page is None:
        page = 1
    # 将页数传递给分页对象获取内容响应客户端
    Lobj = pr.get_page(page)
    return render(request, 'repayment.html', {'Lobj': Lobj})

# 客户还款台账数据导出
@login_required(login_url='/login/')
def taizhang(request,filename):
    payobj = Laundry_list.objects.all()
    header = ['用户姓名', '贷款金额', '还款金额', '待还金额']
    list_data = []
    for pay in payobj:
        list = []
        username = pay.Uid.name
        p_money = pay.Aid.Pid.range
        h_money = pay.repaid
        money = pay.surplus
        list.append(username)
        list.append(p_money)
        list.append(h_money)
        list.append(money)
        list_data.append(list)
    # print(list_data)
    content = toexcel(filename, header, list_data)
    return HttpResponse(content, content_type=True)

# 未放款台账
@login_required(login_url='/login/')
def unpaid(request):
    # 查询受理状态数据
    apply = Apply_progress.objects.all()
    # 查询用户产品中间表，获取申请时间
    # uplist = user_Product.objects.all()
    page_num = 15
    pr = Paginator(apply, page_num)
    # 接收客户端传递的页数
    page = request.GET.get('page')
    # 判断页码是否存在
    if page is None:
        page = 1
    # 将页数传递给分页对象获取内容响应客户端
    apply = pr.get_page(page)
    return render(request,'unpaid.html',{'apply':apply})
# 未放款数据导出

def unpaidtoexcel(request,filename):
    payobj = Laundry_list.objects.all()
    header = ['用户姓名', '未放款金额']
    list_data = []
    for pay in payobj:
        list = []
        username = pay.Uid.name
        unpaidmoney = pay.Pid.range
        list.append(username)
        list.append(unpaidmoney)
        list_data.append(list)
    # print(list_data)
    content = toexcel(filename, header, list_data)
    return HttpResponse(content, content_type=True)

# 全部放款台账
@login_required(login_url='/login/')
def allpaid(request):
    lobj = Laundry_list.objects.all()
    apply = Apply_progress.objects.all()
    # 查询用户产品中间表，获取申请时间
    # uplist = user_Product.objects.all()
    page_num = 15
    pr = Paginator(lobj, page_num)
    # 接收客户端传递的页数
    page = request.GET.get('page')
    # 判断页码是否存在
    if page is None:
        page = 1
    # 将页数传递给分页对象获取内容响应客户端
    lobj = pr.get_page(page)
    return render(request,'allpaid.html',{'lobj':lobj})

# 全部放款台账数据导出
def allpaidtoexcel(request,filename):
    # 流水表对象
    lobj = Laundry_list.objects.all()
    header = ['用户姓名', '放款金额','放款时间','还款时间']
    list_data = []
    for all in lobj:
        list = []
        username = all.Uid.name
        paidmoney = all.Aid.Pid.range
        # 放款时间
        paidtime = all.Aid.lendtime
        # 还款时间
        paytime = all.repaid_time
        list.append(username)
        list.append(paidmoney)
        list.append(paidtime)
        list.append(paytime)
        list_data.append(list)
    # print(list_data)
    content = toexcel(filename, header, list_data)
    return HttpResponse(content, content_type=True)

# 催收池
@login_required(login_url='/login/')
def collection(request):
    colobj = Laundry_list.objects.all()
    nowtime = time.time()
    collist = []
    for c in colobj:
        list =[]
        t =str(c.repaid_time).split('+')[0]
        # 获取还款时间转化为时间戳
        t = time.mktime(time.strptime(t,'%Y-%m-%d %X'))
        coltime =int((nowtime - t)/60/60/24)
        if coltime > 0:
            list.append(c)
            list.append(coltime)
            collist.append(list)
    page_num = 15
    pr = Paginator(collist, page_num)
    # 接收客户端传递的页数
    page = request.GET.get('page')
    # 判断页码是否存在
    if page is None:
        page = 1
    # 将页数传递给分页对象获取内容响应客户端
    collist = pr.get_page(page)
    return render(request,'allcollection.html',{'collist':collist})

# 催收导出
def collectiontoexcel(request,filename):
    colobj = Laundry_list.objects.all()
    header = ['用户姓名', '应还金额', '应还款时间', '拖欠时长(天)']
    nowtime = time.time()
    list_data = []
    for c in colobj:
        list = []
        t = str(c.repaid_time).split('+')[0]
        # 获取还款时间转化为时间戳
        t = time.mktime(time.strptime(t, '%Y-%m-%d %X'))
        coltime = int((nowtime - t) / 60 / 60 / 24)
        if coltime > 0:
            ctime = c.repaid_time.strftime('%Y-%m-%d %H:%M:%S')
            list.append(c.Uid.name)
            list.append(c.surplus)
            list.append(ctime)
            list.append(coltime)
            list_data.append(list)
    content = toexcel(filename, header, list_data)
    return HttpResponse(content, content_type=True)

# 催收业务处理
@login_required(login_url='/login/')
def collectionwork(request):
    colobj = Laundry_list.objects.all()
    nowtime = time.time()
    collist = []
    for c in colobj:
        list = []
        t = str(c.repaid_time).split('+')[0]
        # 获取还款时间转化为时间戳
        t = time.mktime(time.strptime(t, '%Y-%m-%d %X'))
        coltime = int((nowtime - t) / 60 / 60 / 24)
        if 0<coltime <=7 and c.surplus > 0:
            list.append(c)
            list.append(coltime)
            collist.append(list)
    page_num = 15
    pr = Paginator(collist, page_num)
    # 接收客户端传递的页数
    page = request.GET.get('page')
    # 判断页码是否存在
    if page is None:
        page = 1
    # 将页数传递给分页对象获取内容响应客户端
    collist = pr.get_page(page)
    return render(request, 'collectionwork.html', {'collist': collist})
@login_required(login_url='/login/')
def collectionwork2(request):
    colobj = Laundry_list.objects.all()
    nowtime = time.time()
    collist = []
    for c in colobj:
        list = []
        t = str(c.repaid_time).split('+')[0]
        # 获取还款时间转化为时间戳
        t = time.mktime(time.strptime(t, '%Y-%m-%d %X'))
        coltime = int((nowtime - t) / 60 / 60 / 24)

        if 7<coltime < 30 and c.surplus > 0:
            list.append(c)
            list.append(coltime)
            collist.append(list)
    page_num = 15
    pr = Paginator(collist, page_num)
    # 接收客户端传递的页数
    page = request.GET.get('page')
    # 判断页码是否存在
    if page is None:
        page = 1
    # 将页数传递给分页对象获取内容响应客户端
    collist = pr.get_page(page)
    return render(request, 'collectionwork2.html', {'collist': collist})
@login_required(login_url='/login/')
def collectionwork3(request):
    colobj = Laundry_list.objects.all()
    nowtime = time.time()
    collist = []
    for c in colobj:
        list = []
        t = str(c.repaid_time).split('+')[0]
        # 获取还款时间转化为时间戳
        t = time.mktime(time.strptime(t, '%Y-%m-%d %X'))
        coltime = int((nowtime - t) / 60 / 60 / 24)
        if coltime >= 30 and c.surplus > 0:
            list.append(c)
            list.append(coltime)
            collist.append(list)
    page_num = 15
    pr = Paginator(collist, page_num)
    # 接收客户端传递的页数
    page = request.GET.get('page')
    # 判断页码是否存在
    if page is None:
        page = 1
    # 将页数传递给分页对象获取内容响应客户端
    collist = pr.get_page(page)
    return render(request, 'collectionwork3.html', {'collist': collist})

# 封装函数导出催收数据
def function(a,b,interest,d):
    colobj = Laundry_list.objects.all()
    nowtime = time.time()
    list_data = []
    for c in colobj:
        list = []
        t = str(c.repaid_time).split('+')[0]
        # 获取还款时间转化为时间戳
        t = time.mktime(time.strptime(t, '%Y-%m-%d %X'))
        coltime = int((nowtime - t) / 60 / 60 / 24)
        if a < coltime <= b and c.surplus > 0:
            name = c.Uid.name
            list.append(name)
            # 拖欠金额
            sur = c.surplus
            list.append(sur)
            # 利率
            list.append(interest)
            # 待还金额
            will = sur * (1 + interest)*coltime
            list.append(will)
            # 拖欠时间
            list.append(coltime)
            # 催款状态
            list.append(d)
            list_data.append(list)
    header = ['用户姓名', '欠款金额', '还款利率', '待还金额', '拖欠时长(天)', '催款状态']
    return header,list_data
# 催收业务处理（7天以内）
@login_required(login_url='/login/')
def collectionsev(request,filename):
    header, list_data = function(0,7,0.03,'电话提醒')
    content = toexcel(filename, header, list_data)
    return HttpResponse(content, content_type=True)
# 催收业务处理（7-30天以）
@login_required(login_url='/login/')
def collectionsevto(request,filename):
    header, list_data = function(7,30,0.05,'电话催款')
    content = toexcel(filename, header, list_data)
    return HttpResponse(content, content_type=True)
# 催收业务处理（30天以上）
@login_required(login_url='/login/')
def collectionthan(request,filename):
    header, list_data = function(30,300,0.1,'上门催款')
    content = toexcel(filename, header, list_data)
    return HttpResponse(content, content_type=True)

# 申请减免
@login_required(login_url='/login/')
def userbreak(request):
    breaks = Breaks.objects.all()
    page_num = 15
    pr = Paginator(breaks, page_num)
    # 接收客户端传递的页数
    page = request.GET.get('page')
    # 判断页码是否存在
    if page is None:
        page = 1
    # 将页数传递给分页对象获取内容响应客户端
    breaks = pr.get_page(page)
    return render(request,'breaks.html',{'breaks':breaks})
# 通过减免申请，修改数据表
@login_required(login_url='/login/')
def throuthuser(request,id):
    Breaks.objects.filter(id=id).update(b_through=1)
    return HttpResponse('通过申请')
# 拒绝申请
@login_required(login_url='/login/')
def refuseuser(request,id):
    Breaks.objects.filter(id=id).update(b_through=2)
    return HttpResponse('拒绝申请')
# 减免处理清单
@login_required(login_url='/login/')
def breaklist(request):
    breaks = Breaks.objects.all()
    page_num = 15
    pr = Paginator(breaks, page_num)
    # 接收客户端传递的页数
    page = request.GET.get('page')
    # 判断页码是否存在
    if page is None:
        page = 1
    # 将页数传递给分页对象获取内容响应客户端
    breaks = pr.get_page(page)
    return render(request,'breaklist.html',{'breaks':breaks})

# 申请展期处理
def userdelay(request):
    breaks = Breaks.objects.all()
    page_num = 15
    pr = Paginator(breaks, page_num)
    # 接收客户端传递的页数
    page = request.GET.get('page')
    # 判断页码是否存在
    if page is None:
        page = 1
    # 将页数传递给分页对象获取内容响应客户端
    breaks = pr.get_page(page)
    return render(request, 'userdelay.html', {'breaks': breaks})
# 通过展期申请，还款时间延后30天，更改字段和还款时间
def delay(request,id):
    Breaks.objects.filter(id=id).update(d_through=1)
    # 修改还款时间
    ytime = str(Breaks.objects.get(id=id).Lid.repaid_time).split('+')[0]
    print('------------------',ytime)
    # 展期时长30天
    # 获取还款时间转化为时间戳
    ptime = time.mktime(time.strptime(ytime, '%Y-%m-%d %X'))
    # 计算展期30天
    p = ptime+30*24*60*60
    # 将时间戳转化为时间格式
    timeArray = time.localtime(p)
    paytime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print('===========',paytime)
    # 展期后时间字段写入流水表
    lid = Breaks.objects.get(id=id).Lid_id
    Laundry_list.objects.filter(id=lid).update(repaid_time=paytime)
    return HttpResponse('通过申请')
# 拒绝申请

def undelay(request,id):
    Breaks.objects.filter(id=id).update(d_through=2)
    return HttpResponse('拒绝申请')
# 减免处理清单
@login_required(login_url='/login/')
def delaylist(request):
    breaks = Breaks.objects.all()
    page_num = 15
    pr = Paginator(breaks, page_num)
    # 接收客户端传递的页数
    page = request.GET.get('page')
    # 判断页码是否存在
    if page is None:
        page = 1
    # 将页数传递给分页对象获取内容响应客户端
    breaks = pr.get_page(page)
    return render(request,'delaylist.html',{'breaks':breaks})

# 产品配置
@login_required(login_url='/login/')
def inproduct(request):
    if request.POST:
        # 获取产品信息
        p_name = request.POST.get('p_name')
        content = request.POST.get('content')
        protype = request.POST.get('protype')
        range = request.POST.get('range')
        date = request.POST.get('date')
        rate = request.POST.get('rate')
        statdate = request.POST.get('statdate')
        stopdate = request.POST.get('stopdate')
        # 办理期限
        permanent = request.POST.get('permanent')
        # 办理状态
        nowtime = time.time()
        statdate1 = time.mktime(time.strptime(statdate, '%Y-%m-%d %X'))
        stopdate1 = time.mktime(time.strptime(stopdate, '%Y-%m-%d %X'))
        if statdate1< nowtime < stopdate1:
            active = 1
        else:
            active = 0
        # 产品类型编号
        tid = Product_type.objects.get(p_type=protype).id
        Product.objects.create(p_name=p_name,introduc=content,Tid_id=tid,range=range,date=date,rate=rate,active=active,start=statdate,stop=stopdate,permanent=permanent)
        return redirect('/inproduct/')
    else:
        protype = Product_type.objects.all()
        return render(request,'inproduct.html',{'protype':protype})

# 产品详细信息
def inforproduct(request):
    product = Product.objects.all()
    page_num = 15
    pr = Paginator(product, page_num)
    # 接收客户端传递的页数
    page = request.GET.get('page')
    # 判断页码是否存在
    if page is None:
        page = 1
    # 将页数传递给分页对象获取内容响应客户端
    product = pr.get_page(page)
    return render(request,'inforproduct.html',{'product':product})

