from django.urls import path
from .views import NewsList, NewDetail, NewCreate, NewUpdate, NewDelete, NewFilters

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewDetail.as_view(), name='new_detail'),
    path('search/', NewFilters.as_view(), name='new_search'),
    path('add/', NewCreate.as_view(), name='new_create'),
    path('<int:pk>/edit', NewUpdate.as_view(), name='new_update'),
    path('<int:pk>/delete', NewDelete.as_view(), name='new_delete'),
]
