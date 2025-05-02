import json
import pytest


class TestAuthAPI:

    def test_register_new_user(self, client, init_db):
        res = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password123'
        })

        data = json.loads(res.data)
        assert res.status_code == 201
        assert 'token' in data
        assert data['success'] is True

    def test_validate_required_fields(self, client, init_db):
        res = client.post('/api/auth/register', json={
            'name': '',
            'email': 'invalid-email',
            'password': '123'
        })

        data = json.loads(res.data)
        assert res.status_code == 400
        assert 'errors' in data

    def test_not_register_duplicate_email(self, client, init_db):
        res = client.post('/api/auth/register', json={
            'name': 'Another User',
            'email': 'test@example.com',
            'password': 'password123'
        })

        data = json.loads(res.data)
        assert res.status_code == 400
        assert data['msg'] == 'User already exists'

    def test_login_user(self, client, init_db):
        res = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })

        data = json.loads(res.data)
        assert res.status_code == 200
        assert 'token' in data
        assert 'user' in data
        assert data['success'] is True

    def test_not_login_invalid_credentials(self, client, init_db):
        res = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })

        data = json.loads(res.data)
        assert res.status_code == 401
        assert data['msg'] == 'Invalid credentials'

    def test_get_current_user(self, client, init_db):
        login_res = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        token = json.loads(login_res.data)['token']

        res = client.get('/api/auth/me', headers={
            'Authorization': f'Bearer {token}'
        })

        data = json.loads(res.data)
        assert res.status_code == 200
        assert data['name'] == 'Test User'
        assert data['email'] == 'test@example.com'

    def test_not_allow_access_without_token(self, client, init_db):
        res = client.get('/api/auth/me')

        data = json.loads(res.data)
        assert res.status_code == 401
        assert data['success'] is False
