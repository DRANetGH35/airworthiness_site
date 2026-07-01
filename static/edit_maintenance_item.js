const maintenance_id = window.location.href.split("/")[6]

const descriptionEntry = document.getElementById('description')
const aircraftRadioEntry = document.getElementById('maintenance_type_aircraft')
const engineRadioEntry = document.getElementById('maintenance_type_engine')
const singleRadioEntry = document.getElementById('single_radio')
const intervalRadioEntry = document.getElementById('interval_radio')
const tachDueEntry = document.getElementById('tach_due')
const dateDueEntry = document.getElementById('date_due')
const tachSinceLastCompleteEntry = document.getElementById('tach_hours_last_complete')
const dateSinceLastCompleteEntry = document.getElementById('date_last_complete')
const intervalHoursEntry = document.getElementById('interval_hours')
const intervalMonthsEntry = document.getElementById('interval_months')


if (maintenance_id !== "new") {
    url = `/fetch_maintenance_item/${maintenance_id}`

    fetch(url).then(response => response.json()).then(data => {
        console.log(data)
        let description = data['description']
        let maintenance_type = data['maintenance_type']
        let interval = data['interval']
        let due_date = data['due_date']
        let due_tach = data['due_tach']

        let tach_last_completed = data['tach_last_completed']
        let date_last_completed = data['date_last_completed']
        let interval_hours = data['interval_hours']
        let interval_months = data['interval_months']

        descriptionEntry.value = null ? "" : description
        dateDueEntry.value = null ? "" : due_date
        tachDueEntry.value = null ? "" : due_tach

        if (interval) {
            if (tach_last_completed !== null) {
                intervalHoursEntry.disabled = false
            }
            if (date_last_completed !== null) {
                intervalMonthsEntry.disabled = false
            }
            intervalRadioEntry.click()
            tachSinceLastCompleteEntry.value = tach_last_completed
            dateSinceLastCompleteEntry.value = date_last_completed
            intervalHoursEntry.value = interval_hours
            intervalMonthsEntry.value = interval_months
            interval_hours
        }
        if (maintenance_type === "engine") {
            engineRadioEntry.click()
        }
    })
}