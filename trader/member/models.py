from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.utils import timezone

from django.utils.translation import gettext_lazy as _

from core.models import CryptoCoin, Account
from . managers import CustomUserManager, AdminManager, TraderManager


class User(AbstractBaseUser, PermissionsMixin):
    # staff = models.ForeignKey(Staff, models.SET_NULL, null=True, blank=True, verbose_name='所属员工')
    account = models.ForeignKey(Account, models.SET_NULL, null=True, blank=True, verbose_name='所属交易账号')
    name = models.CharField('登录名', max_length=30, unique=True)
    nickname = models.CharField('姓名', max_length=30, null=True, blank=True)
    mobile = models.CharField('手机', max_length=11)
    email = models.EmailField('邮箱', blank=True, null=True)

    # 手续费设置,0:按买入币种比例， 1：按指定币种的比例
    commission_type = models.IntegerField(
        '手续费计费方式', default=0, choices=((0, '按买入币种比例'),))
    commission_coin = models.ForeignKey(
        CryptoCoin, models.SET_NULL, null=True, verbose_name='结算币种',
        help_text='计费方式为按买入币种比例时，本设置无效。', blank=True)
    commission_rate = models.DecimalField(
        '手续费比例', max_digits=9, decimal_places=8, default=0.0001)
    warning_line = models.FloatField(
        '告警线',
        default=0.8,
        validators=[MinValueValidator(0), MaxValueValidator(1)])
    close_out_line = models.FloatField(
        '平仓线',
        default=0.6,
        validators=[MinValueValidator(0), MaxValueValidator(1)])

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['mobile']

    class Meta:
        verbose_name = '交易员'
        verbose_name_plural = '交易员'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.name


class Trader(User):

    objects = TraderManager() 

    class Meta:
        proxy = True
        verbose_name = '交易员'
        verbose_name_plural = '交易员'


class AdminUser(User):
    objects = AdminManager()

    class Meta:
        proxy = True
        verbose_name = '系统管理员'
        verbose_name_plural = '系统管理员'

# class Staff(models.Model):
#     """员工
#     """
#     name = models.CharField('姓名', max_length=21)
#     mobile = models.CharField('手机', max_length=20)
#     identity = models.CharField('身份证号', max_length=20, blank=True, null=True)
#     email = models.EmailField('邮箱', blank=True, null=True)
#     gender = models.CharField('性别', default='M', max_length=1, choices=(('M', '男'), ('F', '女')))
#     description = models.CharField('备注', max_length=1024, blank=True, null=True)
#     create_at = models.DateTimeField('创建时间', auto_now_add=True)
#     join_at = models.DateTimeField('加入时间', null=True, blank=True)

#     class Meta:
#         verbose_name = '员工'
#         verbose_name_plural = '员工'

#     def __str__(self):
#         return self.name



