# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import EmailMultiAlternatives
# from .models import Post, Category
# from django.template.loader import render_to_string
# from django.contrib.auth.models import User
#
#
# @receiver(post_save, sender=Post)
# def notify_subs(sender, instance, **kwargs):
#     cat = instance.postCategory.all()
#     for c in cat:
#         for sub in c.subscribers.all():
#
#             html_content = render_to_string(
#                 'send_create.html',
#                 {'post': instance,}
#             )
#             msg = EmailMultiAlternatives(
#                 subject=f'{instance.title}',
#                 body=f'Здравствуй, {sub}! Новая статья в вашем любимом разделе! {sub_text[:50]}',
#                 from_email='som1414@yandex.ru',
#                 to=[sub.email],
#             )
#             msg.attach_alternative(html_content, 'text/html')
#             msg.send()


