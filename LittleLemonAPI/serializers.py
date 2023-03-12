from rest_framework import serializers
from LittleLemonAPI.models import MenuItem, Category, Cart, Order, OderItem
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
  category = serializers.StringRelatedField(read_only=True)
  category_id = serializers.IntegerField(write_only=True)

  class Meta:
    model = MenuItem
    fields = ['title', 'price', 'featured', 'category', 'category_id']

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']


class UserNameSerializer(serializers.Serializer):
  username =  serializers.CharField(max_length=200)


  def create(self, validated_data):
    user = get_object_or_404(User, **validated_data)
    if not user.groups.filter(name=self.context['search_by']).exists():
      group, created = Group.objects.get_or_create(name=self.context['search_by'])
      user.groups.add(group)
    return user




class CartSerializer(serializers.ModelSerializer):
  menuitem = serializers.StringRelatedField(read_only=True)
  menuitem_id = serializers.IntegerField(write_only=True)
  user = serializers.HiddenField(default=serializers.CurrentUserDefault())

  class Meta:
    model = Cart
    fields = ['user', 'menuitem', 'unit_price', 'price', 'quantity', 'menuitem_id']
    extra_kwargs = {
      'unit_price': {'read_only': True },
      'price': {'read_only': True }, 
      'quantity': {'required': True}
    }


class OderItemSerilizer(serializers.ModelSerializer):

  class Meta:
    model = OderItem
    fields = ['menuitem', 'quantity', 'unit_price', 'price']


class OrderSerilizer(serializers.ModelSerializer):
  user = serializers.StringRelatedField(read_only=True)
  delivery_crew = serializers.StringRelatedField(read_only=True) 
  order_items = OderItemSerilizer(source='oderitem_set', many=True, read_only=True)

  class Meta:
    model = Order
    fields = ['user', 'delivery_crew', 'status', 'total', 'date', 'order_items']


 
  def create(self, validated_data):
    print(validated_data)
    user = self.context['request'].user
    order = Order.objects.create(user= user, **validated_data)
    for cart in Cart.objects.filter(user=user):
      OderItem.objects.create(
        order= order,
        menuitem = cart.menuitem,
        quantity = cart.quantity, 
        unit_price = cart.unit_price,
        price = cart.price
      )
    Cart.objects.filter(user=user).delete()
    return order
