from asyncio.windows_events import NULL
from django.http.response import HttpResponse
from pickle import FALSE, TRUE
import json
from django.http import HttpResponse, JsonResponse
import pymongo
from pymongo import MongoClient, InsertOne, DeleteOne
from pymongo.errors import BulkWriteError
from Crypto.Cipher import AES
import uuid 
import base64, os
import certifi
from .mongo_connection import Mongo_Connection

class Model():

    def createConnectionDB():
        return pymongo.MongoClient("mongodb://localhost:27017/")

    def createConnectionDBKeys():
        return pymongo.MongoClient("mongodb://localhost:27017/")
    
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
        collection = Mongo_Connection.createConnectionDBKeys()
        result = collection.find_one({"cpf_cli":cpf_cli})
        
        if result == NULL:
            return None
        return result

    def Split_Sale():
        collectionVenda = Mongo_Connection.createConnectionDB('Vendas')
        collectionCli = Mongo_Connection.createConnectionDB('Cliente')
        collectionVendaSimples = Mongo_Connection.createConnectionDB('VendaSimples')

        VendasSeparadas = []
        VendasSeparadas = collectionVenda.find({})

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
        return HttpResponse("Tabela Particionada") 
                              
    def insert_sale_old(request):
        collection = Mongo_Connection.createConnectionDB('Vendas')
        collection.insert_one(request)

        return print("Sale and user data added in the database")    

    def insert_sale(request):
        collection = Mongo_Connection.createConnectionDB('VendaSimples')
        collection.insert_one(json.loads(request))

        return print("Sale added in the database")

    def insert_user(request):
        collection = Mongo_Connection.createConnectionDB('Cliente')
        result = collection.insert_one(request)
        
        if(result.inserted_id) != None:
            return print("User added in the database")
        else:
            return print("Error to insert user")
    
    def find_user(cpf_user):
        json_key = Model.key_find(cpf_user)
        if json_key != None:
            id_chave = json_key['id']
            crypto_key = json_key['chave']

            collectionUser = Mongo_Connection.createConnectionDB('Cliente')
            user =  collectionUser.find_one({"id_chave":id_chave})
            name = user['nome_cli']
            tefelone = user['telefone_cli']
            email = user['email_cli']
            cpf = user['cpf_cli']

            encrypto_array = [name,tefelone,email,cpf]
            decrypto_array = []

            for data in encrypto_array:
                crypto_data = Model.decrypt(crypto_key,data).decode("utf-8")
                decrypto_array.append(crypto_data)
            
            request = {"Nome: ":decrypto_array[0],"Telefone: ":decrypto_array[1], "Email: ":decrypto_array[2], "CPF: ":decrypto_array[3]}
            
            return json.loads(request) 
        else:
         return ("User doesnt found.")

    def key_insert(key):
        collection = Mongo_Connection.createConnectionDBKeys()
        result = collection.insert_one(key)

        if(result.inserted_id) != None:
            return print("Key added from database")
        else:
            return print("Error to insert key")

    def key_find(cpf_user):
        collection = Mongo_Connection.createConnectionDBKeys()
        result = collection.find_one({"cpf_client":cpf_user})

        return result         

    def key_delete(cpf_user):
        collection = Mongo_Connection.createConnectionDBKeys()

        result = collection.delete_one({"cpf_client":cpf_user})
        if(result.deleted_count == 1):
            return HttpResponse("Key deleted")      
        else:
            return HttpResponse("Fail to delete key")      

    def client_data_portability(cpf_user):
        collectionPortability = Mongo_Connection.createConnectionDBPortability()
        collectionKeys = Mongo_Connection.createConnectionDBKeys()

        client = Model.find_user(cpf_user)

        if(client != NULL):
            try :
                requests = [InsertOne(client)]
                collectionPortability.bulk_write(requests)
                try:  
                    requestsDelete = [ DeleteOne({'cpf_client':cpf_user})]
                    collectionKeys.bulk_write(requestsDelete)
                    return HttpResponse("The client data was successfully transfered")
                except BulkWriteError as bwe:
                    print(bwe.details)
                    return HttpResponse("There was an error while trying to perform deletion")       
            except BulkWriteError as bwe:
                print(bwe.details)
                return HttpResponse("There was an error while trying to perform insertion")      
        else:    
            return HttpResponse("The client data was not transfered")