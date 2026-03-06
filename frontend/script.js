// script.js
let provider;
let signer;
let userWallet;

const backendURL = "http://127.0.0.1:8000";

async function connectWallet() {
    if (typeof window.ethereum === "undefined") {
        alert("Nenhuma carteira Web3 detectada. Instale MetaMask, Rabby ou OKX.");
        return;
    }

    try {
        provider = new ethers.providers.Web3Provider(window.ethereum);
        await window.ethereum.request({ method: "eth_requestAccounts" });
        signer = provider.getSigner();
        userWallet = await signer.getAddress();

        document.getElementById("walletAddress").innerHTML =
            "<b>Carteira conectada:</b> " + userWallet;

        analyzeWallet(userWallet);
    } catch (error) {
        console.error("Erro ao conectar carteira:", error);
        alert("Erro ao conectar carteira.");
    }
}

async function analyzeWallet(wallet) {
    try {
        const resultDiv = document.getElementById("result");
        resultDiv.innerHTML = "Analisando carteira...";

        const response = await fetch(`${backendURL}/analyze/${wallet}`);
        if (!response.ok) {
            throw new Error("Erro no backend");
        }

        const data = await response.json();
        showResult(data);

        if (typeof renderCharts === "function") {
            renderCharts(data);
        } else {
            console.warn("Função renderCharts não encontrada");
        }
    } catch (error) {
        console.error(error);
        document.getElementById("result").innerHTML = "Erro ao analisar carteira.";
    }
}

function showResult(data) {
    const html = `
    <div class="card">
        <h3>Análise da Carteira</h3>
        <p><b>Endereço:</b> ${data.wallet}</p>
        <p><b>Pontuação de Reputação:</b> ${data.reputation_score.toFixed(2)}</p>
        <p><b>Saldo:</b> ${Number(data.analysis.balance).toFixed(4)} ETH</p>
        <p><b>Transações:</b> ${data.analysis.tx_count}</p>
        <p><b>Score Idade:</b> ${data.analysis.age_score.toFixed(2)}</p>
        <p><b>Score Atividade:</b> ${data.analysis.activity_score.toFixed(2)}</p>
        <p><b>Score Liquidez:</b> ${data.analysis.liquidity_score.toFixed(2)}</p>
        <p><b>Score Governança:</b> ${data.analysis.governance_score.toFixed(2)}</p>
    </div>
    `;
    document.getElementById("result").innerHTML = html;
}

async function loadRanking() {
    try {
        const response = await fetch(`${backendURL}/ranking`);
        const data = await response.json();

        const rankingDiv = document.getElementById("ranking");
        if (!rankingDiv) return;

        let html = "<div class='card'><h3>Top Carteiras</h3>";
        data.forEach((wallet, index) => {
            html += `
            <div class="ranking-row">
                ${index + 1}. ${wallet.wallet}<br>
                <b>Score:</b> ${wallet.score.toFixed(2)}
            </div>
            `;
        });
        html += "</div>";
        rankingDiv.innerHTML = html;
    } catch (error) {
        console.log("Ranking indisponível", error);
    }
}

// Evento para o botão de análise manual
document.getElementById("analyzeManual").addEventListener("click", () => {
    const address = document.getElementById("manualAddress").value.trim();
    if (address && address.startsWith("0x") && address.length === 42) {
        analyzeWallet(address);
    } else {
        alert("Endereço inválido. Certifique-se de que começa com 0x e tem 42 caracteres.");
    }
});

window.addEventListener("load", () => {
    const connectBtn = document.getElementById("connectWallet");
    if (connectBtn) {
        connectBtn.addEventListener("click", connectWallet);
    }
    loadRanking();
});