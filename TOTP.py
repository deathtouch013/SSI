#https://www.rfc-editor.org/rfc/rfc6238.html#appendix-A
import hmac
import hashlib
import time

#se hara modulo con el valor correspondiente y marcara cuantos digitos se devuelven
DIGITOS_MAXIMOS = [10,100,1000,10000,100000,1000000,1000000,10000000,100000000,1000000000,10000000000]
ALGORITMOS_HASH = {'HMACSHA1': hashlib.sha1,'HMACSHA256':hashlib.sha256,'HMACSHA512':hashlib.sha512}

def hmac_sha(algoritmo,keyBites,text):
    return hmac.new(keyBites,text,ALGORITMOS_HASH.get(algoritmo))

    
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




#key es el codigo en hexadecimal(se pasa en string)
#time es el tiempo en hexadecimal(se pasa en string)
#returnDigits es el numero de digitos que devuelve el codigo en base 10 (se pasa en int)
#cryto es el algoritmo de hash con el que se "cifra" (string) ["HMACSHA1","HMACSHA256","HMACSHA512"]
def generateTOTP(key, counter, returnDigits, crypto):
    #El counter tiene un tamaño maximo de 16 porque nos permite guardar valores
    #de tiempo usando 64 bits.
    while len(counter) < 16:
        counter = "0" + counter

    #pasamos a binario counter y key para cifrarlo con el algoritmo seleccionado
    msgBin = bytes.fromhex(counter)
    kBin = bytes.fromhex(key)
    hash_hmac = hmac.new(kBin,msgBin,ALGORITMOS_HASH.get(crypto))

    #en hash lo guardamos en hexadecimal
    hash = hash_hmac.hexdigest()
    #y en hashbin pasamos los valores hexadecimales de dos en dos a una lista
    #(de byte en byte) y despues esa lista la convertimos a una lista de bits
    #(tambien de byte en byte)
    hashbin = listHexToBin(hexListing(hash))

    #se obtiene el offset de los ultimos cuatro bits del hash
    offset = int(hashbin[len(hashbin)-1],2) & 0xf

    #Cogemos los cuatro bytes apartir de el offset (se ignora el ultimo bit del
    #primero, 0x7f, porque se trata con un unsigned de 31 bits segun la RFC de
    #HOTP) y formamos un int.
    binary = (int(hashbin[offset],2) & 0x7f) << 24 \
        | (int(hashbin[offset + 1],2) & 0xff) << 16 \
        | (int(hashbin[offset + 2],2) & 0xff) << 8 \
        | (int(hashbin[offset + 3],2) & 0xff)

    #se cogen las cifras que se nos piden del entero generado
    otp = binary % DIGITOS_MAXIMOS[returnDigits]

    #lo pasamos a un string para poder añadirle ceros a la izquierda para
    #rellenar y que sea del tamaño que nos piden si el numero resultante es
    #menor
    result = str(otp)
    while len(result) < returnDigits:
        result = "0" + result

    return result

now = int(time.time())
counter = int(now/30)

TOTP = generateTOTP("313233313233313233646A776B646861776A646B",\
        format(counter, 'x').upper(), 6, "HMACSHA1")
print(TOTP)

TOTP = generateTOTP("3132333435363738393031323334353637383930",\
        "0000000000000001", 8, "HMACSHA1")
print(TOTP)
TOTP = generateTOTP("31323334353637383930313233343536373839303" +\
        "13233343536373839303132", "0000000000000001", 8, "HMACSHA256")
print(TOTP)
TOTP = generateTOTP("313233343536373839303132333435363738393031323334353637" +\
        "383930313233343536373839303132333435363738393031323334353637383930313" +\
        "23334", "0000000000000001", 8, "HMACSHA512")
print(TOTP)