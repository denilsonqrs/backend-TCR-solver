# 🧮 Congruence Solver (Teorema Chinês do Resto)

Uma aplicação web desenvolvida para calcular e resolver sistemas de congruências lineares utilizando o **Teorema Chinês do Resto (TCR)** e o **Algoritmo de Euclides Estendido**. 

Este projeto foi construído como parte das atividades práticas do curso de Ciência da Computação da UFCG, unindo conceitos de matemática discreta e álgebra com desenvolvimento web moderno.

## 🚀 Funcionalidades

* **Resolução de Sistemas:** Calcula a solução global para múltiplas equações modulares.
* **Validação Automática:** Verifica se os módulos fornecidos são coprimos (condição necessária para o TCR).
* **Interface Intuitiva:** Frontend limpo e responsivo para entrada rápida dos coeficientes, restos e módulos.
* **API RESTful:** Backend isolado, garantindo respostas rápidas e estruturadas em formato JSON.

## 🛠️ Tecnologias Utilizadas

**Backend:**
* Python 3
* FastAPI (Criação das rotas e API)
* Uvicorn (Servidor ASGI)
* Pydantic (Validação de dados)

**Frontend:**
* HTML5
* Vanilla JavaScript (Fetch API para comunicação assíncrona)
* Tailwind CSS (Estilização via CDN)

## ⚙️ Como executar o projeto localmente

Siga os passos abaixo para rodar a aplicação na sua máquina:

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/nome-do-repositorio.git](https://github.com/seu-usuario/nome-do-repositorio.git)
2. **Acesse a pasta do projeto:**
    ```bash
    cd nome-do-repositorio
3. **Crie e ative o Ambiente Virtual:**
    ```bash
    # No Windows (PowerShell/CMD)
    python -m venv venv
    venv\Scripts\activate

    # No Linux/MAC
    python3 -m venv venv
    source venv/bin/activate
4. **Instale as dependencias do Backend:**
    ```bash
    pip install fastapi uvicorn pydantic
5. **Inicie o Servidor Local:**
    ```bash
    uvicorn backend_projeto_TCR:app --reload
6. **Abra o Frontend:**
Com o servidor rodando, abra o arquivo index.html diretamento no seu navegador.

## 👨‍💻 Autores

* Denilson Quaresma - https://github.com/denilsonqrs
* Arthur Vinicius - https://github.com/Avzinn-13

# ⌨️ Desenvolvido com dedicação para facilitar cálculos de Álgebra e Matemática Discreta.