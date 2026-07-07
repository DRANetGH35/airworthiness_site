passwordField = document.getElementById('password')
passwordError = document.getElementById('passwordError')
confirmPasswordField = document.getElementById('confirmPassword')
confirmPasswordError = document.getElementById('confirmPasswordError')
resetPasswordForm = document.getElementById('resetPasswordForm')
submitBtn = document.getElementById('submit')
function containsNumber(string){
    let numbersInString = string.match(/\d+/g);
        if (numbersInString == null){
            return false;
        }
        return numbersInString.length >= 1;

}
function validatePassword() {
    let value = passwordField.value;
    if (value.length < 8) {
        passwordError.innerHTML = "password must be at least 8 characters";
        return false
    }
    if (!containsNumber(value)) {
        passwordError.innerHTML = "password must contain at least one number"
        return false
    }
    passwordError.innerHTML = ""
    return true
}
function validateConfirm() {
    let password = passwordField.value;
    let confirm = confirmPasswordField.value;
    if (confirm === "") {
        confirmPasswordError.innerHTML = "Please confirm your password";
        return false;
    }
    if (confirm !== password) {
        confirmPasswordError.innerHTML = "Passwords do not match";
        return false;
    }
    confirmPasswordError.innerHTML = "";
    return true;
}
resetPasswordForm.addEventListener('submit', function (event){
    result.innerHTML = ""
    if (!validateConfirm()){
        event.preventDefault()
        return 0
    }
    if (!validatePassword()){
        event.preventDefault();
        return 0}
    else if (passwordField.value !== confirmPasswordField.value){
        event.preventDefault()
        result.innerHTML = "Passwords must match"
        return 0
    }else{
        return 1
    }
})