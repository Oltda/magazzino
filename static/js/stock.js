
console.log(stock_array)

console.log(document.querySelectorAll(".expiration"))

exp_column = document.querySelectorAll(".expiration")

for(let i = 0; i < exp_column.length; i++){

if(stock_array[i]['days_left'] < 10){
    exp_column[i].classList.add("red")
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
                var warehouseIdInputId = "warehouseID" +  stockID

                var stockVal = document.getElementById(stockInputId).value
                var quantityVal = document.getElementById(quantityInputId).value
                var expVal = document.getElementById(expInputId).value
                var codeVal = document.getElementById(codeInputId).value
                var warehouseIdVal = document.getElementById(warehouseIdInputId).value



                $.ajax({
                    url:'/stock-items/' + stockID,
                    type: 'PATCH',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                    'edit-product_name':stockVal,
                     'edit-quantity':quantityVal,
                     'edit-expiration_date':expVal,
                     'edit-warehouse_id':warehouseIdVal,
                     'edit-product_code':codeVal,

                    }),

                    success: function (response) {
                        seznam = response['items_list']
                        console.log(seznam);

                        new_stock_item = seznam[seznam.length -1]

                        console.log(new_stock_item['product_code'])

                        document.getElementById("stock" + stockID).innerHTML = stockVal
                        document.getElementById("quantity" + stockID).innerHTML = quantityVal
                        document.getElementById("exp-date" + stockID).innerHTML = expVal
                        document.getElementById("prod-code" + stockID).innerHTML = codeVal
                        document.getElementById("warehouse" + stockID).innerHTML = warehouseIdVal
                        document.getElementById("unit" + stockID).innerHTML = new_stock_item['unit']

                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
                e.preventDefault();
            });




            function deleteStock(){
             var stockID = $(this).attr("data-id")

            console.log(stockID)
            $(this).parent().hide()

                 $.ajax({
                     url: '/stock-items/' + stockID,
                     type: "DELETE"
                 });
            }


            $(".deleteBtn").click(deleteStock)




            seznam = []

            $("#submitBtn").click(function (e) {



                var itemName = $("#item-name").val();
                var quantity = $("#quantity").val();
                var expDate = $("#expiration_date").val();
                var prodCode = $("#product_code").val();
                var warhID = $("#warehouse_id").val();



                $.ajax({
                    url:'/stock-items',
                    type: 'POST',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                     'product_name':itemName,
                     'quantity':quantity,
                     'expiration_date':expDate,
                     'warehouse_id':warhID,
                     'product_code':prodCode

                    }),

                    success: function (response) {
                        seznam = response['items_list']


                        new_item = seznam[seznam.length -1]

                        var row = document.createElement("TR");
                        var tabulka = document.getElementById("stock-table")
                        tabulka.appendChild(row);

                        var td1 = document.createElement('td');
                        td1.innerHTML = new_item['product_name']

                        var td2 = document.createElement('td');
                        td2.innerHTML = new_item['quantity']

                        var td3 = document.createElement('td');


                        let unit = "";

                                for (let i = 0; i < product_code_list.length; i++) {

                                    if(product_code_list[i]['code'] === new_item['product_code']){
                                    unit = product_code_list[i]['unit']


                                    }
                                }
                        td3.innerHTML = unit


                        var td4 = document.createElement('td');
                        td4.innerHTML = new_item['expiration_date']



                        var td5 = document.createElement('td');
                        td5.innerHTML = new_item['product_code']

                        var td6 = document.createElement('td');
                        td6.innerHTML = new_item['warehouse_id']

                        var td6 = document.createElement('td');
                        td6.innerHTML = new_item['warehouse_id']



                        row.appendChild(td1);
                        row.appendChild(td2);
                        row.appendChild(td3);
                        row.appendChild(td4);
                        row.appendChild(td5);
                        row.appendChild(td6);




                        document.getElementById("item-name").value = ""
                        document.getElementById("quantity").value = ""

                        document.getElementById("expiration_date").value = ""
                        document.getElementById("product_code").value = ""

                        document.getElementById("warehouse_id").value = ""


                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
                e.preventDefault();
            })