# Generated by Django 4.2.5 on 2023-10-14 16:53

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publications', '0004_alter_reaction_type_comentario'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comentario',
            new_name='Comment',
        ),
    ]