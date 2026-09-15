const video = document.getElementById("camera");
const button = document.getElementById("startCamera");
const statusElement = document.getElementById("status");

// 🟢 ADICIONADO: Mapeamento dos novos elementos da tela de senha
const blocoFacial = document.getElementById("bloco-facial");
const blocoSenha = document.getElementById("bloco-senha");
const btnEnviarSenha = document.getElementById("btn-enviar-senha");
const inputSenha = document.getElementById("input-senha");

let streamCamera = null;

function atualizarStatus(tipo, mensagem, icone) {
    statusElement.className =
        `alert alert-${tipo} text-center mt-3`;

    statusElement.innerHTML = `
        <i class="bi ${icone}"></i>
        ${mensagem}
    `;
}

async function iniciarCamera() {
    streamCamera = await navigator.mediaDevices.getUserMedia({
        video: {
            width: { ideal: 640 },
            height: { ideal: 480 },
            facingMode: "user"
        },
        audio: false
    });

    video.srcObject = streamCamera;

    // Aguarda o navegador carregar a imagem da câmera
    await new Promise((resolve) => {
        if (video.readyState >= 2) {
            resolve();
            return;
        }

        video.addEventListener("loadeddata", resolve, {
            once: true
        });
    });

    await video.play();
}

function capturarImagem() {
    const canvas = document.createElement("canvas");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const contexto = canvas.getContext("2d");

    contexto.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );

    return canvas.toDataURL("image/jpeg", 0.9);
}

function pararCamera() {
    if (!streamCamera) {
        return;
    }

    streamCamera.getTracks().forEach((track) => {
        track.stop();
    });

    streamCamera = null;
    video.srcObject = null;
}

async function autenticarRosto(imagem) {
    const resposta = await fetch("/login/facial", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            imagem: imagem
        })
    });

    const resultado = await resposta.json();

    if (!resposta.ok || !resultado.sucesso) {
        throw new Error(
            resultado.mensagem ||
            "Não foi possível realizar a autenticação."
        );
    }

    return resultado;
}

// 🟢 ADICIONADO: Nova função para enviar a senha para a Etapa 2
async function autenticarSenha(senhaDigitada) {
    const resposta = await fetch("/login/senha", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            senha: senhaDigitada
        })
    });

    const resultado = await resposta.json();

    if (!resposta.ok || !resultado.sucesso) {
        throw new Error(
            resultado.mensagem || "Senha incorreta ou erro na autenticação."
        );
    }

    return resultado;
}


// ==========================================
// FLUXO DA ETAPA 1 (CÂMERA)
// ==========================================
button.addEventListener("click", async () => {
    button.disabled = true;

    try {
        atualizarStatus(
            "info",
            "Ativando a câmera...",
            "bi-camera-fill"
        );

        if (!streamCamera) {
            await iniciarCamera();
        }

        atualizarStatus(
            "success",
            "Rosto localizado. Realizando autenticação...",
            "bi-person-bounding-box"
        );

        // Pequena espera para estabilizar a imagem da câmera
        await new Promise((resolve) => {
            setTimeout(resolve, 1000);
        });

        const imagem = capturarImagem();
        const resultado = await autenticarRosto(imagem);

        // 🟡 MODIFICADO: Em vez de redirecionar, troca para a tela de senha
        if (resultado.sucesso && resultado.exigir_senha) {
            pararCamera(); // Desliga a luz da webcam
            
            // Oculta a câmera e mostra o campo de senha
            blocoFacial.style.display = "none";
            blocoSenha.style.display = "block";
            
            // Foca o cursor automaticamente para o usuário já ir digitando
            inputSenha.focus();
        }

    } catch (erro) {
        console.error("Erro na autenticação:", erro);

        atualizarStatus(
            "danger",
            erro.message,
            "bi-x-circle-fill"
        );

        button.disabled = false;
        button.innerHTML = `
            <i class="bi bi-arrow-repeat"></i>
            Tentar novamente
        `;
    }
});


// 🟢 ADICIONADO: Evento de clique para o botão da Etapa 2 (Senha)
// ==========================================
// FLUXO DA ETAPA 2 (SENHA)
// ==========================================
btnEnviarSenha.addEventListener("click", async () => {
    const senha = inputSenha.value;

    if (!senha) {
        alert("Por favor, digite sua senha.");
        return;
    }

    // Desabilita o botão para evitar cliques duplos
    btnEnviarSenha.disabled = true;
    btnEnviarSenha.innerHTML = `<i class="bi bi-hourglass-split"></i> Validando...`;

    try {
        const resultado = await autenticarSenha(senha);

        // Sucesso total! Muda a cor do botão e redireciona
        btnEnviarSenha.className = "btn btn-success w-100";
        btnEnviarSenha.innerHTML = `<i class="bi bi-check-circle-fill"></i> Bem-vindo(a), ${resultado.nome}!`;

        setTimeout(() => {
            window.location.href = resultado.redirect;
        }, 800);

    } catch (erro) {
        console.error("Erro na senha:", erro);
        
        // Exibe um alerta com o erro (você pode trocar por um elemento HTML se preferir)
        alert(erro.message);
        
        // Limpa o campo, foca nele novamente e reabilita o botão
        inputSenha.value = "";
        inputSenha.focus();
        btnEnviarSenha.disabled = false;
        btnEnviarSenha.innerHTML = `<i class="bi bi-box-arrow-in-right"></i> Acessar Cofre`;
    }
});


// 🟢 ADICIONADO: Permite que o usuário aperte "Enter" no campo de senha para logar
inputSenha.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        btnEnviarSenha.click();
    }
});

window.addEventListener("beforeunload", pararCamera); 