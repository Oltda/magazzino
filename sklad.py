from flask import (
    Flask,
    request,
    abort,
    jsonify,
    render_template,
    session,
    redirect,
    url_for,
    flash
    )

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from database import setup_db, StockItems, ProductCodes, User, Sales
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from forms import LoginForm, RegistrationForm
import os
from expiration_dates import ExpirationCalculator
from generate_pdf import PdfSheet
from datetime import datetime

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)
    login = LoginManager(app)

    app.secret_key = "ytdytftyfjytfjytfjytf"


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response



    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('show_stock_items'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Wrong username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('show_stock_items'))
        return render_template('login.html', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        #return redirect(url_for('login'))
        return redirect('http://localhost:5000/login')


    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            user.insert()
            return redirect(url_for('login'))
        return render_template('register.html', form=form)



    @app.route('/product-code', methods=['GET'])
    @login_required
    def show_product_codes():


        product_codes_collection = ProductCodes.query.all()
        product_code_list = []

        for i in product_codes_collection:
            product_code_list.append({"id":i.id, "code": i.product_code, "unit": i.unit, "description": i.description})

        return render_template('product-code.html', product_code_list=product_code_list)

    @app.route('/product-code', methods=['POST'])
    @login_required
    def post_product_code():
        try:
            body = request.get_json()

            new_code = body.get('product_code', None)
            new_description = body.get('description', None)
            new_unit = body.get('unit', None)
            user_id = current_user.id

            code = ProductCodes(
                product_code=new_code,
                description=new_description,
                unit=new_unit,
                user_id=user_id
            )

            code.insert()

            product_codes_collection = ProductCodes.query.all()
            product_code_list = []

            for i in product_codes_collection:
                product_code_list.append({"id":i.id, "product_code": i.product_code, "unit": i.unit, "description": i.description})


            Message = {"product_code_list": product_code_list}

            return Message

        except:
            abort(422)





    @app.route('/product-code/<int:code_id>', methods=['PATCH'])
    @login_required
    def update_code(code_id):

        body = request.get_json()

        try:

            edit_code = body.get('edit-product_code', None)
            edit_description = body.get('edit-description', None)
            edit_unit = body.get('edit-unit', None)
            user_id = current_user.id

            code_patch = ProductCodes.query.filter(ProductCodes.id == code_id).one_or_none()

            code_patch.product_code = edit_code
            code_patch.description = edit_description
            code_patch.unit = edit_unit

            code_patch.update()


            product_codes_collection = ProductCodes.query.all()
            product_code_list = []

            for i in product_codes_collection:
                product_code_list.append({"id": i.id, "product_code": i.product_code, "unit": i.unit, "description": i.description})


            Message = {"product_code_list": product_code_list}

            return Message

        except:
            abort(422)






    @app.route('/product-code/<int:code_id>', methods=['DELETE'])
    @login_required
    def delete_product_code(code_id):
        try:
            code_to_delete = ProductCodes.query.filter(ProductCodes.id == code_id).one_or_none()

            if code_to_delete is None:
                abort(404)

            stock_to_delete = StockItems.query.filter(StockItems.product_code == code_to_delete.product_code).all()
            for i in stock_to_delete:
                i.delete()

            code_to_delete.delete()

            return jsonify({
                'success': True,
                'deleted_code': code_id
            })
        except:
            abort(422)




    @app.route('/sell-buy', methods=['GET'])
    @login_required
    def view_sell_buy_stock():


        page = request.args.get('page', 1, type=int)
        stock_paginate = StockItems.query.filter_by(user_id=current_user.id).order_by(StockItems.id.asc()).paginate(page=page, per_page=10)


        items_list = []

        for i in stock_paginate.items:
            items_list.append({"id": i.id,
                               "product_name": i.product_name,
                               "quantity": i.quantity,
                               "expiration_date": i.expiration_date.strftime('%d-%m-%Y'),

                               "product_code": i.product_code})


        for i in items_list:
            date = i['expiration_date']
            i['days_left'] = ExpirationCalculator(date).show_days_left()


        product_codes_collection = ProductCodes.query.all()
        product_code_list = []

        for i in product_codes_collection:
            product_code_list.append({"code": i.product_code, "unit":i.unit, "description":i.description})


        return render_template('sell-buy.html', stock_paginate=stock_paginate, stock_array=items_list, product_code_list=product_code_list)





    @app.route('/sell-buy/<int:stock_id>', methods=['PATCH'])
    @login_required
    def sell_buy_stock(stock_id):

        body = request.get_json()
        try:
            edit_quantity = int(body.get('edit-quantity'))


            stock_patch = StockItems.query.filter(StockItems.id == stock_id).one_or_none()

            original_quantity = stock_patch.quantity
            new_quantity = edit_quantity

            stock_patch.quantity = edit_quantity

            stock_patch.update()

            # SALES--------------------------------------------------------------------------
            sale_patch = Sales.query.filter(Sales.product_id == stock_id).all()
            #current_date = datetime.now().date()
            current_date = datetime.strptime('2021-07-29', '%Y-%m-%d').date()
            sold = original_quantity - new_quantity
            for i in sale_patch:
                if i.sale_date is None or i.sale_date == current_date:
                    i.sale_date = current_date

                    i.sold_quantity = i.sold_quantity + sold
                    i.update()
                else:
                    sale = Sales(sold_product=i.sold_product, sale_date=current_date,
                                 sold_quantity=sold, product_id=stock_id,
                                 user_id=current_user.id)
                    sale.insert()

            # --------------------------------------------------------------------------

            product_codes_collection = ProductCodes.query.all()
            product_code_list = []

            for i in product_codes_collection:
                product_code_list.append({"code": i.product_code, "unit": i.unit, "description": i.description})



            stock_items_collection = StockItems.query.all()
            items_list = []
            for i in stock_items_collection:

                for x in product_code_list:
                    if x['code'] == i.product_code:
                        unit = x['unit']


                items_list.append({
                    "id": i.id,
                    "product_name": i.product_name,
                    "quantity": i.quantity,
                    "expiration_date": i.expiration_date.strftime('%d-%m-%Y'),

                    "product_code": i.product_code,
                    "unit": unit
                })

            for i in items_list:
                date = i['expiration_date']
                i['days_left'] = ExpirationCalculator(date).show_days_left()

            sorted_list = sorted(items_list, key=lambda i: i['id'])

            Message = {"items_list": sorted_list}

            return Message

        except:
            abort(422)











    @app.route('/stock-pdf', methods=['GET'])
    @login_required
    def download_pdf():
        user_id = current_user.id
        selection = StockItems
        pdf_inst = PdfSheet(user_id)

        return pdf_inst.to_pdf()





    @app.route('/stock-items', methods=['GET'])
    @login_required
    def show_stock_items():


        page = request.args.get('page', 1, type=int)
        stock_paginate = StockItems.query.filter_by(user_id=current_user.id).order_by(StockItems.id.asc()).paginate(page=page, per_page=10)


        items_list = []

        for i in stock_paginate.items:
            items_list.append({"id": i.id,
                               "product_name": i.product_name,
                               "quantity": i.quantity,
                               "expiration_date": i.expiration_date.strftime('%d-%m-%Y'),

                               "product_code": i.product_code})


        for i in items_list:
            date = i['expiration_date']
            i['days_left'] = ExpirationCalculator(date).show_days_left()


        product_codes_collection = ProductCodes.query.all()
        product_code_list = []

        for i in product_codes_collection:
            product_code_list.append({"code": i.product_code, "unit":i.unit, "description":i.description})


        return render_template('stock.html', stock_paginate=stock_paginate, stock_array=items_list, product_code_list=product_code_list)





    @app.route('/stock-items', methods=['POST'])
    @login_required
    def post_item():
        try:
            body = request.get_json()

            new_product_name = body.get('product_name', None)
            new_quantity = int(body.get('quantity', None))
            new_expiration_date = body.get('expiration_date', None)
            product_code = body.get('product_code', None)

            user_id = current_user.id





            item = StockItems(product_name=new_product_name, quantity=new_quantity,
                              expiration_date=new_expiration_date,
                              product_code=product_code, user_id=user_id)

            item.insert()



            stock_items_collection = StockItems.query.all()
            items_list = []
            for i in stock_items_collection:
                items_list.append({
                            "id": i.id,
                            "product_name": i.product_name,
                            "quantity": i.quantity,
                            "expiration_date": i.expiration_date.strftime('%d-%m-%Y'),

                            "product_code": i.product_code,
                            "user_id": i.user_id
                            })



            # SALES ------------------------------------------------------------
            last_item = items_list[len(items_list) -1]

            sale = Sales(sold_product=last_item['product_name'], sale_date=None,
                         sold_quantity=0, product_id=last_item['id'],
                         user_id=current_user.id,
                         )
            sale.insert()

            # ------------------------------------------------------------


            product_codes_collection = ProductCodes.query.all()
            product_code_list = []
            for i in product_codes_collection:
                product_code_list.append(i.product_code)

            Message = {"items_list": items_list}

            return Message

        except:
            abort(422)



    @app.route('/stock-items/<int:stock_id>', methods=['PATCH'])
    @login_required
    def edit_stock(stock_id):

        body = request.get_json()

        try:
            edit_product_name = body.get('edit-product_name')
            edit_quantity = int(body.get('edit-quantity'))
            edit_expiration_date = body.get('edit-expiration_date')

            edit_product_code = body.get('edit-product_code')

            stock_patch = StockItems.query.filter(StockItems.id == stock_id).one_or_none()


            stock_patch.product_name = edit_product_name
            stock_patch.quantity = edit_quantity
            stock_patch.expiration_date = edit_expiration_date

            stock_patch.product_code = edit_product_code

            stock_patch.update()




            product_codes_collection = ProductCodes.query.all()
            product_code_list = []

            for i in product_codes_collection:
                product_code_list.append({"code": i.product_code, "unit": i.unit, "description": i.description})



            stock_items_collection = StockItems.query.all()
            items_list = []
            for i in stock_items_collection:

                for x in product_code_list:
                    if x['code'] == i.product_code:
                        unit = x['unit']


                items_list.append({
                    "id": i.id,
                    "product_name": i.product_name,
                    "quantity": i.quantity,
                    "expiration_date": i.expiration_date.strftime('%d-%m-%Y'),

                    "product_code": i.product_code,
                    "unit": unit
                })

            for i in items_list:
                date = i['expiration_date']
                i['days_left'] = ExpirationCalculator(date).show_days_left()

            sorted_list = sorted(items_list, key=lambda i: i['id'])

            Message = {"items_list": sorted_list}

            return Message

        except:
            abort(422)

    @app.route('/stock-items/<int:stock_id>', methods=['DELETE'])
    @login_required
    def delete_warehouse_stock(stock_id):
        try:
            stock_to_delete = StockItems.query.filter(StockItems.id == stock_id).one_or_none()


            if stock_to_delete is None:
                abort(404)

            stock_to_delete.delete()

            return jsonify({
                'success': True,
                'deleted_stock': stock_id
            })
        except:
            abort(422)



    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    return app


app = create_app()

if __name__ == '__main__':
    app.run()