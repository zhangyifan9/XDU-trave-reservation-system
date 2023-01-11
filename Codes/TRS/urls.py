from django.conf.urls import url

from TRS.views import *


urlpatterns = [

    # views
    url(r'cust_login$', cust_login),
    url(r'logout$', logout),
    url(r'register$', register),
    url(r'add_one_customer$', add_one_customer),
    url(r'show_customer$', show_customer),
    url(r'change_one_customer$', change_one_customer),
    url(r'delete_one_customer$', delete_one_customer),
    url(r'add_one_flight$', add_one_flight),
    url(r'show_flight$', show_flight),
    url(r'change_one_flight$', change_one_flight),
    url(r'delete_one_flight$', delete_one_flight),
    url(r'add_one_bus$', add_one_bus),
    url(r'show_bus$', show_bus),
    url(r'change_one_bus$', change_one_bus),
    url(r'delete_one_bus$', delete_one_bus),
    url(r'add_one_hotel$', add_one_hotel),
    url(r'show_hotel$', show_hotel),
    url(r'change_one_hotel$', change_one_hotel),
    url(r'delete_one_hotel$', delete_one_hotel),
    url(r'add_reservation$', add_reservation),
    url(r'show_reservation$', show_reservation),
    url(r'delete_one_reservation$', delete_one_reservation),
    url(r'show_travel_route$', show_travel_route),
    url(r'check_route$', check_route),

]