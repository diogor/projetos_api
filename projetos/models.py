from django.db import models
from django.conf import settings


class ProjetoQuerySet(models.QuerySet):
    def for_user(self, user):
        user_projects = user.membro_de.all()
        created_projects = user.projetos.all()
        return (user_projects | created_projects).distinct()


class Projeto(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    team = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                  related_name='membro_de',
                                  blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='projetos', on_delete=models.CASCADE)

    objects = ProjetoQuerySet.as_manager()

    def __str__(self):
        return self.title
