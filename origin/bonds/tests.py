from rest_framework.test import APISimpleTestCase, RequestsClient
from django.contrib.auth.models import User

from bonds.models import Bond


class HelloWorld(APISimpleTestCase):
    def test_root(self):
        resp = self.client.get("/")
        assert resp.status_code == 200


class BondsAPITesting(APISimpleTestCase):
    databases = '__all__'

    @classmethod
    def setUpTestData(cls):
        cls.testData = Bond.objects.create(isin='12345', size=100000000, currency="EUR", maturity='2028-02-28',
                                           lei='5493001KJTIIGC8Y1R12', legal_name='Bloomberg Finance L.P.')

    @classmethod
    def setUpClass(cls):
        User.objects.create_user(username='testuser', password='12345')
        cls.auth_resp = RequestsClient().post('http://127.0.0.1:8000/api-token-auth/',
                                              json={'username': 'testuser', 'password': '12345'})
        cls.token = 'Token ' + cls.auth_resp.json()['token']

    @classmethod
    def tearDownClass(cls):
        cls.auth_resp = None
        cls.token = None

    def test_get_bonds_unauthenticated(self):
        resp = RequestsClient().get('http://127.0.0.1:8000/bonds/')
        assert resp.status_code == 401

    def test_post_bonds_unauthenticated(self):
        resp = RequestsClient().post('http://127.0.0.1:8000/bonds/',
                                     json={"isin": "12333", "size": 100000000, "currency": "EUR",
                                           "maturity": "2025-02-28",
                                           "lei": "R0MUWSFPU8MPRO8K5P83"})
        assert resp.status_code == 401

    def test_authentication(self):
        assert self.auth_resp.status_code == 200 and len(self.token) == 46

    def test_get_bonds_authenticated(self):
        resp = RequestsClient().get('http://127.0.0.1:8000/bonds/', headers={'Authorization': self.token})
        assert resp.status_code == 200

    def test_post_bonds_authenticated(self):
        resp = RequestsClient().post('http://127.0.0.1:8000/bonds/', headers={'Authorization': self.token},
                                     json={"isin": "12333", "size": 100000000, "currency": "EUR",
                                           "maturity": "2025-02-28",
                                           "lei": "R0MUWSFPU8MPRO8K5P83"})
        assert resp.status_code == 201
        self.get_bond_results_filter()

    def get_bond_results_filter(self):
        resp = RequestsClient().get('http://127.0.0.1:8000/bonds/?legal_name=bnp',
                                    headers={'Authorization': self.token})
        assert resp.status_code == 200
