import json
from django.shortcuts import render
from django.urls import path
from .models import Model
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest,HttpResponse,JsonResponse

# Coisas para melhoerar:
#     Cliente precisa ter id da chave para conseguir descriptografar com mais facilidade
#     Chave deve ter um id proprio, sem ser o do mongo
#     Verificação se há ou não uma chave no banco com o CPF

@csrf_exempt
def add_new_user(request):
    if request.method == "POST":
        crypto_key = Model.generate_secret_key_for_AES_cipher()
        print("Chave: ")
        print(crypto_key)

        dados = json.load(request)
        name = dados['nome_cli']
        tefelone = dados['telefone_cli']
        email = dados['email_cli']
        cpf = dados['cpf_cli']

        key = {"chave":crypto_key,
                "cpf_client":cpf}
        Model.key_insert(key)

        padding_character = "{"
        decrypto_array = [name,tefelone,email,cpf]
        crypto_array = []

        for data in decrypto_array:
            crypto_data = Model.encrypt_message(data,crypto_key,padding_character)
            crypto_array.append(crypto_data)
        
        request = {"nome_cli":crypto_array[0],
                    "telefone_cli": crypto_array[1], 
                    "email_cli": crypto_array[2], 
                    "cpf_cli": crypto_array[3]}

        Model.insert_user(request)
        return JsonResponse({"message":"User added."}, status=200)

def delete_user(cpf_user):
    Model.key_delete(cpf_user)


    







