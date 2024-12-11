async function getDados() {
    // faz a chamada ao endpoint Flask
    const response = await fetch('http://127.0.0.1:5000/soma')

    // verificar se a resposta foi bem sucedida
    if (!response.ok){
        const dados = await response.text()
        console.log(dados)
        document.getElementById('saida').textContent = dados
    }
}

async function buscaCliente() {
    const doc_cpf = document.getElementById("cpf").value;
    if (!doc_cpf) {
        alert("Por favor, insira um CPF.");
        return;
    }

    const response = await fetch(`http://127.0.0.1:5000/consulta?doc=${doc_cpf}`);
    if (response.ok) {
        // CPF encontrado
        const dados = await response.json();
        document.getElementById("nome").textContent = dados.nome;
        document.getElementById("nasc").textContent = dados.data_nascimento;
        document.getElementById("email").textContent = dados.email;
    } else {
        // CPF não encontrado
        const erro = await response.json();
        document.getElementById("resultado").textContent = erro.mensagem;
    }
}


async function cadastrarClientes() {
    const cpf = document.getElementById("cadcpf").value;
    const nome = document.getElementById("cadnome").value;
    const data_nascimento = document.getElementById("cadnascimento").value;
    const email = document.getElementById("cademail").value;

    const payload = {
        cpf,
        dados: {
            nome,
            data_nascimento,
            email,
        },
    };

    const response = await fetch(`http://127.0.0.1:5000/cadastro`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    const resultado = await response.json();
    if (response.ok) {
        // Cadastro bem-sucedido
        alert(resultado.mensagem);
        document.getElementById("cadastro").reset();
    } else {
        // CPF já cadastrado
        alert(resultado.mensagem);
    }
}