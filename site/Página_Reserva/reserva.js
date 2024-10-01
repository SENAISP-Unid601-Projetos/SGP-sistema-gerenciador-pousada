document.addEventListener('DOMContentLoaded', () => {
    const forms = ['reservaDomo', 'reservaCharrua', 'reservaSuite'];

    forms.forEach(formId => {
        const form = document.getElementById(formId);
        if (form) {
            form.addEventListener('submit', function(event) {
                event.preventDefault();
                alert('Reserva realizada com sucesso!');
                this.reset(); // Limpa o formulário após envio
                const modal = bootstrap.Modal.getInstance(this.closest('.modal'));
                modal.hide(); // Fecha o modal
            });
        }
    });

    document.querySelectorAll('.btn-reserva').forEach(button => {
        button.addEventListener('click', () => {
            const modalId = button.getAttribute('data-bs-target');
            const modal = new bootstrap.Modal(document.querySelector(modalId));
            modal.show();
        });
    });
});
