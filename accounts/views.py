from typing import Any, Optional
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from django.db.models import Q
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from django.urls import reverse_lazy
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import (
    AllowAny,
)
from . serializers import (
    RegisterSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response("User created successfully"),
            400: openapi.Response("Bad request"),
        })
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)