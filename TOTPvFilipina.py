import hashlib 
import hmac 
import math 
import time
import base64

length = 6
key = b"123123123djwkdhawjdk"
step_in_seconds = 30 

t = math.floor(time.time() // step_in_seconds)

hmac_object = hmac.new(key, t.to_bytes(length=8, byteorder="big"), hashlib.sha1)
hmac_sha1 = hmac_object.hexdigest()
print(key)
print(t.to_bytes(length=8, byteorder="big"))
token = base64.b32encode(key)
print(token.decode("utf-8"))
print(hmac_sha1)


# truncate to 6 digits
offset = int(hmac_sha1[-1], 16)
print(offset)
binary = int(hmac_sha1[(offset * 2):((offset * 2) + 8)], 16) & 0x7fffffff
print(hmac_sha1[(offset * 2):((offset * 2) + 8)])
totp = str(binary)[-length:]
print(totp)
