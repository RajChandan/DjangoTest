from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path("",views.index, name="ShopHome"),
   path("about/", views.about, name="AboutUs"),
   path("contactus/", views.contact, name="ContactUs"),
   path("tracker", views.tracker, name="TrackingStatus"),
   path("search" , views.search, name="search"),
   path("products/<int:myid>", views.productView, name="prodView"),
   path("checkout/", views.checkout, name="Checkout"),
   path("handlerequest/",views.handlerequest,name="HandleRequest")
   

]
