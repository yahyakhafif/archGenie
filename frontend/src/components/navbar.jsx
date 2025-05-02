import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Navbar = () => {
    const { isAuthenticated, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    return (
        <nav className="navbar">
            <div className="container">
                <h1>
                    <Link to="/" className="navbar-brand">
                        <div className="logo-container">
                            <svg className="logo" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                                <polygon points="50,10 90,90 10,90" fill="none" stroke="currentColor" strokeWidth="4" />
                                <rect x="35" y="50" width="30" height="40" fill="none" stroke="currentColor" strokeWidth="3" />
                                <rect x="45" y="70" width="10" height="20" fill="none" stroke="currentColor" strokeWidth="2" />
                                <line x1="20" y1="90" x2="80" y2="90" stroke="currentColor" strokeWidth="4" />
                            </svg>
                            Architex
                        </div>
                    </Link>
                </h1>
                <ul className="nav-links">
                    <li>
                        <Link to="/">Home</Link>
                    </li>
                    {isAuthenticated ? (
                        <>

                            <li>
                                <Link to="/styles">Styles</Link>
                            </li>
                            <li>
                                <Link to="/styles/add">Add Style</Link>
                            </li>
                            <li>
                                <Link to="/profile">Profile</Link>
                            </li>
                            <li>
                                <button onClick={handleLogout} className="btn btn-outline">
                                    Logout
                                </button>
                            </li>

                        </>
                    ) : (
                        <>
                            <li>
                                <Link to="/login">Login</Link>
                            </li>
                            <li>
                                <Link to="/register">Register</Link>
                            </li>
                        </>
                    )}
                </ul>
            </div>
        </nav>
    );
};

export default Navbar;