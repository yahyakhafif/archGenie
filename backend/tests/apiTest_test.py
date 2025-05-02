import json
import pytest


class TestUsersAPI:

    @pytest.fixture(autouse=True)
    def setup(self, client, init_db):
        self.client = client
        self.db = init_db

        register_res = client.post('/api/auth/register', json={
            'name': 'User Test',
            'email': 'user-test@example.com',
            'password': 'password123'
        })

        data = json.loads(register_res.data)
        if register_res.status_code == 201:
            self.token = data['token']
        else:
            login_res = client.post('/api/auth/login', json={
                'email': 'user-test@example.com',
                'password': 'password123'
            })
            self.token = json.loads(login_res.data)['token']

        user_res = client.get('/api/auth/me', headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.user_id = json.loads(user_res.data)['_id']

        style_res = client.post('/api/styles', json={
            'name': 'Modern Architecture',
            'period': '20th Century',
            'description': 'A style characterized by simplicity and function.',
            'characteristics': ['Clean lines', 'Minimal ornamentation', 'Emphasis on function']
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })

        style_data = json.loads(style_res.data)
        if style_res.status_code == 201:
            self.style_id = style_data['_id']
        else:
            styles_res = client.get('/api/styles/search/Modern Architecture')
            styles = json.loads(styles_res.data)
            self.style_id = styles[0]['_id'] if styles else None

    def test_get_favorites(self):
        res = self.client.get('/api/users/favorites', headers={
            'Authorization': f'Bearer {self.token}'
        })

        data = json.loads(res.data)
        assert res.status_code == 200
        assert isinstance(data, list)

    def test_add_favorite(self):
        res = self.client.put(f'/api/users/favorites/{self.style_id}', headers={
            'Authorization': f'Bearer {self.token}'
        })

        data = json.loads(res.data)
        assert res.status_code == 200
        assert data['success'] is True

    def test_toggle_favorite(self):

        self.client.put(f'/api/users/favorites/{self.style_id}', headers={
            'Authorization': f'Bearer {self.token}'
        })

        res = self.client.put(f'/api/users/favorites/{self.style_id}', headers={
            'Authorization': f'Bearer {self.token}'
        })

        data = json.loads(res.data)
        assert res.status_code == 200
        assert data['success'] is True

    def test_not_toggle_favorites_without_auth(self):
        res = self.client.put(f'/api/users/favorites/{self.style_id}')

        assert res.status_code == 401

    def test_get_all_users(self):
        res = self.client.get('/api/users/', headers={
            'Authorization': f'Bearer {self.token}'
        })

        data = json.loads(res.data)
        assert res.status_code == 200
        assert isinstance(data, list)
        assert len(data) > 0

    def test_not_get_users_without_auth(self):
        res = self.client.get('/api/users/')

        assert res.status_code == 401

    def test_get_user_by_id(self):
        res = self.client.get(f'/api/users/{self.user_id}', headers={
            'Authorization': f'Bearer {self.token}'
        })

        data = json.loads(res.data)
        assert res.status_code == 200
        assert data['_id'] == self.user_id
        assert data['name'] == 'User Test'

    def test_not_get_user_without_auth(self):
        res = self.client.get(f'/api/users/{self.user_id}')

        assert res.status_code == 401

    def test_return_404_for_nonexistent_user(self):
        res = self.client.get('/api/users/999999', headers={
            'Authorization': f'Bearer {self.token}'
        })

        data = json.loads(res.data)
        assert res.status_code == 404
        assert data['msg'] == 'User not found'
