import razorpay
from dotenv import load_dotenv
import os
from rest_framework.serializers import ValidationError
from rest_framework import status


load_dotenv()
razor_pay_id = os.environ.get('RAZOR_PAY_ID')
secret = os.environ.get('SECRET_KEY')

client = razorpay.Client(auth=(razor_pay_id, secret))

def create_order(amount,currency):
    data = {
        "amount":amount,
        "currency":currency,
        # "receipt":order_id
    }
    try:
        payment = client.order.create(data=data)
        return payment
    except Exception as e:
        raise ValidationError(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "msg": e
            }
        )

def verify_payment_signature(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
    try:
        verify_signature = client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
        return verify_signature
    except Exception as e:
        raise ValidationError(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": e
            }
        )