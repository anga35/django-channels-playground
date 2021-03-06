# Generated by Django 4.0.5 on 2022-07-05 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_content', models.TextField()),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('chat_room', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='messages', to='chat.chatroom')),
            ],
        ),
    ]
