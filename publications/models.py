from django.db import models
from users.models import User

# Create your models here.


class Publication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=280, blank=True, null=True)
    multimedia = models.URLField(null=True, blank=True )
    gif = models.URLField(null=True, blank=True )
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20)
    def __str__(self):
        return "id: {} | user: {} | create: {}".format(self.id, self.user, self.create_at)
    class Meta:
        ordering = ['-created_at']
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE, related_name='comentarios')
    body = models.CharField(max_length=280, blank=True, null=True)
    multimedia = models.URLField(null=True, blank=True )
    created_at = models.DateTimeField(auto_now_add=True)
    reactions = models.ManyToManyField('Reaction', blank=True, related_name='comments_reacted')

    def __str__(self):
        return f"Comentario por {self.user.full_name()} en la publicación #{self.publication.id}"
    class Meta:
        ordering = ['-created_at']

class Reaction(models.Model):
    MARAVILLOSO = 'Maravilloso'
    ENTRETENIDO = 'Entretenido'
    DIVERTIDO = 'Divertido'

    PIENSO_IGUAL = 'Pienso Igual'
    IMPRESIONANTE = 'Impresionante'
    MOTIVADOR = 'Motivador'

    TIPOS_DE_REACCIONES = [
        (MARAVILLOSO, 'Maravilloso'),
        (ENTRETENIDO, 'Entretenido'),
        (DIVERTIDO, 'Divertido'),

        (PIENSO_IGUAL, 'Pienso Igual'),
        (IMPRESIONANTE, 'Impresionante'),
        (MOTIVADOR, 'Motivador'),
    ]

    type = models.CharField(max_length=20, choices=TIPOS_DE_REACCIONES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='publication_reactions')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='comment_reactions')

    def __str__(self):
        if self.publication:
            return "(Publicación) {} | {} - {}".format(self.publication.id, self.type, self.user.full_name())
        elif self.comment:
            return "(Comentario) {} | {} - {}".format(self.comment.id, self.type, self.user.full_name())
        else:
            return "Reacción sin publicación ni comentario asociado"

class Category(models.Model):
    ENTRETENIMIENTO = 'Entretenimiento'
    DESARROLLO = 'Desarrollo'

    TIPOS_DE_CATEGORIAS = [
        (ENTRETENIMIENTO, 'Entretenimiento'),
        (DESARROLLO, 'Desarrollo'),
    ]
    type = models.CharField(max_length=20, choices=TIPOS_DE_CATEGORIAS, unique=True)

    def __str__(self):
        return self.type