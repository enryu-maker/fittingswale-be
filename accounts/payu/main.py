import requests
import hashlib
from .utils import generate_payu_hash, generate_verification_hash
from dotenv import load_dotenv
import uuid
import os
load_dotenv()
key = os.getenv("PAYU_TEST_MERCHANT_KEY")
salt = os.getenv("PAYU_TEST_MERCHANT_SALT")
payu_url = os.getenv("PAYU_TEST_URL")


def generate_payment_hash(amount: str, firstname: str, phonenumber: str, email: str, productinfo: str) -> dict[str]:

    txnid = str(uuid.uuid4())
    payu_data = {
        'key': key,
        'txnid': txnid,
        'amount': amount,
        'productinfo': productinfo,
        'firstname': 'John',
        'email': email,
        'phone': phonenumber,
        'surl': 'https://www.fittingswale.com/',
        'furl': 'https://www.fittingswale.com/',
        'hash': generate_payu_hash(key, txnid, amount, productinfo, firstname, email, salt),
        'service_provider': 'payu_paisa'
    }
    return payu_data


def verify_payment(txnid: str) -> bool:
    if txnid == "":
        return False

    command = "verify_payment"
    hash_value = generate_verification_hash(key, command, txnid, salt)

    # Data for the verification request
    data = {
        'key': key,
        'command': command,
        'hash': hash_value,
        'var1': txnid
    }

    # Send the request to PayU
    response = requests.post(
        payu_url+"/merchant/postservice?form=2", data=data)

    if response.status_code == 200:
        if response.json()["status"] == "1" and response.json()["transaction_details"][txnid]["status"] == "success":
            return True
        return False
    else:
        return False
