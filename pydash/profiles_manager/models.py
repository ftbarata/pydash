from django.conf import settings
from django.db import models
from pydash.core.models import Group as MessageGroup


class UserProfile(models.Model):
    photo = models.ImageField('Foto de perfil', blank=True, null=True, upload_to=settings.UPLOAD_TO_PROFILE_MODEL_IMAGE_FIELD_NAME)
    username = models.CharField('Usuário', max_length=30)
    email = models.EmailField(max_length=50)
    lotacao = models.CharField('Lotação', max_length=20)
    phone = models.CharField('Telefone', max_length=15)
    description = models.TextField('Descrição', max_length=300, blank=True, null=True)
    notification_groups = models.ManyToManyField(MessageGroup, verbose_name='Grupos de notificação de e-mail', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

