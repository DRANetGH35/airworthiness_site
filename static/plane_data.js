const tachTimeEntry = document.getElementById("tach_time")
const tachTimeForm = document.getElementById("tach_time_form")
const timeSubmitBtn = document.getElementById("time_submit")
const timeErrorField = document.getElementById("timeEntryError")
const maintenance_table = document.getElementById('maintenance_table')
const planeField = document.getElementById("plane")
const engineField = document.getElementById("engine")

function IterateTable(){
    for (let i = 2; i < maintenance_table.rows.length; i++){
        row = maintenance_table.rows[i]
        type = row.dataset.maintenance_type
        time_due = row.children[2].innerHTML != "---" ?  parseFloat(row.children[2].innerHTML) : null
        date_due = row.children[1].innerHTML != "---" ?  row.children[1].innerHTML : null
        if (date_due){
            date_due = new Date(date_due);
            todays_date = new Date();
            if (date_due < todays_date){
                console.log('date_overdue')
                row.classList.add('table-danger')
            }
        }
        if (type == "engine"){
            if (time_due && time_due < engineTime()){
                row.classList.add('table-danger')
            }
            if(AlmostDue(row, 'engine')){
                row.classList.add('table-warning')
            }
        }
        if (type == "aircraft"){
            if (time_due && time_due < planeTime()){
                row.classList.add('table-danger')
            }
            if (AlmostDue(row, 'aircraft')){
                row.classList.add('table-warning')
            }
        }

    }
}

function AlmostDue(row, maintenance_type){
    if (row.dataset.interval) {
            today = new Date();
            date_due = row.children[1].innerHTML != "---" ?  new Date(row.children[1].innerHTML) : null
            current_time = time_due = row.children[2].innerHTML != "---" ?  parseFloat(row.children[2].innerHTML) : null
            //set total hours to hours recorded on engine or aircraft depending on row
            total_hours = maintenance_type == "engine" ? engineTime() : planeTime()
            interval_hours = row.dataset.interval_hours != "" ? parseFloat(row.dataset.interval_hours): null;
            interval_months = row.dataset.interval_months != "" ? parseFloat(row.dataset.interval_months): null;
            if (interval_hours){
                tach_hours_till_due = current_time - total_hours
                percentage_complete = ((tach_hours_till_due / interval_hours) * 100)
                if (((tach_hours_till_due / interval_hours) * 100) < 25){
                    return true
                }
            }
            if (interval_months){
                ms_till_due = date_due - today
                s_till_due = Math.floor(ms_till_due / 1000)
                min_till_due = Math.floor(s_till_due / 60)
                hr_till_due = Math.floor(min_till_due / 60)
                d_till_due = Math.floor(hr_till_due / 24)
                months_till_due = Math.floor(d_till_due / 30)
                percentage_until_due = 100 - ((d_till_due / (interval_months * 30)) * 100)
                if (percentage_until_due > 25){
                    return true
                }
            }
        }
    return false
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
IterateTable();