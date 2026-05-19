const registerForm = document.getElementById('registerForm');
const nameInput = document.getElementById('name');
const nameError = document.getElementById('nameError');
const emailInput = document.getElementById('email');
const emailError = document.getElementById('emailError');
const passwordInput = document.getElementById('password');
const passwordError = document.getElementById('passwordError');
const confirmInput = document.getElementById('confirm');
const confirmError = document.getElementById('confirmError')
const submitBtn = document.getElementById("submit");
const result = document.getElementById('result');
const numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
const symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]

function clearError(el) {
    el.innerHTML = ""
}
function validateName(){
    let name = nameInput.value;
    if (name.length < 3) {
        showError(nameError,"username must be at least 3 characters long");
        return false;
    }
    clearError(nameError);
    return true;
}
function showError(el, message){
    el.innerHTML = message;
}
function containsNumber(string){
    let numbersInString = string.match(/\d+/g);
        if (numbersInString == null){
            return false;
        }
        return numbersInString.length >= 1;

}

function validateEmail() {
    let value = emailInput.value.trim();
    if (!(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value))) {
        showError(emailError,"Please enter a valid email address");
        return false;
    }
    clearError(emailError);
    return true;
}
function validatePassword() {
    let value = passwordInput.value;
    if (value.length < 8) {
        showError(passwordError, "password must be at least 8 characters");
        return false
    }
    if (!containsNumber(value)){
        showError(passwordError, "must contain at least one number");
        return false
    }
    clearError(passwordError);
    return true
}
function validateConfirm() {
    let password = passwordInput.value;
    let confirm = confirmInput.value;
    if (confirm === "") {
        showError(confirmError, "Please confirm your password");
        return false;
    }
    if (confirm !== password) {
        showError(confirmError, "Passwords do not match");
        return false;
    }
    clearError(confirmError);
    return true;
}
function validateForm() {
    let nameOK = validateName();
    let emailOK = validateEmail();
    let passwordOK = validatePassword();
    let confirmOK = validateConfirm();
    return nameOK && emailOK && passwordOK && confirmOK;
}

//prevent default reloading
registerForm.addEventListener('submit', function (event) {
    //clear result
    result.innerHTML = "";
    //validate form
    if (validateForm()) {
        result.innerHTML = "Form is valid"
        result.classList.remove('error')
        console.log('submit!')
    }else{
        event.preventDefault();
        result.innerHTML = "Please fix the errors"
        result.classList.add('error')
    }
});