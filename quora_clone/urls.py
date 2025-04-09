from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post/', views.post_question, name='post_question'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('like/<int:answer_id>/', views.like_answer, name='like_answer'),
    path('delete-question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('delete-answer/<int:answer_id>/', views.delete_answer, name='delete_answer'),
]