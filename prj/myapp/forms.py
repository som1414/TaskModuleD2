from django.forms import ModelForm, BooleanField  # ,EmailField, CharField
from .models import Post  # Category, Author
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User


class NewForm(ModelForm):
    check_box = BooleanField(label='Согласен!')

    class Meta:
        model = Post
        fields = ['author', 'categorySort', 'postCategory', 'rating']


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

# class BaseRegisterForm(UserCreationForm):
#     email = EmailField(label="Email")
#     first_name = CharField(label="Имя")
#     last_name = CharField(label="Фамилия")
#
#     class Meta:
#         model = User
#         fields = ("username",
#                   "first_name",
#                   "last_name",
#                   "email",
#                   "password1",
#                   "password2", )
