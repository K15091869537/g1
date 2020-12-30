import time
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from app.models import Auth_user,Apply_progress,Laundry_list,user_Product,Emp,Coupons,Coupons_type,user_coupons,Blacklist
# Create your views here.
def index(request):
    return render(request,'index.html')

#-------------------------------------业务查询功能（开始）---------------------------------------------
#全部业务查询
def showBusiness(request):
    userlists = Auth_user.objects.all()#获取所有用户
    applylist = Apply_progress.objects.all()#获取受理状态
    laundrylist = Laundry_list.objects.all()#获取流水表
    productlist = user_Product.objects.all()#获取产品
    paginator1 = Paginator(applylist, 15)
    # 接受客户端传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/showBusiness/?page=1')
    # 将页数传递给分页对象获取内容响应客户端
    applylist = paginator1.page(page)
    context = {}
    context['userlists'] = userlists#获取所有用户
    context['applylists'] = applylist#获取受理状态
    context['laundrylists'] = laundrylist#获取流水表
    context['productlists'] = productlist#获取产品
    return render(request,'showBusiness.html',context)

#申请业务查询
def showApply(request):
    userlists = Auth_user.objects.all()  # 获取所有用户
    applylist = Apply_progress.objects.all()  # 获取受理状态
    laundrylist = Laundry_list.objects.all()  # 获取流水表
    productlist = user_Product.objects.all()  # 获取产品
    applys = []
    for i in applylist:
        if i.grant != 1 :
            if i.audit != 2 and i.approval != 2:
                applys.append(i)
    paginator1 = Paginator(applys, 15)
    # 接受客户端传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/showApply/?page=1')
    # 将页数传递给分页对象获取内容响应客户端
    applys = paginator1.page(page)
    context = {}
    context['userlists'] = userlists  # 获取所有用户
    context['applylists'] = applys  # 获取受理状态
    context['laundrylists'] = laundrylist  # 获取流水表
    context['productlists'] = productlist  # 获取产品
    return render(request,'showApply.html', context)

#审核业务查询
def showAudit(request):
    userlists = Auth_user.objects.all()  # 获取所有用户
    applylist = Apply_progress.objects.all()  # 获取受理状态
    laundrylist = Laundry_list.objects.all()  # 获取流水表
    productlist = user_Product.objects.all()  # 获取产品
    applys = []
    for i in applylist:
        if i.apply == 1 and i.approval == 0:
            if i.audit != 2 and i.approval != 2:
                applys.append(i)
    paginator1 = Paginator(applys, 15)
    # 接受客户端传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/showAudit/?page=1')
    # 将页数传递给分页对象获取内容响应客户端
    applys = paginator1.page(page)
    context = {}
    context['userlists'] = userlists  # 获取所有用户
    context['applylists'] = applys  # 获取受理状态
    context['laundrylists'] = laundrylist  # 获取流水表
    context['productlists'] = productlist  # 获取产品
    return render(request,'showAudit.html', context)

#通过业务查询
def showThrough(request):
    userlists = Auth_user.objects.all()  # 获取所有用户
    applylist = Apply_progress.objects.all()  # 获取受理状态
    laundrylist = Laundry_list.objects.all()  # 获取流水表
    productlist = user_Product.objects.all()  # 获取产品
    applys = []
    for i in applylist:
        if i.approval == 1 :
            applys.append(i)
    paginator1 = Paginator(applys, 15)
    # 接受客户端传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/showThrough/?page=1')
    # 将页数传递给分页对象获取内容响应客户端
    applys = paginator1.page(page)
    context = {}
    context['userlists'] = userlists  # 获取所有用户
    context['applylists'] = applys  # 获取受理状态
    context['laundrylists'] = laundrylist  # 获取流水表
    context['productlists'] = productlist  # 获取产品
    return render(request,'showThrough.html',context)

#拒绝业务查询
def showRefused(request):
    userlists = Auth_user.objects.all()  # 获取所有用户
    applylist = Apply_progress.objects.all()  # 获取受理状态
    laundrylist = Laundry_list.objects.all()  # 获取流水表
    productlist = user_Product.objects.all()  # 获取产品
    applys = []
    for i in applylist:
        if i.approval == 2 or i.audit == 2:
            applys.append(i)
    paginator1 = Paginator(applys, 15)
    # 接受客户端传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/showRefused/?page=1')
    # 将页数传递给分页对象获取内容响应客户端
    applys = paginator1.page(page)
    context = {}
    context['userlists'] = userlists  # 获取所有用户
    context['applylists'] = applys  # 获取受理状态
    context['laundrylists'] = laundrylist  # 获取流水表
    context['productlists'] = productlist  # 获取产品
    return render(request,'showRefused.html',context)

#放款业务查询
def showLending(request):
    userlists = Auth_user.objects.all()  # 获取所有用户
    applylist = Apply_progress.objects.all()  # 获取受理状态
    laundrylist = Laundry_list.objects.all()  # 获取流水表
    productlist = user_Product.objects.all()  # 获取产品
    applys = []
    for i in applylist:
        if i.approval == 1 and i.grant == 0:
            applys.append(i)
    paginator1 = Paginator(applys, 15)
    # 接受客户端传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/showLending/?page=1')
    # 将页数传递给分页对象获取内容响应客户端
    applys = paginator1.page(page)
    context = {}
    context['userlists'] = userlists  # 获取所有用户
    context['applylists'] = applys  # 获取受理状态
    context['laundrylists'] = laundrylist  # 获取流水表
    context['productlists'] = productlist  # 获取产品
    return render(request,'showLending.html',context)

#还款业务查询
def showAlso(request):
    userlists = Auth_user.objects.all()  # 获取所有用户
    applylist = Apply_progress.objects.all()  # 获取受理状态
    laundrylist = Laundry_list.objects.all()  # 获取流水表
    productlist = user_Product.objects.all()  # 获取产品
    laundry = []
    for i in laundrylist:
        if i.surplus != 0:
            laundry.append(i)
    paginator1 = Paginator(laundry, 15)
    # 接受客户端传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/showAlso/?page=1')
    # 将页数传递给分页对象获取内容响应客户端
    laundry = paginator1.page(page)
    context = {}
    context['userlists'] = userlists  # 获取所有用户
    context['applylists'] = applylist  # 获取受理状态
    context['laundrylists'] = laundry  # 获取流水表
    context['productlists'] = productlist  # 获取产品
    return render(request,'showAlso.html',context)

#结清业务查询
def showSettlement(request):
    userlists = Auth_user.objects.all()  # 获取所有用户
    applylist = Apply_progress.objects.all()  # 获取受理状态
    laundrylist = Laundry_list.objects.all()  # 获取流水表
    productlist = user_Product.objects.all()  # 获取产品
    laundry = []
    for i in laundrylist:
        if i.surplus == 0:
            laundry.append(i)
    paginator1 = Paginator(laundry, 15)
    # 接受客户端传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/showSettlement/?page=1')
    # 将页数传递给分页对象获取内容响应客户端
    laundry = paginator1.page(page)
    context = {}
    context['userlists'] = userlists  # 获取所有用户
    context['applylists'] = applylist  # 获取受理状态
    context['laundrylists'] = laundry  # 获取流水表
    context['productlists'] = productlist  # 获取产品
    return render(request,'showSettlement.html',context)

#逾期业务查询
def showTimeout(request):
    userlists = Auth_user.objects.all()  # 获取所有用户
    applylist = Apply_progress.objects.all()  # 获取受理状态
    laundrylist = Laundry_list.objects.all()  # 获取流水表
    productlist = user_Product.objects.all()  # 获取产品
    applys = []
    for i in applylist:
        if i.yq == 1:
            applys.append(i)
    paginator1 = Paginator(applys, 15)
    # 接受客户端传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/showTimeout/?page=1')
    # 将页数传递给分页对象获取内容响应客户端
    applys = paginator1.page(page)
    context = {}
    context['userlists'] = userlists  # 获取所有用户
    context['applylists'] = applys  # 获取受理状态
    context['laundrylists'] = laundrylist  # 获取流水表
    context['productlists'] = productlist  # 获取产品
    return render(request,'showTimeout.html',context)

#违约业务查询
def showDefault(request):
    userlists = Auth_user.objects.all()  # 获取所有用户
    applylist = Apply_progress.objects.all()  # 获取受理状态
    laundrylist = Laundry_list.objects.all()  # 获取流水表
    productlist = user_Product.objects.all()  # 获取产品
    applys = []
    for i in applylist:
        if i.yq == 1:
            applys.append(i)
    paginator1 = Paginator(applys, 15)
    # 接受客户端传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/showDefault/?page=1')
    # 将页数传递给分页对象获取内容响应客户端
    applys = paginator1.page(page)
    context = {}
    context['userlists'] = userlists  # 获取所有用户
    context['applylists'] = applys  # 获取受理状态
    context['laundrylists'] = laundrylist  # 获取流水表
    context['productlists'] = productlist  # 获取产品
    return render(request,'showDefault.html',context)
#------------------------------业务查询管理（结束）------------------------------------------

#------------------------------项目审核管理（开始）------------------------------------------
#待审核用户
def auditList(request):
    userlists = Auth_user.objects.all()  # 获取所有用户
    applylist = Apply_progress.objects.all()  # 获取受理状态
    laundrylist = Laundry_list.objects.all()  # 获取流水表
    productlist = user_Product.objects.all()  # 获取产品
    applys = []
    for i in applylist:
        if i.apply == 1 and i.approval == 0:
            if i.audit != 2 and i.approval != 2:
                applys.append(i)
    paginator1 = Paginator(applys, 15)
    # 接受客户端传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/auditList/?page=1')
    # 将页数传递给分页对象获取内容响应客户端
    applys = paginator1.page(page)
    context = {}
    context['userlists'] = userlists  # 获取所有用户
    context['applylists'] = applys  # 获取受理状态
    context['laundrylists'] = laundrylist  # 获取流水表
    context['productlists'] = productlist  # 获取产品
    return render(request,'auditList.html',context)


#审核处理功能
def deal(request,id):#同意
    Apply_progress.objects.filter(id=id).update(audit=1)
    return redirect('/auditDeal/')
def refused(request,id):#拒绝
    Apply_progress.objects.filter(id=id).update(audit=2)
    return redirect('/auditDeal/')
#待审核用户
def auditDeal(request):
    userlists = Auth_user.objects.all()  # 获取所有用户
    applylist = Apply_progress.objects.all()  # 获取受理状态
    laundrylist = Laundry_list.objects.all()  # 获取流水表
    productlist = user_Product.objects.all()  # 获取产品
    applys = []
    for i in applylist:
        if i.audit == 0:
            applys.append(i)
    print(applys)
    paginator1 = Paginator(applys, 15)
    # 接受客户端传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/auditDeal/?page=1')
    # 将页数传递给分页对象获取内容响应客户端
    applys = paginator1.page(page)
    context = {}
    context['userlists'] = userlists  # 获取所有用户
    context['applylists'] = applys  # 获取受理状态
    context['laundrylists'] = laundrylist  # 获取流水表
    context['productlists'] = productlist  # 获取产品
    return render(request,'auditDeal.html',context)

#待审批用户
def deal1(request,id):#同意
    Apply_progress.objects.filter(id=id).update(approval=1)
    return redirect('/approvalDeal/')
def refused1(request,id):#拒绝
    Apply_progress.objects.filter(id=id).update(approval=2)
    return redirect('/approvalDeal/')

def approvalDeal(request):
    userlists = Auth_user.objects.all()  # 获取所有用户
    applylist = Apply_progress.objects.all()  # 获取受理状态
    laundrylist = Laundry_list.objects.all()  # 获取流水表
    productlist = user_Product.objects.all()  # 获取产品
    applys = []
    for i in applylist:
        if i.audit == 1 and i.approval == 0:
            applys.append(i)
    paginator1 = Paginator(applys, 15)
    # 接受客户端传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/approvalDeal/?page=1')
    # 将页数传递给分页对象获取内容响应客户端
    applys = paginator1.page(page)
    context = {}
    context['userlists'] = userlists  # 获取所有用户
    context['applylists'] = applys  # 获取受理状态
    context['laundrylists'] = laundrylist  # 获取流水表
    context['productlists'] = productlist  # 获取产品
    return render(request, 'approvalDeal.html', context)

#待放款客户列表
def deal2(request,id):#同意
    lendtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    Apply_progress.objects.filter(id=id).update(grant=1,lendtime=lendtime)
    return redirect('/lendingList/')
def refused2(request,id):#拒绝
    Apply_progress.objects.filter(id=id).update(grant=2)
    return redirect('/lendingList/')
def lendingList(request):
    userlists = Auth_user.objects.all()  # 获取所有用户
    applylist = Apply_progress.objects.all()  # 获取受理状态
    laundrylist = Laundry_list.objects.all()  # 获取流水表
    productlist = user_Product.objects.all()  # 获取产品
    applys = []
    for i in applylist:
        if i.approval == 1 and i.grant == 0:
            applys.append(i)
    paginator1 = Paginator(applys, 15)
    # 接受客户端传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/lendingList/?page=1')
    # 将页数传递给分页对象获取内容响应客户端
    applys = paginator1.page(page)
    context = {}
    context['userlists'] = userlists  # 获取所有用户
    context['applylists'] = applys  # 获取受理状态
    context['laundrylists'] = laundrylist  # 获取流水表
    context['productlists'] = productlist  # 获取产品
    return render(request,'lendingList.html',context)

#审核统计查询
def auditCount(request):
    return render(request,'auditCount.html')
#------------------------------项目审核管理（结束）------------------------------------------

#--------------------------优惠券管理（开始）----------------------------------------
#优惠券
def showCoupons(request):
    couponslist = Coupons.objects.all()  #获取优惠券对象
    paginator = Paginator(couponslist,13)
    #接受客户传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/showCoupons/?page=1')
    #将页数传递分页对象获取内容响应客户端
    couponslist = paginator.page(page)
    context = {}
    context['couponslist'] = couponslist
    return render(request,'coupons.html',context)
#添加
def addCoupons(request):
    if request.POST:
        c_title = request.POST.get('c_title')
        c_start = request.POST.get('c_start')
        c_stop = request.POST.get('c_stop')
        discount = request.POST.get('discount')
        c_num = request.POST.get('c_num')
        c_type = request.POST.get('c_type')
        c_type_id = Coupons_type.objects.get(t_name=c_type).id
        Coupons.objects.create(c_title=c_title,c_type_id=c_type_id,c_start=c_start,c_stop=c_stop,discount=discount,c_num=c_num)
        return redirect('/showCoupons/')
        pass
    else:
        return render(request,'addCoupons.html')

#删除
def delCoupons(request,id):
    Coupons.objects.filter(id=id).delete()
    return redirect('/showCoupons/')

#派发明细
def Detail(request):
    uc_list = user_coupons.objects.all()
    paginator = Paginator(uc_list, 15)
    # 接受客户传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/Detail/?page=1')
    # 将页数传递分页对象获取内容响应客户端
    uc_list = paginator.page(page)
    context = {}
    context['uc_list'] = uc_list
    return render(request, 'coupons_detail.html',context)

#使用情况
def State(request):
    uc_list = user_coupons.objects.all()
    paginator = Paginator(uc_list, 15)
    # 接受客户传递的页数
    try:
        page = int(request.GET.get('page'))
    except:
        return redirect('/State/?page=1')
    # 将页数传递分页对象获取内容响应客户端
    uc_list = paginator.page(page)
    context = {}
    context['uc_list'] = uc_list
    return render(request,'coupons_state.html',context)
#--------------------------优惠券管理（结束）----------------------------------------


#---------------------------注册用户管理（开始）---------------------------
#全部注册用户
def userlist(request):
    users = Auth_user.objects.all()
    paginator = Paginator(users,15)
    try:
        page = int(request.GET.get('page'))
        users = paginator.get_page(page)
        print(users)
    except:
        return redirect('/userlist/?page=1')
    context = {}
    context['users'] = users
    return render(request,'Userlist.html',context)

#注册未申请用户
def n_userlist(request):
    users = Auth_user.objects.all()
    paginator = Paginator(users, 15)
    try:
        page = int(request.GET.get('page'))
        users = paginator.get_page(page)
    except:
        return redirect('/n_userlist/?page=1')
    context = {}
    context['users'] = users
    return render(request, 'n_Userlist.html', context)

#注册以申请用户
def y_userlist(request):
    users = Auth_user.objects.all()
    p_list = user_Product.objects.all()
    paginator = Paginator(users, 15)

    try:
        page = int(request.GET.get('page'))
        users = paginator.get_page(page)
    except:
        return redirect('/y_userlist/?page=1')
    context = {}
    context['users'] = users
    context['plist'] = p_list
    return render(request, 'y_Userlist.html', context)

#黑名单用户
def blacklist(request):
    users = Blacklist.objects.all()
    paginator = Paginator(users, 15)
    try:
        page = int(request.GET.get('page'))
        users = paginator.get_page(page)
    except:
        return redirect('/blacklist/?page=1')
    context = {}
    context['users'] = users
    return render(request, 'blacklist.html', context)
#---------------------------注册用户管理（结束）---------------------------