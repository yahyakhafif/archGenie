import json
import pytest


class TestStylesAPI:

    @pytest.fixture(autouse=True)
    def setup(self, client, init_db):
        self.client = client
        self.db = init_db

        register_res = client.post('/api/auth/register', json={
            'name': 'Style Test User',
            'email': 'style-test@example.com',
            'password': 'password123'
        })

        data = json.loads(register_res.data)
        if register_res.status_code == 201:
            self.token = data['token']
        else:
            login_res = client.post('/api/auth/login', json={
                'email': 'style-test@example.com',
                'password': 'password123'
            })
            self.token = json.loads(login_res.data)['token']

        user_res = client.get('/api/auth/me', headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.user_id = json.loads(user_res.data)['_id']

    def test_create_style(self):
        style_data = {
            'name': 'Gothic Architecture',
            'period': '12th-16th Century',
            'description': 'Gothic architecture is a style that flourished in Europe during the High and Late Middle Ages.',
            'characteristics': ['Pointed arches', 'Ribbed vaults', 'Flying buttresses'],
            'mainFeatures': ['Tall spires', 'Large stained glass windows'],
            'famousExamples': [{
                'name': 'Notre-Dame Cathedral',
                'location': 'Paris, France',
                'architect': 'Unknown',
                'year': '1163-1345'
            }],
            'imageUrl': 'https://example.com/gothic.jpg'
        }

        res = self.client.post('/api/styles', json=style_data, headers={
            'Authorization': f'Bearer {self.token}'
        })

        data = json.loads(res.data)
        assert res.status_code == 201
        assert data['name'] == 'Gothic Architecture'
        assert data['createdBy'] == self.user_id

        self.__class__.style_id = data['_id']

    def test_not_create_style_without_auth(self):
        res = self.client.post('/api/styles', json={
            'name': 'Renaissance',
            'period': '14th-17th Century',
            'description': 'Renaissance architecture.',
            'characteristics': ['Symmetry', 'Proportion']
        })

        assert res.status_code == 401

    def test_validate_required_fields(self):
        res = self.client.post('/api/styles', json={
            'name': 'Incomplete Style',
            'period': '',
            'description': '',
            'characteristics': []
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })

        data = json.loads(res.data)
        assert res.status_code == 400
        assert 'errors' in data

    def test_get_all_styles(self):
        res = self.client.get('/api/styles')

        data = json.loads(res.data)
        assert res.status_code == 200
        assert isinstance(data, list)

    def test_get_style_by_id(self):
        create_res = self.client.post('/api/styles', json={
            'name': 'Test Style By ID',
            'period': '20th Century',
            'description': 'Test style for get by ID.',
            'characteristics': ['Test']
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        created = json.loads(create_res.data)
        style_id = created['_id']

        res = self.client.get(f'/api/styles/{style_id}')

        data = json.loads(res.data)
        assert res.status_code == 200
        assert data['_id'] == style_id

    def test_return_404_for_nonexistent_style(self):
        res = self.client.get('/api/styles/999999')

        data = json.loads(res.data)
        assert res.status_code == 404
        assert data['msg'] == 'Style not found'

    def test_update_style(self):
        create_res = self.client.post('/api/styles', json={
            'name': 'Update Test Style',
            'period': '20th Century',
            'description': 'Original description.',
            'characteristics': ['Test']
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        created = json.loads(create_res.data)
        style_id = created['_id']

        res = self.client.put(f'/api/styles/{style_id}', json={
            'description': 'Updated description for test style'
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })

        data = json.loads(res.data)
        assert res.status_code == 200
        assert data['description'] == 'Updated description for test style'

    def test_not_update_without_auth(self):
        res = self.client.put('/api/styles/1', json={
            'name': 'Hacked Style'
        })

        assert res.status_code == 401

    def test_delete_style(self):
        create_res = self.client.post('/api/styles', json={
            'name': 'Delete Test Style',
            'period': '20th Century',
            'description': 'Style to be deleted.',
            'characteristics': ['Test']
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        created = json.loads(create_res.data)
        style_id = created['_id']

        res = self.client.delete(f'/api/styles/{style_id}', headers={
            'Authorization': f'Bearer {self.token}'
        })

        data = json.loads(res.data)
        assert res.status_code == 200
        assert data['msg'] == 'Style removed'

    def test_search_styles(self):
        self.client.post('/api/styles', json={
            'name': 'Baroque Architecture',
            'period': '17th-18th Century',
            'description': 'Baroque is a highly ornate style of architecture, music, and art.',
            'characteristics': ['Dramatic use of light', 'Curved lines', 'Grand scale']
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })

        res = self.client.get('/api/styles/search/baroque')

        data = json.loads(res.data)
        assert res.status_code == 200
        assert isinstance(data, list)
        assert len(data) > 0

    def test_search_empty_results(self):
        res = self.client.get('/api/styles/search/nonexistentstyle')

        data = json.loads(res.data)
        assert res.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 0
