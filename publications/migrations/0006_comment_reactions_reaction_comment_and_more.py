# Generated by Django 4.2.5 on 2023-10-14 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0005_rename_comentario_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reactions',
            field=models.ManyToManyField(blank=True, related_name='comments_reacted', to='publications.reaction'),
        ),
        migrations.AddField(
            model_name='reaction',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='publications.comment'),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='publication',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='publications.publication'),
        ),
    ]