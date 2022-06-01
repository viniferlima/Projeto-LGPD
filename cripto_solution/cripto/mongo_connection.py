from pymongo import MongoClient
import pymongo
import certifi   
    
class Mongo_Connection(): 
    
    def createConnectionDB(config):
        if config == 'Cliente':
            clusterUser = MongoClient("mongodb://localhost:27017/")
            dbUser = clusterUser['TopicosAvançados']
            collectionUser = dbUser['Cliente']
            return collectionUser
        elif config == 'VendaSimples':
            clusterVendas = MongoClient("mongodb://localhost:27017/")
            db = clusterVendas['TopicosAvançados']
            collectionVendaSimples = db['VendaSimples']
            return collectionVendaSimples
        elif config == 'Vendas':
            cluster = MongoClient("mongodb://localhost:27017/")
            db = cluster['TopicosAvançados']
            collectionVendas = db['Vendas']
            return collectionVendas
        else:
            return "Database not found..."

    def createConnectionDBKeys():
        cluster = MongoClient("mongodb://localhost:27017/")
        db = cluster['Keys']
        collectionKeys = db['CryptoKey']
        return collectionKeys

    def createConnectionDBPortability():
        ca = certifi.where()    
        clusterPortability = MongoClient("mongodb://localhost:27017/ssl=true&sslAllowInvalidCertificates=true")
        dbPortability = clusterPortability['DataPortability']
        collectionPortability = dbPortability['client']
        
        ##mongodb+srv://system:system@cluster0.tafgc.mongodb.net/DataPortability?retryWrites=true&w=majority
        ##ssl = True,
        ##ssl_certfile='selfsigned.crt',
        #ssl_keyfile='private.key')
        return collectionPortability
        


    