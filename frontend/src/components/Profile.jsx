import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { userAPI } from '../api/api';

const Profile = () => {
    const { user } = useAuth();
    const [favorites, setFavorites] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchFavorites = async () => {
            try {
                const res = await userAPI.getFavorites();
                setFavorites(res.data);
            } catch (err) {
                setError('Failed to load favorite styles');
                console.error('Error fetching favorites:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchFavorites();
    }, []);

    const removeFavorite = async (styleId) => {
        try {
            await userAPI.toggleFavorite(styleId);
            setFavorites(favorites.filter(fav => fav._id !== styleId));
        } catch (err) {
            console.error('Error removing favorite:', err);
        }
    };

    if (loading) {
        return <div className="center">Loading...</div>;
    }

    return (
        <div className="profile-container">
            <div className="profile-header">
                <h1>My Profile</h1>
            </div>

            <div className="profile-content">
                <div className="user-info card">
                    <h2>Account Information</h2>
                    <div className="user-details">
                        <p><strong>Name:</strong> {user.name}</p>
                        <p><strong>Email:</strong> {user.email}</p>
                        <p><strong>Account Type:</strong> {user.isAdmin ? 'Administrator' : 'User'}</p>
                    </div>
                </div>

                <div className="favorites-section">
                    <h2>Favorite Styles</h2>

                    {error && <div className="alert alert-danger">{error}</div>}

                    {favorites.length === 0 ? (
                        <div className="empty-favorites">
                            <p>You haven't added any favorite styles yet.</p>
                            <Link to="/styles" className="btn btn-primary">
                                Browse Styles
                            </Link>
                        </div>
                    ) : (
                        <div className="styles-grid">
                            {favorites.map((style) => (
                                <div key={style._id} className="style-card">
                                    {style.imageUrl && (
                                        <img
                                            src={style.imageUrl}
                                            alt={style.name}
                                            className="style-image"
                                        />
                                    )}
                                    <div className="style-content">
                                        <h3>{style.name}</h3>
                                        <p className="period">{style.period}</p>
                                        <p>{style.description.substring(0, 80)}...</p>
                                        <div className="card-actions">
                                            <Link to={`/styles/${style._id}`} className="btn btn-outline">
                                                View Details
                                            </Link>
                                            <button
                                                onClick={() => removeFavorite(style._id)}
                                                className="btn btn-danger"
                                            >
                                                Remove
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Profile;