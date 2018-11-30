from django.db import models

from collections import namedtuple
from jsonfield import JSONField


class CryptoCoin(models.Model):
    """加密币类型
    """
    coinId = models.CharField('代号', max_length=33, primary_key=True)
    name = models.CharField('名称', max_length=100)
    website = models.URLField('网站', null=True, blank=True)
    description = models.CharField('描述', max_length=256,
                                   blank=True, null=True)
    class Meta:
        verbose_name = '加密货币'
        verbose_name_plural = '加密货币'

    def __str__(self):
        return self.coinId


class Platform(models.Model):
    """交易所
    """
    name = models.CharField('名称', max_length=50)
    slug = models.SlugField('代号', help_text='允许英文，数字及下划线',
                            unique=True)
    website = models.URLField('网站', null=True, blank=True)
    description = models.CharField('描述', max_length=256,
                                   blank=True, null=True)
    last_checksum = models.CharField(
        '信息签名', max_length=100, null=True, blank=True,
        help_text='用于检查服务器返回数据是否更新')

    commission_asset = models.ForeignKey(
        CryptoCoin, models.SET_NULL, null=True, blank=True,
        verbose_name='结算币', help_text='交易佣金结算币')
    commission_rate = models.DecimalField('交易手续费率', max_digits=9,
                                          decimal_places=8, default=0.01)

    class Meta:
        verbose_name = '交易所'
        verbose_name_plural = '交易所'

    def __str__(self):
        return self.name


class Market(models.Model):
    platform = models.ForeignKey(Platform, models.SET_NULL, null=True,
                                 blank=True, verbose_name='交易平台')
    symbol = models.CharField('币对', max_length=50, help_text='使用大写')
    coin = models.ForeignKey(CryptoCoin, models.SET_NULL, null=True,
                             blank=True, verbose_name='交易资产')
    coin_precision = models.IntegerField('交易资产精度',  default=8,
        help_text='精确到小数点后8位')
    currency = models.ForeignKey(CryptoCoin, models.SET_NULL, null=True,
                                 blank=True, verbose_name='报价资产',
                                 related_name='currencymarket')
    currency_precision = models.IntegerField('报价资产精度', default=8,
        help_text='精确到小数点后8位')
    diaable = models.BooleanField('禁止交易', default=False)
    status = models.CharField('市场状态', max_length=20, null=True, blank=True)
    order_types = models.CharField('支持交易类型', max_length=200, null=True, blank=True)
    iceberg_allowed = models.BooleanField('允许冰山交易', default=False)
    extra_info = JSONField('其他信息', null=True, blank=True)
    last_checksum = models.CharField(
        '信息签名', max_length=100, null=True, blank=True,
        help_text='用于检查服务器返回数据是否更新')

    class Meta:
        verbose_name = '交易市场'
        verbose_name_plural = '交易市场'
        unique_together = ['platform', 'symbol']

    def __str__(self):
        return f'{self.symbol}@{self.platform.name}'


class Account(models.Model):
    """交易所账号
    """
    platform = models.ForeignKey(Platform, models.SET_NULL,
                                verbose_name='交易所', null=True)
    name = models.CharField(
        '账号名', max_length=100, help_text='使用真实的邮箱或账号名')
    key = models.CharField('api key', max_length=250,
                            blank=True, null=True)
    secret = models.CharField('api secret', max_length=250,
                               blank=True, null=True)
    description = models.CharField('描述', max_length=256,
                                    blank=True, null=True)
    create_at = models.DateTimeField('创建时间', auto_now_add=True)

    can_trade = models.BooleanField('可变易', default=True, editable=False)
    can_withdraw = models.BooleanField('可提现', default=True, editable=False)
    can_deposit = models.BooleanField('可充值', default=True, editable=False)

    maker_commission = models.IntegerField('Maker手续费',
                                            default=0, editable=False)
    taker_commission = models.IntegerField('Taker手续费',
                                            default=0, editable=False)
    buyer_commission = models.IntegerField('买家手续费',
                                           default=0, editable=False)
    seller_commission = models.IntegerField('卖家续费',
                                            default=0, editable=False)
    extra_info = JSONField('其他信息', null=True, blank=True)
    laset_sync = models.BigIntegerField('最后同步时间', default=0, editable=False)

    class Meta:
        verbose_name = '交易所账号'
        verbose_name_plural = '交易所账号'
        unique_together = ('platform', 'name')

    def availbale(self):
        return self.laset_sync > 0

    availbale.short_description = '可用'
    availbale.boolean = True

    def __str__(self):
        return self.name
