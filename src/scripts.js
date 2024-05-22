$(function() {
    // Инициализация Datepicker
    $("#datepicker").datepicker({
        dateFormat: "dd-mm-yy",
        onSelect: function(dateText) {
            selectedDate = dateText;
            console.log("Выбранная дата: " + selectedDate);
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
