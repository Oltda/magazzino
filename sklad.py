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

from database import setup_db, Warehouse, StockItems, ProductCodes, User
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from forms import LoginForm, RegistrationForm

import os


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
            return redirect(url_for('show_warehouses'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Wrong username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('show_warehouses'))
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






    @app.route('/warehouse', methods=['GET'])
    @cross_origin()
    @login_required
    def show_warehouses():
        warehouse_collection = Warehouse.query.all()
        warehouse_list = []

        for i in warehouse_collection:
            warehouse_list.append({
                "id": i.id,
                "name": i.name,
                "address": i.address
            })

        stock = StockItems.query.all()

        stock_array = []
        for i in stock:
            code = ProductCodes.query.filter_by(product_code=i.product_code).first()
            stock_item = {
                'id': i.id,
                'name': i.product_name,
                'quantity': i.quantity,
                'expiration_date': i.expiration_date.strftime('%d-%b-%Y'),
                'warehouse_id': i.warehouse_id,
                'product_code': i.product_code,
                'unit': code.unit
            }
            stock_array.append(stock_item)




        # if request.method == 'POST':
        #     new_warehouse_name = request.form['warehouse-name']
        #     new_warehouse_address = request.form['address']
        #
        #     user_id = current_user.id
        #
        #     warehouse = Warehouse(name=new_warehouse_name,
        #                           address=new_warehouse_address,
        #                           user_id=user_id)
        #
        #     warehouse.insert()
        #
        #     return render_template('home.html', stock_array=stock_array, warehouse_list=warehouse_list)


        return render_template('home.html', stock_array=stock_array, warehouse_list=warehouse_list)




    @app.route('/warehouse', methods=['POST'])
    @cross_origin()
    @login_required
    def post_warehouse():

        body = request.get_json()

        new_warehouse_name = body.get('name')
        new_warehouse_address = body.get('address')
        user_id = current_user.id



        warehouse = Warehouse(name=new_warehouse_name,
                              address=new_warehouse_address,
                              user_id=user_id)

        warehouse.insert()


        warehouse_collection = Warehouse.query.all()
        warehouse_list = []

        for i in warehouse_collection:
            warehouse_list.append({
                "id": i.id,
                "name": i.name,
                "address": i.address
            })

        Message = {"warehouse_list": warehouse_list}

        return Message

    @app.route('/warehouse/<int:warehouse_id>', methods=['PATCH'])
    @login_required
    def edit_warehouse(warehouse_id):

        body = request.get_json()

        try:
            edited_name = body.get('edit-name')
            edited_address = body.get('edit-address')
            user_id = current_user.id

            warehouse_patch = Warehouse.query.filter(Warehouse.id == warehouse_id).one_or_none()

            warehouse_patch.name = edited_name
            warehouse_patch.address = edited_address

            warehouse_patch.update()

            warehouse_collection = Warehouse.query.all()
            warehouse_list = []

            for i in warehouse_collection:
                warehouse_list.append({
                    "id": i.id,
                    "name": i.name,
                    "address": i.address
                })

            # return jsonify({
            #     'success': True,
            #     'warehouse_list': warehouse_list,
            #     'edited_warehouse_id': warehouse_patch.id
            # })

            Message = {"warehouse_list": warehouse_list}

            return Message

        except:
            abort(422)

    @app.route('/warehouse/<int:warehouse_id>', methods=['DELETE'])
    @login_required
    def delete_warehouse(warehouse_id):
        try:
            warehouse_to_delete = Warehouse.query.filter(Warehouse.id == warehouse_id).one_or_none()

            if warehouse_to_delete is None:
                abort(404)


            stock_to_delete = StockItems.query.filter(StockItems.warehouse_id == warehouse_id).all()

            for i in stock_to_delete:
                i.delete()

            warehouse_to_delete.delete()

            return jsonify({
                'success': True,
                'deleted_warehouse': warehouse_id
            })
        except:
            abort(422)

    @app.route('/product-code', methods=['GET'])
    @login_required
    def show_product_codes():

        codes_collection = ProductCodes.query.all()
        codes_list = []

        for i in codes_collection:
            codes_list.append(i.product_code)


        return jsonify({
            'success': True,
            'codes_list': codes_list
        })

    @app.route('/product-code', methods=['POST'])
    @login_required
    def post_product_code():
        try:
            body = request.get_json()

            new_code = body.get('product_code', None)
            new_description = body.get('description', None)
            new_unit = body.get('unit', None)

            code = ProductCodes(
                product_code=new_code,
                description=new_description,
                unit=new_unit
            )

            code.insert()

            codes_collection = ProductCodes.query.all()
            codes_list = []

            for i in codes_collection:
                codes_list.append(i.product_code)

            return jsonify({
                'success': True,
                'codes_list': codes_list,
                'new_code_id': code.id
            })

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

    @app.route('/stock-items', methods=['GET'])
    @login_required
    def show_stock_items():

        stock_items_collection = StockItems.query.all()
        items_list = []

        for i in stock_items_collection:
            items_list.append({"id": i.id,
                               "product_name": i.product_name,
                               "quantity": i.quantity,
                               "expiration_date": i.expiration_date.strftime('%d-%b-%Y'),
                               "warehouse_id": i.warehouse_id,
                               "product_code": i.product_code})


        product_codes_collection = ProductCodes.query.all()


        product_code_list = []

        for i in product_codes_collection:
            product_code_list.append({"code": i.product_code, "unit":i.unit, "description":i.description})


        return render_template('stock.html', stock_array=items_list, product_code_list=product_code_list)



    @app.route('/stock-items/<int:warehouse_id>', methods=['GET'])
    @login_required
    def show_warehouse_stock(warehouse_id):

        warehouse = Warehouse.query.get(warehouse_id)

        stock = StockItems.query.filter_by(warehouse_id=warehouse_id).all()
        stock_array = []

        for i in stock:

            code = ProductCodes.query.filter_by(product_code=i.product_code).first()
            stock_item = {
                          'id': i.id,
                          'product_name': i.product_name,
                          'quantity': i.quantity,
                          'expiration_date': i.expiration_date.strftime('%d-%b-%Y'),
                          'warehouse_id': i.warehouse_id,
                          'product_code': i.product_code,
                          'unit': code.unit
                          }
            stock_array.append(stock_item)


        product_codes_collection = ProductCodes.query.all()
        product_code_list = []

        for i in product_codes_collection:
            product_code_list.append({"code": i.product_code, "unit":i.unit, "description":i.description})

        warehouse_collection = Warehouse.query.all()
        warehouse_list = []

        for i in warehouse_collection:
            warehouse_list.append({
                "id": i.id,
                "name": i.name,
                "address": i.address})

        # return jsonify({
        #     'success': True,
        #     'stock_array': stock_array,
        #     'warehouse_list': warehouse_list,
        # })
        return render_template('stock.html', stock_array=stock_array, product_code_list=product_code_list)

    @app.route('/stock-items', methods=['POST'])
    @login_required
    def post_item():
        try:
            body = request.get_json()

            new_product_name = body.get('product_name', None)
            new_quantity = int(body.get('quantity', None))
            new_expiration_date = body.get('expiration_date', None)
            warehouse_id = int(body.get('warehouse_id', None))
            product_code = body.get('product_code', None)

            user_id = current_user.id

            item = StockItems(product_name=new_product_name, quantity=new_quantity,
                              expiration_date=new_expiration_date, warehouse_id=warehouse_id,
                              product_code=product_code, user_id=user_id)

            item.insert()

            stock_items_collection = StockItems.query.all()
            items_list = []
            for i in stock_items_collection:
                items_list.append({
                            "id": i.id,
                            "product_name": i.product_name,
                            "quantity": i.quantity,
                            "expiration_date": i.expiration_date.strftime('%d-%b-%Y'),
                            "warehouse_id": i.warehouse_id,
                            "product_code": i.product_code,
                            "user_id": i.user_id
                            })

            product_codes_collection = ProductCodes.query.all()
            product_code_list = []
            for i in product_codes_collection:
                product_code_list.append(i.product_code)

            Message = {"items_list": items_list}

            return Message

            # return jsonify({
            #     'success': True,
            #     'items_list': items_list,
            #     'codes': product_code_list,
            #     'new_stock_id': item.id
            # })
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
            edit_warehouse_id = int(body.get('edit-warehouse_id'))
            edit_product_code = body.get('edit-product_code')

            stock_patch = StockItems.query.filter(StockItems.id == stock_id).one_or_none()


            stock_patch.product_name = edit_product_name
            stock_patch.quantity = edit_quantity
            stock_patch.expiration_date = edit_expiration_date
            stock_patch.warehouse_id = edit_warehouse_id
            stock_patch.product_code = edit_product_code

            stock_patch.update()

            warehouse_collection = Warehouse.query.all()
            warehouse_list = []
            for i in warehouse_collection:
                warehouse_list.append({
                    "id": i.id,
                    "name": i.name,
                    "address": i.address
                })

            stock_items_collection = StockItems.query.all()
            items_list = []
            for i in stock_items_collection:
                items_list.append({
                    "id": i.id,
                    "product_name": i.product_name,
                    "quantity": i.quantity,
                    "expiration_date": i.expiration_date.strftime('%d-%b-%Y'),
                    "warehouse_id": i.warehouse_id,
                    "product_code": i.product_code
                })

            product_codes_collection = ProductCodes.query.all()
            product_code_list = []
            for i in product_codes_collection:
                product_code_list.append(i.product_code)

            # return jsonify({
            #     'success': True,
            #     'warehouse_list': warehouse_list,
            #     'items_list': items_list,
            #     'codes': product_code_list
            # })

            # dodelat warehouselist a product code list
            Message = {"items_list": items_list}

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