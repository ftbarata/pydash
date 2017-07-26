from django.db import models


class Message(models.Model):

    message = models.TextField('Mensagem', max_length=1000)
    detailed_message = models.TextField('Mensagem técnica detalhada', max_length=1000)
    author = models.CharField('Autor', max_length=100, default='Sistema')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    severity = models.CharField('Severidade', max_length=20)

    class Meta:
        verbose_name = 'mensagem'
        verbose_name_plural = 'mensagens'


class Group(models.Model):
    name = models.CharField('Grupos', max_length=50, unique=True)
    messages = models.ManyToManyField(Message, blank=True)

    def clean(self):
        super(Group, self).clean()
        self.name = self.name.capitalize()

    class Meta:
        verbose_name = 'grupo'
        verbose_name_plural = 'grupos'

    def __str__(self):
        return self.name
