const time_input = document.getElementById("time");

const buses = document.querySelectorAll(".bus");

const radio_buttons = document.querySelectorAll(".radioButton")

if (time_input.value) {
    buses.forEach(bus => {
        if (bus.id == "hour" + time_input.value.replace(":","")) {
            bus.classList.remove("nodisplay");
        };
    });
};

time_input.addEventListener("change", (event) =>  {
    buses.forEach(bus => {
        bus.classList.add("nodisplay");
        if (bus.id == "hour" + event.target.value.replace(":","")) {
            bus.classList.remove("nodisplay");
        };
    });
});

time_input.addEventListener("change", () => {
    radio_buttons.forEach(radio_button => {
        radio_button.checked = false;
    });
});