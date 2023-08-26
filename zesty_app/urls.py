from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.display_menu, name='api_menu'),
    path('add_dish/', views.add_dish, name='api_add_dish'),
    path('update_dish/<int:dish_id>/', views.update_dish_availability, name='api_update_dish'),
    path('delete_dish/<int:dish_id>/', views.delete_dish, name='api_delete_dish'),

     path('signup/', views.signup, name='signup'),
     path('login/', views.login_view, name='user_login'),

    path('orders/', views.display_orders, name='api_orders'),
    path('place_order/', views.place_order, name='api_place_order'),
    path('update_order/<int:order_id>/', views.update_order_status, name='api_update_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='api_delete_order'),
    
    path('chatbot/', views.process_chatbot_message, name='chatbot_response'),

    path('save_notification/', views.save_notification, name='api_save_notification'),
    path('delete_notification/<int:notif_id>/', views.delete_notification, name='api_delete_notification'),
    path('get_notifications/', views.get_notifications, name='api_get_notifications'),

    path('feedback/', views.feedback_view, name='feedback'),
    path('allfeedbacks/', views.get_all_feedbacks, name='get_all_feedbacks'),
]
