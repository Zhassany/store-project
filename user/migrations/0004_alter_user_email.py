# Generated by Django 5.1.2 on 2024-11-12 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='null', max_length=254, unique=True),
            preserve_default=False,
        ),
    ]
