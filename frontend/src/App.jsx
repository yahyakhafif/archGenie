import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './hooks/useAuth';
import PrivateRoute from './components/PrivateRoute';
import Navbar from './components/navbar';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import StylesList from './components/StylesList';
import StyleDetail from './components/StyleDetail';
import StyleForm from './components/StyleForm';
import Profile from './components/Profile';
import NotFound from './components/NotFound';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <div className="container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/styles" element={<StylesList />} />
            <Route path="/styles/:id" element={<StyleDetail />} />
            <Route
              path="/styles/add"
              element={
                <PrivateRoute>
                  <StyleForm />
                </PrivateRoute>
              }
            />
            <Route
              path="/styles/edit/:id"
              element={
                <PrivateRoute adminOnly={true}>
                  <StyleForm />
                </PrivateRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <PrivateRoute>
                  <Profile />
                </PrivateRoute>
              }
            />
            <Route
              path="/styles/add"
              element={
                <PrivateRoute>
                  <StyleForm />
                </PrivateRoute>
              }
            />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App;