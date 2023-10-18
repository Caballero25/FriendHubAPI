# Generated by Django 4.2.5 on 2023-10-17 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0007_remove_publication_reactions_alter_category_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='publication',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='publication',
            old_name='create_at',
            new_name='created_at',
        ),
    ]