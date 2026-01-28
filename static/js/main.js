// Main JS file for frontend interactions

document.addEventListener('DOMContentLoaded', () => {
    console.log('BloodBridge App Loaded');

    // Add 3D effect to cards on mousemove
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * -2; // Reduced rotation
            const rotateY = ((x - centerX) / centerX) * 2;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
        });
    });
});

function validateRegisterForm() {
    const password = document.getElementById('password').value;
    if (password.length < 4) {
        alert('Password must be at least 4 characters long');
        return false;
    }
    return true;
}
