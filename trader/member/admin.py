from django.contrib import admin
from django import forms

from . models import Trader, AdminUser


class UserCreateionForm(forms.ModelForm):
    """创建用户表单
    """
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = Trader
        fields = ('name', 'mobile', 'email', 'account')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('两次密码不一致')
        return password2

    def save(self, commit=True):
        trader = super(UserCreateionForm, self).save(commit=False)
        trader.set_password(self.cleaned_data['password2'])
        if commit:
            trader.save()
        return trader


class TraderAdmin(admin.ModelAdmin):
    form = UserCreateionForm

    list_display = ('name', 'mobile', 'email', 'account', 'is_active')
    search_fields = ('name', 'nickname', 'mobile')
    list_select_related = ['account']

admin.site.register(Trader, TraderAdmin)
admin.site.register(AdminUser)