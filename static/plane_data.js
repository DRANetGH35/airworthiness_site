const tachTimeEntry = document.getElementById("tach_time")
const tachTimeForm = document.getElementById("tach_time_form")
const timeSubmitBtn = document.getElementById("time_submit")
const timeErrorField = document.getElementById("timeEntryError")



function timeFormValid(){
    value = tachTimeEntry.value;
    if (value == ""){
        timeErrorField.innerHTML = "Please fill the time field"
        return false
    }
    if (parseFloat(value) === NaN) {
        timeErrorField.innerHTML = "Please enter a number"
        return false
    }
    timeErrorField.innerHTML = ""
    return true
}

tachTimeForm.addEventListener('submit', function (event) {
    if (timeFormValid()){

    }else{
        event.preventDefault();
    }
})