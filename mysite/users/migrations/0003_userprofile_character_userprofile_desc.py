# Generated by Django 4.1 on 2024-01-19 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_emailverifyrecord_alter_userprofile_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='character',
            field=models.CharField(blank=True, default='还没想好！', max_length=100, verbose_name='个性签名'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='desc',
            field=models.TextField(blank=True, default='平平无奇的咸鱼', max_length=200, verbose_name='个人简介'),
        ),
    ]
