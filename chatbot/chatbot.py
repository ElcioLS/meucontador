

#Importando e configurações iniciais
import numpy as np
import pandas as pd
import google.generativeai as genai
from IPython.display import Markdown
from flask import Flask, render_template, request, jsonify


GOOGLE_API_KEY="AIzaSyBcgI_1yM3htUaJNcveSGZmLw3qiqBBOko"
genai.configure(api_key=GOOGLE_API_KEY)


for m in genai.list_models():
  if 'embedContent' in m.supported_generation_methods:
    print(m.name)


    #Exemplo de embedding
title = "MEI - Micro Empreendedor Individual "
sample_text = ("Título: Como explorar todas as vantagens de ser um MEI?"
    "\n"
    "Artigo completo:\n"
    "\n"
    "Gemini API & Google AI Studio: criando protótipos com aplicações de IA generativa")

embeddings = genai.embed_content(model="models/embedding-001",
                                 content=sample_text,
                                 title=title,
                                 task_type="RETRIEVAL_DOCUMENT")


# Modelo de embedding
model = "models/embedding-001"

# Informações sobre MEI
DOCUMENT1 = {
    "Nome": "Limite de Faturamento MEI",
    "Descricao": "O limite de faturamento anual para um MEI em 2023 é de R$ 81.000. Se você ultrapassar esse limite, precisará se desenquadrar do MEI e optar por outro regime tributário."
}

DOCUMENT2 = {
    "Nome": "Declaração Anual MEI (DASN-SIMEI)",
    "Descricao": "Todo MEI precisa entregar a Declaração Anual do Simples Nacional (DASN-SIMEI) até o dia 31 de maio de cada ano. Essa declaração informa à Receita Federal o seu faturamento anual."
}

DOCUMENT3 = {
    "Nome": "Crédito para MEI",
    "Descricao": "Existem diversas linhas de crédito disponíveis para MEI, como microcrédito, empréstimos para capital de giro e financiamentos para compra de equipamentos. Consulte o Sebrae ou instituições financeiras para conhecer as opções."
}

DOCUMENT4 = {
    "Nome": "Treinamento e Capacitação para MEI",
    "Descricao": "O Sebrae oferece diversos cursos e workshops gratuitos para MEI em áreas como gestão financeira, marketing, vendas e planejamento. Aproveite essas oportunidades para desenvolver suas habilidades empresariais."
}

DOCUMENT5 = {
    "Nome": "Compra de Veículos para MEI",
    "Descricao": "Alguns programas de financiamento oferecem condições especiais para a compra de veículos para MEI, como taxas de juros mais baixas e prazos de pagamento mais longos."
}

DOCUMENT6 = {
    "Nome": "Reforma da Empresa para MEI",
    "Descricao": "É possível utilizar linhas de crédito específicas para reformar ou ampliar o seu espaço físico, como o programa de microcrédito do BNDES."
}

# Crie uma lista de documentos
documents = [DOCUMENT1, DOCUMENT2, DOCUMENT3, DOCUMENT4, DOCUMENT5, DOCUMENT6]

# Crie um DataFrame a partir da lista de documentos
df = pd.DataFrame(documents)

# Função para gerar embeddings
def embed_fn(title, text):
    return genai.embed_content(model=model,
                              content=text,
                              title=title,
                              task_type="RETRIEVAL_DOCUMENT")["embedding"]

# Gere embeddings para cada documento
df["Embeddings"] = df.apply(lambda row: embed_fn(row["Nome"], row["Descricao"]), axis=1)

# Função para gerar e buscar consulta
def gerar_e_buscar_consulta(consulta, base, model):
    embedding_da_consulta = genai.embed_content(model=model,
                                              content=consulta,
                                              task_type="RETRIEVAL_QUERY")["embedding"]
    produtos_escalares = np.dot(np.stack(df["Embeddings"]), embedding_da_consulta)

    indice = np.argmax(produtos_escalares)
    return df.iloc[indice]["Descricao"]

# Configuração de geração de texto
generation_config = {
    "temperature": 0.7, # Ajuste para controlar a criatividade das respostas
    "candidate_count": 1
}

# Modelo para geração de texto
model_2 = genai.GenerativeModel("gemini-1.0-pro", generation_config=generation_config)

# Loop principal do chatbot
while True:
    consulta = input("Olá! Sou seu assistente contábil para MEI. O que você gostaria de saber? ")

    if consulta.lower() == "sair":
        break

    trecho = gerar_e_buscar_consulta(consulta, df, model)

    # Prompt para o modelo de linguagem
    prompt = f"Responda a seguinte pergunta de um MEI em um tom amigável e informativo: {consulta}. Use a seguinte informação na sua resposta: {trecho}"

    # Gere a resposta
    response = model_2.generate_content(prompt)
    print(response.text)

