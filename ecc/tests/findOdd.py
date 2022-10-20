from FieldElement.Point import Point, KeyPair, GeneratorPoint

if '__main__' == __name__:
    for i in range(1,50):
        priv_key= str(i).zfill(32)
        print (str(i).zfill(2), priv_key)
        priv_key_bytes = bytes.fromhex(priv_key)
        priv_key_int = int.from_bytes(priv_key_bytes, byteorder="big")
        G = GeneratorPoint()
        pubkey = priv_key_int * G
        print ("even" if pubkey.y._num % 2 == 0 else "odd")



