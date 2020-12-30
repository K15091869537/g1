from django.db import models
from django.contrib.auth.models import AbstractUser #导入权限模块
# Create your models here.
#用户表（继承原类）
class Auth_user(models.Model):
    account = models.CharField(max_length=20, verbose_name='登录账号', unique=True)
    password = models.CharField(max_length=20, verbose_name='登录密码')
    name = models.CharField(max_length=20,verbose_name='姓名',null=True)
    card = models.CharField(max_length=18,verbose_name='身份证',unique=True,null=True)
    work = models.CharField(max_length=20, verbose_name='职业',null=True)
    tel = models.IntegerField(verbose_name='电话',null=True)
    card_z = models.TextField(verbose_name='身份证正面',null=True)
    card_f = models.TextField(verbose_name='身份证反面',null=True)
    company = models.CharField(max_length=20,verbose_name='公司名称',unique=True,null=True)
    credit_code = models.CharField(max_length=50,verbose_name='统一社会信用代码',unique=True,null=True)
    company_img = models.TextField(verbose_name='公司资质照片',null=True)
    u_type = models.IntegerField(verbose_name='个人或企业',null=True)


#职位
class Job(models.Model):
    Job_name = models.CharField(max_length=20,verbose_name='职位类型')

#员工表
class Emp(AbstractUser):
    work_num = models.CharField(max_length=20,verbose_name='工号',unique=True)
    e_work = models.ForeignKey(Job,on_delete=models.CASCADE,verbose_name='职位ID')
    Uid = models.ForeignKey(Auth_user,on_delete=models.CASCADE,verbose_name='用户ID')

#黑名单
class Blacklist(models.Model):
    Uid = models.ForeignKey(Auth_user,on_delete=models.CASCADE,verbose_name='用户ID')

#征信表
class Credit_reporting(models.Model):
    c_credit = models.IntegerField(verbose_name='贷款记录')
    higher = models.IntegerField(verbose_name='贷款额度')
    overdue = models.IntegerField(verbose_name='逾期记录')
    black = models.ForeignKey(Blacklist,on_delete=models.CASCADE,verbose_name='黑名单')
    three_parties = models.IntegerField(verbose_name='第三方贷款记录')
    rate = models.IntegerField(verbose_name='信用度')

#用户-征信（中间表）
class User_credit(models.Model):
    Uid = models.ForeignKey(Auth_user,on_delete=models.CASCADE,verbose_name='用户ID')
    Cid = models.ForeignKey(Credit_reporting,on_delete=models.CASCADE,verbose_name='征信ID')

#产品类型表
class Product_type(models.Model):
    p_type = models.CharField(max_length=20,verbose_name='产品类型')

#产品表
class Product(models.Model):
    p_name = models.CharField(max_length=20,verbose_name='产品名称')
    introduc = models.CharField(max_length=100,verbose_name='产品简介')
    Tid = models.ForeignKey(Product_type,on_delete=models.CASCADE,verbose_name='产品类型ID')
    range = models.IntegerField(verbose_name='可贷额度')
    date = models.IntegerField(verbose_name='贷款周期',null=True)
    rate = models.FloatField(verbose_name='利息')
    active = models.IntegerField(verbose_name='办理状态')
    start = models.DateTimeField(verbose_name='开始办理日期')
    stop = models.DateTimeField(verbose_name='截止办理日期')
    permanent = models.IntegerField(verbose_name='办理期限')

#用户产品中间表
class user_Product(models.Model):
    up_time = models.DateTimeField(verbose_name='申请日期')
    Uid = models.ForeignKey(Auth_user,on_delete=models.CASCADE,verbose_name='用户ID')
    Pid = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='产品ID')

#受理状态
class Apply_progress(models.Model):
    apply = models.IntegerField(verbose_name='申请状态')
    audit = models.IntegerField(verbose_name='审核状态')
    approval = models.IntegerField(verbose_name='审批状态')
    grant = models.IntegerField(verbose_name='放款状态')
    Pid = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='放款金额(关联产品)')
    lendtime = models.DateTimeField(verbose_name='放款时间')
    yq = models.IntegerField(verbose_name='是否逾期')
    Uid = models.ForeignKey(Auth_user,on_delete=models.CASCADE,verbose_name='用户ID')

#三方支付
class Pays(models.Model):
    pay_way = models.CharField(max_length=10,verbose_name='支付方式')

#流水表
class Laundry_list(models.Model):
    Aid = models.ForeignKey(Apply_progress,on_delete=models.CASCADE,verbose_name='受理流程表ID')
    repaid = models.IntegerField(verbose_name='还款金额')
    repaid_time = models.DateTimeField(verbose_name='还款时间')
    surplus = models.IntegerField(verbose_name='未还金额')
    Pid = models.ForeignKey(Pays,on_delete=models.CASCADE,verbose_name='支付方式')
    Uid = models.ForeignKey(Auth_user,on_delete=models.CASCADE,verbose_name='用户ID')

#减免申请表
class Breaks(models.Model):
    breaks = models.IntegerField(verbose_name='是否发起减免申请') # 是否发起减免申请
    b_reason = models.CharField(max_length=100,verbose_name='减免理由')# 减免理由
    b_through  = models.IntegerField(verbose_name='是否通过减免')# 是否通过减免
    delay = models.IntegerField(verbose_name='是否发起展期申请')# 是否发起展期申请
    d_reason = models.CharField(max_length=100,verbose_name='展期理由')# 展期理由
    d_through = models.IntegerField(verbose_name='是否通过展期',default=0)# 是否通过展期
    Lid = models.ForeignKey(Laundry_list,on_delete=models.CASCADE,verbose_name='流水ID')

#公告表
class Announcement(models.Model):
    banner = models.CharField(max_length=500,verbose_name='轮播图存储路径',null=True)

#新闻表
class News(models.Model):
    title = models.CharField(max_length=30,verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    ntime = models.DateTimeField(verbose_name='发布时间')

#站内信息表
class Information(models.Model):
    i_talk = models.CharField(max_length=500,verbose_name='发送内容')
    i_time = models.DateTimeField(verbose_name='发送日期')
    i_read = models.IntegerField(verbose_name='是否已读')

#回复表
class Reply(models.Model):
    r_talk = models.CharField(max_length=500,verbose_name='回复内容')
    r_time = models.DateTimeField(verbose_name='回复日期')
    r_read= models.IntegerField(verbose_name='是否已读')

#员工-用户-站内信息（中间表）
class Auth_user_emp_information(models.Model):
    Uid = models.ForeignKey(Auth_user,on_delete=models.CASCADE,verbose_name='用户ID')
    Eid = models.ForeignKey(Emp, on_delete=models.CASCADE, verbose_name='员工ID')
    Iid = models.ForeignKey(Information, on_delete=models.CASCADE, verbose_name='站内信息ID')

#员工-用户-回复（中间表）
class Auth_user_emp_reply(models.Model):
    Uid = models.ForeignKey(Auth_user,on_delete=models.CASCADE,verbose_name='用户ID')
    Eid = models.ForeignKey(Emp, on_delete=models.CASCADE, verbose_name='员工ID')
    Rid = models.ForeignKey(Reply, on_delete=models.CASCADE, verbose_name='回复信息ID')

#优惠券类型
class Coupons_type(models.Model):
    t_name = models.CharField(max_length=20,verbose_name='优惠卷类型')

#优惠券
class Coupons(models.Model):
    c_title = models.CharField(max_length=20,verbose_name='优惠券名称')
    c_type = models.ForeignKey(Coupons_type,on_delete=models.CASCADE,verbose_name='优惠券类型')
    c_start = models.DateTimeField(verbose_name='开始使用期限')
    c_stop = models.DateTimeField(verbose_name='截止使用期限')
    discount = models.CharField(max_length=20,verbose_name='折扣',null=True)
    c_num = models.IntegerField(verbose_name='优惠券数量',null=True)

#用户-优惠券
class user_coupons(models.Model):
    state = models.IntegerField(verbose_name='使用情况')
    Cid = models.ForeignKey(Coupons,on_delete=models.CASCADE,verbose_name='优惠券')
    Uid = models.ForeignKey(Auth_user,on_delete=models.CASCADE,verbose_name='用户ID')

#日志
class Log(models.Model):
    Uid = models.ForeignKey(Emp,on_delete=models.CASCADE,verbose_name='用户ID')
    time = models.DateTimeField(verbose_name='登录时间')
    operation = models.CharField(max_length=100, verbose_name='操作',null=True)