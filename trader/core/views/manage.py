import logging

from django_framework import viewsets
from django_framework.permissions import IsAuthenticated, IsAdminUser
from django_framework.reponse import Response
from django_framework.viewsets import GenericViewSet

from . serializers import UserSerializer, TraderSerializer


log = logging.getLogger(__name__)


class UserViewSet(viewsets.GenericViewSet):
	serializer_class = UserSerializer
	permission_classes = [IsAuthenticated]

	def list(self, request, *args, **kwargs):
		serializer = UserSerializer(request.user)
		return Response(serializer.data)


class TraderViewSet(GenericViewSet):
	serializer_class = TraderSerializer
	permission_classes = [IsAuthenticated, IsAdminUser]

	def get_queryset(self):
		user = self.request.user

	def update(self, request, *args, **kwargs):
		pass