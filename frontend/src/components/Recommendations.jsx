import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { styleAPI } from '../api/api';
import { useAuth } from '../hooks/useAuth';

const Recommendations = () => {
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { isAuthenticated } = useAuth();

    useEffect(() => {
        const fetchRecommendations = async () => {
            if (!isAuthenticated) {
                setLoading(false);
                return;
            }

            try {
                const res = await styleAPI.getRecommendations();
                setRecommendations(res.data);
            } catch (err) {
                setError('Failed to load recommendations');
                console.error('Error fetching recommendations:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchRecommendations();
    }, [isAuthenticated]);

    if (!isAuthenticated) {
        return (
            <div className="recommendations-section">
                <h2>Personalized Recommendations</h2>
                <p>Sign in to get personalized architectural style recommendations.</p>
            </div>
        );
    }

    if (loading) {
        return <div className="center">Loading recommendations...</div>;
    }

    if (error) {
        return <div className="alert alert-danger">{error}</div>;
    }

    if (recommendations.length === 0) {
        return (
            <div className="recommendations-section">
                <h2>Recommendations</h2>
                <p>Add some favorite styles to get personalized recommendations.</p>
            </div>
        );
    }

    return (
        <div className="recommendations-section">
            <h2>Recommended For You</h2>
            <p className="recommendation-explanation">
                Based on your favorites, you might also like these architectural styles:
            </p>

            <div className="styles-grid">
                {recommendations.map((style) => (
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
                            <p className="origin">Origin: {style.origin}</p>
                            <p>{style.description.substring(0, 100)}...</p>
                            <div className="style-characteristics">
                                {style.characteristics.slice(0, 2).map((char, index) => (
                                    <span key={index} className="badge badge-primary">
                                        {char}
                                    </span>
                                ))}
                            </div>
                            <Link to={`/styles/${style._id}`} className="btn btn-outline">
                                Learn More
                            </Link>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Recommendations;