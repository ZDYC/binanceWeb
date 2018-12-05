from django.contrib.auth.models import UserManager
from django.db.models import Q


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, name, password, **extra_field):
        if not name:
            raise ValueError('The given name must be set!')
        user = self.model(name=name, **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, password=None, **extra_field):
        extra_field.setdefault('is_staff', False)
        extra_field.setdefault('is_superuser', False)
        return self._create_user(name, password, **extra_field)

    def create_superuser(self, name, password, **extra_field):
        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_superuser', True)

        if extra_field.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_field.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(name, password, **extra_field)


class AdminManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)


class TraderManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            Q(is_staff=False) | Q(account__isnull=False))