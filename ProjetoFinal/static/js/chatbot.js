async function enviarMensagem() {
  const inputMensagem = document.querySelector("input").value;
  const respostaParagrafo = document.querySelector("p");

  if (!inputMensagem) {
    respostaParagrafo.textContent = "Por favor, digite uma mensagem!";
    return;
  }

  // Define o contexto pré-selecionado
  const contexto =
    "Nesta conversa, você terá que me responder dúvidas sobre uma pousada. Saiba que essa pousada tem 4 quartos livres e 2 ocupados, os quartos que estão livres estão na faixa de preço de 500 reais a diária.";

  // Concatena o contexto com a mensagem do usuário
  const mensagemCompleta = contexto + inputMensagem;
  console.log(JSON.stringify({ text: mensagemCompleta }));

  try {
    const response = await fetch("http://localhost:7000/ia", {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // Certifique-se de que este cabeçalho está presente
      },
      body: JSON.stringify({ text: mensagemCompleta }), // Converte os dados para JSON
    });

    if (!response.ok) {
      throw new Error("Erro na requisição: " + response.statusText);
    }

    const responseText = await response.text(); // Obtenha a resposta como texto
    try {
      const data = JSON.parse(responseText); // Tente parsear como JSON
      respostaParagrafo.textContent = data.response;
    } catch (error) {
      respostaParagrafo.textContent = responseText; // Se falhar, exiba o texto puro
    }
  } catch (error) {
    respostaParagrafo.textContent = "Erro ao enviar a mensagem.";
    console.error("Erro:", error);
  }
}