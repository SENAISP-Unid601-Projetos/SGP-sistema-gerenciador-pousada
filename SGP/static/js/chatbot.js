messageCount = 0; // Contador para gerar IDs únicos

async function enviarMensagem() {
  const inputMensagem = document.querySelector("input").value;
  const respostaContainer = document.getElementById("chatbotContent");
  
  // Verificação e exibição de mensagem de erro
  if (!inputMensagem) {
    const respostaParagrafo = document.getElementById("errorMessage");
    respostaParagrafo.textContent = "Por favor, digite uma mensagem!";
    return;
  }

  // Cria e exibe a mensagem do usuário
  const userMessageElement = document.createElement("div");
  userMessageElement.classList.add("message", "user-message");
  userMessageElement.textContent = inputMensagem;
 

  // Cria e exibe um elemento de resposta do bot com um id único
  const botResponseElement = document.createElement("div");
  botResponseElement.classList.add("message", "bot-message");
  botResponseElement.id = `botResponse-${messageCount}`; // Adiciona um id com o número atual
  botResponseElement.textContent = "Carregando resposta...";
  

  // Incrementa o contador para o próximo par de mensagens
  messageCount++;

  // Define o contexto e concatena a mensagem do usuário
  const contexto =
    "Nesta conversa, você terá que me responder dúvidas sobre uma pousada. Saiba que essa pousada tem 4 quartos livres e 2 ocupados, os quartos que estão livres estão na faixa de preço de 500 reais a diária.";
  const mensagemCompleta = contexto + inputMensagem;
  console.log(JSON.stringify({ text: mensagemCompleta }));
  console.log("ENVIOU");

  try {
    const response = await fetch("http://localhost:7000/ia", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: mensagemCompleta }),
    });

    if (!response.ok) {
      throw new Error("Erro na requisição: " + response.statusText);
    }

    const responseText = await response.text();
    try {
      const data = JSON.parse(responseText);
      document.getElementById(`botResponse-${messageCount - 1}`).textContent = data.response;
    } catch (error) {
      document.getElementById(`botResponse-${messageCount - 1}`).textContent = responseText;
    }
  } catch (error) {
    document.getElementById(`botResponse-${messageCount - 1}`).textContent = "Erro ao enviar a mensagem.";
    console.error("Erro:", error);
  }
}
