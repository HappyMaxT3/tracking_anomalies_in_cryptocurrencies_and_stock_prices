document.getElementById('scrollButton').addEventListener('click', function() {
    // Найти целевой элемент
    var target = document.getElementById('targetSection');
    
    // Прокрутить до целевого элемента
    target.scrollIntoView({ behavior: 'smooth' });
});



$(function() {
    // Инициализация Datepicker
    $("#datepicker1").datepicker({
        dateFormat: "dd-mm-yy",
        onSelect: function(dateText) {
            selectedDateStart = dateText;
        }
    });

    let selectedDateStart = "";

    // Показать календарь при нажатии на иконку
    // $("#calendar-icon").click(function() {
    //     $("#datepicker").datepicker("show");
    // });

    // Сохранение даты в локальной переменной
    $("#datepicker1").on("change", function() {
        selectedDateStart = $(this).val();
    });
});

$(function() {
    // Инициализация Datepicker
    $("#datepicker2").datepicker({
        dateFormat: "dd-mm-yy",
        onSelect: function(dateText) {
            selectedDateEnd = dateText;
        }
    });

    let selectedDateEnd = "";

    $("#datepicker2").on("change", function() {
        selectedDateEnd = $(this).val();
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
    const stockErrorMessage = document.getElementById('stockErrorMessage');
    const portfelErrorMessage = document.getElementById('portfelErrorMessage');

    const invalidChars = /[.,<>?=+\-~\[\]#*]/;
    const validChasStock = /[ABCDEFGHIJKLMNOPQRSTUVWXYZ -]/;

    function validateInput() {
        const stockValue = stockInput.value;
        const portfelValue = portfelInput.value;
        let isValid = true;

        if (!validChasStock.test(stockValue)) {
            stockErrorMessage.textContent = 'incorrect';
            stockErrorMessage.parentElement.style.display = 'block';
            isValid = false;
        } else {
            stockErrorMessage.parentElement.style.display = 'none';
        }

        if (invalidChars.test(portfelValue)) {
            portfelErrorMessage.textContent = 'incorrect';
            portfelErrorMessage.parentElement.style.display = 'block';
            isValid = false;
        } else {
            portfelErrorMessage.parentElement.style.display = 'none';
        }

        return isValid;
    }

    stockInput.addEventListener('input', validateInput);
    portfelInput.addEventListener('input', validateInput);

    form.addEventListener('submit', function(event) {
        if (!validateInput()) {
            event.preventDefault();
        }
    });
});
