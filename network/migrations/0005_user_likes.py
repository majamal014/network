# Generated by Django 4.0.5 on 2022-07-17 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_user_followers_user_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_users', to='network.post'),
        ),
    ]
