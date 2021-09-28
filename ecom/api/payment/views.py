from django.shortcuts import render
from django.http import HttpRequest,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import braintree

# Create your views here.
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="7gnb7ks9qzdkhv8j",
        public_key="4ytqf75bx6c4hqmf",
        private_key="e421066e923370a49eea25e3aa3ac6e7def"
    )
)

def validate_user_session(id,token):
    UserModel=get_user_model()

    try:
        user=UserModel.objects.get(pk=id)
        if user.sesson_token== token:
            return True
        else:
            return False
    except UserModel.DoesNotExist:
        return False



@csrf_exempt
def generate_token(request,id,token):
    if not validate_user_session(id,token):
        return JsonResponse({"error":"Invalid session please login again"})
    
    return JsonResponse({"clientToken":gateway.client_token.generate({"customer_id": id}),"success":True})


@csrf_exempt
def process_payment(request,id,token):
    if not validate_user_session(id,token):
        return JsonResponse({"error":"Invalid session please login again"})\
    
    nonce_from_the_client=request.POST["paymentMethodNonce"]
    amount_from_the_client=request.POST["amount"]

    result = gateway.transaction.sale({
    "amount": amount_from_the_client,
    "payment_method_nonce": nonce_from_the_client,
    "options": {
      "submit_for_settlement": True
    }
})

    if result.is_success:
        return JsonResponse({"success":result.is_success,"transction":{"id":result.transction.id,"amount":result.transction.amount}})

    else:
        return JsonResponse({"error":True,"success":False})
