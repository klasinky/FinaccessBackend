from django.db.models.signals import post_save
import requests
import sys
from api.serializers.notifications import NotificationModelSerializer
from app import settings
from core.models import Post, Notification, Comment, UserFollowing
from rest_framework.authtoken.models import Token


def post_created(sender, instance, created, **kwargs):
    if not created: return
    followers = instance.author.followers.all()
    for follower in followers:
        notification = Notification.objects.create(
            to_user=follower.user,
            id_type=instance.pk,
            from_user=instance.author,
            notification_type='post',
            content='ha creado un post.'
        )
        serializer = NotificationModelSerializer(notification).data
        send_ws_info(serializer, follower.user.id)


def comment_created(sender, instance, created, **kwargs):
    if not created or instance.author == \
            instance.post.author:
        return
    notification = Notification.objects.create(
        to_user=instance.post.author,
        id_type=instance.post.pk,
        from_user=instance.author,
        notification_type='comment',
        content='ha realizado un comentario en tu post.'
    )
    serializer = NotificationModelSerializer(notification).data
    send_ws_info(serializer, instance.post.author.id)


def following_created(sender, instance, created, **kwargs):
    if not created: return
    notification = Notification.objects.create(
        to_user=instance.following,
        id_type=instance.user.pk,
        from_user=instance.user,
        notification_type='follow',
        content='ha comenzado a seguirte.'
    )
    serializer = NotificationModelSerializer(notification).data
    print("Instance Following, ", instance.following)
    send_ws_info(serializer, instance.following.id)


if 'test' not in sys.argv:
    post_save.connect(post_created, sender=Post)
    post_save.connect(comment_created, sender=Comment)
    post_save.connect(following_created, sender=UserFollowing)


def send_ws_info(serializer, id):
    url = f'{settings.WS_URL}/notify/{id}'
    token, created = Token.objects.get_or_create(user__id=id)
    headers = {'Authorization': f'Token {token.key}'}
    requests.post(url=url, json=serializer, headers=headers)
