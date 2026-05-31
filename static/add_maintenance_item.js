const form = document.getElementById('form')

const description = document.getElementById('description')
const singleRadio =  document.getElementById('single_radio')
const intervalRadio = document.getElementById('interval_radio')
const intervalDiv = document.getElementById('interval_div')
const singleDiv = document.getElementById('single_div')
const hoursLastComplete = document.getElementById('tach_hours_last_complete')
const dateLastComplete = document.getElementById('date_last_complete')
const intervalHours = document.getElementById('interval_hours')
const intervalMonths = document.getElementById('interval_months')
const dateDue = document.getElementById('date_due')
const error = document.getElementById('error')
const dateLastCompleteError = document.getElementById('date_last_complete_error')
const intervalHoursError = document.getElementById('interval_hours_error')
const intervalMonthsError = document.getElementById('interval_months_error')
const descriptionError = document.getElementById('description_error')

singleRadio.addEventListener('click', singleClicked)
intervalRadio.addEventListener('click', intervalClicked)
//intervalHours.addEventListener('keyup', intervalHoursTyped)
//intervalMonths.addEventListener('keyup', intervalMonthsTyped)
hoursLastComplete.addEventListener('keyup', hoursLastCompleteTyped)
dateLastComplete.addEventListener('change', dateLastCompleteTyped)

function clearAllErrors(){
    dateLastCompleteError.innerHTML = ""
    intervalHoursError.innerHTML = ""
    intervalMonthsError.innerHTML = ""
}


function singleClicked(){
    singleDiv.classList.remove('hidden')
    intervalDiv.classList.remove('show')
    singleDiv.classList.add('show')
    intervalDiv.classList.add('hidden')
}

function intervalClicked(){
    singleDiv.classList.remove('show')
    intervalDiv.classList.remove('hidden')
    singleDiv.classList.add('hidden')
    intervalDiv.classList.add('show')
}


function hoursLastCompleteTyped(){
    if (hoursLastComplete.value !== ""){
        intervalHours.disabled = false
    }else{
        intervalHours.disabled = true
    }
}
function dateLastCompleteTyped(){
    if (dateLastComplete.value !== ""){
        intervalMonths.disabled = false
    }else{
        intervalMonths.disabled = true
    }
}

function validateForm(){
    clearAllErrors();
    if (description.value === ""){
        console.log('no desc')
        descriptionError.innerHTML = "Description cannot be empty"
        return false
    }

    if (singleRadio.checked) {
        return true
    }else{
        if (hoursLastComplete.value === "" && dateLastComplete.value === ""){
            console.log('empty')
            dateLastCompleteError.innerHTML = "Please enter a date or hour value"
            return false
        }
        if (hoursLastComplete.value !== "" && intervalHours.value === "") {
            console.log('hours')
            intervalHoursError.innerHTML = "must not be empty"
            return false
        }
        if (dateLastComplete.value !== "" && intervalMonths.value === ""){
            console.log('date')
            intervalMonthsError.innerHTML = "must not be empty"
            return false
        }
        }
    return true
}

form.addEventListener('submit', function (event) {
    //validate form
    if (validateForm()) {
    }else{
        event.preventDefault();
    }
});

clearAllErrors();