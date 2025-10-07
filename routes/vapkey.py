from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64

def b64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

private_key_bytes = private_key.private_numbers().private_value.to_bytes(32, "big")
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)

print("VAPID PRIVATE KEY:", b64url(private_key_bytes))
print("VAPID PUBLIC KEY:", b64url(public_key_bytes))
