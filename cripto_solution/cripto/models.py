from asyncio.windows_events import NULL
from http.client import HTTPResponse
from pickle import FALSE, TRUE
from sre_constants import SUCCESS
import ssl
from telnetlib import TLS
from tkinter.tix import Tree
from urllib import request
from django import http
from django.db import models
from hashlib import algorithms_available
import json
from django.http import HttpResponse, JsonResponse
from matplotlib.font_manager import json_load
from numpy import true_divide
import pymongo
import time
from cryptography.fernet import Fernet
from pymongo import MongoClient
from Crypto.Cipher import AES
import uuid 
import base64, os
from django.views.decorators.csrf import csrf_exempt
import certifi

class Model():

    def createConnectionDB():
        return pymongo.MongoClient("mongodb://localhost:27017/")
        ##mongodb+srv://system:system@cluster0.tafgc.mongodb.net/TopicosAvançados?retryWrites=true&w=majority

    def createConnectionDBKeys():
        return pymongo.MongoClient("mongodb://localhost:27017/")
        ##mongodb+srv://system:system@cluster0.tafgc.mongodb.net/Keys?retryWrites=true&w=majority

    
    def createConnectionDBPortability():
        ca = certifi.where()
        return pymongo.MongoClient("mongodb://localhost:27017/ssl=true&sslAllowInvalidCertificates=true"
    
        ##mongodb+srv://system:system@cluster0.tafgc.mongodb.net/DataPortability?retryWrites=true&w=majority
        ##ssl = True,
        ##ssl_certfile='selfsigned.crt',
        #ssl_keyfile='private.key')
        )
        

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
        db = cluster['TopicosAvançados']
        collection = db['VendaSimples']

        result =  collection.insert_one(json.loads(request.body))

        return print("Sale added in the database")

    def insert_user(request):
        cluster = Model.createConnectionDB()
        db = cluster['TopicosAvançados']
        collection = db['Cliente']

        result =  collection.insert_one(request)
        
        return print("User added in the database")
    
    def find_user(cpf_user):
        json_key = Model.key_find(cpf_user)
        id_chave = json_key['id']
        crypto_key = json_key['chave']

        clusterUser = Model.createConnectionDB()
        dbUser = clusterUser['TopicosAvançados']
        collectionUser = dbUser['Cliente']
        user =  collectionUser.find_one({"id_chave":id_chave})

        name = user['nome_cli']
        tefelone = user['telefone_cli']
        email = user['email_cli']
        cpf = user['cpf_cli']

        encrypto_array = [name,tefelone,email,cpf]
        decrypto_array = []

        for data in encrypto_array:
            crypto_data = Model.decrypt(crypto_key,data)
            decrypto_array.append(crypto_data)

        request = ["Nome: ",decrypto_array[0].decode("utf-8")," - Telefone: ",decrypto_array[1].decode("utf-8"), " - Email: ",decrypto_array[2].decode("utf-8"), " - CPF: ",decrypto_array[3].decode("utf-8")]

        json_data = json.dumps(request)
        
        if request != None:
            return json_data
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

        result = collection.delete_one({"cpf_client":cpf_user})
        if(result.deleted_count == 1):
            return ("SUCCESS")
        else:
            return("Error")

    def client_data_portability(cpf_user):
        cluster = Model.createConnectionDBPortability()
        db = cluster['DataPortability']
        collection = db['client']
        #session = cluster.start_session(causal_consistency=True)

        
        client = Model.find_user(cpf_user)
        client = json.loads(client)
        print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
        print(client)

        if(client != NULL):
         #   session.start_transaction()

            try:
                insertClient =  collection.insert_one(client)#, session=session
                if (insertClient.acknowledged):
                   # session.commit_transaction()
                    deleteKey = Model.key_delete(cpf_user)

                    if (deleteKey != 'Error'):
                        return HTTPResponse("The client data was successfully transfered")
                    else:
                        return HTTPResponse("There was an error while trying to delete the key")
                else:
                    return HTTPResponse("There was an error while trying to insert the document")

            except:
                return ("")
               # session.abort_transaction()
           # finally:
               # session.end_session()

                #return HttpResponse("n porto")