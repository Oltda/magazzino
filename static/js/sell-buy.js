



            function checkDate(){
            exp_column = document.querySelectorAll(".expiration")

            exp_notif = document.getElementById("exp_notif")

                for(let i = 0; i < exp_column.length; i++){

                if(stock_array[i]['days_left'] < 10){
                    exp_column[i].classList.add("red")
                }

                }


            }



            function showSellBtn(element){
                var formChildren = element.parentNode.parentNode.children
                formChildren[6].classList.add("show")

            }





            seznam = []
            $(".sellBtn").click(function (e) {
                var stockID = $(this).attr("data-id")

                $(this).parent().removeClass("show")

                var quantityInputId = "quantityID" +  stockID

                var quantityVal = document.getElementById(quantityInputId).value



                $.ajax({
                    url:'/sell-buy/' + stockID,
                    type: 'PATCH',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({

                     'edit-quantity':quantityVal


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






                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
                e.preventDefault();
            });






















