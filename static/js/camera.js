const video = document.getElementById("camera");
const button = document.getElementById("startCamera");
const statusElement = document.getElementById("status");

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

        atualizarStatus(
            "success",
            `Bem-vindo(a), ${resultado.nome}!`,
            "bi-check-circle-fill"
        );

        pararCamera();

        setTimeout(() => {
            window.location.href = resultado.redirect;
        }, 800);

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


window.addEventListener("beforeunload", pararCamera);