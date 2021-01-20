from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('sign_in', views.sign_in),
    path('register', views.register),
    path('create_user', views.create_user),
    path('authenticate', views.authenticate),
    path('dashboard/admin', views.display_dashboard_admin),
    path('dashboard', views.display_dashboard),
    path('logout', views.logout),
    path('users/new', views.new),
    path('add_new_user', views.add_new_user),
    path('<int:user_id>/delete_user', views.delete_user),
    path('users/edit/<int:user_id>', views.display_user),
    path('users/update/<int:user_id>', views.update_user),
    path('users/change_password/<int:user_id>', views.change_password),
    path('users/edit', views.display_user_profile),
    path('users/update', views.normal_user_update),
    path('user/change_pw', views.change_pw),
    path('user/update_description', views.update_description),
    path('users/show/<int:user_id>', views.show_user_wall),
    path('users/post_message/<int:user_id>', views.create_message),
    path('users/post_comment/<int:message_id>/<int:user_id>', views.create_comment),
]