from django.urls import path
from apps.views.views import *
from apps.views.items_view import *
from apps.views.categories_view import *
urlpatterns = [
    path('signup/',signup,name='signup'),
    path('verify/<str:email>/',verify,name='verify'),
    # path('thankyou/',index)
    path('logout/',logout_user,name='logout'),
    path('signin/',signin,name='signin'),
    # path('home/',home,name='home'),
    path('user_details/',user_details,name='user_details'),

    ###### Home pageurls
    
    path('home/',item_list,name='home'),
    path('item_not_available/',make_item_unavailable,name='make_item_unavailable'),
    path('item_available/',make_item_available,name='make_item_available'),
    path('filter/<int:category_id>/', filter_items, name='filter_items'),
    
]