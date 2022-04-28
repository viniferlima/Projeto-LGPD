from asyncio.windows_events import NULL
from http.client import HTTPResponse
from pickle import FALSE, TRUE
from urllib import request
from django.db import models
from hashlib import algorithms_available
import json
from django.http import JsonResponse
from matplotlib.font_manager import json_load
import pymongo
import time
from cryptography.fernet import Fernet
from pymongo import MongoClient
from Crypto.Cipher import AES
import uuid
import base64, os

class Model():

    def createConnectionDB():
        return pymongo.MongoClient("mongodb+srv://system:system@cluster0.tafgc.mongodb.net/TopicosAvançados?retryWrites=true&w=majority")

    def createConnectionDBKeys():
        return pymongo.MongoClient("mongodb+srv://system:system@cluster0.tafgc.mongodb.net/Keys?retryWrites=true&w=majority")

    def generate_secret_key_for_AES_cipher():
        # AES key length must be either 16, 24, or 32 bytes long
        AES_key_length = 12 # use larger value in production
        # generate a random secret key with the decided key length
        # this secret key will be used to create AES cipher for encryption/decryption
        secret_key = os.urandom(AES_key_length)
        # encode this secret key for storing safely in database
        encoded_secret_key = base64.b64encode(secret_key).decode("utf-8")
        return encoded_secret_key

    def encrypt(crypto_key, text):
        BS = len(crypto_key)
        IV = "1234567890123456"
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        cryptor = AES.new(crypto_key.encode("utf8"), AES.MODE_CBC, IV.encode("utf8"))
        ciphertext = cryptor.encrypt(bytes(pad(text), encoding="utf8"))

        return base64.b64encode(ciphertext)

    def decrypt(crypto_key, text):
        unpad = lambda s: s[0:-ord(s[-1:])]
        decode = base64.b64decode(text)
        IV = "1234567890123456"
        cryptor = AES.new(crypto_key.encode("utf8"), AES.MODE_CBC, IV.encode("utf8"))

        plain_text = cryptor.decrypt(decode)

        return unpad(plain_text)

    def key_verification(cpf_cli):
        cluster = Model.createConnectionDBKeys()
        db = cluster['Keys']
        collection = db['CryptoKey']

        result = collection.find_one({"cpf_cli":cpf_cli})
        if result == NULL:
            return FALSE
        return result

    def Split_Sale():
        cluster = Model.createConnectionDB()
        db = cluster['TopicosAvançados']
        collectionVenda = db['Vendas']
        VendasSeparadas = []
        VendasSeparadas = collectionVenda.find({})
        collectionCli = db['Cliente']
        collectionVendaSimples = db['VendaSimples']
        for dado in VendasSeparadas:
            id = dado['_id']
            produto = dado['produto_venda']
            valor = dado['valor_venda']
            qtd = dado['qtd_venda']
            id_cli = uuid.uuid4().hex
            name = dado['nome_cli']
            telefone = dado['telefone_cli']
            email = dado['email_cli']
            cpf = dado['cpf_cli']
            idChave = dado['id_chave']

            requestCli = { "id": id_cli,
                    "nome_cli":name,
                    "telefone_cli": telefone, 
                    "email_cli": email, 
                    "cpf_cli": cpf,
                    "id_chave": idChave}
            collectionCli.insert_one(requestCli)

            requestVendaSimples = {"_id":id,
                    "produto_venda": produto, 
                    "valor_venda": valor, 
                    "qtd_venda": qtd,
                   "idCli": id_cli}
            collectionVendaSimples.insert_one(requestVendaSimples)
        return HTTPResponse("Tabela Particionada") 
                              
    def insert_sale_old(request):
        cluster = Model.createConnectionDB()
        db = cluster['TopicosAvançados']
        collection = db['Vendas']

        result =  collection.insert_one(request)

        return print("Sale and user data added in the database")    

    def insert_sale(request):
        cluster = Model.createConnectionDB()
        db = cluster['client']
        collection = db['VendaSimples']

        result =  collection.insert_one(json.loads(request.body))

        return print("Sale added in the database")

    def insert_user(request):
        cluster = Model.createConnectionDB()
        db = cluster['TopicosAvançados']
        collection = db['client']

        result =  collection.insert_one(request)
        
        return print("User added in the database")
    
    def find_user(cpf_user):
        json_key = Model.key_find(cpf_user)
        #json_key = json_load(data)
        id_chave = json_key['id']
        crypto_key = json_key['chave']
        print("Chave ID na Chave:")
        print(id_chave)
        print(crypto_key)

        clusterUser = Model.createConnectionDB()
        dbUser = clusterUser['TopicosAvançados']
        collectionUser = dbUser['client']
        user =  collectionUser.find_one({"id_chave":id_chave})
        print("Chave ID no User:")
        print(user['id_chave'])

        name = user['nome_cli']
        tefelone = user['telefone_cli']
        email = user['email_cli']
        cpf = user['cpf_cli']

        encrypto_array = [name,tefelone,email,cpf]
        decrypto_array = []

        for data in encrypto_array:
            crypto_data = Model.decrypt(crypto_key,data)
            decrypto_array.append(crypto_data)
        
        # request = {"nome_cli":decrypto_array[0],
        #             "telefone_cli": decrypto_array[1], 
        #             "email_cli": decrypto_array[2], 
        #             "cpf_cli": decrypto_array[3]}

        request = ["Nome: ",decrypto_array[0]," - Telefone: ",decrypto_array[1], " - Email: ",decrypto_array[2], " - CPF: ",decrypto_array[3]]

        if request:
         return request
        else:
         return JsonResponse({"message" : "User doesnt found."}, status=200)

    def key_insert(key):
        cluster = Model.createConnectionDBKeys()
        db = cluster['Keys']
        collection = db['CryptoKey'] 

        result = collection.insert_one(key)

        return print("Key added from database")

    def key_find(cpf_user):
        cluster = Model.createConnectionDBKeys()
        db = cluster['Keys']
        collection = db['CryptoKey']

        result = collection.find_one({"cpf_client":cpf_user})

        return result         

    def key_delete(cpf_user):
        cluster = Model.createConnectionDBKeys()
        db = cluster['Keys']
        collection = db['CryptoKey']

        result = collection.delete_one({"cli_cpf":cpf_user})

        return print("Key deleted from database")         

