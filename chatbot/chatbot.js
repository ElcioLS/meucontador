function enviarPergunta() {
    var pergunta = document.getElementById("pergunta").value;
    if (pergunta) {
        adicionarAoHistorico("Você: " + pergunta);
        document.getElementById("pergunta").value = "";
        
        fetch('/perguntar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: "pergunta=" + encodeURIComponent(pergunta)
        })
        .then(response => response.json())
        .then(data => {
            adicionarAoHistorico("Chatbot: " + data.resposta);
        });
    }
}

function adicionarAoHistorico(texto) {
    var historico = document.getElementById("historico");
    var novaMensagem = document.createElement("p");
    novaMensagem.innerText = texto;
    historico.appendChild(novaMensagem);
}