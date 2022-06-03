# Tópicos Avançados
O projeto tem como proposta de desenvolver uma soluçao para problemas relacionados a LGPD.

### Exclusão de Dados
Hoje, para uma empresa realizar a exclusão do dado de um dos seus clientes existe um processo um pouco complicado, pois há empresas que tem inumeros backup dos dados em várias bases. Exclusão de dados de clientes é simplificada, pois para deletar esses dados do banco de dados de algumas empresas, esse processo precisa ser feito em dezenas ou centenas de backups.
A criptografia auxilia na privatização desses dados.

### Particionamento
O particionamento funciona da seguinte maneira, partimos da tabela "vendas", onde nela tinham tanto os dados da venda quanto do clinete que fez a venda, a partir do momento que particionamos essa tabela, separamos os dados da venda e do cliente, sendo assim possivel apagar os dados do cliente sem precisar apagar a venda.
Para fazer isso foi necessário primeiro fazer pegar os dados da tabela "vendas", e após isso foi feito a separação dos dados. Com os dados que foram separados inserimos em outros 2 bancos.

<a name="estrutura"></a>
# Estrutura do Projeto
## Diagrama de caso de uso:
![Casos de uso](/Documentos/CasoUso1.png)


## Modelo do banco de dados:
**CryptoKey**
```json
{
  "_id": {
    "$oid": "62993c873c933fa7e6706a6f"
  },
  "id": {
    "$numberLong": "1509293973392"
  },
  "chave": "K5OLfuM/DmQ5bQphAxlGvtWqB8HqxX7m",
  "cpf_client": "3574789"
}
```

**Client(Tabela Portabilizada)**
```json
{
  "_id": {
    "$oid": "62993da53c933fa7e6707442"
  },
  "Nome": "Deanna Vaughn",
  "Telefone": "1-947-658-1423",
  "Email": "non.massa@aol.net",
  "CPF": "7866913"
}
```

**Vendas(Tabela antes do particionamento)**
```json
{
  "_id": {
    "$oid": "62993c873c933fa7e6706a69"
  },
  "produto_venda": "enim. Etiam gravida molestie arcu. Sed eu nibh vulputate mauris",
  "valor_venda": 99576,
  "qtd_venda": 14907,
  "idCli": "bab20b48541b40b698acd801cb387a71"
}
```


**Cliente(Tabela depois do particionamento)**
```json
{
  "_id": {
    "$oid": "62993ccc3c933fa7e6707239"
  },
  "id": "bab20b48541b40b698acd801cb387a71",
  "nome_cli": "En+NXk0VcSekegz/dPh0CRSeNXws2Hhfs1aBKxQ9AZM=",
  "telefone_cli": "oGAcP86TGsiAjme5Od7h43DI4J8WhYK4CdDo92lA2vg=",
  "email_cli": "4QF1Tu97bmASRyNyBENlbfiPczI3nhFEfo3TQO3vamU=",
  "cpf_cli": "bMKtl9cg8CxIdPt3yjSumWFwzplAOSDDcC+5JyDT3sU=",
  "id_chave": {
    "$numberLong": "1509293239536"
  }
}
```

**VendaSimples(Tabela depois do particionamento)**
```json
{
  "_id": {
    "$oid": "62993c873c933fa7e6706a69"
  },
  "produto_venda": "enim. Etiam gravida molestie arcu. Sed eu nibh vulputate mauris",
  "valor_venda": 99576,
  "qtd_venda": 14907,
  "idCli": "bab20b48541b40b698acd801cb387a71"
}
```

## Documentação da API
<details >
<summary>
<b>🟦GET</b>  /find_user/[CPF usuário]/ 
</summary>

Busca uma vaga por id.
<p>Response 200:</p>

``` json
{
    "Nome": "Alden Harper",
    "Telefone": "1-998-995-1116",
    "Email": "in@outlook.com",
    "CPF": "6735596"
}
```
</details>

<details>
<summary>
<b>🟩POST</b> /insert_user
</summary>
Insere uma vaga.
<p>Exemplo de parâmetro:</p>

``` json
{"produto_venda":"elementum at,",
"valor_venda":49510,
"qtd_venda":31484,
"nome_cli":"Deanna Vaughn",
"telefone_cli":"1-947-658-1423",
"cpf_cli":666222,
"email_cli":"non.massa@aol.net"}
```
</details>

<details>
<summary>
<b>🟥DELETE</b> delete_user/6735596[CPF do usuário]
</summary>
Exclui a vaga baseada no parâmetro, caso encontrada.
<p>Response 200:</p>

``` json
{
   "message": "Key deleted"
}
```
</details>

<details>
<summary>
<b>🟩POST</b> /old_sales
</summary>
<p>Response 200:</p>
</details>

<details>
<summary>
<b>🟩POST</b> /split_sale
</summary>
Tabela Particionada
<p>Response 200:</p>
``` json
{
   "message": "Currículo inserido com sucesso"
}
```
</details>

<details>
<summary>
<b>🟩POST</b> client_data_portability/[CPF do usuário]
</summary>
Faz a portabilidade do usuário
<p>Response 200:</p>
</details>


<a name="tecnologia"></a>
## Tecnologias Utilizadas:
 * python
 ** Django
 ** criptografia simetrica aes128 bytes
 * MongoDb


<a name="equipe"></a>
# INTEGRANTES
 * GUSTAVO RIBEIRO DOS SANTOS 
 * ARTHUR CARDOSO RINALDI DA SILVA
 * VINICIUS FERNANDES DE LIMA 
