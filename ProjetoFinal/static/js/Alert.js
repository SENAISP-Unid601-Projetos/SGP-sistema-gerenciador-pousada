document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();  // Previne o envio padrão do formulário

    // Coleta os dados do formulário
    let formData = new FormData(this);

    // Faz a requisição para o Flask
    fetch('/addData', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);  // Exibe o erro
        } else if (data.success) {
            alert(data.success);  // Exibe a mensagem de sucesso
            window.location.href = "/";  // Redireciona após sucesso
        }
    })
    .catch(error => console.error('Erro na requisição:', error));
});

