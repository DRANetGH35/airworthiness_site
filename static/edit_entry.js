
document.querySelectorAll('#editBtn').forEach(btn => {
    const id = btn.dataset.entryid;
    btn.addEventListener('click', () => {showEditFields(id)})
})

document.querySelectorAll('#cancelBtn').forEach(btn => {
    const id = btn.dataset.entryid;
    btn.addEventListener('click', () => {cancelEditField(id)})
})

document.querySelectorAll('#saveBtn').forEach(btn => {
    const id = btn.dataset.entryid;
    btn.addEventListener('click', () => {saveEditField(id)})
})

function saveEditField(id){
    let url = `/edit_time_entry/${id}`
    const editField = document.getElementById(`edit_field_${id}`)
    let data = new FormData();
    let value = editField.value
    data.append("value", value)
    fetch(url, {
        "method": "POST",
        "body": data
    })
    const tach_time_p = document.getElementById(`tach_time_${id}`)
    const hobbs_time_p = document.getElementById(`hobbs_time_${id}`)
    tach_time_p.innerHTML = value
    hobbs_time_p.innerHTML = +(value * 1.2).toFixed(2)
    cancelEditField(id)
}

function cancelEditField(id){
    let id_selector = `time_entry_id_${id}`
    let row = document.getElementById(id_selector)
    let tach_time = row.children[1].children[0]
    let tach_entry = row.children[1].children[1]
    let button_cell = row.children[3].children[0]
    let save_cell = row.children[3].children[1]

    console.log(button_cell.children)
    tach_time.classList.remove('hidden')
    button_cell.classList.remove('hidden')
    tach_entry.classList.add('hidden')
    save_cell.classList.add('hidden')
}

function showEditFields(id){
    let id_selector = `time_entry_id_${id}`
    let editField = document.getElementById(`edit_field_${id}`)
    let row = document.getElementById(id_selector)
    let tach_time = row.children[1].children[0]
    let tach_entry = row.children[1].children[1]
    let button_cell = row.children[3].children[0]
    let save_cell = row.children[3].children[1]

    editField.value = tach_time.innerHTML

    console.log(button_cell.children)
    tach_time.classList.add('hidden')
    button_cell.classList.add('hidden')
    tach_entry.classList.remove('hidden')
    save_cell.classList.remove('hidden')
}