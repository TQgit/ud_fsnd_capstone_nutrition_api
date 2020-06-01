import unittest
import os
import json
import random
import string
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_test_db, Restaurant, Order


class NutritionTest(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.db = SQLAlchemy()
        self.database_path = os.environ['TEST_DATABASE_URL']
        setup_test_db(self.app, self.database_path)

        self.headers = {
            'Authorization': f'bearer {os.environ["DEMO_JWT_MODERATOR"]}'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        restaurant_one = Restaurant.query.filter_by(id=1).one_or_none()
        if restaurant_one is None:
            first_resto = Restaurant(name="THE FIRST RESTO", cuisine="TEST")
            first_resto.insert()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_qet_restaurants(self):
        res = self.client().get('/restaurants', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['restaurants'])

    def test_qet_orders(self):
        res = self.client().get('/orders', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['orders'])

    def test_qet_orders_of_resto(self):
        res = self.client().get('/restaurants/1/orders', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['orders'])

    def test_delete_restaurant(self):
        new_r = Restaurant(name='THE RESTO', cuisine='THE CUISINE')
        new_r.insert()
        r_id = Restaurant.query.filter_by(name='THE RESTO').first().id

        res = self.client().delete(f'/restaurants/{r_id}',
                                   headers=self.headers)
        data = json.loads(res.data)

        restaurant = Restaurant.query.filter_by(id=r_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(restaurant, None)
        self.assertEqual(data['delete'], r_id)
        self.assertTrue(data['success'])

    def test_delete_order(self):
        new_o = Order(restaurant_id=1, name='TEST_ORDER', calories=1, sodium=1,
                      total_carbs=1, total_fat=1, cholesterol=1, protein=1)
        new_o.insert()
        o_id = Order.query.filter_by(name='TEST_ORDER').first().id

        res = self.client().delete(f'/orders/{o_id}', headers=self.headers)
        data = json.loads(res.data)

        order = Order.query.filter_by(id=o_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(order, None)
        self.assertEqual(data['delete'], o_id)
        self.assertTrue(data['success'])

    def test_add_restaurant(self):
        letters = string.ascii_letters
        random_name = ''.join(random.choice(letters) for i in range(12))

        new_r = Restaurant(name=random_name, cuisine="POST_TEST_CUISINE")

        res = self.client().post(f'/restaurants', json=new_r.format(),
                                 headers=self.headers)
        data = json.loads(res.data)

        restaurant = Restaurant.query.filter_by(name=random_name).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['restaurants'][0]['name'], restaurant.name)
        self.assertTrue(restaurant.id)
        self.assertTrue(data['success'])

    def test_add_order(self):
        letters = string.ascii_letters
        random_name = ''.join(random.choice(letters) for i in range(12))

        new_o = Order(restaurant_id=1, name='POST_TEST_' + random_name,
                      calories=1, sodium=1, total_carbs=1, total_fat=1,
                      cholesterol=1, protein=1)

        res = self.client().post(f'/orders', json=new_o.format(),
                                 headers=self.headers)
        data = json.loads(res.data)

        order = Order.query.filter_by(
            name='POST_TEST_' + random_name).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['orders'][0]['name'], order.name)
        self.assertTrue(order.id)
        self.assertTrue(data['success'])

    def test_patch_restaurant(self):
        letters = string.ascii_letters
        random_name = ''.join(random.choice(letters) for i in range(12))

        new_r = Restaurant(name=random_name, cuisine="PATCH_TEST_CUISINE")
        new_r.insert()

        restaurant = Restaurant.query.filter_by(name=random_name).one_or_none()
        id = restaurant.id
        body = {'name': restaurant.name + 'PATCHED!',
                'cuisine': 'PATCHED'}

        res = self.client().patch(f'/restaurants/{id}', json=body,
                                  headers=self.headers)
        data = json.loads(res.data)

        restaurant = Restaurant.query.filter_by(id=id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(restaurant.name, random_name + "PATCHED!")
        self.assertEqual(data['restaurants'][0]['cuisine'], "PATCHED")
        self.assertTrue(data['success'])

    def test_patch_order(self):
        letters = string.ascii_letters
        random_name = ''.join(random.choice(letters) for i in range(12))

        new_o = Order(restaurant_id=1, name=random_name, calories=1, sodium=1,
                      total_carbs=1, total_fat=1, cholesterol=1, protein=1)
        new_o.insert()

        order = Order.query.filter_by(name=random_name).one_or_none()
        id = order.id
        body = {'name': order.name + 'PATCHED!',
                'calories': 20}

        res = self.client().patch(f'/orders/{id}', json=body,
                                  headers=self.headers)
        data = json.loads(res.data)

        order = Order.query.filter_by(id=id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(order.name, random_name + "PATCHED!")
        self.assertEqual(data['orders'][0]['calories'], 20)
        self.assertTrue(data['success'])

    def test_400_bad_add_restaurant(self):
        res = self.client().post('/restaurants',
                                 json={'name': 'Is this enough?'},
                                 headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertTrue(data['message'])
        self.assertFalse(data['success'])

    def test_404_get_orders_for_resto_not_found(self):
        res = self.client().get('/restaurants/9999/orders',
                                headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])
        self.assertFalse(data['success'])

    def test_404_patch_order_not_found(self):
        res = self.client().patch('/orders/99999', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])
        self.assertFalse(data['success'])

    def test_405_delete_restaurants(self):
        res = self.client().delete('/restaurants', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertTrue(data['message'])
        self.assertFalse(data['success'])

    def test_400_get_restaurants_no_header(self):
        res = self.client().get('/restaurants')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertTrue(data['message'])
        self.assertFalse(data['success'])

    def test_403_trusted_editor_not_allowed_delete_resto(self):
        self.headers.update({
            'Authorization': f'bearer {os.environ["DEMO_JWT_TRUSTED_EDITOR"]}'
        })
        res = self.client().delete('/restaurants/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['error'], 403)
        self.assertTrue(data['message'])
        self.assertFalse(data['success'])

    def test_403_contributor_not_allowed_patch_resto(self):
        self.headers.update({
            'Authorization': f'bearer {os.environ["DEMO_JWT_CONTRIBUTOR"]}'
        })
        res = self.client().patch('/restaurants/1', json={'name': 'Try me!'},
                                  headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['error'], 403)
        self.assertTrue(data['message'])
        self.assertFalse(data['success'])

    def test_401_malformed_authorization_no_bearer_get_orders(self):
        self.headers.update({
            'Authorization': f'{os.environ["DEMO_JWT_TRUSTED_EDITOR"]}'
        })
        res = self.client().get('/orders', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['error'], 401)
        self.assertTrue(data['message'])
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
