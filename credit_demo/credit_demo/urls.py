"""credit_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# 梁
from app_thrid.views import chat,reply_user,addbanner,del_pic,news,add_news,update_news,del_news,show_mess,log,show_log,update_log,del_login,manage_creid
# 任凯
from app import views
# 吉国君
from app4.views import userindex,blog,blog_details,contact,userlogin,login1,uploadcard_p,uploadcard_r
from app4.views import apply,userdeta,breaks1,delay1,checkuser,addcoupons,company_img
# cherish
from app_first.views import index,newemp,thirdpay,cashpay,downloadexcel,carshload,repayment,gologin,updatamesage,administration,addemp,updateemp,daleemp
from app_first.views import exit,taizhang,unpaid,unpaidtoexcel,allpaid,allpaidtoexcel,collection,collectiontoexcel,collectionwork,collectionsev
from app_first.views import collectionsevto,collectionthan,userbreak,throuthuser,refuseuser,breaklist,userdelay,delay,undelay,delaylist,inproduct
from app_first.views import inforproduct,collectionwork3,collectionwork2
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',index),
    path('newemp/',newemp),
    path('login/',gologin),#员工登录
    path('thirdpay/',thirdpay), #财务资金管理-三方支付流水
    path('cashpay/',cashpay),#线下支付流水
    path('downloadexcel/<str:filename>',downloadexcel),#excel导出功能
    path('carshload/<str:filename>',carshload),#excel导出功能(现金流水)
    path('repayment/',repayment),#客户还款台账
    path('updatamesage/',updatamesage),#修改个人资料
    path('administration/',administration),#人员管理
    path('addemp/',addemp),#添加员工
    path('updateemp/<int:id>/',updateemp),#修改员工信息
    path('daleemp/<int:id>/',daleemp),#删除员工
    path('exit/',exit),#退出登录
    path('taizhang/<str:filename>',taizhang),#客户还款台账
    path('unpaid/',unpaid),#未放款台账
    path('unpaidtoexcel/<str:filename>',unpaidtoexcel),#未放款台账数据导出
    path('allpaid/',allpaid),#全部放款台账
    path('allpaidtoexcel/<str:filename>',allpaidtoexcel),#全部放款台账数据导出
    path('collection/',collection),#催收池
    path('collectiontoexcel/<str:filename>',collectiontoexcel),#催收池导出excel
    path('collectionwork/',collectionwork),#催收任务处理
    path('collectionwork2/', collectionwork2),  # 催收任务处理
    path('collectionwork3/',collectionwork3),#催收任务处理
    path('collectionsev/<str:filename>',collectionsev),#催收导出（0-7）
    path('collectionsevto/<str:filename>',collectionsevto),#催收导出（8-30）
    path('collectionthan/<str:filename>',collectionthan),#催收导出（30以上）
    path('userbreak/',userbreak),#减免申请
    path('throuthuser/<int:id>/',throuthuser),#通过申请
    path('refuseuser/<int:id>/',refuseuser),#拒绝申请
    path('breaklist/',breaklist),#减免处理清单
    path('userdelay/',userdelay),#展期申请处理
    path('delay/<int:id>/',delay),#通过展期申请
    path('undelay/<int:id>/',undelay),#拒绝展期申请
    path('delaylist/',delaylist),#展期处理清单
    path('inproduct/',inproduct),#产品配置
    path('inforproduct/',inforproduct),#产品详情
    #     任凯
    path('showBusiness/',views.showBusiness),     #全部业务查询
    path('showApply/',views.showApply),           #申请业务查询
    path('showAudit/',views.showAudit),           #审核业务查询
    path('showThrough/',views.showThrough),       #通过业务查询
    path('showRefused/',views.showRefused),       #拒绝业务查询
    path('showLending/',views.showLending),       #放款业务查询
    path('showAlso/',views.showAlso),             #还款业务查询
    path('showSettlement/',views.showSettlement), #结清业务查询
    path('showTimeout/',views.showTimeout),       #逾期业务查询
    path('showDefault/',views.showDefault),       #违约业务查询
    # ------------------------项目审核管理--------------------------------
    path('auditList/', views.auditList),  # 待审核用户
    path('auditDeal/', views.auditDeal),  # 审核任务处理
    path('deal/<int:id>', views.deal),  # 通过
    path('refused/<int:id>', views.refused),  # 拒绝
    path('approvalDeal/', views.approvalDeal),  # 审批任务处理
    path('deal1/<int:id>', views.deal1),  # 通过1
    path('refused1/<int:id>', views.refused1),  # 拒绝1
    path('lendingList/', views.lendingList),  # 放款任务处理
    path('deal2/<int:id>', views.deal2),  # 通过1
    path('refused2/<int:id>', views.refused2),  # 拒绝1
    path('auditCount/', views.auditCount),  # 审核统计查询
#------------------------优惠券管理-------------------------------
    path('showCoupons/',views.showCoupons),         #优惠券
    path('addCoupons/',views.addCoupons),           #添加优惠券
    path('delCoupons/<int:id>',views.delCoupons),  #删除优惠券
    path('Detail/',views.Detail),                   #优惠券派发明细
    path('State/',views.State),                     #优惠券使用情况
    #-------------------------注册用户管理----------------------------
    path('userlist/',views.userlist),               #全部注册用户
    path('n_userlist/',views.n_userlist),           #注册未申请用户
    path('y_userlist/',views.y_userlist),           #注册未申请用户
    path('blacklist/',views.blacklist),           #注黑名单用户
#     梁彦龙

    path('chat/',chat),
    path('reply/',reply_user),
    path('pic/',addbanner),
    path('del/<int:id>',del_pic),
    path('news/',news),
    path('add_news/',add_news),
    path('update_news/<int:id>',update_news),
    path('del_news/<int:id>',del_news),
    path('get_ip/',log),
    path('show_login/',show_log),
    path('update_login/<int:id>',update_log),
    path('del_login/<int:id>',del_login),
    path('manage_creid/',manage_creid),
    # path('get_ip/',log),
    path('per_usermess/<int:id>',show_mess),


#     吉国君
    path('blog/<int:id>/', blog),
    path('userindex/<int:id>/', userindex),
    path('blog_details/<int:id>/<int:nid>/', blog_details),
    path('contact/<int:id>/<int:eid>/', contact),
    path('userlogin/<int:id>/', userlogin),
    path('login1/', login1),
    path('checkuser/<str:username>/', checkuser),
    path('uploadcard_p/', uploadcard_p),
    path('uploadcard_r/', uploadcard_r),
    path('apply/<int:id>/<int:pid>/', apply),
    path('userdeta/<int:id>/', userdeta),
    path('breaks1/<int:id>/', breaks1),
    path('delay1/<int:id>/', delay1),
    path('addcoupons/<int:id>/<int:cid>/', addcoupons),
    path('company_img/', company_img),
]
