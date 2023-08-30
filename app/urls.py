from django.urls import path

from . import views
# url patterns

urlpatterns = [
    path('', views.user_home, name = 'user_home'),
    path('delete_image/',views.delete_image, name='delete_image'),
    path('update_checkbox/', views.update_checkbox, name='update_checkbox'),
    path('update_approve/', views.update_approve, name = 'update_approve'),
    path('approve_entire_post/', views.approve_entire_post, name='approve_entire_post'),
    path('user_form', views.edit_user_form, name = 'edit_user_form'),
    path('generate_shows/', views.generate_shows, name = 'generate_shows')
]