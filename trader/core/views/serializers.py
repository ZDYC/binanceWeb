from rest_framework import serializers

from member.models import Trader, User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
		'id',
		'is_staff',
		'name',
		'nickname',
		'email',
		'is_active',
		'password',
		'commission_type',
        'commission_coin',
        'commission_rate',
        'warning_line',
        'close_out_line',
		]

	def validata(self, attrs):
		pass 

	def update(self, instance, validated_data):
        password = validated_data.pop('password', '')
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class TraderSerializer(UserSerializer):

	def create(self, validated_data):
		# superior = self.context['superior']
		pass
