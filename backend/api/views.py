from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import IngredientFilter, RecipeFilter
from api.models import (Favorite, Ingredient, IngredientQnt, Recipe,
                        ShoppingList, Tag)
from api.pagination import PageNumberPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeListSerializer, RecipeWriteSerializer,
                             ShoppingListSerializer, TagSerializer)


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    filter_backends = [IngredientFilter]
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeWriteSerializer

    def add_and_delete(self, request, pk, serializer, model):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            recipe, created = model.objects.get_or_create(
                user=user, recipe=recipe
            )
            if created:
                serializer = serializer()
                return Response(
                    serializer.to_representation(instance=recipe),
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Рецепт уже добавлен'},
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            model.objects.filter(
                user=user, recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['DELETE', 'POST'],
        permission_classes=[IsAuthenticated],
        url_path='favorite'
    )
    def favorite(self, request, pk):
        return (self.add_and_delete(request, pk, FavoriteSerializer, Favorite))

    @action(
        detail=True,
        methods=['DELETE', 'POST'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        return (self.add_and_delete(request, pk, ShoppingListSerializer,
                ShoppingList))

    @action(
        methods=['get'], detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientQnt.objects.filter(
            recipe__shoppinglist__user=request.user.id
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(total=Sum('amount'))
        shopping_cart = '\n'.join([
            f'{ingredient["ingredient__name"]} - {ingredient["total"]}/'
            f'{ingredient["ingredient__measurement_unit"]}'
            for ingredient in ingredients
        ])
        filename = 'shopping_cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
