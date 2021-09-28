from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model,login,logout
from django.views.decorators.csrf import csrf_exempt
import re
import random
# Create your views here.


def generate_ssesson_token(length=10):
    return "".join(random.choice([chr(i) for i in range(97,123)]+[chr(j) for j in range(65,91)]+ [str(k) for k in range(0,10)]) for _ in range(length))

@csrf_exempt
def signin(request):
    if not request.method=='POST':
        return JsonResponse({'error':"send a post request with valid parameter only"})

    username=request.POST['email']
    password=request.POST['password']

# validationpart

    # if not re.match("\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b",username):
    #     return JsonResponse({'error':'enter a valid email'})

    # if (len(password)<7):
    #     return JsonResponse({'error':'password must be atleast 7 character long'})
    
    UserModel=get_user_model()

    try:
        user=UserModel.objects.get(email=username)
        
        if user.check_password(password):
            usr_dict=UserModel.objects.filter(email=username).values().first()
            usr_dict.pop('password')

            if user.sesson_token !='0':
                user.sesson_token="0"
                user.save()
                return JsonResponse({"error":"Previous sessson already exists"})

            token=generate_ssesson_token()
            user.sesson_token=token
            user.save()
            login(request,user)
            return JsonResponse({"token":token,"user":usr_dict})

        else:
            return JsonResponse({"error":"Invalid password"})

    except UserModel.DoesNotExist:
        return JsonResponse({'error':'invalid email'})


@csrf_exempt
def signout(request,id):
    logout(request)
    
    UserModel=get_user_model()

    try:
        user=UserModel.objects.get(pk=id)
        user.sesson_token="0"
        user.save()
    except UserModel.DoesNotExist:
        return JsonResponse({"error":"Invalid user ID"})
    
    return JsonResponse({"success":"Logout success"})



class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action={"create":[AllowAny]}

    queryset=CustomUser.objects.all().order_by('id')
    serializer_class=UserSerializer

    def get_permission(self):
        try:
            return [permission() for permission in self.permission_classes_by_action]
        except KeyError:
            return [permission() for permission in self.permission_classes]