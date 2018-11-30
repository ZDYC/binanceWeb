from django.contrib import admin
from django.conf import settings
from .models import CryptoCoin, Platform, Account, Market
from django.utils.html import format_html

from datetime import datetime
from .services import account

import logging


log = logging.getLogger(__name__)


class CryptoCoinAdmin(admin.ModelAdmin):
    list_display = ['name', 'coinId', 'website', 'description']
    search_fields = ['name', 'coinId']
    list_filter = ['name', 'coinId']


class PlatformAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'website', 'description']


class AccountAdmin(admin.ModelAdmin):

    def laset_sync_time(self, account):
        if account.laset_sync == 0:
            return '未同步'
        dt =datetime.fromtimestamp(account.laset_sync / 1000)
        fmt = '%Y年%m月%d日 %H时%M分'
        return dt.strftime(fmt)

    def edit(self, account):
        tpl = f"""
        <span><a href="#" @click="checkAsset({account.id});">查看资产</a></span>
        &nbsp;&nbsp
        """
        return format_html(tpl)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if (not change) or (obj.laset_sync == 0):
            log.info(f'新账号(id:{obj.id})或未同步，去同步一下')
            try:
                account.inital_account(obj)
            except ExchangeException as e:
                log.exception('账号执行同步失败', exc_info=True)
                messages.warning(request, f'账号未能验证, 原因:{e.message}')
            except Exception:
                log.exception('账号执行同步失败', exc_info=True)
                message.warning(request, '账号未能验证并初始, 账号暂时不可用')

    def delete_model(self, request, obj):
        """删除数据
        """
        log.info(f'将删除交易所帐号 {obj.name}')
        # if obj.platform.slug == 'binance':
            # remove_ws_process.delay(obj.id)
        super().delete_model(request, obj)

    class Media:
        css = {
            'all': ('https://unpkg.com/element-ui/lib/theme-chalk/index.css',)
        }
        js = (
            'https://unpkg.com/vue@2.5.16/dist/vue.js',
            'https://unpkg.com/element-ui/lib/index.js',
        )


    edit.short_description = '操作'
    laset_sync_time.short_description = '最后更新时间'
 
    list_display = ['platform', 'name', 'description', 'create_at', 'laset_sync_time', 'edit']
    search_fields = ['platform', 'name']
    list_filter = ['platform', 'create_at']


class MarketAdmin(admin.ModelAdmin):
    list_display = ['platform', 'symbol']





admin.site.register(CryptoCoin, CryptoCoinAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Market, MarketAdmin)


admin.site.site_header = settings.SITE_NAME
admin.site.site_title = settings.SITE_NAME