from ast import If
from doctest import FAIL_FAST
import json
from math import prod
from pickle import FALSE
import re
from django.shortcuts import render
from django.urls import path
from matplotlib.font_manager import json_load
from .models import Model
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest,HttpResponse,JsonResponse

@csrf_exempt
def all_data_insert_sale(request):
    if request.method == "POST":
        with open("C:/Users/Mars/OneDrive - Mars Inc/Área de Trabalho/lgpd/cripto_solution/cripto/temp.json", "r") as infile:
            datas = json.loads(infile.read())
        print(datas)
        for data in datas:
            print("document:")
            print(data)
            crypto_key = Model.generate_secret_key_for_AES_cipher()
            print("Chave: ")
            print(crypto_key)

            #dados = json.loads(str(data))
            produto = data["produto_venda"]
            valor = data["valor_venda"]
            qtd = data["qtd_venda"]
            name = data['nome_cli']
            tefelone = data['telefone_cli']
            email = data['email_cli']
            cpf = str(data['cpf_cli'])
            
            id_chave = id(crypto_key)
            key = {"id":id_chave,
                    "chave":crypto_key,
                    "cpf_client":cpf}
            Model.key_insert(key)

            decrypto_array = [name,tefelone,email,cpf]
            crypto_array = []

            for data in decrypto_array:
                print(data)

        for data in decrypto_array:
            crypto_data = Model.encrypt(crypto_key,data)
            crypto_array.append(crypto_data)
            
            request = {"produto_venda":produto,
                        "valor_venda":valor,
                        "qtd_venda":qtd,
                        "nome_cli":crypto_array[0],
                        "telefone_cli": crypto_array[1], 
                        "email_cli": crypto_array[2], 
                        "cpf_cli": crypto_array[3],
                        "id_chave":id_chave}

            Model.insert_sale_old(request)
        return JsonResponse({"message":"User added."}, status=200)

@csrf_exempt
def add_new_user(request):
    if request.method == "POST":

        dados = json.load(request)
        name = dados['nome_cli']
        tefelone = dados['telefone_cli']
        email = dados['email_cli']
        cpf = dados['cpf_cli']

        key_verification = Model.key_verification(cpf)
        if key_verification == FALSE:
            crypto_key = Model.generate_secret_key_for_AES_cipher()
            id_chave = id(crypto_key)
            key = {"id":id_chave,
                "chave":crypto_key,
                "cpf_client":cpf}
            Model.key_insert(key)
        else:
            id_chave = key_verification['id']

        decrypto_array = [name,tefelone,email,cpf]
        crypto_array = []

        for data in decrypto_array:
            print(data)

        for data in decrypto_array:
            crypto_data = Model.encrypt(crypto_key,data)
            crypto_array.append(crypto_data)
        
        request = {"nome_cli":crypto_array[0],
                    "telefone_cli": crypto_array[1], 
                    "email_cli": crypto_array[2], 
                    "cpf_cli": crypto_array[3],
                    "id_chave":id_chave}

        Model.insert_user(request)
        return HttpResponse("User added!")


    return JsonResponse({"message":"Erro na requisição. Método esperado: POST."}, status=500) 

def delete_user(request,cpf):
    if request.method == "DELETE":
        return Model.key_delete(cpf)

    return JsonResponse({"message":"Erro na requisição. Método esperado: DELETE."}, status=500) 

def find_user(request, cpf):
    if request.method == "GET":
        result = Model.find_user(cpf)
        return HttpResponse(result, status=500) 
        
    return JsonResponse({"message":"Erro na requisição. Método esperado: GET."}, status=500) 

def Split_Venda(request):
    if request.method == "POST":
        return Model.Split_Sale()

    return JsonResponse({"message":"Venda Efetuada."}, status=500) 

    







