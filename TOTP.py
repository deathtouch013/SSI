#https://www.rfc-editor.org/rfc/rfc6238.html#appendix-A
import hmac
import hashlib

#se hara modulo con el valor correspondiente y marcara cuantos digitos se devuelven
DIGITOS_MAXIMOS = [1,10,100,1000,10000,100000,100000,1000000]
ALGORITMOS_HASH = {'HmacSHA1': hashlib.sha1,'HmacSHA256':hashlib.sha256,'HmacSHA512':hashlib.sha512}

def hmac_sha(algoritmo,keyBites,text):
    return hmac.new(keyBites,text,ALGORITMOS_HASH.get(algoritmo))


def strToHex(str):
    return int(str,16)

def hexToBin(hex):
    return bin(int(hex, 16))[2:].zfill(8)

def strToBin(str):
    return str.encode('ascii')

#key es el codigo en hexadecimal(se pasa en string)
#time es el tiempo en hexadecimal(se pasa en string)
#returnDigits es el numero de digitos que devuelve el codigo en base 10
#cryto es el algoritmo de hash con el que se "cifra" (string) ["HmacSHA1","HmacSHA256","HmacSHA512"]
def generateTOTP(key, time, returnDigits, crypto):
    #TODO pasar returnDigits a int
    maxDigitos = int(returnDigits)

    #TODO asegurar que time tiene 16 caracteres, sino se añade 0
    while len(time) < 16:
        time = "0" + time
    #TODO pasar key y time a hexadecimal
    msg = hexToBin(time)
    k = hexToBin(key)

    #hash = hmac_sha(crypto,k,msg)
    hash = hmac.new(k,msg,ALGORITMOS_HASH.get(crypto))

    offset = hash[len(hash)] & 0xf

    binary = (hash[offset] & 0x7f) << 24
    binary = binary | (hash[offset +1] & 0xff) << 16
    binary = binary | (hash[offset +2] & 0xff) << 8
    binary = binary | (hash[offset +3] & 0xff)

    otp = binary % DIGITOS_MAXIMOS[maxDigitos]

    #TODO pasar otp a string
    result = str(otp)

    #TODO asegurarse de que string tiene el numero de caracteres adecuado
    while len(result) < returnDigits:
        result = "0" + result

    return result