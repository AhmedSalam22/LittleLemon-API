from django.shortcuts import render
from rest_framework import viewsets
from LittleLemonAPI.models import MenuItem, Cart, Order
from LittleLemonAPI.serializers import MenuItemSerializer, UserSerializer, UserNameSerializer, CartSerializer, OrderSerilizer
from LittleLemonAPI.permissions import MangerMofidyOrReadOnly, MangerOnly
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth.models import Group, User
from rest_framework.response import Response
from http import HTTPStatus
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import mixins


class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset  = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [MangerMofidyOrReadOnly]


class MangerViewSet(viewsets.ViewSet):
    permission_classes  = [MangerOnly]
    search_by = 'Manger'
   
    def list(self, request):
        group = User.objects.filter(groups__name=self.search_by)
        serializer = UserSerializer(group, many=True)
        return Response(serializer.data)


    def create(self, request):
        serializer = UserNameSerializer(data=request.data,context={"search_by":self.search_by})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, 201)
    

    def destroy(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        if user.groups.filter(name=self.search_by).exists():
            group, created = Group.objects.get_or_create(name=search_by)
            group.user_set.remove(user)
        return Response(status=HTTPStatus.NO_CONTENT)

    
class DeliveryCrewViewSet(MangerViewSet):
    search_by = 'delivery crew'



class CartViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset  = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated ]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    
    def destroy(self, request, *args, **kwargs):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=204)


class OrdersViewSet(
         mixins.ListModelMixin,
         mixins.CreateModelMixin,
         mixins.RetrieveModelMixin,
         viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated ]
    serializer_class =  OrderSerilizer
    queryset = Order.objects.all()
    # ordering_fields  = ['-date']

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            return super().get_queryset().order_by('-date')
        elif user.groups.filter(name="delivery crew").exists():
            return user.order_set.all()
        return  super().get_queryset().filter(user=user).order_by('-date')
    

    def retrieve(self, request, order_id=None,  *args, **kwargs):
        order =  get_object_or_404(Order, pk=order_id, user=request.user)
        serializer = OrderSerilizer(order)
        return Response(serializer.data)


    
    
    

    
    