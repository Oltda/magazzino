





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
                        var tabulka = document.getElementById("product-table")
                        tabulka.appendChild(row);

                        var td = document.createElement('td');
                        td.innerHTML = new_code['product_code']

                        var td2 = document.createElement('td');
                        td2.innerHTML = new_code['unit']

                        var td3 = document.createElement('td');
                        td3.innerHTML = new_code['description']

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