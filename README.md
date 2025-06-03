# 🤖 PyBot - Assistente Virtual com Interface Gráfica

PyBot é um assistente virtual interativo desenvolvido em Python com interface gráfica usando Tkinter. Ele é capaz de responder perguntas comuns, realizar buscas na internet (Google e Wikipedia), contar piadas, exibir um menu de produtos e até simular uma compra via WhatsApp. Além disso, o PyBot utiliza síntese de voz (TTS) com `pyttsx3`, tornando a interação mais humana.

---

## 🧠 Funcionalidades

- ✅ Respostas automáticas para perguntas comuns
- ✅ Busca no Google com comando de voz ou texto
- ✅ Resumo de termos via Wikipedia
- ✅ Integração com WhatsApp para simulação de compra
- ✅ Interface gráfica com animação facial simples
- ✅ Síntese de fala com `pyttsx3` (fala com o usuário)
- ✅ Sistema de produtos com menu interativo

---

## 🖼️ Interface

O PyBot possui uma interface gráfica amigável com uma carinha animada, que muda quando está "falando". Tudo isso usando apenas a biblioteca Tkinter!

---

## 📦 Tecnologias Utilizadas

| Tecnologia     | Descrição                                      |
|----------------|-----------------------------------------------|
| `Python`       | Linguagem de programação principal             |
| `Tkinter`      | Interface gráfica (GUI)                        |
| `pyttsx3`      | Síntese de fala (Text-to-Speech)               |
| `wikipedia`    | Busca de informações resumidas                 |
| `webbrowser`   | Abertura de URLs para pesquisas e WhatsApp     |
| `difflib`      | Identificação de perguntas similares           |
| `threading`    | Execução de fala de forma assíncrona           |

---

## 📋 Comandos Suportados

### 🤔 Perguntas Gerais
- `qual é o seu nome`
- `como você está`
- `o que você faz`
- `que dia é hoje`
- `quem criou o python`
- `o que é inteligência artificial`
- `qual a linguagem de programação mais usada`
- `me conte uma piada`
- `adeus`

### 🔎 Buscas
- `pesquise por [termo]` → abre busca no Google
- `procure por [termo]` ou `busque [termo]` → busca resumo na Wikipedia

### 🛒 Menu de Produtos
Digite `menu de produtos` para visualizar os itens:
- 1 - Notebook Ultra X
- 2 - Smartphone Alpha 5G
- 3 - Smart TV Vision 50"

Após escolher um produto, você pode:
- Digitar `comprar` → abre WhatsApp
- Digitar `menu` → retorna ao menu de produtos

---

## 🚀 Como Executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/devKaioLimaGit/chatbot.git
