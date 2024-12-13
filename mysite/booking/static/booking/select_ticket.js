const time_input = document.getElementById("time");

const buses = document.querySelectorAll(".bus");

if (time_input.value) {
    buses.forEach(bus => {
        if (bus.id == "hour" + time_input.value.replace(":","")) {
            bus.classList.remove("nodisplay");
        };
    });
};

time_input.addEventListener("change", (event) =>  {
    console.log(event.target.value);
    buses.forEach(bus => {
        bus.classList.add("nodisplay");
        if (bus.id == "hour" + event.target.value.replace(":","")) {
            bus.classList.remove("nodisplay");
        };
    });
});

buses.forEach(bus => {
    console.log(bus.id)
});