from rest_framework import viewsets
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .serializers import OrderSerializer
from .models import Order
from django.views.decorators.csrf import csrf_exempt
# Create your views here.



def validate_user_session(id,token):
    UserModel=get_user_model()

    try:
        user=UserModel.objects.get(pk=id)
        if (user.sesson_token == token) :
            return True
        else:
            return False
    except UserModel.DoesNotExist:
        return False


@csrf_exempt
def add(request,id,token):
    if not validate_user_session(id,token):
        return JsonResponse({"error":"Please login first to continue","code":"500"})

    if request.method == "POST":
        user_id=id
        transaction_id=request.POST["transaction_id"]
        amount=request.POST["amount"]
        products=request.POST["products"]
        
        total_pro=len(products.split(",")[:-1])

        UserModel=get_user_model()

        try:
            user=UserModel.objects.get(pk=id)
        except UserModel.DoesNotExist:
            return JsonResponse({"error":"User does not exist"})

        ordr=Ordew(user=user,product_names=products,transaction_id=transaction_id,total_products=total_pro,total_amount=amount)

        ordr.save()
        return JsonResponse({"success":True,"error":False,"msg":"Order placed successfully"})

        class OrderViewSet(viewsets.ModelViewSet):
            queryset=Order.objets.all().order_by("id")
            serializer_class=OrderSerializer


