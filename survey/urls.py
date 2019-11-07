from django.urls import path
from . import views

app_name = 'survey'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:pk>/vote/', views.vote, name='vote'),
    path('new/', views.question_create, name='question_create'),
    path('<int:pk>/edit', views.question_edit, name='question_edit'),
    path('<int:pk>/delete', views.question_delete, name='question_delete'),
]