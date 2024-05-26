$(function() {
    // Инициализация Datepicker
    $("#datepicker").datepicker({
        dateFormat: "dd-mm-yy",
        onSelect: function(dateText) {
            selectedDate = dateText;
        }
    });

    let selectedDate = "";

    // Показать календарь при нажатии на иконку
    // $("#calendar-icon").click(function() {
    //     $("#datepicker").datepicker("show");
    // });

    // Сохранение даты в локальной переменной
    $("#datepicker").on("change", function() {
        selectedDate = $(this).val();
    });
});


document.addEventListener('DOMContentLoaded', function() {
    var emailForm = document.getElementById('emailForm');
    var emailInput = document.getElementById('email');

    emailForm.addEventListener('submit', function(event) {
        var emailValue = emailInput.value;
        if (!validateEmail(emailValue)) {
            event.preventDefault(); // Останавливаем отправку формы только если email некорректен
        } else {
            emailError.style.display = 'none';
        }
    });

    function validateEmail(email) {
        var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('validNames');
    const stockInput = document.getElementById('stock');
    const portfelInput = document.getElementById('portfel');
    const errorMessage = document.getElementById('errorMessage');

    const invalidChars = /[.,<>?=+\-~\[\]#*]/;

    function validateInput() {
        const stockValue = stockInput.value;
        const portfelValue = portfelInput.value;

        if (invalidChars.test(stockValue) || invalidChars.test(portfelValue)) {
            errorMessage.textContent = 'Введенные данные некорректны';
            errorMessage.style.display = 'block';
        } else {
            errorMessage.style.display = 'none';
        }
    }

    stockInput.addEventListener('input', validateInput);
    portfelInput.addEventListener('input', validateInput);

    form.addEventListener('submit', function(event) {
        const stockValue = stockInput.value;
        const portfelValue = portfelInput.value;

        if (invalidChars.test(stockValue) || invalidChars.test(portfelValue)) {
            errorMessage.textContent = 'Введенные данные некорректны';
            errorMessage.style.display = 'block';
            event.preventDefault();
        } else {
            errorMessage.style.display = 'none';
        }
    });
});