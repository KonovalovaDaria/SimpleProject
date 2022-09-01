from django.urls import path

from authors import views

app_name = 'authors'

urlpatterns = [
    path('create/', views.CreateAuthor.as_view(), name='create_author'),
    path('update/<int:author_id>/', views.UpdateAuthor.as_view(), name='update_author'),
    path('get_all/', views.GetAllAuthors.as_view(), name='get_all'),
]