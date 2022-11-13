#https://www.rfc-editor.org/rfc/rfc6238.html#appendix-A
import hmac
import hashlib
import time
import base64

#se hara modulo con el valor correspondiente y marcara cuantos digitos se devuelven
DIGITOS_MAXIMOS = [10,100,1000,10000,100000,1000000,1000000,10000000,100000000,1000000000,10000000000]
ALGORITMOS_HASH = {'SHA1': hashlib.sha1,'SHA256':hashlib.sha256,'SHA512':hashlib.sha512}

def hmac_sha(algoritmo,keyBites,text):
    return hmac.new(keyBites,text,ALGORITMOS_HASH.get(algoritmo))


def stringToHex(string):
    hexadecimal = []
    for i in string:
        hexadecimal.append(format(ord(i), "x"))
    return hexadecimal
    
def listHexToBin(hexa):
    binario = []
    for i in hexa:
        binario.append(bin(int(i, 16))[2:].zfill(8))
    return binario

def hexListing(hexa):
    lista = []
    cnt = 0
    hexadecimal = str(hexa)
    if(len(hexadecimal) % 2 == 1):
        hexadecimal = "0" + hexadecimal
    while cnt < len(hexadecimal):
        lista.append(hexadecimal[cnt] + hexadecimal[cnt + 1])
        cnt = cnt + 2
    return lista

def listConcatBin(lista):
    string = ""
    for i in lista:
        string = string + i
    return string


#key es el codigo en hexadecimal(se pasa en string)
#time es el tiempo en hexadecimal(se pasa en string)
#returnDigits es el numero de digitos que devuelve el codigo en base 10
#cryto es el algoritmo de hash con el que se "cifra" (string) ["HmacSHA1","HmacSHA256","HmacSHA512"]
def generateTOTP(key, counter, returnDigits, crypto):
    maxDigitos = int(returnDigits)

    while len(counter) < 16:
        counter = "0" + counter

    msgBin = bytes.fromhex(counter)
    kBin = bytes.fromhex(key)

    #kBin = b"123123123djwkdhawjdk"

    hash_hmac = hmac.new(kBin,msgBin,ALGORITMOS_HASH.get(crypto))
    hash = hash_hmac.hexdigest()

    hashbin = listHexToBin(hexListing(hash))
    #hashbin = hexListing(hash[2:])

    offset = int(hashbin[len(hashbin)-1],2) & 0xf

    binary = (int(hashbin[offset],2) & 0x7f) << 24
    offset = offset + 1
    binary = binary | (int(hashbin[offset],2) & 0xff) << 16
    offset = offset + 1
    binary = binary | (int(hashbin[offset],2) & 0xff) << 8
    offset = offset + 1
    binary = binary | (int(hashbin[offset],2) & 0xff)

    otp = binary % DIGITOS_MAXIMOS[maxDigitos]

    result = str(otp)

    while len(result) < maxDigitos:
        result = "0" + result

    return result

def TOTPcodeFromUser(b32key, codeLength):

    #obtenemos clave formato hexadecimal
    hexkey = base64.b32decode(b32key).hex()

    #obtenemos contador en funcion de hora actual
    time_rn = int(time.time())
    step = int(time_rn/30)
    hex_step = format(step, 'x').upper()

    return generateTOTP(hexkey, hex_step, codeLength, 'SHA1')

#now = int(time.time())
#counter = int(now/30)

#clave: GEZDGMJSGMYTEM3ENJ3WWZDIMF3WUZDL
#TOTP = generateTOTP("313233313233313233646A776B646861776A646B", format(counter, 'x').upper(), "6", "SHA1")
#print(TOTP)

#TOTP = generateTOTP("3132333435363738393031323334353637383930", "0000000000000001", "8", "SHA1")
#print(TOTP)
#TOTP = generateTOTP("3132333435363738393031323334353637383930313233343536373839303132", "0000000000000001", "8", "SHA256")
#print(TOTP)
#TOTP = generateTOTP("31323334353637383930313233343536373839303132333435363738393031323334353637383930313233343536373839303132333435363738393031323334", str(counter), "6", "SHA512")
#print(TOTP)