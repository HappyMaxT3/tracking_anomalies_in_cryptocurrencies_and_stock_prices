//hide password
document.addEventListener('DOMContentLoaded', function () {
    const togglePasswordButton = document.getElementById('togglePasswordButton');
    const togglePasswordIcon = document.getElementById('togglePasswordIcon');
    if (togglePasswordButton) {
        togglePasswordButton.addEventListener('click', function () {
            const passwordField = document.getElementById('password');
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                togglePasswordIcon.src = '../static/images/show_password_icon.png'; 
                togglePasswordIcon.alt = 'Hide Password';
            } else {
                passwordField.type = 'password';
                togglePasswordIcon.src = '../static/images/hide_password_icon.png'; 
                togglePasswordIcon.alt = 'Show Password';
            }
        });
    }
});


//scroll button
document.getElementById('scrollButton').addEventListener('click', function() {
    // Найти целевой элемент
    var target = document.getElementById('targetSection');
    // Прокрутить до целевого элемента
    target.scrollIntoView({ behavior: 'smooth' });
});


//calendars
$(function() {
    // Инициализация Datepicker
    $("#datepicker1").datepicker({
        dateFormat: "dd-mm-yy",
        firstDay: 1,
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
        firstDay: 1,
        onSelect: function(dateText) {
            selectedDateEnd = dateText;
        }
    });

    let selectedDateEnd = "";

    $("#datepicker2").on("change", function() {
        selectedDateEnd = $(this).val();
    });
});


//correct input check
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('validNames');
    const stockInput = document.getElementById('stock');
    const portfelInput = document.getElementById('portfel');
    const stockErrorMessage = document.getElementById('stockErrorMessage');
    const portfelErrorMessage = document.getElementById('portfelErrorMessage');
    const validChars = /^[A-Z -]*$/; 

    function validateInput() {
        const stockValue = stockInput.value.toUpperCase();
        const portfelValue = portfelInput.value.toUpperCase();
        
        stockInput.value = stockValue; // Преобразование в заглавные буквы
        portfelInput.value = portfelValue; // Преобразование в заглавные буквы

        let isValid = true;

        if (stockValue && !validChars.test(stockValue)) {
            stockErrorMessage.textContent = 'incorrect';
            stockErrorMessage.parentElement.style.display = 'block';
            isValid = false;
        } else {
            stockErrorMessage.parentElement.style.display = 'none';
        }

        if (!validChars.test(portfelValue)) {
            portfelErrorMessage.textContent = 'incorrect';
            portfelErrorMessage.parentElement.style.display = 'block';
            isValid = false;
        } else {
            portfelErrorMessage.parentElement.style.display = 'none';
        }

        if (stockValue.includes('-USD')) {
            portfelInput.value = stockValue;
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


//autocomplete
function autocomplete(inp, arr) {
    let currentFocus;
    inp.addEventListener("input", function(e) {
        let a, b, i, val = this.value;
        closeAllLists();
        if (!val) { return false; }
        currentFocus = -1;
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        this.parentNode.appendChild(a);
        for (i = 0; i < arr.length; i++) {
            if (arr[i].substr(0, val.length).toUpperCase() === val.toUpperCase()) {
                b = document.createElement("DIV");
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                b.addEventListener("click", function(e) {
                    inp.value = this.getElementsByTagName("input")[0].value;
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });

    inp.addEventListener("keydown", function(e) {
        let x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            currentFocus++;
            addActive(x);
        } else if (e.keyCode == 38) {
            currentFocus--;
            addActive(x);
        } else if (e.keyCode == 13) {
            e.preventDefault();
            if (currentFocus > -1) {
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        for (let i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        let x = document.getElementsByClassName("autocomplete-items");
        for (let i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

const suggestions = ["AAPL", "ANTANANARIVU", "ALYASKA", "BIMBIMBAMBAMFIRST", "BIMBIMBAMBAMSECOND", "PIZDEC", "SUKA", "BLYAT"];
autocomplete(document.getElementById("stock"), suggestions);


//email check
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

