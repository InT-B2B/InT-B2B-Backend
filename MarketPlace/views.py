from drf_yasg.utils import swagger_auto_schema
from django.http import Http404
from rest_framework import (
    generics,
    views,
    permissions,
    response,
    status);
from .models import *
from .serializers import *
from helpers.err_response import CustomErrorResponse
from helpers.pagination import PaginatorGenerator


class ProductRecommendationView(generics.ListAPIView):
    """ List recommended Products """
    serializer_class = ProductSerializer
    permission_classes = []

    @swagger_auto_schema(tags=['MarketPlace'])
    def list(self, request):
        try:
            recommended_products = self.get_recommended_products()
            serialized_data = ProductSerializer(recommended_products, many=True).data

            response_data = {
                'status': 200,
                'success': True,
                'message': 'Recommended products',
                'data': serialized_data
            }
            return response.Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return CustomErrorResponse(status.HTTP_404_NOT_FOUND, "Product not found")

    def get_recommended_products(self):
        highest_quantity_products = self.get_products_by_highest_quantity()
        highest_discount_products = self.get_products_by_highest_discount()

        return list(
            set(
                highest_quantity_products | highest_discount_products
            )
        )[:20]

    def get_products_by_highest_quantity(self):
        return Product.objects.filter(
            admin_status='approved', is_deleted=False
        ).order_by('-quantity')[:20]
    
    def get_products_by_highest_rating(self):
        return Product.objects.filter(
            admin_status='approved', is_deleted=False
        ).order_by('-discount_price')[:20]

    def get_products_by_highest_discount(self):
        return Product.objects.filter(
            admin_status='approved', is_deleted=False
        ).order_by('-discount_price')[:20]

    """ add :
        get_products_by_highest_rating
        get_products_by_lowest_tax
    """

class ProductDetailView(generics.GenericAPIView):
    """ A single Product detail """
    serializer_class = ProductSerializer
    permission_classes = []

    @swagger_auto_schema(tags=['MarketPlace'])
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)

            response_data = {
                    "status_code": status.HTTP_200_OK,
                    "count": len(serializer.data),
                    "data": serializer.data,
                    "status": "success",
                }
        
            return response.Response(response_data, status=status.HTTP_200_OK)
        except Http404:
            return CustomErrorResponse(status.HTTP_404_NOT_FOUND, "Product Not Found")
        except Exception as e:
            return CustomErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                   f"An error occurred while retrieving Product with id-{product_id}: {str(e)}")
 

class ProductsListBaseView(generics.ListAPIView):
    """ List All Products """
    serializer_class = ProductSerializer
    permission_classes = []
    pagination_class = PaginatorGenerator()(_page_size=8)

    def get_current_category(self, category_id=None):
        try:
            return ProductCategory.objects.get(id=category_id)
        except ProductCategory.DoesNotExist:
            return None
        
    def get_current_subcategory(self, category_id=None, sub_category_id=None):
        parent_category = self.get_current_category(category_id)
        try:
            query = ProductSubCategory.objects.get(parent_category=parent_category, id=sub_category_id)
            return query
        except ProductSubCategory.DoesNotExist:
            return None        

    def get_products(self, request, filters, message):
        try:
            queryset = Product.objects.filter(**filters).order_by('-updated_at')
            page = self.paginate_queryset(queryset)
            print(page)
            
            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.serializer_class(queryset, many=True)
            # No pagination, return all data
            response_data = {
                "status_code": status.HTTP_200_OK,
                "message": message,
                "count": len(serializer.data),
                "data": serializer.data,
                "status": "success",
            }
            return response.Response(response_data, status=status.HTTP_200_OK)
        
        except Http404:
            return CustomErrorResponse(status.HTTP_404_NOT_FOUND, "Product Not Found")
        except Exception as e:
            return CustomErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                f"An error occurred while retrieving {message}: {str(e)}")

class ProductListView(ProductsListBaseView):
    """ List Products in the same category """

    @swagger_auto_schema(tags=['MarketPlace'])
    def list(self, request):
        products = self.get_products(request, {}, "All Products")
        if products:
            return products
        else:
            return CustomErrorResponse(status.HTTP_404_NOT_FOUND, "Product not found") 

class CategoryProductListView(ProductsListBaseView):
    """ List Products in the same category """

    @swagger_auto_schema(tags=['MarketPlace'])
    def list(self, request, category_id):
        current_category = self.get_current_category(category_id)
        if current_category:
            return self.get_products(
                request,
                {
                    'category': current_category,
                },
                f"{current_category} Category Products",
            )
        else:
            return CustomErrorResponse(status.HTTP_404_NOT_FOUND, "Product not found")

class SubCategoryProductListView(ProductsListBaseView):
    """ List Products in the same category """

    @swagger_auto_schema(tags=['MarketPlace'])
    def list(self, request, category_id, subcategory_id):
        current_category = self.get_current_category(category_id)
        current_sub_category = self.get_current_subcategory(category_id, subcategory_id)
        if current_category:
            return self.get_products(
                request,
                {
                    'category': current_category,
                    'sub_category': current_sub_category,
                },
                f"{current_sub_category} Sub-Category Products",
            )
        else:
            return CustomErrorResponse(status.HTTP_404_NOT_FOUND, "Product not found")              
     
        
class SimilarProductBaseView(generics.ListAPIView):
    """ Base class for listing similar products """
    serializer_class = ProductSerializer
    permission_classes = []

    def get_current_product(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

    def get_similar_products(self, filters, product_id, message):
        try:
            queryset = Product.objects.filter(**filters).exclude(id=product_id)
            similar_products = queryset[:4]
            serializer = ProductSerializer(similar_products, many=True)

            response_data = {
                "status_code": status.HTTP_200_OK,
                "message": message,
                "count": len(serializer.data),
                "data": {"products": serializer.data},
                "status": "success",
            }

            return response.Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return CustomErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                   f"An error occurred while retrieving {message}: {str(e)}")        

class SimilarProductListView(SimilarProductBaseView):
    """ List Similar Products with the currently viewed product """

    @swagger_auto_schema(tags=['MarketPlace'])
    def list(self, request, product_id):      
        current_product = self.get_current_product(product_id)
        if current_product:
            return self.get_similar_products(
                {
                    'category': current_product.category,
                    'sub_category': current_product.sub_category
                },
                product_id,
                "Similar products",
            )
        else:
            return CustomErrorResponse(status.HTTP_404_NOT_FOUND, "Product not found")
      
class LimitedOfferListView(generics.ListAPIView):
    """ List Limited Offer Products """
    serializer_class = ProductSerializer
    permission_classes = []

    @swagger_auto_schema(tags=['MarketPlace'])
    def list(self, request):
        try:
            queryset = Product.objects.filter(has_discount=True).exclude(discount_price=0.00).order_by('-updated_at')

            paginator = pagination.PageNumberPagination()
            paginator.page_size = 10
            result = paginator.paginate_queryset(queryset, request)

            req_response = {
                'success': True,
                'status': 200,
                'error': None,
                'message': 'Successfully Fetched Limited Offer Products',
                'data': self.get_serializer(result, many=True).data,
                'page_info': {
                    'count': paginator.page.paginator.count,
                    'next': paginator.get_next_link(),
                    'previous': paginator.get_previous_link(),
                }
            }

            return response.Response(req_response, status=status.HTTP_200_OK)
        except Http404:
            return CustomErrorResponse(status.HTTP_404_NOT_FOUND, "Not Found")
        except Exception as e:
            return CustomErrorResponse(status.HTTP_400_BAD_REQUEST, str(e))
        
class CategoryNameView(generics.ListAPIView):
    """
    List Category Names
    """
    serializer_class = ProductCategorySerializer
    permission_classes = []

    @swagger_auto_schema(tags=['MarketPlace'])
    def list(self, request):
        try:
            queryset = ProductCategory.objects.all()
            serializer = ProductCategorySerializer(queryset, many=True)

            response_data = {
                'status': status.HTTP_200_OK,
                'success': True,
                'message': 'Category names returned successfully',
                'data': serializer.data
            }

            return response.Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return CustomErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
        
class SubCategoryNameView(generics.ListAPIView):
    """
    List Category Names
    """
    serializer_class = ProductSubCategorySerializer
    permission_classes = []

    @swagger_auto_schema(tags=['MarketPlace'])
    def list(self, request, category_id):
        try:
            category = ProductCategory.objects.filter(id=category_id)
            queryset = ProductSubCategory.objects.filter(parent_category=category[:1])
            serializer = ProductSubCategorySerializer(queryset, many=True)

            response_data = {
                'status': status.HTTP_200_OK,
                'success': True,
                'message': 'SubCategory names returned successfully',
                'data': serializer.data
            }

            return response.Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return CustomErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, f'An unexpected error occurred')        