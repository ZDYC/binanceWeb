from django.db import models

from collections import namedtuple
from jsonfield import JSONField
from . managers import AssetManager, OrderManager

from django.conf import settings


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
    # coin = models.ForeignKey(CryptoCoin, models.SET_NULL, null=True,
                             # blank=True, verbose_name='交易资产')

    coin = models.CharField('coin', max_length=33, null=True, blank=True)

    coin_precision = models.IntegerField('交易资产精度',  default=8,
        help_text='精确到小数点后8位')
    # currency = models.ForeignKey(CryptoCoin, models.SET_NULL, null=True,
                                 # blank=True, verbose_name='报价资产',
                                 # related_name='currencymarket')

    currency = models.CharField('currency', max_length=33, null=True, blank=True)

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
        return self.symbol
        # return f'{self.symbol}@{self.platform.name}'


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


class Order(models.Model):

    ORDER_TYPE_LIMIT = 'LIMIT'
    ORDER_TYPE_MARKET = 'MARKET'
    ORDER_TYPE_STOP_LOSS = 'STOP_loss'
    ORDER_TYPE_STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'
    ORDER_TYPE_TAKE_PROFIT = 'TAKE_PROFIT'
    ORDER_TYPE_TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'
    ORDER_TYPE_LIMIT_MAKER = 'LIMIT_MAKER'

    SIDE_BUY = 'BUY'
    SIDE_SELL = 'SELL'

    ORDER_TIF_GTC = 'GTC'
    ORDER_TIF_IOC = 'IOC'
    ORDER_TIF_FOK = 'FOK'

    ORDER_STATUS_PREPARE = 'PREPARE'
    ORDER_STATUS_NEW = 'NEW'
    ORDER_STATUS_PARTIALLY_FILLED = 'PARTIALLY_FILLED'  # 部份成交
    ORDER_STATUS_FILLED = 'FILLED'  # 已全部成交
    ORDER_STATUS_PREPARE_CANCEL = 'PREPARE_CANCEL'  # 本地提交取消，交易平台未提交
    ORDER_STATUS_CANCELED = 'CANCELED'  # 已取消
    ORDER_STATUS_PENDING_CANCEL = 'PENDING_CANCEL'  # 正在取消。
    ORDER_STATUS_REJECTED = 'REJECTED'  # 被拒绝
    ORDER_STATUS_EXPIRED = 'EXPIRED'  # 已超时
    ORDER_STATUS_DELETED = 'DELETED'  # 已删除

    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL,
                             null=True, verbose_name='交易员')
    account = models.ForeignKey(Account, models.SET_NULL,
                                null=True, verbose_name='交易所账号')
    symbol = models.CharField('交易币对', max_length=50)
    quantity = models.DecimalField('数量', max_digits=19,
                                   decimal_places=8, default=0)
    time_in_force = models.CharField('有效期', default='GTC', max_length=3,
                                     choices=(('GTC', 'GTC'),
                                              ('IOC', 'IOC'),
                                              ('FOK', 'FOK')))
    price = models.DecimalField('价格', max_digits=19, decimal_places=8)
    stop_price = models.DecimalField('止盈止损价格', max_digits=19, null=True,
                                     blank=True, decimal_places=8, default=None)
    side = models.CharField('方向', default='SELL', max_length=10,
                            choices=(('SELL', '卖出'), ('BUY', '买入')))
    order_type = models.CharField('类型', default='LIMIT', max_length=30,
                                  choices=(('LIMIT', '限价单'),
                                           ('MARKET', '市价单'),
                                           ('STOP_LOSS', '止损单'),
                                           ('STOP_LOSS_LIMIT', '止损限价单'),
                                           ('TAKE_PROFIT', '获利单'),
                                           ('TAKE_PROFIT_LIMIT', '获利限价单'),
                                           ('LIMIT_MAKER', '限价造市')))
    buy = models.ForeignKey(CryptoCoin, models.SET_NULL, null=True,
                            verbose_name='买入对象', related_name='buying')
    sell = models.ForeignKey(CryptoCoin, models.SET_NULL, null=True,
                             verbose_name='卖出对象', related_name='selling')
    platform_order_id = models.IntegerField('平台订单号', default=-1, db_index=True)
    iceberg_quantity = models.DecimalField('冰山交易量', default=0.0,
                                           null=True, blank=True,
                                           max_digits=19, decimal_places=8)
    status = models.CharField('状态', max_length=20,
                              default=ORDER_STATUS_PREPARE,
                              choices=((ORDER_STATUS_PREPARE, '准备中'),
                                       (ORDER_STATUS_NEW, '新订单'),
                                       (ORDER_STATUS_PARTIALLY_FILLED, '部份完成'),
                                       (ORDER_STATUS_FILLED, '已完成'),
                                       (ORDER_STATUS_PREPARE_CANCEL, '准备取消'),
                                       (ORDER_STATUS_CANCELED, '已取消'),
                                       (ORDER_STATUS_PENDING_CANCEL, '取消中'),
                                       (ORDER_STATUS_REJECTED, '被拒绝'),
                                       (ORDER_STATUS_EXPIRED, '超时'),
                                       (ORDER_STATUS_DELETED, '已删除')))
    create_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_at = models.DateTimeField('修改时间', auto_now=True)
    extra_info = JSONField('其他信息', null=True, blank=True)

    objects = OrderManager()

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'

    def __str__(self):
        return self.symbol
        # return f'{self.symbol}({self.pk})'


class Trade(models.Model):
    order = models.ForeignKey(Order, models.SET_NULL, null=True, blank=True,
                              verbose_name='订单')
    quantity = models.DecimalField('数量', max_digits=19, decimal_places=8)
    price = models.DecimalField('价格', max_digits=19, decimal_places=8)
    commission = models.DecimalField('佣金', max_digits=19, decimal_places=8)
    commission_asset = models.CharField('佣金结算货币', max_length=20)
    is_buyer = models.BooleanField('是否买家')
    is_maker = models.BooleanField('是否造市', default=False)
    is_best_match = models.BooleanField('最佳匹配', default=True)
    platform_trade_id = models.IntegerField('平台交易号', default=-1)
    platform_order_id = models.IntegerField('平台订单号', default=-1, db_index=True)
    trade_time = models.BigIntegerField('交易时间')
    create_at = models.DateTimeField('记录时间', auto_now_add=True)
    extra_info = JSONField('其他信息', null=True, blank=True)

    class Meta:
        verbose_name = '交易'
        verbose_name_plural = '交易'
        # unique_together = []


class FrozenAsset(models.Model):
    account = models.ForeignKey(
        Account, models.SET_NULL, blank=True, null=True, verbose_name='交易员账号')
    # user = models.ForeignKey(
        # settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True, verbose_name='交易员')
    order = models.ForeignKey(
        Order, models.SET_NULL, blank=True, null=True, verbose_name='所属订单')
    coin = models.ForeignKey(
        CryptoCoin, models.PROTECT, null=True, verbose_name='资产')
    quantity = models.DecimalField('数量', max_digits=19, decimal_places=8)
    free = models.BooleanField('是否解冻', default=False, help_text='交易成功返回的')
    manual = models.BooleanField('是否人工冻结', default=False)
    create_at = models.DateTimeField('发生时间', auto_now_add=True)
    # creator = models.ForeignKey(
        # settings.AUTH_USER_MODEL, models.SET_NULL,
        # blank=True, null=True, verbose_name='操作人', related_name='frozen')
    # content_type = models.ForeignKey(
    #     ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    # object_id = models.PositiveIntegerField(null=True, blank=True)
    # related_object = GenericForeignKey('content_type', 'object_id')

    # objects = FrozenAssetManager()

    class Meta:
        verbose_name = '冻结资产'
        verbose_name_plural = '冻结资产'


class AssetLog(models.Model):

    ASSETLOG_TYPE_ACCOUNT_IN = 0  # 交易帐号转入资产
    ASSETLOG_TYPE_ACCOUNT_OUT = 1  # 交易帐号转出资产
    ASSETLOG_TYPE_ACCOUNT_BUY = 2  # 交易帐号买入
    ASSETLOG_TYPE_ACCOUNT_SELL = 3  # 交易帐号卖出
    ASSETLOG_TYPE_ACCOUNT_COMISSION = 4  # 交易帐号交易佣金
    ASSETLOG_TYPE_TRADER_IN = 10  # 交易员入帐，通常发生在初次分配
    ASSETLOG_TYPE_TRADER_OUT = 11  # 交易员转出
    ASSETLOG_TYPE_TRADER_BUY = 12  # 交易员买入
    ASSETLOG_TYPE_TRADER_SELL = 13  # 交易员卖出
    ASSETLOG_TYPE_COMISSION_IN = 14  # 本平台手续费收入
    ASSETLOG_TYPE_COMISSION_OUT = 15  # 交易员交易产生的手续费
    ASSETLOG_TYPE_TRANSFER_OUT = 16  # 交易员转帐至其他交易员
    ASSETLOG_TYPE_TRANSFER_IN = 17  # 其他交易员转帐入本交易员

    ASSETLOG_CHOICES = (
        (ASSETLOG_TYPE_ACCOUNT_IN, '帐号转入'),
        (ASSETLOG_TYPE_ACCOUNT_OUT, '帐号转出'),
        (ASSETLOG_TYPE_ACCOUNT_BUY, '帐号买入'),
        (ASSETLOG_TYPE_ACCOUNT_SELL, '帐号买出'),
        (ASSETLOG_TYPE_ACCOUNT_COMISSION, '帐号交易手续费'),
        (ASSETLOG_TYPE_TRADER_IN, '交易员转入'),
        (ASSETLOG_TYPE_TRADER_OUT, '交易员转出'),
        (ASSETLOG_TYPE_TRADER_BUY, '交易买入'),
        (ASSETLOG_TYPE_TRADER_SELL, '交易员卖出'),
        (ASSETLOG_TYPE_COMISSION_IN, '平台佣金'),
        (ASSETLOG_TYPE_COMISSION_OUT, '交易员手续费'),
        (ASSETLOG_TYPE_TRANSFER_OUT, '交易员转帐（转出）'),
        (ASSETLOG_TYPE_TRANSFER_IN, '交易员转帐（转入）'),
    )
    account = models.ForeignKey(Account, models.SET_NULL, blank=True, null=True, verbose_name='交易所账号')
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True, verbose_name='交易员')
    order = models.ForeignKey(Order, models.SET_NULL, blank=True, null=True, verbose_name='所属订单')
    # trader = models.ForeignKey(Trader, models.SET_NULL, blank=True, null=True, verbose_name='所属交易')
    coin = models.ForeignKey(CryptoCoin, models.PROTECT, null=True, verbose_name='资产')
    coin_type = models.IntegerField('类型', choices=ASSETLOG_CHOICES)
    quantity = models.DecimalField('数量', max_digits=19, decimal_places=8)
    effect_account = models.BooleanField('影响账户资产', default=True, editable=False)
    usdt_value = models.DecimalField('USDT价值', max_digits=19, decimal_places=8, default=0)
    create_date = models.DateTimeField('发生日期', auto_now_add=True, db_index=True)
    create_time = models.TimeField('发生时间', auto_now_add=True)

    # content_type = models.ForeignKey(
    #     ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    # object_id = models.PositiveIntegerField(null=True, blank=True)
    # related_object = GenericForeignKey('content_type', 'object_id')

    objects = AssetManager()

    def __str__(self):
        tp = dict(AssetLog.ASSETLOG_CHOICES)[self.type]
        return '类型 %s: 资产：%s 数量：%.8f' % (
            tp, self.coin_id, self.quantity
        )

    class Meta:
        verbose_name = '资产明细'
        verbose_name_plural = '资产明细'
