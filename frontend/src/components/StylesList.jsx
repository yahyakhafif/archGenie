import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { styleAPI } from '../api/api';
import { useAuth } from '../hooks/useAuth';

const StylesList = () => {
    const [styles, setStyles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const { isAuthenticated } = useAuth();

    useEffect(() => {
        const fetchStyles = async () => {
            try {
                const res = await styleAPI.getAllStyles();
                setStyles(res.data);
            } catch (err) {
                setError('Failed to load architectural styles');
                console.error('Error fetching styles:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchStyles();
    }, []);

    const handleSearch = async (e) => {
        e.preventDefault();

        if (!searchTerm.trim()) {
            try {
                setLoading(true);
                const res = await styleAPI.getAllStyles();
                setStyles(res.data);
            } catch (err) {
                setError('Failed to load architectural styles');
            } finally {
                setLoading(false);
            }
            return;
        }

        try {
            setLoading(true);
            const res = await styleAPI.searchStyles(searchTerm);
            setStyles(res.data);
        } catch (err) {
            setError('Error searching styles');
            console.error('Search error:', err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <div className="center">Loading...</div>;
    }

    if (error) {
        return <div className="alert alert-danger">{error}</div>;
    }

    return (
        <div className="styles-container">
            <div className="styles-header">
                <h1>Architectural Styles</h1>
                {isAuthenticated && (
                    <Link to="/styles/add" className="btn btn-primary">
                        Add New Style
                    </Link>
                )}
            </div>

            <div className="search-container">
                <form onSubmit={handleSearch}>
                    <div className="search-form">
                        <input
                            type="text"
                            placeholder="Search styles..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="form-control"
                        />
                        <button type="submit" className="btn btn-primary">
                            Search
                        </button>
                    </div>
                </form>
            </div>

            {styles.length === 0 ? (
                <div className="alert alert-info">
                    No architectural styles found. {isAuthenticated && (
                        <Link to="/styles/add">Add a new style</Link>
                    )}
                </div>
            ) : (
                <div className="styles-grid">
                    {styles.map((style) => (
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
                                <p>{style.description.substring(0, 100)}...</p>
                                <div className="style-characteristics">
                                    {style.characteristics.slice(0, 2).map((char, index) => (
                                        <span key={index} className="badge badge-primary">
                                            {char}
                                        </span>
                                    ))}
                                    {style.characteristics.length > 2 && (
                                        <span className="badge badge-secondary">
                                            +{style.characteristics.length - 2} more
                                        </span>
                                    )}
                                </div>
                                <Link to={`/styles/${style._id}`} className="btn btn-outline">
                                    Learn More
                                </Link>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default StylesList;