(() => {
    const passwordInputContainer = document.querySelector('.form__input-container:has(#password)');

    const togglePasswordVisibility = (inputContainer) => {
        const input = inputContainer.querySelector('#password'),
            eyeIcon = inputContainer.querySelector('.form__input-container__icon-container:has(.eye)'),
            eyeHiddenIcon = inputContainer.querySelector('.form__input-container__icon-container:has(.eye-hidden)');

        eyeIcon.addEventListener('click', () => {
            eyeIcon.classList.remove('active');
            eyeHiddenIcon.classList.add('active');

            input.type = 'text';
        });

        eyeHiddenIcon.addEventListener('click', () => {
            eyeIcon.classList.add('active');
            eyeHiddenIcon.classList.remove('active');

            input.type = 'password';
        });
    };

    passwordInputContainer && togglePasswordVisibility(passwordInputContainer);
})();
