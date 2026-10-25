"""
URL configuration for tripwise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from tripmater.views import SignupView
from tripmater.views import TripListCreateView
from tripmater.views import TripRetriveUpdateDeleteView
from tripmater.views import AddMemberview
from tripmater.views import Expenselistcreateview
from tripmater.views import ExpenseRetriveUpdateDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/register/",SignupView.as_view()),
    path("api/trips/",TripListCreateView.as_view()),
    path("api/trips/<int:pk>/",TripRetriveUpdateDeleteView.as_view()),
    path("api/trips/<int:pk>/member",AddMemberview.as_view()),
    path("api/trips/<int:pk>/expenses/",Expenselistcreateview.as_view()),
    path("api/expenses/<int:pk>",ExpenseRetriveUpdateDeleteView.as_view()),
]
