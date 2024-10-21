// Gráfico de Linha (Exemplo)
const linhaCtx = document.getElementById('linha-chart').getContext('2d');
const linhaChart = new Chart(linhaCtx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
            label: 'Reservas por Mês',
            data: [10, 20, 30, 40, 35, 25, 45, 50, 60, 55, 70, 80],
            borderColor: '#4CAF50',
            fill: false
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            }
        }
    }
});

// Gráfico de Rosca (Exemplo)
const satisfacaoCtx = document.getElementById('satisfacaoChart').getContext('2d');
const satisfacaoChart = new Chart(satisfacaoCtx, {
    type: 'doughnut',
    data: {
        labels: ['Satisfeitos', 'Neutros', 'Insatisfeitos'],
        datasets: [{
            label: 'Satisfação dos Clientes',
            data: [85, 10, 5],
            backgroundColor: ['#4CAF50', '#FFC107', '#F44336'],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom',
            }
        }
    }
});

const feedbackItems = document.querySelectorAll('.feedback-item');
let currentFeedbackIndex = 0;

function showFeedback() {
    feedbackItems.forEach((item, index) => {
        item.classList.remove('active');
        if (index === currentFeedbackIndex) {
            item.classList.add('active');
        }
    });
    currentFeedbackIndex = (currentFeedbackIndex + 1) % feedbackItems.length;
}

// Mostra o primeiro feedback ao carregar
showFeedback();
// Muda o feedback a cada 5 segundos
setInterval(showFeedback, 5000);


// Função para atualizar a satisfação
function atualizarSatisfacao(novaSatisfacao) {
  const porcentagemElemento = document.querySelector('.satisfaction-percentage');
  const progressElemento = document.querySelector('.progress');

  porcentagemElemento.textContent = novaSatisfacao + '%';
  progressElemento.style.width = novaSatisfacao + '%';
}

// Exemplo de uso
atualizarSatisfacao(85); // Você pode mudar esse valor conforme necessário







