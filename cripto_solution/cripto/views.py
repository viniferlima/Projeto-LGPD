import json
from django.shortcuts import render
from django.urls import path
from .models import Model
from django.http import HttpResponse,JsonResponse

def all_data_insert_sale(request):
    if request.method == "POST":
        with open("cripto/temp.json", "r") as infile:
            datas = json.loads(infile.read())
        for data in datas:
            crypto_key = Model.generate_secret_key_for_AES_cipher()

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
                crypto_data = Model.encrypt(crypto_key,data).decode("utf-8")
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
        return HttpResponse("User added.", status=200)

def add_new_user(request):
    if request.method == "POST":
        dados = json.load(request)
        name = dados['nome_cli']
        tefelone = dados['telefone_cli']
        email = dados['email_cli']
        cpf = str(dados['cpf_cli'])

        key_verification = Model.key_verification(cpf)
        if key_verification == None:
            try:
                crypto_key = Model.generate_secret_key_for_AES_cipher()
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
                    crypto_data = Model.encrypt(crypto_key,data).decode("utf-8")
                    crypto_array.append(crypto_data)
                
                request = {"nome_cli":crypto_array[0],
                            "telefone_cli": crypto_array[1], 
                            "email_cli": crypto_array[2], 
                            "cpf_cli": crypto_array[3],
                            "id_chave":id_chave}
                Model.insert_user(request)
                return HttpResponse("User added!")
            except Exception as e: 
                return print(e)
        return HttpResponse("User not added. There is recorded in database with the same datas.")
    return JsonResponse({"message":"Erro na requisição. Método esperado: POST."}, status=500) 

def delete_user(request,cpf):
    if request.method == "DELETE":
        newcpf = str(cpf)
        return Model.key_delete(newcpf)

    return JsonResponse({"message":"Erro na requisição. Método esperado: DELETE."}, status=500) 

def find_user(request, cpf):
    if request.method == "GET":
        result = Model.find_user(cpf)
        return JsonResponse(result, status=500) 
        
    return JsonResponse({"message":"Erro na requisição. Método esperado: GET."}, status=500) 

def Split_Venda(request):
    if request.method == "POST":
        return Model.Split_Sale()

    return JsonResponse({"message":"Erro na requisição. Método esperado: POST."}, status=500) 

def client_data_portability(request, cpf):
    if request.method == "POST":
       return Model.client_data_portability(cpf)
        
    return JsonResponse({"message":"Erro na requisição. Método esperado: POST."}, status=500)     







