from django.urls import path, include
from rest_framework.routers import DefaultRouter
from LittleLemonAPI.views import MenuItemsViewSet, MangerViewSet, DeliveryCrewViewSet, CartViewSet,OrdersViewSet

router = DefaultRouter()
router.register('menu-items', MenuItemsViewSet)
router.register('groups/manager/users', MangerViewSet, basename='mangers')
router.register('groups/delivery-crew/users', DeliveryCrewViewSet, basename='delivery-crew')
urlpatterns = router.urls

urlpatterns += [
    path('cart/menu-items', CartViewSet.as_view({'post': 'create', 'get':'list', 'delete':'destroy'}), name='create-cart'),
    path('orders', OrdersViewSet.as_view({'get':'list', 'post': 'create'}), name='orders'),
    path('orders/<int:order_id>', OrdersViewSet.as_view({'get': 'retrieve'}))
]