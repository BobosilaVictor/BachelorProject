from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('items/<str:item_name>/', views.render_items, name='device'),
    path('groups/<str:group_name>/', views.render_groups, name='group'),
    path('groups/', views.groups, name='groups')
]