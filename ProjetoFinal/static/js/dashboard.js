// Gráfico de Linha (Tema Escuro)
const linhaCtx = document.getElementById('linha-chart').getContext('2d');
const linhaChart = new Chart(linhaCtx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
            label: 'Reservas por Mês',
            data: [10, 20, 30, 40, 35, 25, 45, 50, 60, 55, 70, 80],
            borderColor: '#4CAF50', // Cor da linha (verde claro)
            backgroundColor: 'rgba(76, 175, 80, 0.2)', // Fundo transparente para a linha
            fill: true // Preencher a área abaixo da linha
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    color: '#ffffff' // Cor da legenda (branco)
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#ffffff' // Cor dos labels do eixo X (branco)
                },
                grid: {
                    color: '#333333' // Cor da grade do eixo X (cinza escuro)
                }
            },
            y: {
                ticks: {
                    color: '#ffffff' // Cor dos labels do eixo Y (branco)
                },
                grid: {
                    color: '#333333' // Cor da grade do eixo Y (cinza escuro)
                }
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
            borderColor: ['#2E7D32', '#FFA000', '#D32F2F'], // Cor das bordas
            borderWidth: 2, // Aumentando a espessura da borda
            hoverBackgroundColor: ['#66BB6A', '#FFD54F', '#E57373'], // Cor ao passar o mouse
            hoverBorderColor: ['#1B5E20', '#FF8F00', '#C62828'], // Borda ao passar o mouse
        }]
    },
    options: {
        responsive: true,
        cutout: '70%', // Aumenta o espaço no centro do gráfico de rosca
        plugins: {
            legend: {
                position: 'bottom', // Posiciona a legenda na parte inferior
                labels: {
                    color: '#FFF', // Define a cor do texto da legenda no tema escuro
                    font: {
                        size: 14 // Tamanho da fonte
                    }
                }
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.7)', // Fundo da tooltip escuro
                titleColor: '#FFF', // Cor do título na tooltip
                bodyColor: '#FFF', // Cor do conteúdo na tooltip
                borderColor: '#FFF', // Borda branca na tooltip
                borderWidth: 1, // Espessura da borda
            }
        },
        animation: {
            animateRotate: true, // Animação de rotação ao carregar
            animateScale: true   // Animação de escala ao carregar
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

//menu
function toggleMenu() {
    var sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
  }





