let equacoes = [];

function adicionarEquacao() {
    let a = parseInt(document.getElementById('input_a').value);
    if (isNaN(a)) a = 1;

    const b = parseInt(document.getElementById('input_b').value);
    const n = parseInt(document.getElementById('input_n').value);

    if (isNaN(b) || isNaN(n)) {
        alert("Por favor, preencha os campos de Resto e Mod.");
        return;
    }

    equacoes.push({ a, b, n });

    document.getElementById('input_a').value = '';
    document.getElementById('input_b').value = '';
    document.getElementById('input_n').value = '';

    atualizarTela();
}

function removerEquacao(index) {
    equacoes.splice(index, 1);
    atualizarTela();
}

function mudarCorResultado(status) {
    const container = document.getElementById('resultado-container');
    const header = document.getElementById('resultado-header');
    const icon = document.getElementById('resultado-icon');
    const body = document.getElementById('resultado-body');
    const statusText = document.getElementById('status-final');

    // 1. Removemos TODAS as cores para limpar o terreno
    container.classList.remove('border-blue-300', 'border-green-300', 'border-red-300');
    header.classList.remove('bg-blue-100', 'text-blue-800', 'border-blue-300', 'bg-green-100', 'text-green-800', 'border-green-300', 'bg-red-100', 'text-red-800', 'border-red-300');
    body.classList.remove('bg-blue-50', 'text-blue-900', 'bg-green-50', 'text-green-900', 'bg-red-50', 'text-red-900');

    // 2. Aplicamos a cor certa e trocamos o ícone e o texto
    if (status === 'aguardando') {
        container.classList.add('border-blue-300');
        header.classList.add('bg-blue-100', 'text-blue-800', 'border-blue-300');
        body.classList.add('bg-blue-50', 'text-blue-900');
        icon.className = 'fas fa-clock text-blue-700'; // Ícone de relógio
        statusText.innerText = "Aguardando";
    } else if (status === 'success') {
        container.classList.add('border-green-300');
        header.classList.add('bg-green-100', 'text-green-800', 'border-green-300');
        body.classList.add('bg-green-50', 'text-green-900');
        icon.className = 'fas fa-check-circle text-green-700'; // Ícone de sucesso
        statusText.innerText = "Success";
    } else if (status === 'error') {
        container.classList.add('border-red-300');
        header.classList.add('bg-red-100', 'text-red-800', 'border-red-300');
        body.classList.add('bg-red-50', 'text-red-900');
        icon.className = 'fas fa-exclamation-circle text-red-700'; // Ícone de erro
        statusText.innerText = "Error";
    }
}

function atualizarTela() {
    const container = document.getElementById('lista-equacoes');
    const btnResolver = document.getElementById('btn_resolver');

    container.innerHTML = '';

    // Renderiza cada equação
    equacoes.forEach((eq, index) => {
        const textoA = eq.a !== 1 ? eq.a : '';

        container.innerHTML += `
            <div class="flex items-center justify-between border border-gray-200 rounded-lg p-3 bg-white shadow-sm">
                <span class="text-sm text-gray-700 font-serif">Equação ${index + 1}: ${textoA}x &equiv; ${eq.b} (mod ${eq.n})</span>
                <button onclick="removerEquacao(${index})" class="text-gray-400 hover:text-red-500 transition-colors">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </div>
        `;
    });
    if (equacoes.length >= 2) {
        btnResolver.disabled = false;
        btnResolver.classList.remove('opacity-50', 'cursor-not-allowed');
    } else {
        btnResolver.disabled = true;
        btnResolver.classList.add('opacity-50', 'cursor-not-allowed');
    }
}

async function resolverTCR() {
    // 1. Dados fixos de teste (nosso próximo passo é pegar isso da tela)
    const payload = {
        "all_x": equacoes.map(eq => eq.a),
        "remains": equacoes.map(eq => eq.b),
        "mods": equacoes.map(eq => eq.n)
    };

    // Muda o texto para mostrar que está carregando
    const textoResultado = document.getElementById('texto-resultado');
    textoResultado.innerText = "Calculando...";
    mudarCorResultado('aguardando');
    try {
        // 2. Chama a API (O garçom)
        const resposta = await fetch('http://127.0.0.1:8000/api/solve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });


        // 3. Recebe a resposta do Python
        const dados = await resposta.json();
        console.log("Retorno do Python:", dados);

        // 4. Injeta a resposta na tela
        if (dados.status === "success") {
            for (let i = 1; i <= 5; i++) {
                document.getElementById(`passo${i}-content`).innerHTML = '';
            }

            textoResultado.innerText = dados.texto_exibicao;
            document.getElementById('status-final').innerText = "Success";
            mudarCorResultado('success');

            if (dados.passos) {
                document.getElementById('passo1-content').innerHTML = dados.passos.passo1.map(p => `<p>${p}</p>`).join('');
                document.getElementById('passo2-content').innerHTML = dados.passos.passo2.map(p => `<p>${p}</p>`).join('');
                document.getElementById('passo3-content').innerHTML = dados.passos.passo3.map(p => `<p>${p}</p>`).join('');
                document.getElementById('passo4-content').innerHTML = dados.passos.passo4.map(p => `<p>${p}</p>`).join('');
                document.getElementById('passo5-content').innerHTML = dados.passos.passo5.map(p => `<p>${p}</p>`).join('');
            }

            if (window.MathJax) {
                MathJax.typesetPromise();
            }


        } else {
            textoResultado.innerText = dados.message;
            document.getElementById('status-final').innerText = "Error";
            mudarCorResultado('error');

            for (let i = 1; i <= 5; i++) {
                document.getElementById(`passo${i}-content`).innerHTML = '';
            }
        }

    } catch (erro) {
        console.error("Erro na comunicação:", erro);
        document.getElementById('texto-resultado').innerText = "Erro ao conectar com o servidor. O backend está rodando?";

        mudarCorResultado('error');
    }
}