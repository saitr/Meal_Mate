from django.urls import path
from apps.views.views import *
from apps.views.items_view import *
from apps.views.cart_views import *
from apps.views.order_views import *
from apps.rest_api.items import *
from apps.rest_api.users import *
from apps.rest_api.cart import *
from apps.rest_api.orders import *









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


    ############### Cart page urls ######################

    path('cart/<int:item_id>/',add_to_cart,name='cart'),
    path('cart_list/',cart_list,name='cart_list'),
    path('update_cart/<int:item_id>/',update_cart_item,name='update_cart_item'),
    path('cart_delete_all/',delete_cart_all_items,name='cart_delete_all'),
    path('delete_single_cart_item/<int:item_id>/',delete_single_cart_item,name='delete_single_cart_item'),

    ############ Order page urls #######################

   
    path('checkout/', checkout, name='order'),


    ####################### rest views ########################

    path('item_list/',ItemList.as_view(), name='Item List'),
    
    ######################## user rest view ###################

    path('rest_signup/',SignUpView.as_view(), name='rest_signup'),

    path('rest_signin/',SigninView.as_view(),name='rest_signin'),

    path('rest_logout/',LogoutView.as_view(), name='rest_logout'),

    path('rest_verify/<str:email>/',VerifyOtpView.as_view(), name='VerifyRestEmail'),

    ############################# Categories #######################

    path('rest_category/',CategoryListView.as_view(),name='rest_category'),

    ############################ Carts #############################

    path('rest_cart/<int:user_id>/',CartListView.as_view(),name='rest_cart'),

    path('restadd_cart/<int:user_id>/',CartAddView.as_view(),name='rest_cart_add'),

    path('restupdate_cart/<int:pk>/<int:user_id>/',CartItemUpdateView.as_view(),name='rest_cart_update'),

    path('delete_cart/<int:pk>/',CartDestroyView.as_view(),name='rest_cart_destroy'),

    ########################### Order Api #############################

    path('rest_order/',OrderAdd.as_view(),name="rest_order")
]