$(document).ready(function () {
    $(".nav-link").on("click", function () {
        $(".nav-link").removeClass("active");
        $(this).addClass("active");
    });
});

const loginForm = document.querySelector('form');
loginForm.addEventListener('submit', function (event) {
    event.preventDefault();
    loginForm.classList.add('animate__animated', 'animate__fadeOut');
    setTimeout(function () {
        loginForm.submit();
    }, 1000);
});