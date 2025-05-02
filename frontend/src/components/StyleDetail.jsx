import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { styleAPI, userAPI } from '../api/api';
import { useAuth } from '../hooks/useAuth';

const StyleDetail = () => {
    const { id } = useParams();
    const [style, setStyle] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isFavorite, setIsFavorite] = useState(false);
    const { isAuthenticated, user } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchStyle = async () => {
            try {
                const res = await styleAPI.getStyleById(id);
                setStyle(res.data);

                if (isAuthenticated && user) {
                    const favRes = await userAPI.getFavorites();
                    setIsFavorite(
                        favRes.data.some((fav) => fav._id === res.data._id)
                    );
                }
            } catch (err) {
                setError('Failed to load style details');
                console.error('Error fetching style:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchStyle();
    }, [id, isAuthenticated, user]);

    const handleDelete = async () => {
        if (user._id !== style.createdBy) {
            setError('You are not authorized to delete this style');
            return;
        }

        if (window.confirm('Are you sure you want to delete this style?')) {
            try {
                await styleAPI.deleteStyle(id);
                navigate('/styles');
            } catch (err) {
                setError('Failed to delete style');
                console.error('Delete error:', err);
            }
        }
    };

    const toggleFavorite = async () => {
        if (!isAuthenticated) {
            navigate('/login');
            return;
        }

        try {
            await userAPI.toggleFavorite(id);
            setIsFavorite(!isFavorite);
        } catch (err) {
            console.error('Error toggling favorite:', err);
        }
    };

    if (loading) {
        return <div className="center">Loading...</div>;
    }

    if (error || !style) {
        return <div className="alert alert-danger">{error || 'Style not found'}</div>;
    }

    const isCreator = isAuthenticated && user && style.createdBy === user._id;

    return (
        <div className="style-detail-container">
            <div className="style-detail-header">
                <h1>{style.name}</h1>
                <div className="style-actions">
                    {isAuthenticated && (
                        <button
                            onClick={toggleFavorite}
                            className={`favorite-btn ${isFavorite ? 'active' : ''}`}
                            title={isFavorite ? 'Remove from favorites' : 'Add to favorites'}
                        >
                            {isFavorite ? '★' : '☆'}
                        </button>
                    )}
                    {isCreator && (
                        <>
                            <Link
                                to={`/styles/edit/${style._id}`}
                                className="btn btn-secondary"
                            >
                                Edit
                            </Link>
                            <button onClick={handleDelete} className="btn btn-danger">
                                Delete
                            </button>
                        </>
                    )}
                </div>
            </div>

            <div className="style-detail-content">
                <div className="style-main-info">
                    {style.imageUrl && (
                        <img
                            src={style.imageUrl}
                            alt={style.name}
                            className="style-detail-image"
                        />
                    )}
                    <div className="style-info">
                        <div className="info-item">
                            <h3>Period</h3>
                            <p>{style.period}</p>
                        </div>
                        <div className="info-item">
                            <h3>Description</h3>
                            <p>{style.description}</p>
                        </div>
                    </div>
                </div>

                <div className="style-characteristics-section">
                    <h3>Key Characteristics</h3>
                    <ul className="characteristics-list">
                        {style.characteristics.map((char, index) => (
                            <li key={index}>{char}</li>
                        ))}
                    </ul>
                </div>

                {style.mainFeatures && style.mainFeatures.length > 0 && (
                    <div className="style-features-section">
                        <h3>Main Features</h3>
                        <ul className="features-list">
                            {style.mainFeatures.map((feature, index) => (
                                <li key={index}>{feature}</li>
                            ))}
                        </ul>
                    </div>
                )}

                {style.famousExamples && style.famousExamples.length > 0 && (
                    <div className="famous-examples-section">
                        <h3>Famous Examples</h3>
                        <div className="examples-grid">
                            {style.famousExamples.map((example, index) => (
                                <div key={index} className="example-card">
                                    {example.imageUrl && (
                                        <img
                                            src={example.imageUrl}
                                            alt={example.name}
                                            className="example-image"
                                        />
                                    )}
                                    <div className="example-info">
                                        <h4>{example.name}</h4>
                                        <p>{example.location}</p>
                                        {example.architect && <p>Architect: {example.architect}</p>}
                                        {example.year && <p>Year: {example.year}</p>}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>

            <Link to="/styles" className="back-link">
                Back to Styles
            </Link>
        </div>
    );
};

export default StyleDetail;