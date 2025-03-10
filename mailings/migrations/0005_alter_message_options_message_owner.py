# Generated by Django 5.1.6 on 2025-03-10 08:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailings", "0004_rename_campaign_campaignattempt_mailing_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="message",
            options={
                "permissions": [
                    ("view_all_messages", "Может просматривать все сообщения"),
                    ("change_all_messages", "Может редактировать все сообщения"),
                ]
            },
        ),
        migrations.AddField(
            model_name="message",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
