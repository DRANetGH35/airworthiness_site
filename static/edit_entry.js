const editBtns = document.querySelectorAll('#editBtn')


document.querySelectorAll('#editBtn').forEach(btn => {
    const id = btn.dataset.entryid;
    btn.addEventListener('click', () => {showEditFields(id)})
})



function showEditFields(time_entry_id){
    let id_selector = `time_entry_id_${time_entry_id}`
    let row = document.getElementById(id_selector)
    let tach_time = row.children[1].children[0]
    let tach_entry = row.children[1].children[1]
    let button_cell = row.children[3].children[0]
    let save_cell = row.children[3].children[1]

    console.log(button_cell.children)
    tach_time.classList.add('hidden')
    button_cell.classList.add('hidden')
    tach_entry.classList.remove('hidden')
    save_cell.classList.remove('hidden')
}