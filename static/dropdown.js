const statusDropdowns = document.querySelectorAll('#maintenance_item_dropdown')

statusDropdowns.forEach(dropdownDiv => {
    dropdown = dropdownDiv.children[0]
    const id = dropdown.dataset.id
    url = `/fetch_maintenance_item/${id}`

    //set select to saved value
    fetch(url).then(response => response.json()).then(data => {
        task_status = data['status']
        dropdown.value = task_status
    })

    //event listener for change event
    dropdown.addEventListener('change', (event) => {
        const selected_value = event.target.value
        changeEvent(id, selected_value)
    })
})
// change value in backend when select changed
function changeEvent(id, selected_value){
    url = `/change_maintenance_status`;
    let data= new FormData;
    data.append('id', id)
    data.append('selected_value', selected_value)
    fetch(url, {
        "method": "POST",
        "body": data
    })
    window.location.reload()
}
