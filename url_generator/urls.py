from django.urls import path

from .views import GeneratorOfUrlsCreateView, retrieve_to_origin_url

app_name = __name__

urlpatterns = [
    path('', GeneratorOfUrlsCreateView.as_view(), name='create-new-url'),
    path('<str:generated_url>/', retrieve_to_origin_url, name='retrieve-origin-url'),
]
