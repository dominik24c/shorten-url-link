from django.conf import settings
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from .models import GeneratedUrls
from .serializers import GeneratedUrlsSerializer
from .url_generator import generate_url, utilize_url


class GeneratorOfUrlsCreateView(CreateAPIView):
    serializer_class = GeneratedUrlsSerializer

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            validated_url = serializer.validated_data.get('origin_url')

            origin_url = utilize_url(validated_url)
            if origin_url is None:
                origin_url = validated_url

            generated_url_obj = GeneratedUrls.objects.filter(origin_url=origin_url).first()
            if generated_url_obj is not None:
                return Response({"url": generated_url_obj.alias_url}, status=status.HTTP_200_OK)

            url = generate_url(validated_url)
            alias_url = f'{request.META.get("HTTP_HOST", settings.BASE_URL)}/{url}'
            generated_url_obj = GeneratedUrls(origin_url=origin_url, alias_url=url)
            generated_url_obj.save()

            return Response({"url": alias_url}, status=status.HTTP_201_CREATED)

        return Response({"message": "Invalid url!"}, status=status.HTTP_400_BAD_REQUEST)


def retrieve_to_origin_url(request: HttpRequest, generated_url: str) -> HttpResponse:
    generated_url_obj = GeneratedUrls.objects.filter(alias_url=generated_url).first()
    if generated_url_obj is None:
        return HttpResponse("<h1>Not found url!</h1>", status=status.HTTP_404_NOT_FOUND)
    return redirect(f'http://{generated_url_obj.origin_url}')
