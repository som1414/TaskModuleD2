from django.urls import path
from .views import NewsList, NewDetail, NewCreate, NewUpdate, NewDelete, NewFilters  # ,BaseRegisterView
from .views import upgrade_me
# from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewDetail.as_view(), name='new_detail'),
    path('search/', NewFilters.as_view(), name='new_search'),
    path('add/', NewCreate.as_view(), name='new_create'),
    path('<int:pk>/edit', NewUpdate.as_view(), name='new_update'),
    path('<int:pk>/delete', NewDelete.as_view(), name='new_delete'),
    path('upgrade/', upgrade_me, name='upgrade')
    # path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    # path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
]
