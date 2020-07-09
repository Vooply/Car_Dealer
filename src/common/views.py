from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.dealers.models import Dealer
from common.forms import LoginForm
from common.serializers import LoginSerializer, RegistrationSerializer


class LoginViewSimple(View):
    '''
    Simple login view without token and drf
    for working need refactoring settings
    '''

    def get(self, request):
        return render(request, "login_page.html", {"login_form": LoginForm()})

    def post(self, request):

        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("success"))

        return render(request, "login_page.html", {"login_form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'address': user.address,
        })


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'token': serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


def home(request):
    return render(request, 'home.html')


def verify(request, uuid):
    try:
        user = Dealer.objects.get(verification_uuid=uuid, is_verified=False)
    except Dealer.DoesNotExist:
        raise Http404("User does not exist or is already verified")

    user.is_verified = True
    user.save()

    return redirect('home')
