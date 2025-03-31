document.addEventListener('DOMContentLoaded', () => {
    console.log('El DOM se ha cargado correctamente.');

    const btnRegistro = document.getElementById('btn-registro');
    const btnLogin = document.getElementById('btn-login');
    const formRegistro = document.getElementById('form-registro');
    const formLogin = document.getElementById('form-login');

    console.log('btnRegistro:', btnRegistro);
    console.log('btnLogin:', btnLogin);
    console.log('formRegistro:', formRegistro);
    console.log('formLogin:', formLogin);

    if (btnRegistro && btnLogin && formRegistro && formLogin) {
        console.log('Elementos encontrados: btnRegistro, btnLogin, formRegistro, formLogin');

        btnRegistro.addEventListener('click', () => {
            console.log('Clic en Registrarse');
            formRegistro.style.display = 'block';
            formLogin.style.display = 'none';
            btnRegistro.classList.add('btn-primary');
            btnRegistro.classList.remove('btn-secondary');
            btnLogin.classList.add('btn-secondary');
            btnLogin.classList.remove('btn-primary');
        });

        btnLogin.addEventListener('click', () => {
            console.log('Clic en Iniciar Sesión');
            formRegistro.style.display = 'none';
            formLogin.style.display = 'block';
            btnLogin.classList.add('btn-primary');
            btnLogin.classList.remove('btn-secondary');
            btnRegistro.classList.add('btn-secondary');
            btnRegistro.classList.remove('btn-primary');
        });
    } else {
        console.error('No se encontraron los elementos necesarios para alternar los formularios.');
    }
});