import React, { useEffect, useState, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { styleAPI, userAPI } from '../api/api';
import { useAuth } from '../hooks/useAuth';

const Home = () => {
    const [featuredStyles, setFeaturedStyles] = useState([]);
    const [recommendedStyles, setRecommendedStyles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { isAuthenticated, user } = useAuth();

    const staticFeaturedStyles = [
        {
            _id: 'static1',
            name: 'Gothic',
            period: '12th-16th century',
            description: 'Gothic architecture is characterized by pointed arches, ribbed vaults, flying buttresses, and large stained glass windows which allowed more light to enter than was possible with the thick walls of Romanesque architecture.',
            imageUrl: 'https://images.unsplash.com/photo-1543832923-44667a44c804?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            isStatic: true
        },
        {
            _id: 'static2',
            name: 'Art Deco',
            period: '1920s-1930s',
            description: 'Art Deco architecture is characterized by bold geometric patterns, vibrant colors, and lavish ornamentation. It represented luxury, glamour, exuberance, and faith in social and technological progress.',
            imageUrl: 'https://images.unsplash.com/photo-1519501025264-65ba15a82390?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            isStatic: true
        },
        {
            _id: 'static3',
            name: 'Modernism',
            period: '1920s-1980s',
            description: 'Modernist architecture emphasizes function, simplicity, clean lines, and the use of industrial materials like concrete, glass, and steel. Form follows function is a key principle.',
            imageUrl: 'https://images.unsplash.com/photo-1487958449943-2429e8be8625?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            isStatic: true
        }
    ];

    const fetchRecommendations = useCallback(async () => {
        if (!isAuthenticated) return;

        try {
            setLoading(true);
            const res = await styleAPI.getRecommendations();
            setRecommendedStyles(res.data);
            setLoading(false);
        } catch (err) {
            console.error('Error fetching recommendations:', err);
            setError('Failed to load recommendations');
            setLoading(false);
        }
    }, [isAuthenticated]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);

                if (isAuthenticated) {
                    await fetchRecommendations();
                } else {
                    setFeaturedStyles(staticFeaturedStyles);
                    setLoading(false);
                }
            } catch (err) {
                console.error('Error loading data:', err);
                setError('Failed to load content');
                setLoading(false);
            }
        };

        fetchData();
    }, [isAuthenticated, fetchRecommendations]);

    const toggleFavorite = async (styleId) => {
        if (!isAuthenticated) return;

        try {
            await userAPI.toggleFavorite(styleId);

            setRecommendedStyles(prev => prev.filter(style => style._id !== styleId));

            fetchRecommendations();
        } catch (err) {
            console.error('Error toggling favorite:', err);
        }
    };

    const displayStyles = isAuthenticated ? recommendedStyles : featuredStyles;

    if (loading) {
        return <div className="center">Loading...</div>;
    }

    return (
        <div className="home">
            <section className="hero">
                <div className="hero-content">
                    <div className="hero-logo-container">
                        <svg className="hero-logo" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                            <polygon points="50,10 90,90 10,90" fill="none" stroke="currentColor" strokeWidth="4" />
                            <rect x="35" y="50" width="30" height="40" fill="none" stroke="currentColor" strokeWidth="3" />
                            <rect x="45" y="70" width="10" height="20" fill="none" stroke="currentColor" strokeWidth="2" />
                            <line x1="20" y1="90" x2="80" y2="90" stroke="currentColor" strokeWidth="4" />
                        </svg>
                    </div>
                    <h1>Discover Architecture with Architex</h1>
                    <p>
                        Explore the beauty and history of architecture from around the world.
                        Learn about different styles, their characteristics, and famous examples.
                    </p>
                    {isAuthenticated && (
                        <Link to="/styles" className="btn btn-primary">
                            Browse Styles
                        </Link>
                    )}
                </div>
            </section>

            <section className="featured">
                <h2>{isAuthenticated ? 'Recommended For You' : 'Featured Styles'}</h2>

                {isAuthenticated && (
                    <p className="section-description">
                        Based on your favorites, you might also like these architectural styles.
                    </p>
                )}

                {error && <div className="alert alert-danger">{error}</div>}

                {displayStyles.length === 0 && isAuthenticated ? (
                    <div className="empty-recommendations">
                        <p>Add some favorite styles to get personalized recommendations.</p>
                        <Link to="/styles" className="btn btn-outline">Browse Styles</Link>
                    </div>
                ) : (
                    <div className="styles-grid">
                        {displayStyles.map((style) => (
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
                                    <p className={isAuthenticated ? "period-highlight" : "period"}>{style.period}</p>
                                    <p>{style.description.substring(0, 100)}...</p>

                                    <div className="card-actions">
                                        <Link to={!style.isStatic ? `/styles/${style._id}` : '/styles'} className="btn btn-outline">
                                            Learn More
                                        </Link>

                                        {isAuthenticated && !style.isStatic && (
                                            <button
                                                onClick={() => toggleFavorite(style._id)}
                                                className="favorite-btn add"
                                                title="Add to favorites"
                                            >
                                                ★
                                            </button>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </section>

            <section className="info">
                <div className="info-content">
                    <h2>About Architex</h2>
                    <p>
                        Architex is your comprehensive resource for exploring architectural styles throughout history.
                        Whether you're a student, professional architect, or simply an enthusiast, our platform provides
                        detailed information about architectural movements, their distinctive features, and iconic examples.
                    </p>
                    <p>
                        {isAuthenticated
                            ? "Explore different styles and add them to your favorites to get personalized recommendations."
                            : "Create an account to save your favorite styles and get personalized recommendations."}
                    </p>
                </div>
            </section>
        </div>
    );
};

export default Home;