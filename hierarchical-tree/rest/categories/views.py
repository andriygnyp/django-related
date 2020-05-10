import json

from django.http import (JsonResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseServerError)
from django.shortcuts import get_object_or_404
from django.views import View

from .models import create_tree, Category


class Categories(View):
    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Category, pk=kwargs.get('category_id'))
        return JsonResponse(item.tree_view())

    def post(self, request, *args, **kwargs):
        if args or kwargs:
            return HttpResponseNotAllowed('Invalid parameter(s) in URL')

        try:
            data = json.loads(request.body)
        except Exception as e:
            print(f'Error loading POST body, {e}')
            return HttpResponseBadRequest('Invalid JSON')

        try:
            count = create_tree(data)
        except Exception as e:
            return HttpResponseServerError(f'{e}')

        return JsonResponse({'count': count}, status=201)
