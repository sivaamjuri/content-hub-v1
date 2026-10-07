from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status
from .models import Category, ArticlePage
from .serializers import CategorySerializer, ArticleSerializer


class ArticleListView(APIView):
    """
    GET /api/articles/
    Public endpoint — consumed by React / Next.js frontend (no auth required).
    Returns lightweight listing of all published ArticlePages.
    Full content (StreamField body) is served via Wagtail API v2.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        articles = ArticlePage.objects.live().public().select_related('category')
        serializer = ArticleSerializer(articles, many=True)
        return Response({
            'count': articles.count(),
            'results': serializer.data
        })


class CategoryListView(APIView):
    """
    GET  /api/categories/   — list all categories (authenticated editors only)
    POST /api/categories/   — create a new category (admin only)

    Demonstrates layered permission approach:
    - GET: IsAuthenticated
    - POST: IsAdminUser
    """

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CategoryDetailView(APIView):
    """
    GET    /api/categories/<id>/  — retrieve (authenticated)
    PUT    /api/categories/<id>/  — update (admin only)
    DELETE /api/categories/<id>/  — delete (admin only)

    Demonstrates object-level permission pattern.
    """

    def get_permissions(self):
        if self.request.method in ('PUT', 'DELETE'):
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        cat = self.get_object(pk)
        if not cat:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(CategorySerializer(cat).data)

    def put(self, request, pk):
        cat = self.get_object(pk)
        if not cat:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(cat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cat = self.get_object(pk)
        if not cat:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
