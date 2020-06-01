import os
from flask import Flask, request, abort, jsonify, render_template
from flask_cors import CORS
from models import setup_db, Restaurant, Order
from auth import requires_auth, AuthError


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,DELETE')
        return response

    @app.route('/')
    def index():
        return render_template('index.html', login_url=os.environ['LOGIN_URL'],
                               github_url=os.environ['GITHUB_URL'])

    @app.route('/restaurants')
    @requires_auth('get:restaurants')
    def get_restos(payload):
        restaurants = [resto.format() for resto in Restaurant.query.all()]

        return jsonify({'success': True,
                        'restaurants': restaurants})

    @app.route('/orders')
    @requires_auth('get:orders')
    def get_orders(payload):
        orders = [order.format() for order in Order.query.all()]

        return jsonify({'success': True,
                        'orders': orders})

    @app.route('/restaurants/<int:resto_id>/orders')
    @requires_auth('get:orders')
    def get_orders_of_resto(payload, resto_id):
        orders = [order.format() for order in
                  Order.query.filter_by(restaurant_id=resto_id).all()]
        if not orders:
            abort(404)

        return jsonify({'success': True,
                        'orders': orders})

    @app.route('/restaurants', methods=['POST'])
    @requires_auth('post:restaurants')
    def post_restaurant(payload):
        try:
            data = request.get_json()

            name = data['name']
            cuisine = data['cuisine']

            new_restaurant = Restaurant(name=name, cuisine=cuisine)
            new_restaurant.insert()
        except Exception:
            abort(400)

        return jsonify({'success': True,
                        'restaurants': [new_restaurant.format()]})

    @app.route('/orders', methods=['POST'])
    @requires_auth('post:orders')
    def post_order(payload):
        try:
            data = request.get_json()

            resto_id = data['restaurant_id']
            name = data['name']
            calories = data['calories']
            total_fat = data['total_fat']
            cholesterol = data['cholesterol']
            sodium = data['sodium']
            total_carbs = data['total_carbs']
            protein = data['protein']

            new_order = Order(restaurant_id=resto_id, name=name,
                              calories=calories, total_fat=total_fat,
                              cholesterol=cholesterol, sodium=sodium,
                              total_carbs=total_carbs, protein=protein)
            new_order.insert()
        except Exception:
            abort(400)

        return jsonify({'success': True,
                        'orders': [new_order.format()]})

    @app.route('/restaurants/<int:id>', methods=['PATCH'])
    @requires_auth('patch:restaurants')
    def patch_restaurant(payload, id):
        resto = Restaurant.query.filter_by(id=id).one_or_none()
        if resto is None:
            abort(404)

        try:
            data = request.get_json()

            if 'name' in data:
                resto.name = data['name']

            if 'cuisine' in data:
                resto.cuisine = data['cuisine']

            resto.update()
        except Exception:
            abort(400)

        return jsonify({'success': True, 'restaurants': [resto.format()]})

    @app.route('/orders/<int:id>', methods=['PATCH'])
    @requires_auth('patch:orders')
    def patch_order(payload, id):
        order = Order.query.filter_by(id=id).one_or_none()
        if order is None:
            abort(404)

        try:
            data = request.get_json()
            if 'name' in data:
                order.name = data['name']
            if 'calories' in data:
                order.calories = data['calories']
            if 'total_fat' in data:
                order.total_fat = data['total_fat']
            if 'cholesterol' in data:
                order.cholesterol = data['cholesterol']
            if 'sodium' in data:
                order.sodium = data['sodium']
            if 'total_carbs' in data:
                order.total_carbs = data['total_carbs']
            if 'protein' in data:
                order.protein = data['protein']

            order.update()
        except Exception:
            abort(400)

        return jsonify({'success': True, 'orders': [order.format()]})

    @app.route('/restaurants/<int:id>', methods=['DELETE'])
    @requires_auth('delete:restaurants')
    def delete_restaurant(payload, id):
        resto = Restaurant.query.filter_by(id=id).one_or_none()
        if resto is None:
            abort(404)

        try:
            resto.delete()

        except Exception:
            abort(400)

        return jsonify({'success': True, 'delete': id})

    @app.route('/orders/<int:id>', methods=['DELETE'])
    @requires_auth('delete:orders')
    def delete_order(payload, id):
        order = Order.query.filter_by(id=id).one_or_none()
        if order is None:
            abort(404)

        try:
            order.delete()

        except Exception:
            abort(400)

        return jsonify({'success': True, 'delete': id})

    @app.route('/login-confirmation')
    def confirm_login():
        return render_template('login-confirm.html')

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': False,
                        'error': 400,
                        'message': 'bad request'
                        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({'success': False,
                        'error': 405,
                        'message': 'method not allowed'
                        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'success': False,
                        'error': 500,
                        'message': 'Internal server error'
                        }), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(AuthError)
    def authorization_error(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": AuthError.error['description']
        }), AuthError.status_code

    # Uncomment this endpoint for a quick way to add dummy data to the db
    '''
    @app.route('/populate-db')
    def populate_db():
        names = ['KFC', 'Five Guys', 'Starbucks', 'Chipotle']
        cuisines = ['Fast Food', 'Burgers', 'Cafe', 'Mexican']
        restaurants = []

        for i in range(len(names)):
            restaurants.append(Restaurant(name=names[i], cuisine=cuisines[i]))

        [resto.insert() for resto in restaurants]

        first_resto_id = restaurants[0].id
        order_names = ['Spicy Zinger', 'Cheeseburger', 'Caramel Macchiato',
                       'Burrito']
        calories = [480, 840, 240, 1000]
        fats = [19, 55, 7, 39]
        cholesterols = [110, 165, 25, 195]
        sodiums = [900, 1050, 130, 1855]
        carbs = [48, 40, 34, 104]
        proteins = [28, 47, 10, 60]
        orders = []

        for i in range(len(order_names)):
            orders.append(Order(restaurant_id=first_resto_id + i,
                                name=order_names[i], calories=calories[i],
                                total_fat=fats[i], sodium=sodiums[i],
                                cholesterol=cholesterols[i],
                                total_carbs=carbs[i], protein=proteins[i]))

        [order.insert() for order in orders]

        return jsonify(
            {
                'success': True,
                'restaurants': [resto.format() for resto in restaurants]
            })
    '''

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
