async function resolverTCR() {
    // 1. Dados fixos de teste (nosso próximo passo é pegar isso da tela)
    const payload = {
        "all_x": [1, 1, 1],
        "remains": [2, 3, 2],
        "mods": [3, 5, 7]
    };

    // Muda o texto para mostrar que está carregando
    document.getElementById('texto-resultado').innerText = "Calculando...";

    try {
        // 2. Chama a API (O garçom)
        const resposta = await fetch('http://127.0.0.1:8000/api/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        // 3. Recebe a resposta do Python
        const dados = await resposta.json();

        // 4. Injeta a resposta na tela
        if (dados.status === "success") {
            document.getElementById('texto-resultado').innerText = dados.texto_exibicao;
        } else {
            document.getElementById('texto-resultado').innerText = "Erro: " + dados.message;
        }

    } catch (erro) {
        console.error("Erro na comunicação:", erro);
        document.getElementById('texto-resultado').innerText = "Erro ao conectar com o servidor. O backend está rodando?";
    }
}