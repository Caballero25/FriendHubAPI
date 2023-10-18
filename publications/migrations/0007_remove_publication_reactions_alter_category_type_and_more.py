# Generated by Django 4.2.5 on 2023-10-14 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0006_comment_reactions_reaction_comment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='reactions',
        ),
        migrations.AlterField(
            model_name='category',
            name='type',
            field=models.CharField(choices=[('Entretenimiento', 'Entretenimiento'), ('Desarrollo', 'Desarrollo')], max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='category',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_reactions', to='publications.comment'),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publication_reactions', to='publications.publication'),
        ),
    ]