from django.db.models.signals import post_save

from core.models import Post, Notification, Comment, UserFollowing


def post_created(sender, instance, created, **kwargs):
    if not created: return
    followers = instance.author.followers.all()
    for follower in followers:
        Notification.objects.create(
            to_user=follower.user,
            id_type=instance.pk,
            from_user=instance.author,
            notification_type='post',
            content='ha creado un post.'
        )


def comment_created(sender, instance, created, **kwargs):
    if not created or instance.author == \
            instance.post.author:
        return
    Notification.objects.create(
        to_user=instance.post.author,
        id_type=instance.post.pk,
        from_user=instance.author,
        notification_type='comment',
        content='ha realizado un comentario en tu post.'
    )


def following_created(sender, instance, created, **kwargs):
    if not created: return
    Notification.objects.create(
        to_user=instance.following,
        id_type=instance.user.pk,
        from_user=instance.user,
        notification_type='follow',
        content='ha comenzado a seguirte.'
    )


post_save.connect(post_created, sender=Post)
post_save.connect(comment_created, sender=Comment)
post_save.connect(following_created, sender=UserFollowing)
