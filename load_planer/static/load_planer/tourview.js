document.addEventListener("DOMContentLoaded", function() {
    // let's make the page display Tours for today when loaded
    const todaydate = new Date().toISOString().split('T')[0];
    getTourList(todaydate);
    crdateInpandButton();
});

/** Creates date inputfield and button with even listener
 * when date is selected, fetches data from db, generates a table of fetched 
 * tours and display each of them in onw row, with a link to tour page
 */
function crdateInpandButton() {
    const sideBar = document.getElementById('view_tours_input_field');
    const viewDate = document.createElement('input');
    viewDate.type = 'date';
    viewDate.id = 'view_date_input';
    viewDate.classList = 'form-control';
    
    sideBar.appendChild(viewDate);
    //creating label for input
    const dateLabel = document.createElement('label');
    dateLabel.for = 'view_date_input';
    dateLabel.innerHTML = 'Date:';
    dateLabel.classList = "form-label";
    sideBar.appendChild(dateLabel);

    //creating button
    const buttonField = document.getElementById('view_tours_button_field');
    const showToursButton = document.createElement('button');
    showToursButton.classList = 'btn btn-success form-control';
    showToursButton.type = 'submit';
    showToursButton.textContent = "Find Tours";
    buttonField.appendChild(showToursButton);
    showToursButton.addEventListener('click', function(){
        //cleaning up all data in tour_display_list if any
        const tourDisp = document.getElementById('tour_display_list');
        tourDisp.replaceChildren();
        //get value from viewDate input
        if (viewDate.value != "") {
            getTourList(viewDate.value);
        }
        else {
            viewDate.focus();
        }
    })
}

/** get a tour list for a selected date and adds it to the table */
function getTourList(date){
    const tourList = document.getElementById('tour_display_list');

    const headderL = document.createElement('h4');
    headderL.innerHTML = `Tour list for: ${date}`
    tourList.appendChild(headderL);

    // make table
    const tableL = document.createElement('table');
    tableL.id = 'tour_table'
    tableL.classList = "table table-hover";
    tourList.appendChild(tableL);
    // adding table head
    const tlHead = document.createElement('thead');
    tableL.appendChild(tlHead);
    const trHead = document.createElement('tr');
    tlHead.appendChild(trHead);
    const trHeadList = ['Tour id', 'Delivery id', 'Driver id', 'Truck id', 'Destinations'];

    trHeadList.forEach( item => {
        const thItem = document.createElement('th');
        thItem.innerHTML = item;
        trHead.appendChild(thItem);
    }) 
     // adding table body
    const tBody = document.createElement('tbody');
    tableL.appendChild(tBody);

    // getting data
    fetch(`/get_tour_list/${date}`)
    .then(response => response.json())
    .then(data => {
        data.forEach(element => {
            const rowL = document.createElement('tr');
            tBody.appendChild(rowL);
            Object.entries(element).forEach(entry => {
                const [key, value] = entry
                const rowData = document.createElement('td');
                rowData.innerHTML = value;
                rowData.classList = 'table-control';
                rowL.appendChild(rowData);
                if (key == "tour_id"){
                    rowData.innerHTML = "";
                    const aTag = document.createElement('a');
                    aTag.href = `/tour/${value}`;
                    aTag.innerHTML = value;
                    aTag.target = "_blank";
                    rowData.appendChild(aTag);
                }
            });
        })
    })
}


