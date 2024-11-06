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
    "Nesta conversa, você terá que me responder dúvidas sobre a pousada Quinta Do Ypuã. A seguir, te darei as informações gerais da pousada e você terá que responder duvidas sobre a pousada com base nas informações que te passei. A pousada Quinta do Ypuã é um ambiente com muita natureza e ótimo atendimento, para alugar os quartos, é necessário se fazer uma reserva de no minimo 2 dias, tendo como opções os quartos: Domo - A novidade da pousada, com design geodésico sustentável. Ideal para quem busca uma estadia inovadora e diferenciada. R$ 590,00/noite. Chalé Família - Com dois quartos climatizados, cozinha equipada, churrasqueira e sacada com vista para o mar. R$ 590,00/noite. Charrua - Ônibus remodelado em quarto aconchegante, combinando o charme da estrada com conforto. R$ 490,00/noite. Cabana - Em área reservada, oferece camas confortáveis, cozinha, varanda e deck com churrasqueira e vista para o mar. R$ 490,00/noite. Suíte com Cozinha - Suíte com vista para o mar, cozinha equipada, deck com churrasqueira. R$ 390,00/noite. Estacionamento para Overlanders - Espaço para veículos, com pontos de água, luz, banheiro e churrasqueira. R$ 100,00/noite.  Todos os quartos tem wifi, tv a cabo, ar-condicionado e cozinha, com exceção do estacionamento, que apenas possui wifi e ducha";
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
