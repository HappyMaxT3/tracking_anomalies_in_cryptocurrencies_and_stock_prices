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

        // проверка на акцию или крипту
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

    // Autocomplete functionality
    const stockDropdown = document.getElementById('stock-dropdown');
    const portfelDropdown = document.getElementById('portfel-dropdown');
    const stockOptions = [
        "AAPL",
        "AMZN",
        "MSFT",
        "GOOGL",
        "TSLA",
        "META",
        "NVDA",
        "PYPL",
        "NFLX",
        "INTC",
        "CSCO",
        "ADBE",
        "QCOM",
        "TXN",
        "IBM",
        "BTC-USD",
        "ETH-USD",
        "USDT-USD",
        "BNB-USD",
        "XRP-USD",
        "ADA-USD",
        "SOL-USD",
        "DOGE-USD",
        "DOT-USD",
        "AVAX-USD",
        "SHIB-USD",
        "MATIC-USD",
        "LTC-USD",
        "LINK-USD",
        "UNI-USD"
      ];
    const portfelOptions = [    
    "GSPC",
    "DJI",
    "IXIC",
    "FTSE",
    "GDAXI",
    "FCHI",
    "HSI",
    "BSESN",
    "BTC-USD",
    "ETH-USD",
    "USDT-USD",
    "BNB-USD",
    "XRP-USD",
    "ADA-USD",
    "SOL-USD",
    "DOGE-USD",
    "DOT-USD",
    "AVAX-USD",
    "SHIB-USD",
    "MATIC-USD",
    "LTC-USD",
    "LINK-USD",
    "UNI-USD"
];

    function filterOptions(options, query) {
        return options.filter(option => option.toLowerCase().includes(query.toLowerCase()));
    }

    function showDropdown(dropdown, options) {
        dropdown.innerHTML = '';
        options.forEach(option => {
            const optionElement = document.createElement('div');
            optionElement.className = 'autocomplete-option';
            optionElement.textContent = option;
            optionElement.addEventListener('click', function() {
                if (dropdown.id === 'stock-dropdown') {
                    stockInput.value = option;
                } else {
                    portfelInput.value = option;
                }
                dropdown.innerHTML = '';
            });
            dropdown.appendChild(optionElement);
        });
        dropdown.style.display = 'block';
    }

    stockInput.addEventListener('focus', function() {
        showDropdown(stockDropdown, stockOptions);
    });

// autocomplete(document.getElementById("stock"), suggestions);

    stockInput.addEventListener('input', function() {
        const filteredOptions = filterOptions(stockOptions, stockInput.value);
        showDropdown(stockDropdown, filteredOptions);
    });

    portfelInput.addEventListener('focus', function() {
        showDropdown(portfelDropdown, portfelOptions);
    });

    portfelInput.addEventListener('input', function() {
        const filteredOptions = filterOptions(portfelOptions, portfelInput.value);
        showDropdown(portfelDropdown, filteredOptions);
    });

    document.addEventListener('click', function(e) {
        if (!e.target.closest('.autocomplete')) {
            stockDropdown.style.display = 'none';
            portfelDropdown.style.display = 'none';
        }
    });
});
