function goBack() {
    window.history.back(); // Navigate to the previous page
}

document.getElementById("male-btn").addEventListener("click", function () {
    // Set the value of the hidden gender input to "male"
    document.getElementById("gender").value = "male";
    // Apply the selected class to the male button and remove it from the female button
    document.getElementById("male-btn").classList.add("selected");
    document.getElementById("female-btn").classList.remove("selected");
});

document.getElementById("female-btn").addEventListener("click", function () {
    // Set the value of the hidden gender input to "female"
    document.getElementById("gender").value = "female";
    // Apply the selected class to the female button and remove it from the male button
    document.getElementById("female-btn").classList.add("selected");
    document.getElementById("male-btn").classList.remove("selected");
});
