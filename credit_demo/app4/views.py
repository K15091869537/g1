from django.shortcuts import render,redirect,HttpResponse
from app.models import Product,Auth_user,Laundry_list,Pays,Apply_progress,News,user_Product,Breaks,Coupons,user_coupons,Information,Emp,Auth_user_emp_information
from django.core.paginator import Paginator
import time,os,uuid
# Create your views here.
# 用户登录
def login1(request):
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        # 读取session
        result=request.session.get('username')
        print(result)
        # 如果存在,并且与输入名一致
        if result==username:
            # 获取用户
            auth_user=Auth_user.objects.get(account=username)
            id=auth_user.id
            print(id)
            return redirect('/userindex/{0}/'.format(id))
        # 否则
        else:
            try:
                print('表里有')
                # session里不存在，但表里有
                u=Auth_user.objects.get(account=username)
                # 重新写入session
                request.session['username'] = username
                id =u.id
                return redirect('/userindex/{0}/'.format(id))
            except:
                print('表里没有')
                # session里不存在，表里也没有
                # 写入数据表
                auth_user = Auth_user.objects.create(account=username, password=password)
                id = auth_user.id
                return redirect('/userindex/{0}/'.format(id))
    else:
        return render(request,'login1.html')

# 用户名唯一验证
def checkuser(request,username):
    # 获取所有用户
    alist=Auth_user.objects.all()
    # 获取用户名列表：
    userlist=[]
    # 遍历用户，得到用户名，写入列表中
    for user in alist:
        account=user.account
        userlist.append(account)
    print(userlist)
    # 判断用户名是否已存
    if username in userlist:
        return HttpResponse('flase')
    else:
        return HttpResponse('true')

# 用户进入主页
def userindex(request,id):
    if request.POST:
        sum_many=request.POST.get('sum_many')#贷款金额
        pays=request.POST.get('pays')#还款方式
        pid=Pays.objects.get(id=pays)#获取还款方式对象
        repaid=request.POST.get('repaid')#还款金额
        name=request.POST.get('name')#用户名
        tel=request.POST.get('tel')#用户电话
        submit=request.POST.get('submit')
        aid=Apply_progress.objects.get(id=5)   #模拟受理状态
        uid=Auth_user.objects.get(id=id) #用户对象
        username =uid.name  # 用户实名
        print(username)
        # 判断是否实名认证
        if username:
            # 还款时间
            repaid_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            # 分几次还款
            # if submit==1:
            # 写入流水，跳转到客服页面
            print(repaid_time)
            # 未还金额
            surplus=int(sum_many)-int(repaid)
            # 写入流水
            Laundry_list.objects.create(repaid=repaid,repaid_time=repaid_time,surplus=surplus,Aid=aid,Uid=uid,Pid=pid)
            # 提示一下
            return HttpResponse('<script>alert("还款成功");location.href="/userindex/{0}/"</script>'.format(id))
        # 一次性还清
        #     else:
        #         # 写入流水
        #         Laundry_list.objects.create(repaid=repaid, repaid_time=repaid_time, surplus=surplus, Aid=aid, Uid=uid,Pid=pid)
        else:
            # 跳转到申请信息补全
            return redirect('/userlogin/{0}/'.format(id))
        pass
    else:
        # 获取当前用户对象
        u=Auth_user.objects.get(id=id)
        # 得到员工对象
        emplist=Emp.objects.all()
        # 获取所有支付方式
        payslist=Pays.objects.all()
        # 获取产品信息
        productlist=Product.objects.all().order_by('id')[0:5]
        # 获取优惠券信息
        couponslist=Coupons.objects.all().order_by('id')[0:5]
        # 获取流水对象结果集，得未还金额
        laundrylist = Laundry_list.objects.filter(Uid=u)
        # 得结果集总个数，第一条写入的数据，最后一条写入的数据
        # print(laundrylist.count())
        # print(laundrylist.first())
        # print(laundrylist.last())
        # 得到用户最后一条写入还款流水
        surplus = laundrylist.last()
        try:
            # 获取用户对应的受理状态
            a = Apply_progress.objects.get(Uid=u)
            # 获取流水对象结果集，得未还金额
            laundrylist=Laundry_list.objects.filter(Uid=u)
            #得结果集总个数，第一条写入的数据，最后一条写入的数据
            # print(laundrylist.count())
            # print(laundrylist.first())
            # print(laundrylist.last())
            #得到用户最后一条写入还款流水
            surplus=laundrylist.last()
            print('无异常进入（有受理状态）')
            return render(request, 'userindex.html', {'productlist':productlist,'emplist':emplist, 'couponslist':couponslist,'payslist': payslist, 'u': u, 'a': a})
        except:
            print('异常进入（无受理状态）')
            return render(request, 'userindex.html', {'productlist': productlist,'emplist':emplist,'couponslist':couponslist, 'payslist': payslist, 'surplus':surplus,'u': u})

# 申请信息(补全信息)
def userlogin(request,id):
    if request.POST:
        name=request.POST.get('name')#实名
        card=request.POST.get('card')#身份证
        work=request.POST.get('work')#职业
        tel=request.POST.get('tel')#电话
        card_p=request.POST.get('card_p')#身份证正面
        card_r=request.POST.get('card_r')#身份证反面
        u_type=request.POST.get('u_type')#个人或企业
        company=request.POST.get('company')#公司名称
        credit_code=request.POST.get('credit_code')#统一社会信用代码
        if u_type==0:
            # 补全数据表数据
            Auth_user.objects.filter(id=id).update(name=name,card=card,work=work,tel=tel,card_z=card_purl,card_f=card_rurl,u_type=u_type)
            # 跳转到主页重新申请贷款
            return redirect('/userindex/{0}/'.format(id))
        else:
            Auth_user.objects.filter(id=id).update(name=name, card=card, work=work, tel=tel, card_z=card_purl,card_f=card_rurl, u_type=u_type,company=company,credit_code=credit_code,company_img=company_img)
            # 跳转到主页重新申请贷款
            return redirect('/userindex/{0}/'.format(id))
    else:
        auth_user=Auth_user.objects.get(id=id)
        return render(request, 'userlogin.html',{'auth_user':auth_user})

# 上传身份证正面
card_purl=''
def uploadcard_p(request):
    file=request.FILES.get('card_p')
    print(file)
    filename=file.name
    filetype=filename.split('.')[-1]
    # 放文件的文件夹
    cpath='app4/static/file'
    # 如果没有文件夹，创建
    if not os.path.exists(cpath):
        os.mkdir(cpath)
    # 文件路径
    global card_purl
    card_purl = '/static/file/' + str(uuid.uuid1())+'.'+filetype
    # 循环分块上传
    with open('app4'+card_purl,mode='wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    return HttpResponse(card_purl)

# 上传身份证反面
card_rurl=''
def uploadcard_r(request):
    file=request.FILES.get('card_r')
    print(file)
    filename=file.name
    filetype=filename.split('.')[-1]
    cpath='app/static/file'
    # 如果没有文件夹，创建
    if not os.path.exists(cpath):
        os.mkdir(cpath)
    # 文件路径
    global card_rurl
    card_rurl = '/static/file/'+ str(uuid.uuid1())+'.'+filetype
    # 循环分块写入
    with open('app4'+card_rurl,mode='wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    return HttpResponse(card_rurl)

# 上传公司证件
companyimgurl=''
def company_img(request):
    file=request.FILES.get('company_img')
    print(file)
    filename=file.name
    filetype=filename.split('.')[-1]
    cpath='app/static/file'
    # 如果没有文件夹，创建
    if not os.path.exists(cpath):
        os.mkdir(cpath)
    # 文件路径
    global companyimgurl
    companyimgurl = '/static/file/'+ str(uuid.uuid1())+'.'+filetype
    # 循环分块写入
    with open('app4'+companyimgurl,mode='wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    return HttpResponse(companyimgurl)

# 用户进入个人详情页
def userdeta(request,id):
    # 获取用户对象
    u=Auth_user.objects.get(id=id)
    # 通过中间表，获取用户对应的产品
    plist=user_Product.objects.filter(Uid=u)
    return render(request,'userdeta.html',{'u':u,'plist':plist})

# 申请减免
def breaks1(request,id):
    # 获取用户对象u
    u = Auth_user.objects.get(id=id)
    # 通过中间表，获取用户对应的产品
    plist = user_Product.objects.filter(Uid=u)
    l = Laundry_list.objects.filter(Uid=u).first()  # 取第一条流水表对象
    print(l)
    if request.POST:
        # 获取减免理由
        b1=request.POST.get('breaks')
        print(b1)
        # 通过用户对象获取流水，再获取减免,判断其是否申请过减免
        b = Breaks.objects.filter(Lid=l)
        print(b)
        # 申请过，不可再申请
        if b:
            return HttpResponse('<script>alert("亲，不要重复申请哦");location.href="/userindex/{0}/";</script>'.format(id))
        # Breaks.objects.get(Lid=l).update(delay=1, d_reason=delay,d_through=0)
        else:
            # 没申请过，写入到减免展期表中
            Breaks.objects.create(breaks=0, b_reason=b1, b_through=0, delay=1, d_reason=0, d_through=0, Lid=l)
            print('no')
            return HttpResponse('<script>alert("申请成功");location.href="/userindex/{0}/";</script>'.format(id))
        pass
    else:
        return render(request,'breaks1.html',{'u':u,'plist':plist})

# 申请展期
def delay1(request, id):
    # 获取用户对象u
    u = Auth_user.objects.get(id=id)
    # 通过中间表，获取用户对应的产品
    plist = user_Product.objects.filter(Uid=u)
    print(plist)
    l = Laundry_list.objects.filter(Uid=u).first()  # 取第一条流水表对象
    print(l)
    if request.POST:
        # 获取展期理由
        d1 = request.POST.get('delay')
        print(d1)
        # 通过用户对象获取流水，再获取减免,判断其是否申请过减免
        b = Breaks.objects.filter(Lid=l)
        print(b)
        # 申请过，不可再申请
        if b:
            return HttpResponse('<script>alert("亲，不要重复申请哦");location.href="/userindex/{0}/";</script>'.format(id))
        else:
            # 没申请过，写入到减免展期表中
            Breaks.objects.create(breaks=0, b_reason=0, b_through=0, delay=1, d_reason=d1,d_through=0, Lid=l)
            print('no')
            return HttpResponse('<script>alert("申请成功");location.href="/userindex/{0}/";</script>'.format(id))
    else:
        return render(request, 'delay.html', {'u': u, 'plist': plist})

# 用户进入申请贷款,带用户ID，带产品ID
#模拟客服实时确认
def apply(request,id,pid):
    # 获取用户对象，产品对象
    u = Auth_user.objects.get(id=id)
    p = Product.objects.get(id=pid)
    # 通过用户获取优惠券
    uclist=user_coupons.objects.filter(Uid=u)
    if request.POST:
        # 将用户对象与产品对象添加到中间表
        uptime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        user_Product.objects.create(up_time=uptime,Uid=u,Pid=p)
        # 添加受理状态
        Apply_progress.objects.create(apply=1,audit=0,approval=0,grant=0,Pid=p,lendtime=uptime,yq=0,Uid=u)
        # 获取优惠券使用情况
        ra = int(request.POST.get('ra'))
        if ra==1:
            # 使用优惠券，更改中间表
            user_coupons.objects.filter(Uid=u).update(state=1)
        # 跳转到主页面
        return redirect('/userindex/{0}/'.format(id))
    else:
        username = u.name  # 用户实名
        # 判断是否实名，实名才可申请
        if username:
            return render(request,'apply.html',{'u':u,'p':p,'uclist':uclist})
        else:
            return HttpResponse('<script>alert("信息不全，请补全信息");location.href="/userlogin/{0}/"</script>'.format(id))

# 将用户与优惠券关联
def addcoupons(request,id,cid):
    # 获取用户对象，优惠券对象
    u = Auth_user.objects.get(id=id)
    c = Coupons.objects.get(id=cid)
    user_coupons.objects.create(state=0,Cid=c,Uid=u)
    return HttpResponse('<script>alert("恭喜领劵成功");location.href="/userindex/{0}/"</script>'.format(id))


# 用户进入新闻展示页，并设置分页,可以实现简单的搜索功能
def blog(request,id):
    if request.POST:
        # 获取搜索对象
        q = request.POST.get('q')
        newslist = News.objects.filter(title__icontains=q).order_by('id')
        return render(request, 'blog.html', {'newslist': newslist})
        pass
    else:
        # 获取所有新闻
        newslist=News.objects.all().order_by('id')
        # 建立分页器对象，设置每页3条
        pr=Paginator(newslist,2)
        # 接收客户端传递的页数
        page=request.GET.get('page')
        if page is None:
            page=1 #若无值，则给1
        # 将页数传给分页对象，获取内容
        newlist1=pr.get_page(page)
        # 获取当前登录用户
        u=Auth_user.objects.get(id=id)
        return render(request,'blog.html',{'newslist':newlist1,'u':u})

# 进入新闻回复页
def blog_details(request,id,nid):
    # 获取用户对象
    u = Auth_user.objects.get(id=id)
    # 获取新闻对象
    n=News.objects.get(id=nid)
    return render(request,'blog-details.html',{'u':u})

# 消息页
def contact(request,id,eid):
    # 获取用户对象
    u = Auth_user.objects.get(id=id)
    # 获取员工对象
    e = Emp.objects.get(id=eid)
    aeilist=Auth_user_emp_information.objects.filter(Uid=u,Eid=e)
    print(aeilist)
    if request.POST:
        # 接收信息内容
        i_talk=request.POST.get('i_talk')
        # 发信时间
        i_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # 写入信息表
        i=Information.objects.create(i_talk=i_talk,i_time=i_time,i_read=0)
        # 写入信息中间表
        Auth_user_emp_information.objects.create(Uid=u,Eid=e,Iid=i)
        return HttpResponse('<script>alert("信息发送成功");location.href="/userindex/{0}/"</script>'.format(id))
    else:
        return render(request,'contact.html',{'u':u,'e':e,'aeilist':aeilist})