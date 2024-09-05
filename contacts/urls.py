from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    # 认证相关
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # 主要列表视图
    path('', views.contact_list_view, name='contact_list'),
    path('blacklist/', views.blacklist_view, name='blacklist'),
    path('all_todos/', views.all_todos, name='all_todos'),

    # 联系人操作
    path('add/', views.add_contact, name='add_contact'),
    path('<str:ct_id>/edit/', views.edit_contact, name='edit_contact'),
    path('<str:ct_id>/', views.contact_detail, name='contact_detail'),
    path('<str:ct_id>/block/', views.block_contact_view, name='block_contact'),
    path('<str:ct_id>/unblock/', views.unblock_contact, name='unblock_contact'),
    path('<str:ct_id>/delete/', views.delete_contact_view, name='delete_contact'),

    # 待办事项操作
    path('<str:ct_id>/add_todo/', views.add_todo, name='add_todo'),
    path('<str:ct_id>/delete_todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('<str:ct_id>/toggle_todo/<int:todo_id>/', views.toggle_todo, name='toggle_todo'),
]