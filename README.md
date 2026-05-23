# 📋 Fila de Requisições

Sistema de filas desenvolvido em Python com Flask para gerenciar
requisições em alta demanda, processando cada tarefa na ordem de
chegada sem derrubar o servidor.

## 🚀 Como usar

1. Clone o repositório
2. Instale as dependências:
pip install flask
3. Execute:
python app.py
4. Acesse: http://127.0.0.1:5000

## ✨ Funcionalidades
- Fila com limite de 10 tarefas simultâneas
- Processamento automático em background com threads
- Dashboard em tempo real com contadores
- Rejeição com HTTP 503 quando fila está cheia
- Log completo de todas as tarefas

## 🧠 Como funciona
Cada requisição entra numa fila e é processada na ordem de chegada.
Se a fila estiver cheia, a requisição é rejeitada com erro 503.
O dashboard atualiza automaticamente a cada 500ms.

