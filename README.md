# Catu - Desafio Backend

## 🏖️ Aloha!

Seja bem vindo ao repositório do desafio de backend da Catu! O objetivo aqui é testar seus conhecimentos em procedimentos básicos do desenvolvimento backend, especialmente a utilização do Django Rest Framework, utilizando dados próximos daqueles que você encontrará no dia-a-dia da empresa.

A proposta aqui é simples:

- Crie um repositório privado e copie todos os arquivos 
- Desenvolva sua solução no seu repo
- Quando tudo estiver pronto, nos dê acesso ao seu repositório

## Descrição do dataset

Neste repositório você encontrará um banco de dados SQLite, com notas fiscais de entrada e saída de um cliente hipotético. A análise dos dados faz parte do desafio, mas atente-se para alguns detalhes:

- Os dados correspondem a dois models, Invoice e InvoiceItem. Cada Invoice pode ter de 1 a N InvoiceItems.
- Cada InvoiceItem possi um valor unitário e quantidade. O valor de cada item deve ser calculado como `quantidade_comercial * valor_unitario_comercial`. O valor de um Invoice equivale à soma dos valores dos seus itens. Outras características relevantes do item são a sua unidade comercial, e CFOP (Código Fiscal de Operações e Prestações).
- Neste dataset, existem duas unidades comerciais: KG e SC. Sempre que necessário agregar os dados, considere que 1 SC equivale a 60 KG
- Cada Invoice possui necessariamente um CPF ou CNPJ emitente, mas nunca os dois. Da mesma forma, há sempre um CPF ou CNPJ destinatário, mas nunca os dois. 
- O cnpj do cliente hipotético que possui os dados desse desafio é `94617590711426269531`. Uma nota será considerada "entrada" se cnpj_destinatario == cnpj desse cliente, e será considerada "saída" se cnpj_emitente == cnpj desse cliente. Todos os outros documentos (CNPJ ou CPF) que aparecem aqui correspondem aos produtores para quem o cliente presta serviços. OBS: os dados presentes neste desafio não correspondem a CPFs ou CNPJs válidos, e devem ser considerados apenas um identificador numérico.
- Para as notas de saída, só devem ser consideradas aquelas com o status `autorizado`. Nenhuma nota com o valor de `is_deleted` igual a `true` deve ser considerada. 

## Desafio

Para facilitar a visualização dos dados, o repositório já inclui um endpoint básico de listagem. Sua tarefa será adicionar mais funcionalidades e endpoints, seguindo os passos abaixo:

### 1. Implementar filtros

O endpoint pré-existente de listagem deve poder receber os seguintes parâmetros:

- `document_number` (opcional): documento de um produtor
- `document_type` (opcional): tipo do documento (`cpf` ou `cnpj`)
- `cfop` (opcional): valor numérico com 4 dígitos
- `date_min` (opcional): uma data no formato `YYYY-MM-DD`
- `date_max` (opcional): uma data no formato `YYYY-MM-DD`, posterior a date_min
- `type` (opcional): um valor binário (`1` ou `0`). Se for enviado o valor `0`, deverão ser exibidas apenas as notas de entrada, e para o valor `1`, apenas as notas de saída (veja a definição de notas de entrada/saída acima).

Caso os parâmetros sejam enviados, o retorno da listagem deve trazer apenas as notas fiscais referentes a esse produtor, filtrando também pelo CFOP, intervalo de datas e tipo de nota.

Além disso, modifique o código para que cada item retorne o seu valor, e cada nota retorne a quantidade total e valor total.

> **Exemplo**: `GET /list/all/?document_type=cpf&document_number=10087689222880160494&type=1`
```
[
    {
        "id": 63,
        "quantidade_total": "6300",
        "valor_total": "126000",
        "itens": [
            {
                "quantidade_comercial": "6300",
                "valor_unitario_comercial": "20",
                "valor_item": "126000",
                ...
            }
        ],
        "data_emissao": "2024-06-27",
        "cnpj_emitente": "94617590711426269531",
        "cpf_destinatario": "10087689222880160494",
        ...
    }
]
```

### 2. Endpoint de saldos

Implemente um endpoint `GET` /balance, que pode receber os parâmetros:

- `document_number` (opcional): documento de um produtor
- `document_type` (opcional): tipo do documento (`cpf` ou `cnpj`)
- `cfop` (opcional): valor numérico com 4 dígitos
- `date` (obrigatório): uma data no formato `YYYY-MM-DD`

O seu endpoint deverá retornar o saldo fiscal, em KG, dos produtores (ou de um produtor específico, se os parâmetros `document_number` e `document_type` forem enviados). O saldo é considerado como a soma de todas as notas de entrada menos a soma de todas as notas de saída, relativas a um determinado produtor, até a data enviada no parâmetro `date` (veja a definição de notas de entrada/saída acima). 

Além disso, você deve retornar o saldo geral (a soma de todos os saldos individuais).

> **Exemplo**: `GET /balance/?document_type=cpf&document_number=10087689222880160494&date=2024-06-28`
```
{
   "balances":{
      "10087689222880160494":"900"
   },
   "total_balance":"900"
}
```

### 3. Endpoint de variação de saldo

Finalmente, crie um endpoint `GET` /balance-daily, que pode receber os parâmetros:

- `document_number` (opcional): documento de um produtor
- `document_type` (opcional): tipo do documento (`cpf` ou `cnpj`)
- `cfop` (opcional): valor numérico com 4 dígitos
- `date_min` (obrigatório): uma data no formato `YYYY-MM-DD`
- `date_max` (obrigatório): uma data no formato `YYYY-MM-DD`, posterior a date_min

O seu endpoint deverá retornar, para todos os produtores (ou um produtor específico enviado pelos parâmetros), um dicionário em que as chaves são todas as datas do intervalo `[date_min, date_max]`, e os valores são o saldo, em KG, do produtor naquela data.
> **Exemplo**: `GET /balance-daily/?document_type=cpf&document_number=10087689222880160494&date_min=2024-06-24&date_max=2024-06-27`
```
{
   "daily-balances":{
      "10087689222880160494":{
         "2024-06-24":"0",
         "2024-06-25":"7200",
         "2024-06-26":"7200",
         "2024-06-27":"900"
      }
   }
}
```

### Bônus

Para você que está afiado e achou muito fácil o desafio até agora, aqui estão algumas tarefas bônus para se destacar. Indique em um comentário no início do ChallengeViewset quais tarefas bônus você realizou, caso tenha feito alguma. 

- A serialização dos dados utilizando a classe ModelSerializer do DRF, especialmente com um grande número de MethodFields, pode ser bastante lenta para grandes volumes de dados. Encontre uma solução melhor.
- No endpoint de listagem, a quantidade de dados retornados pode ser muito alta. Implemente paginação, permitindo o envio de um parâmetro `page_size` para determinar quantas notas devem ser retornadas em cada página.

## 🔧 Stack

Este desafio foi criado utilizando **[Django](https://www.djangoproject.com/)**, mais especificamente o **[Django Rest Framework](https://www.django-rest-framework.org/)**.

Para executar o projeto, você precisa ter o python3 instalado em sua máquina (ou um contâiner) e executar os comandos:

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py runserver
```

Ao executar, você terá inicialmente disponível uma requisição `GET` para `http://localhost:8000/challenge/list/all/`, retornando todos os dados do banco. A partir dai é só você fazer sua mágica!

Você pode utilizar outras bibliotecas python para escrever seu código, desde que adicione as mesmas no arquivo `requirements.txt`.

> **Importante**: você não precisa se preocupar com CORS, faça funcionar com seu app preferido de requisições para APIs

## O que estamos avaliando?

É sempre importante entendermos o motivo das coisas. Este teste pretende avaliar:

- Capacidade de avaliação de requisitos e de comunicação para tirar dúvidas
- Habilidade em começar e finalizar PoCs
- Estrutura lógica da solução
- Legibilidade e organização da solução
- Eficiência do código apresentado, mesmo para um volume de dados superior ao presente neste desafio

## 🖥️ É isso! Happy Coding!

Para sanar qualquer dúvida, entre em contato com o nosso time!

