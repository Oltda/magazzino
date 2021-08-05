
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


                $(".deleteBtn").click(function (e) {
                codeID = $(this).attr("data-id")

                $(this).parent().parent().hide()

                 $.ajax({
                 url: '/product-code/' + codeID,
                 type: "DELETE"
                    });
                e.preventDefault();
            });






            seznam = []
            $(".editButton").click(function (e) {


                var editCodeID = $(this).attr("data-id")



                var codeInputId = "codeID" +  editCodeID
                var unitInputId = "unitID" +  editCodeID
                var descriptionInputId = "descriptionID" +  editCodeID

                var codeVal = document.getElementById(codeInputId).value
                var unitVal = document.getElementById(unitInputId).value
                var descriptionVal = document.getElementById(descriptionInputId).value



                $.ajax({
                    url:'/product-code/' + editCodeID,
                    type: 'PATCH',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                    'edit-product_code':codeVal,
                     'edit-description':descriptionVal,
                     'edit-unit':unitVal,
                    }),

                    success: function (response) {
                        seznam = response['product_code_list']
                        console.log(seznam);




                        document.getElementById("code" + editCodeID).innerHTML = codeVal
                        document.getElementById("unit" + editCodeID).innerHTML = unitVal
                        document.getElementById("description" + editCodeID).innerHTML = descriptionVal
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
                e.preventDefault();
            });







            seznam = []
            $("#submitBtn").click(function (e) {

                var prodCode = $("#productCode").val();
                var unit = $("#unit").val();
                var description = $("#description").val();

                $.ajax({
                    url:'/product-code',
                    type: 'POST',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                    'product_code':prodCode,
                     'unit':unit,
                     'description': description
                    }),

                    success: function (response) {
                        seznam = response['product_code_list']
                        console.log(seznam);

                        new_code = seznam[seznam.length -1]

                        var row = document.createElement("TR");
                        var tabulka = document.getElementById("code-table")
                        tabulka.appendChild(row);

                        var td = document.createElement('td');
                        td.innerHTML = new_code['product_code']
                        td.classList.add("column")

                        var td2 = document.createElement('td');
                        td2.innerHTML = new_code['unit']
                        td2.classList.add("column")

                        var td3 = document.createElement('td');
                        td3.innerHTML = new_code['description']
                        td3.classList.add("column")

                        row.appendChild(td);
                        row.appendChild(td2);
                        row.appendChild(td3);

//                        document.getElementById("warehouse-name").value = ""
//                        document.getElementById("address").value = ""

                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
                e.preventDefault();
            });




