$(document).ready(function(){
    function delete_product(id){
    $.ajax({
        url: "/delete",
        type: "POST",
        dataType: "json",
        data : {
            id : id
        }
    })
    }
  });