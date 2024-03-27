from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import (
    generics,
    views,
    permissions,
    response,
    status,
    decorators)

from .models import Shop, ShopOwner
from Accounts.models import Company, CustomUser
from .serializers import *
from MarketPlace.views import ProductsListBaseView
from helpers.err_response import CustomErrorResponse
from helpers.pagination import PaginatorGenerator

class ShopsListBaseView(generics.ListAPIView):
    """ List All Products """
    serializer_class = ShopSerializer
    permission_classes = []  
    pagination_class = PaginatorGenerator()(_page_size=15)   

    def get_shops(self, request, filters, message):
        try:
            queryset = Shop.objects.filter(**filters).order_by('-updated_at')
            serializer = ShopSerializer(queryset, many=True)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.serializer_class(queryset, many=True)
            
            # self.get_paginated_response(serializer.data)
            
            response_data = {
                "status_code": status.HTTP_200_OK,
                "message": message,
                "count": len(serializer.data),
                "data": serializer.data,
                "status": "success",
            }

            return response.Response(response_data, status=status.HTTP_200_OK)
        except Http404:
            return CustomErrorResponse(status.HTTP_404_NOT_FOUND, "Shop Not Found")
        except Exception as e:
            return CustomErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                   f"An error occurred while retrieving {message}: {str(e)}")

class ShopListView(ShopsListBaseView):
    """ List all shops available """

    @swagger_auto_schema(tags=['Shops'])
    def list(self, request):
        shops = self.get_shops(request, {}, "All Shops")
        if shops:
            return shops
        else:
            return CustomErrorResponse(status.HTTP_404_NOT_FOUND, "Shop not found")
        
class CompanyShopListView(ShopsListBaseView):
    """ List all shops available """

    @swagger_auto_schema(tags=['Shops'])
    def list(self, request, company_id):
        current_company = Company.objects.get(id=company_id)
        shops = self.get_shops(
            request,
            {
                'company': current_company,
            },
            "All Shops")
        if shops:
            return shops
        else:
            return CustomErrorResponse(status.HTTP_404_NOT_FOUND, "Shop not found")

class ShopDetailView(generics.GenericAPIView):
    """ A single Product detail """
    serializer_class = ShopSerializer
    permission_classes = []

    @swagger_auto_schema(tags=['Shops'])
    def get(self, request, shop_id):
        try:
            shop = Shop.objects.get(id=shop_id)
            serializer = ShopSerializer(shop)

            response_data = {
                    "status_code": status.HTTP_200_OK,
                    "data": serializer.data,
                    "status": "success",
                }
        
            return response.Response(response_data, status=status.HTTP_200_OK)
        except Http404:
            return CustomErrorResponse(status.HTTP_404_NOT_FOUND, "Shop Not Found")
        except Exception as e:
            return CustomErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                   f"An error occurred while retrieving Shop with id-{shop_id}: {str(e)}")               
        
class ShopProductListView(ProductsListBaseView):
    """ List Products in the the shop """

    @swagger_auto_schema(tags=['Shops'])
    def list(self, request, shop_id):
        current_shop = Shop.objects.get(id=shop_id)
        products = self.get_products(
            request,
            {
                'shop': current_shop,
            },
            "Shop Products")
        if products:
            return products
        else:
            return CustomErrorResponse(status.HTTP_404_NOT_FOUND, "Product not found") 
