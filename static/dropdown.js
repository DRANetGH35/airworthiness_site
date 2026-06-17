const statusDropdowns = document.querySelectorAll('#maintenance_item_dropdown')

statusDropdowns.forEach(dropdown => {
    const id = dropdown.dataset.id
    url = `/fetch_maintenance_item/${id}`
    saved_value = fetch(url)
    console.log(saved_value)
    dropdown.value = saved_value

    dropdown.addEventListener('change', (event) => {
        const selected_value = event.target.value
        changeEvent(id, selected_value)
    })
})

function changeEvent(id, selected_value){
    url = `/change_maintenance_status`;
    let data= new FormData;
    data.append('id', id)
    data.append('selected_value', selected_value)
    fetch(url, {
        "method": "POST",
        "body": data
    })
    if (selected_value === "delete"){
        window.location.reload
    }
}
