import difflib
import datetime
import pyttsx3
import tkinter as tk
from tkinter import ttk
import threading
import wikipedia
import webbrowser

voz = pyttsx3.init()
voz.setProperty('rate', 150)
voz.setProperty('volume', 1.0)


wikipedia.set_lang("pt")


perguntas_respostas = {
    "qual é o seu nome": "Meu nome é PyBot, seu assistente virtual!",
    "como você está": "Estou funcionando perfeitamente, obrigado!",
    "o que você faz": "Respondo perguntas e ajudo nas suas dúvidas.",
    "que dia é hoje": f"Hoje é {datetime.datetime.now().strftime('%d/%m/%Y')}.",
    "qual a capital do brasil": "A capital do Brasil é Brasília.",
    "quem criou o python": "O Python foi criado por Guido van Rossum, em 1991.",
    "o que é inteligência artificial": "É a capacidade de máquinas simularem a inteligência humana.",
    "qual a linguagem de programação mais usada": "Atualmente, Python é uma das mais usadas, junto com JavaScript.",
    "me conte uma piada": "Por que o computador foi ao médico? Porque ele tinha um vírus!",
    "adeus": "Tchau! Volte sempre para bater um papo.",
}

produtos = {
    "1": {
        "nome": "Notebook Ultra X",
        "descricao": "Notebook de alto desempenho com processador i7, 16GB de RAM e SSD de 512GB.",
        "preco": "R$ 4.299,00"
    },
    "2": {
        "nome": "Smartphone Alpha 5G",
        "descricao": "Smartphone com câmera de 108MP, 5G, tela AMOLED e 256GB de armazenamento.",
        "preco": "R$ 2.599,00"
    },
    "3": {
        "nome": "Smart TV Vision 50\"",
        "descricao": "Smart TV 4K com HDR, controle por voz e integração com assistentes virtuais.",
        "preco": "R$ 2.099,00"
    }
}


def encontrar_resposta(pergunta_usuario):
    pergunta_usuario = pergunta_usuario.lower()

    if pergunta_usuario == "menu de produtos":
        return "menu_produtos"

    if pergunta_usuario.startswith("pesquise por ") or pergunta_usuario.startswith("procure no google "):
        termo = pergunta_usuario.replace("pesquise por ", "").replace("procure no google ", "")
        url = f"https://www.google.com/search?q={termo.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Pesquisando por '{termo}' no Google..."

    if pergunta_usuario.startswith("procure por ") or pergunta_usuario.startswith("busque "):
        termo = pergunta_usuario.replace("procure por ", "").replace("busque ", "")
        try:
            resumo = wikipedia.summary(termo, sentences=2)
            return f"Aqui está o que encontrei sobre '{termo}': {resumo}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"O termo '{termo}' é muito genérico. Seja mais específico. Exemplos: {', '.join(e.options[:3])}"
        except wikipedia.exceptions.PageError:
            return f"Não encontrei nada sobre '{termo}' na Wikipedia."
        except Exception as erro:
            return f"Ocorreu um erro ao buscar na Wikipedia: {erro}"

    perguntas = list(perguntas_respostas.keys())
    correspondencias = difflib.get_close_matches(pergunta_usuario, perguntas, n=1, cutoff=0.5)
    if correspondencias:
        pergunta_aproximada = correspondencias[0]
        return perguntas_respostas[pergunta_aproximada]
    else:
        return "Desculpe, ainda não sei responder isso."


class PyBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyBot - Assistente Virtual")

        self.estado = "normal"
        self.produto_selecionado = None
        self.falando = False
        self.lock = threading.Lock()

        self.canvas = tk.Canvas(root, width=200, height=200, bg="white")
        self.canvas.pack(pady=10)
        self.desenhar_carinha(sorrindo=True)

        self.output = tk.Text(root, height=10, width=50, state='disabled', wrap='word')
        self.output.pack(pady=5)

        self.input = tk.Entry(root, width=50)
        self.input.pack(pady=5)
        self.input.bind("<Return>", self.enviar)

        self.botao = ttk.Button(root, text="Enviar", command=self.enviar)
        self.botao.pack(pady=5)

        self.falar("Olá! Eu sou o PyBot. Pode perguntar algo ou digitar 'menu de produtos'!")

    def desenhar_carinha(self, sorrindo=True):
        self.canvas.delete("all")
        self.canvas.create_oval(50, 50, 150, 150, fill="#ffd966", outline="")
        self.canvas.create_oval(75, 80, 85, 90, fill="black")
        self.canvas.create_oval(115, 80, 125, 90, fill="black")
        if sorrindo:
            self.canvas.create_arc(80, 100, 120, 140, start=0, extent=-180, style=tk.ARC, width=2)
        else:
            self.canvas.create_oval(90, 115, 110, 130, fill="red")

    def falar(self, texto):
        with self.lock:
            voz.stop()
            self.falando = True

        self.output.configure(state='normal')
        self.output.insert(tk.END, f"PyBot: {texto}\n")
        self.output.configure(state='disabled')
        self.output.see(tk.END)

        def falar_thread():
            self.desenhar_carinha(sorrindo=False)
            try:
                voz.say(texto)
                voz.runAndWait()
            except:
                pass
            self.desenhar_carinha(sorrindo=True)
            with self.lock:
                self.falando = False

        threading.Thread(target=falar_thread).start()

    def enviar(self, event=None):
        entrada = self.input.get().strip()
        if not entrada:
            return

        with self.lock:
            if self.falando:
                voz.stop()
                self.falando = False

        self.output.configure(state='normal')
        self.output.insert(tk.END, f"Você: {entrada}\n")
        self.output.configure(state='disabled')
        self.output.see(tk.END)
        self.input.delete(0, tk.END)

        if entrada.lower() in ["sair", "exit", "fechar"]:
            self.falar("Até logo! Foi um prazer conversar com você.")
            self.root.after(3000, self.root.quit)
            return

        if self.estado == "menu_produtos":
            if entrada in produtos:
                prod = produtos[entrada]
                self.produto_selecionado = prod
                self.estado = "opcoes_produto"
                texto = (f"{prod['nome']}:\n{prod['descricao']}\nPreço: {prod['preco']}\n\n"
                         "Digite 'menu' para voltar ou 'comprar' para abrir no WhatsApp.")
                self.falar(texto)
            else:
                self.falar("Opção inválida. Digite 1, 2 ou 3.")
            return

        if self.estado == "opcoes_produto":
            if entrada.lower() == "menu":
                self.estado = "menu_produtos"
                self.produto_selecionado = None
                self.falar("Voltando ao menu de produtos.\n1 - Notebook Ultra X\n2 - Smartphone Alpha 5G\n3 - Smart TV Vision 50\"")
            elif entrada.lower() == "comprar":
                if self.produto_selecionado:
                    nome = self.produto_selecionado["nome"]
                    texto_whatsapp = f"Olá, gostaria de comprar o produto {nome}"
                    url = f"https://wa.me/5581985801560?text={texto_whatsapp.replace(' ', '%20')}"
                    webbrowser.open(url)
                    self.falar("Abrindo WhatsApp para finalizar a compra.")
                    self.estado = "normal"
                    self.produto_selecionado = None
                else:
                    self.falar("Nenhum produto selecionado.")
            else:
                self.falar("Opção inválida. Digite 'menu' para voltar ou 'comprar' para abrir no WhatsApp.")
            return

        resposta = encontrar_resposta(entrada)
        if resposta == "menu_produtos":
            self.estado = "menu_produtos"
            menu_texto = (
                "Menu de Produtos:\n"
                "1 - Notebook Ultra X\n"
                "2 - Smartphone Alpha 5G\n"
                "3 - Smart TV Vision 50\"\n"
                "Digite o número do produto."
            )
            self.falar(menu_texto)
        else:
            self.estado = "normal"
            self.falar(resposta)

# Executar app
if __name__ == "__main__":
    root = tk.Tk()
    app = PyBotGUI(root)
    root.mainloop()
