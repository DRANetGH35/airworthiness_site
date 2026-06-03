const tachTimeEntry = document.getElementById("tach_time")
const tachTimeForm = document.getElementById("tach_time_form")
const timeSubmitBtn = document.getElementById("time_submit")
const timeErrorField = document.getElementById("timeEntryError")
const maintenance_table = document.getElementById('maintenance_table')
const planeField = document.getElementById("plane")
const engineField = document.getElementById("engine")

function colorTableOverdue(){
    for (let i = 2; i < maintenance_table.rows.length; i++){
        row = maintenance_table.rows[i]
        type = row.dataset.maintenance_type
        time_due = row.children[2].innerHTML
        if (type == "engine"){
            if (time_due < engineTime()){
                row.classList.add('table-danger')
            }
        }
        if (type == "aircraft"){
            if (time_due < planeTime()){
                row.classList.add('table-danger')
            }
        }
    }
}


function planeTime(){
    return parseFloat(planeField.innerHTML.split(":")[1].split(" ")[1])
}

function engineTime(){
    return parseFloat(engineField.innerHTML.split(":")[2].split(" ")[1])
}

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
colorTableOverdue();