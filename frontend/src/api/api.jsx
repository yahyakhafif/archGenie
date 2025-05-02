import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export const authAPI = {
    register: (userData) => api.post('/api/auth/register', userData),
    login: (userData) => api.post('/api/auth/login', userData),
    getCurrentUser: () => api.get('/api/auth/me')
};

export const userAPI = {
    getAllUsers: () => api.get('/api/users'),
    getUserById: (id) => api.get(`/api/users/${id}`),
    toggleFavorite: (styleId) => api.put(`/api/users/favorites/${styleId}`),
    getFavorites: () => api.get('/api/users/favorites')
};

export const styleAPI = {
    getAllStyles: () => api.get('/api/styles'),
    getStyleById: (id) => api.get(`/api/styles/${id}`),
    createStyle: (styleData) => api.post('/api/styles', styleData),
    updateStyle: (id, styleData) => api.put(`/api/styles/${id}`, styleData),
    deleteStyle: (id) => api.delete(`/api/styles/${id}`),
    searchStyles: (keyword) => api.get(`/api/styles/search/${keyword}`),
    getRecommendations: (limit = 3, excludeIds = []) => {
        const excludeParam = excludeIds.length > 0 ? `&exclude=${excludeIds.join(',')}` : '';
        return api.get(`/api/styles/recommendations?limit=${limit}${excludeParam}`);
    },

    getReplacementRecommendation: (currentIds = []) => {
        const currentParam = currentIds.length > 0 ? `?current=${currentIds.join(',')}` : '';
        return api.get(`/api/styles/recommendations/replacement${currentParam}`);
    }
}

export default api;