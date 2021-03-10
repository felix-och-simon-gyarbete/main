function delete_product(id) {

    $.ajax({
        url: "/delete",
        type: "POST",
        dataType: "json",
        data: {
            id: id
        }

    });
    location.reload()
}
let adminList = [];
function addToAdminList(id) {
    if (!adminList.includes(id)) {
        adminList.push(id);
    }
    else { adminList.pop(id) }
}
let deleteList = [];
function addToAdminList(id) {
    if (!deleteList.includes(id)) {
        deleteList.push(id);
    }
    else { deleteList.pop(id) }
}

function saveChanges(){
    for(element e : deleteList){
        
    }

}