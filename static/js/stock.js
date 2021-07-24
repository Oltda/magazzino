



function checkDate(){
exp_column = document.querySelectorAll(".expiration")
    console.log("checked")

    for(let i = 0; i < exp_column.length; i++){

    if(stock_array[i]['days_left'] < 10){
        exp_column[i].classList.add("red")
    }

    }
}


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
                var stockID = $(this).attr("data-id")


                var stockInputId = "stockID" +  stockID
                var quantityInputId = "quantityID" +  stockID
                var expInputId = "exp-dateID" +  stockID
                var codeInputId = "prod-codeID" +  stockID

                var stockVal = document.getElementById(stockInputId).value
                var quantityVal = document.getElementById(quantityInputId).value
                var expVal = document.getElementById(expInputId).value
                var codeVal = document.getElementById(codeInputId).value



                $.ajax({
                    url:'/stock-items/' + stockID,
                    type: 'PATCH',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                    'edit-product_name':stockVal,
                     'edit-quantity':quantityVal,
                     'edit-expiration_date':expVal,

                     'edit-product_code':codeVal,

                    }),

                    success: function (response) {
                        seznam = response['items_list']






                                          exp_column = document.querySelectorAll(".expiration")

                                          for(let i = 0; i < exp_column.length; i++){

                                                if(seznam[i]['days_left'] < 10){
                                                    exp_column[i].classList.add("red")
                                                }else{
                                                exp_column[i].classList.remove("red")
                                                }

                                          }




                        new_stock_item = seznam[seznam.length -1]

                        console.log(new_stock_item['product_code'])

                        document.getElementById("stock" + stockID).innerHTML = stockVal
                        document.getElementById("quantity" + stockID).innerHTML = quantityVal
                        document.getElementById("exp-date" + stockID).innerHTML = expVal
                        document.getElementById("prod-code" + stockID).innerHTML = codeVal
                        document.getElementById("unit" + stockID).innerHTML = new_stock_item['unit']

                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
                e.preventDefault();
            });




                $(".deleteBtn").click(function (e) {
                var stockID = $(this).attr("data-id")

                $(this).parent().parent().hide()

                 $.ajax({
                 url: '/stock-items/' + stockID,
                 type: "DELETE"
                    });
                e.preventDefault();
            });



            seznam = []

            $("#submitBtn").click(function (e) {

                var itemName = $("#item-name").val();
                var quantity = $("#quantity").val();
                var expDate = $("#expiration_date").val();
                var prodCode = $("#product_code").val();


                $.ajax({
                    url:'/stock-items',
                    type: 'POST',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                     'product_name':itemName,
                     'quantity':quantity,
                     'expiration_date':expDate,

                     'product_code':prodCode

                    }),

                    success: function (response) {
                        seznam = response['items_list']


                        new_item = seznam[seznam.length -1]

                        var row = document.createElement("TR");
                        row.classList.add("row")
                        var tabulka = document.getElementById("stock-table")
                        tabulka.appendChild(row);

                        var td1 = document.createElement('td');
                        td1.innerHTML = new_item['product_name']
                        td1.classList.add("column")

                        var td2 = document.createElement('td');
                        td2.innerHTML = new_item['quantity']
                        td2.classList.add("column")

                        var td3 = document.createElement('td');
                        td3.classList.add("column")

                        let unit = "";

                                for (let i = 0; i < product_code_list.length; i++) {

                                    if(product_code_list[i]['code'] === new_item['product_code']){
                                    unit = product_code_list[i]['unit']


                                    }
                                }
                        td3.innerHTML = unit


                        var td4 = document.createElement('td');
                        td4.innerHTML = new_item['expiration_date']
                        td4.classList.add("column")



                        var td5 = document.createElement('td');
                        td5.innerHTML = new_item['product_code']
                        td5.classList.add("column")





                        row.appendChild(td1);
                        row.appendChild(td2);
                        row.appendChild(td3);
                        row.appendChild(td4);
                        row.appendChild(td5);





                        document.getElementById("item-name").value = ""
                        document.getElementById("quantity").value = ""

                        document.getElementById("expiration_date").value = ""
                        document.getElementById("product_code").value = ""




                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
                e.preventDefault();
            })









