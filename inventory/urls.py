from django.urls import path
from .views import *

urlpatterns = [

    path('add-single-inventory-item', AddInventoryItem.as_view(), name ='add-single-inventory-item'),
    path('edit-inventory-item/<str:id>', EditInventoryItem.as_view(), name ='edit-inventory-item'),
    path('delete-inventory-item/<str:id>', DeleteInventoryItem.as_view(), name ='delete-inventory-item'),
    path('add-category', AddNewCategory.as_view(), name='add-category'),
    path('delete-category/<str:id>', DeleteCategory.as_view(), name ='delete-category'),
    path('edit-category/<str:id>', EditCategory.as_view(), name ='edit-category'),
    path('add-warehouse', AddWarehouse.as_view(), name ='add-warehouse'),
    path('edit-warehouse/<str:id>', EditWarehouse.as_view(), name ='edit-warehouse'),
    path('delete-warehouse/<str:id>', DeleteWarehouse.as_view(), name ='delete-warehouse'),
    path('add-rack', AddRack.as_view(), name ='add-rack'),
    path('delete-rack/<str:id>', DeleteRack.as_view(), name ='delete-rack'),
    path('edit-rack/<str:id>', EditRack.as_view(), name ='edit-rack'),
    path('get-warehouse-rack/<str:name>', GetWarehouseRack.as_view(), name ='get-warehouse-rack'),

]