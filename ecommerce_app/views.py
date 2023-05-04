from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from .models import *
import random
from .serializers import *
from django.contrib import messages
import string
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout, login
from django.http import HttpResponse, HttpResponseRedirect, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class CartAPI(APIView):
    """ This cart view are create,read,update and delete cart items """
    def get_object(self, pk):
        try:
            return Cart.objects.get(item_name=pk)
        except Cart.DoesNotExist:
            raise Http404
    def get(self, request):
        requested_user = self.request.user
        if vars(requested_user):
            queryset = Cart.objects.filter(owner=requested_user)
            serializer = CartSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            # request.session.flush()
            res = vars(request.session).get('_session_cache').values()
            print(res,'-----------------')
            return Response(res)

    def post(self, request):
        user = self.request.user
        data = request.data
        quantity = data['quantity']
        item = data['item_name']
        if request.data.get('price'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if vars(user):
            print(vars(user),'in user side',type(user))
            cart_object = Item.objects.get(pk=item)
            final_price = str(int(quantity)*int(cart_object.price))
            data['price'] = final_price
            serializer = CartSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(owner=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            """ non authenticated user add """
            print('================')
            cookie = request.session.get(str(item))
            if cookie:
                return Response('Item already in cart')
            else:
                cart_object = Item.objects.get(pk=item)
                final_price = str(int(quantity)*int(cart_object.price))
                data['price'] = final_price
                response = request.session[str(item)] = data
            # if serializer.is_valid(raise_exception=True):
            #     serializer.save()
                return Response(response, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if vars(self.request.user):
            cart_object = self.get_object(pk)
            data = request.data
            quantity = data['quantity']
            if data.get('price'):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            price = int(cart_object.item_name.price)
            final_price = str(int(quantity)*price)
            print('=======',price)
            data['price']=final_price
            serializer = CartQuantitySerializer(cart_object, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
             """ non authenticated user update """
            cart_object = Item.objects.get(pk=pk)
            cookie = request.session.get(str(pk))
            print('cookie: ',cookie)
            quantity = request.data['quantity']
            price = int(cart_object.price)
            final_price = str(int(quantity)*int(price))
            cookie['price'] = final_price
            cookie['quantity'] = quantity
            response = request.session[str(pk)] = cookie
            return Response(response)
        return Response(serializer)

    def delete(self, request, pk):
        if vars(self.request.user):
            cart_object = self.get_object(pk)
            cart_object.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        else:
             """ non authenticated user delete """
            data = request.session[str(pk)]
            if data:
                del request.session[str(pk)]
                return Response(status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryAPI(APIView):
    """ Filter all items according to category """
    def get(self, request):
        cat = request.query_params.get('category')
        queryset = Item.objects.filter(cat_name__name=cat)
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)
        