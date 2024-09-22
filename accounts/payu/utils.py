import hashlib


def generate_payu_hash(key, txnid, amount, productinfo, firstname, email, salt):
    hash_string = f"""{key} | {txnid} | {amount} | {
        productinfo} | {firstname} | {email} | | | | | | | | | | | {salt}"""
    return hashlib.sha512(hash_string.encode('utf-8')).hexdigest()


def generate_verification_hash(key, command, var1, salt):
    hash_string = f"{key}|{command}|{var1}|{salt}"
    return hashlib.sha512(hash_string.encode('utf-8')).hexdigest()
