from django.urls import path
from .views import *
urlpatterns = [
    path('', Product_Page, name="Product"),
    path('detail/<int:pk>/', Detail_Product, name="Product_Detail"),
    path('update/<int:pk>/', Update_Product, name="Product_Update"),
    path('delete/<int:pk>/', Delete_Product, name="Product_Delete"),
    path('Category/', Category_Page, name="Category"),
    path('search_product/', Search_Product, name="Search_Product"), 
]