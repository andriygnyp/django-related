from django.urls import path

from . import views

urlpatterns = [
    path('', views.Categories.as_view()),
    path('<int:category_id>', views.Categories.as_view()),
]
