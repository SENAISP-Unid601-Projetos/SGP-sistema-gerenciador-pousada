document.querySelector('form').onsubmit = function() {
    const checkin = new Date(document.getElementById('checkin').value);
    const checkout = new Date(document.getElementById('checkout').value);
    if (checkin >= checkout) {
        return false; // Impede o envio do formulário
    }
    return true; // Permite o envio
};
