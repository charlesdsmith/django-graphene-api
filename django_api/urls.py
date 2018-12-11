"""django_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from graphene_django.views import GraphQLView
from api import views

router = routers.DefaultRouter()
router.register(r'purchases', views.getAdesaPurchases)
router.register(r'carfax', views.GetCarFax)
router.register(r'recalls', views.Recalls)
router.register(r'adesa_run_list', views.AdesaRunList)
router.register(r'shopping_list', views.ShoppingList)

admin.autodiscover()


from rest_framework import generics, permissions, serializers

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('graphql', GraphQLView.as_view(graphiql=True)),

]


'''urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/purchases/$', views.getAdesaPurchases.as_view({'get': 'list'}), name='list'),
    url(r'^api/v1/purchases/(?P<pk>[\w-]+)/$', views.getAdesaPurchases.as_view({'get': 'retrieve'}), name='retrieve'),
    url(r'^api/v1/purchases/create/$', views.getAdesaPurchases.as_view({'post': 'create'}), name='create'),
    url(r'^api/v1/carfax/$', views.GetCarFax.as_view({'get': 'list'}), name='list'),
    url(r'^api/v1/get_carfax/(?P<pk>[\w-]+)/$', views.GetCarFax.as_view({'get': 'retrieve'}), name='retrieve'),
    url(r'^api/v1/carfax/create/$', views.PostCarFax.as_view({'post': 'create'}), name='create'),
    url('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]'''

