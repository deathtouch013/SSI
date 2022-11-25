#https://www.rfc-editor.org/rfc/rfc6238.html#appendix-A
import hmac
import hashlib
import time
import base64

class TOTP:

    #se hara modulo con el valor correspondiente y marcara cuantos digitos se devuelven
    _DIGITOS_MAXIMOS = [10,100,1000,10000,100000,1000000,1000000,10000000,100000000,1000000000,10000000000]
    #algoritmos disponibles para realizar el TOTP
    _ALGORITMOS_HASH = {'HMACSHA1': hashlib.sha1,'HMACSHA256':hashlib.sha256,'HMACSHA512':hashlib.sha512}

    #funcion que pasa de una lista de valores hexadecimales de dos en dos, a una
    #de valores en binario de 8 en 8, convierte bytes en hexadecimal a binario
    #(ambos en un elemento de lista)
    def _listHexToBin(self,hexa):
        binario = []
        for i in hexa:
            binario.append(bin(int(i, 16))[2:].zfill(8))
        return binario

    #convierte de una cadena hexadecimal a una lista de valores hexadecimal de
    #dos en dos (de byte en byte)
    def _hexListing(self,hexa):
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
    #time es el tiempo en hexadecimal(se pasa en string) y en mayusculas, para parsearlo se puede usar format(counter, 'x').upper()
    #returnDigits es el numero de digitos que devuelve el codigo en base 10 (se pasa en int)
    #cryto es el algoritmo de hash con el que se "cifra" (string) ["HMACSHA1","HMACSHA256","HMACSHA512"]
    def generateTOTPFull(self,key, counter, returnDigits, crypto):
        #El counter tiene un tamaño maximo de 16 porque nos permite guardar
        #valores de tiempo usando 64 bits.
        while len(counter) < 16:
            counter = "0" + counter

        #pasamos a binario counter y key para cifrarlo con el algoritmo seleccionado
        msgBin = bytes.fromhex(counter)
        kBin = bytes.fromhex(key)
        hash_hmac = hmac.new(kBin,msgBin,self._ALGORITMOS_HASH.get(crypto))

        #en hash lo guardamos en hexadecimal
        hash = hash_hmac.hexdigest()
        #y en hashbin pasamos los valores hexadecimales de dos en dos a una lista
        #(de byte en byte) y despues esa lista la convertimos a una lista de bits
        #(tambien de byte en byte)
        hashbin = self._listHexToBin(self._hexListing(hash))

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
        otp = binary % self._DIGITOS_MAXIMOS[returnDigits]

        #lo pasamos a un string para poder añadirle ceros a la izquierda para
        #rellenar y que sea del tamaño que nos piden si el numero resultante es
        #menor
        result = str(otp)
        while len(result) < returnDigits:
            result = "0" + result

        return result

    #genera el codigo del tiempo actual, pero hay que pasarle el resto de parametros
    def generateTOTPNow(self,key, returnDigits, crypto):
        now = int(time.time())
        counter = int(now/30)
        return self.generateTOTPFull(key, format(counter, 'x').upper(), returnDigits, crypto)


    def generateTOTPNowb32(self, key, returnDigits, crypto):

        bkey = base64.b32decode(key).hex()
        return self.generateTOTPNow(bkey, returnDigits, crypto)

    def test(self):
        #claves usadas por la RFC
        key1 = "3132333435363738393031323334353637383930"
        key256 = "3132333435363738393031323334353637383930313233343536373839303132"
        key512 = "3132333435363738393031323334353637383930313233343536373839303132" + \
            "3334353637383930313233343536373839303132333435363738393031323334"
        #contadores usados por la RFC
        counter = ["0000000000000001","00000000023523EC","00000000023523ED","000000000273EF07","0000000003F940AA","0000000027BC86AA"]
        algoritmo = ["HMACSHA1","HMACSHA256","HMACSHA512"]
        #codigos resultantes para cada contador, puestos en listas de 3 elementos haciendo referencia a que algoritmo fue usado ["HMACSHA1","HMACSHA256","HMACSHA512"]
        codigos = [["94287082","46119246","90693936"],["07081804","68084774","25091201"],["14050471","67062674","99943326"],["89005924","91819424",\
            "93441116"],["69279037","90698825","38618901"],["65353130","77737706","47863826"]]

        cnt = 0
        #si uno falla se muestra que codigo mostró y cual deberia mostrar
        while cnt < len(counter):
            codigo = totp.generateTOTPFull(key1, counter[cnt], 8, algoritmo[0])
            if codigo != codigos[cnt][0]:
                print("El codigo generado fue: \"" + codigo + "\" pero deberia ser: \"" + codigos[cnt][0] + "\"")
                print("key: " + key1)
                print("Counter: " + counter[cnt] + " Algoritmo: " + algoritmo[0])
                exit()
            codigo = totp.generateTOTPFull(key256, counter[cnt], 8, algoritmo[1])
            if codigo != codigos[cnt][1]:
                print("El codigo generado fue: \"" + codigo + "\" pero deberia ser: \"" + codigos[cnt][0] + "\"")
                print("key: " + key256)
                print("Counter: " + counter[cnt] + " Algoritmo: " + algoritmo[1])
                exit()
            codigo = totp.generateTOTPFull(key512, counter[cnt], 8, algoritmo[2])
            if codigo != codigos[cnt][2]:
                print("El codigo generado fue: \"" + codigo + "\" pero deberia ser: \"" + codigos[cnt][0] + "\"")
                print("key: " + key512)
                print("Counter: " + counter[cnt] + " Algoritmo: " + algoritmo[2])
                exit()
            cnt = cnt + 1

""" 

totp = TOTP()

totp.test()

codigo = totp.generateTOTPNow("313233313233313233646A776B646861776A646B", 6, "HMACSHA1")
print(codigo)

 """