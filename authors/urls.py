from django.urls import path

from authors import views

app_name = 'authors'

urlpatterns = [
    path('', views.Author.as_view(), name='author'),
    path('<int:author_id>/', views.Author.as_view(), name='author'),

    path('all/', views.GetAllAuthors.as_view(), name='all'),

    path('report/', views.GetAuthorsReport.as_view(), name='report'),
]