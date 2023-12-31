from django.urls import path

from blog import views

urlpatterns =[
    path('', views.post_list, name='post_list'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('posts/<int:id>/edit', views.post_edit, name='post_edit'),
    path('posts/<int:id>/publish', views.post_publish, name='post_publish'),
    path('posts/<int:id>/add_comment', views.add_comment, name='add_comment'),
    path('posts/add/', views.post_edit, name='post_add'),
]
