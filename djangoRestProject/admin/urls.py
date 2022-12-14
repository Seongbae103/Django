"""admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from admin.views import hello

urlpatterns = [
    path('', hello),
    path('blog/auth/', include('blog.b_users.urls')),
    #path('blog/stroke/', include('blog.stroke.urls')),
    path('dlearn/', include('basic.dlearn.urls')),
    path('webcrawler/', include('basic.webcrawler.urls')),
    path('imdb/', include('basic.nlp.urls')),
    path('imdb/', include('basic.nlp.urls')),
    path('security/', include('security.users.urls')),

]
