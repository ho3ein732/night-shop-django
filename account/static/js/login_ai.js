document.querySelectorAll('.close-btn').forEach((btn) => {
    btn.addEventListener('click', function () {
        this.parentElement.style.display = 'none';
    });
});
