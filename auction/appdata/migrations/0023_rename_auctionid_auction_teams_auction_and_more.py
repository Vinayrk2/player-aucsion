# Generated by Django 5.0.3 on 2024-04-06 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appdata', '0022_rename_adminid_auctionadmin_adminid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction_teams',
            old_name='auctionId',
            new_name='auction',
        ),
        migrations.RenameField(
            model_name='auction_teams',
            old_name='teamId',
            new_name='team',
        ),
        migrations.RenameField(
            model_name='auctionplayer',
            old_name='auctionId',
            new_name='auction',
        ),
        migrations.RenameField(
            model_name='auctionplayer',
            old_name='playerId',
            new_name='player',
        ),
        migrations.RenameField(
            model_name='auctionplayer',
            old_name='teamId',
            new_name='team',
        ),
        migrations.RemoveField(
            model_name='auction',
            name='team',
        ),
    ]
