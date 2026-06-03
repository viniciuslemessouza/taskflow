const listContainer = document.getElementById('notebooks-container');

function editing_mode(){
    listContainer.classList.add('editing')
    listContainer.classList.remove('not-editing')
}

function view_mode(){
    listContainer.classList.remove('editing')
    listContainer.classList.add('not-editing')
}