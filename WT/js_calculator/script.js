let inputField = document.getElementById('inputField');

function appendNumber(value) {
        console.log("Button pressed:", value); 
    inputField.value += value;
}

function clearInput() {
    inputField.value = '';
}

function calculate() {
    let input = inputField.value;

    if (!isValidInput(input)) {
        alert("Invalid input! Please check your numbers and operators.");
        inputField.value = '';
        return;
    }

    try {
        let result = eval(input);
        inputField.value = result;
    } catch (e) {
        alert("Error in calculation. Please check your input.");
        inputField.value = '';
    }
}

function isValidInput(input) {
    return /^[0-9+\-*/.]+$/.test(input);
}

function calculateSquare() {
    let input = inputField.value;
    if (input === '') {
        alert("Please enter a number first.");
    } else if (isNaN(input)) {
        alert("Invalid input! Please enter a valid number.");
    } else {
        let result = Math.pow(input, 2);
        inputField.value = result;
    }
}

