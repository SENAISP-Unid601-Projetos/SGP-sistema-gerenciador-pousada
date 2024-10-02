document.addEventListener('DOMContentLoaded', () => {
    // Animação do texto na seção hero ao carregar a página
    const heroText = document.querySelector('.hero-text');
    heroText.classList.add('mover'); // Adiciona a classe para mover o texto

    // Efeito de scroll suave
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            target.scrollIntoView({ behavior: 'smooth' });
        });
    });

    // Animação das imagens na seção sobre
    const images = document.querySelectorAll('.imagem-wrapper');
    let currentIndex = 0;

    function showNextImage() {
        images[currentIndex].classList.remove('active'); // Remove a classe ativa da imagem atual
        currentIndex = (currentIndex + 1) % images.length; // Incrementa o índice
        images[currentIndex].classList.add('active'); // Adiciona a classe ativa à nova imagem
    }

    setInterval(showNextImage, 3000); // Muda a imagem a cada 3 segundos
});
