



            function showEdit(element){
            var formChildren =  element.parentNode.children

            for(let i = 0; i < formChildren.length; i++){

                if(formChildren[i].hasChildNodes() == true){

                    for(let y = 0; y < formChildren[i].children.length; y++){
                    formChildren[i].children[y].classList.toggle("editing")
                    }

                }

            }




            }


            seznam = []
            $(".editButton").click(function (e) {
                var editWarehouseID = $(this).attr("data-id")


                var addressInputId = "address" +  editWarehouseID
                var warehouseInputId = "warehouse" +  editWarehouseID

                var warehouseVal = document.getElementById(warehouseInputId).value
                var addressVal = document.getElementById(addressInputId).value



                $.ajax({
                    url:'/warehouse/' + editWarehouseID,
                    type: 'PATCH',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                    'edit-name':warehouseVal,
                     'edit-address':addressVal
                    }),

                    success: function (response) {
                        seznam = response['warehouse_list']
                        console.log(seznam);

                        new_wareh = seznam[seznam.length -1]
                        console.log(editWarehouseID)

                        document.getElementById("warh" + editWarehouseID).innerHTML = warehouseVal
                        document.getElementById("addr" + editWarehouseID).innerHTML = addressVal

                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
                e.preventDefault();
            });










            $(".deleteBtn").click(function (e) {
                warehouseID = $(this).attr("data-id")

                $(this).parent().parent().hide()

                 $.ajax({
                 url: '/warehouse/' + warehouseID,
                 type: "DELETE"
                    });
                e.preventDefault();
            });






//            function deleteWarehouse(element) {
//
//            warehouseID = element.getAttribute('data-id')
//            element.parentElement.parentElement.style.display = "None";
//
//                $.ajax({
//                 url: '/warehouse/' + warehouseID,
//                 type: "DELETE"
//                    });
//
//            }



            seznam = []
            $("#submitBtn").click(function (e) {

                var warhName = $("#warehouse-name").val();
                var address = $("#address").val();
                $.ajax({
                    url:'/warehouse',
                    type: 'POST',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                    'name':warhName,
                     'address':address
                    }),

                    success: function (response) {
                        seznam = response['warehouse_list']
                        console.log(seznam);

                        new_wareh = seznam[seznam.length -1]

                        var row = document.createElement("TR");
                        var tabulka = document.getElementById("warehouse-table")
                        tabulka.appendChild(row);
                        var td = document.createElement('td');
                        td.innerHTML = new_wareh['name']
                        var td2 = document.createElement('td');
                        td2.innerHTML = new_wareh['address']
                        row.appendChild(td);
                        row.appendChild(td2);


                        document.getElementById("warehouse-name").value = ""
                        document.getElementById("address").value = ""

                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
                e.preventDefault();
            });




