import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { styleAPI } from '../api/api';
import { useAuth } from '../hooks/useAuth';

const StyleForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const { user } = useAuth();
    const isEditMode = Boolean(id);

    const [loading, setLoading] = useState(isEditMode);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const [submitting, setSubmitting] = useState(false);
    const [styleCreator, setStyleCreator] = useState(null);

    const [formData, setFormData] = useState({
        name: '',
        period: '',
        description: '',
        characteristics: [''],
        mainFeatures: [''],
        famousExamples: [
            { name: '', location: '', architect: '', year: '', imageUrl: '' }
        ],
        imageUrl: ''
    });

    useEffect(() => {
        if (!isEditMode) return;

        styleAPI.getStyleById(id)
            .then(res => {
                const d = res.data;
                setStyleCreator(d.createdBy);

                if (user && user._id !== d.createdBy) {
                    setError('You are not authorized to edit this style');
                    setTimeout(() => navigate('/styles'), 2000);
                    return;
                }

                setFormData({
                    name: d.name || '',
                    period: d.period || '',
                    description: d.description || '',
                    characteristics: d.characteristics.length ? d.characteristics : [''],
                    mainFeatures: d.mainFeatures?.length ? d.mainFeatures : [''],
                    famousExamples: d.famousExamples?.length ? d.famousExamples : [{ name: '', location: '', architect: '', year: '', imageUrl: '' }],
                    imageUrl: d.imageUrl || ''
                });
            })
            .catch(() => setError('Failed to load style data.'))
            .finally(() => setLoading(false));
    }, [id, isEditMode, user, navigate]);

    const handleChange = e => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleArrayChange = (field, idx, value) => {
        const arr = [...formData[field]];
        arr[idx] = value;
        setFormData({ ...formData, [field]: arr });
    };

    const handleExampleChange = (idx, key, value) => {
        const ex = [...formData.famousExamples];
        ex[idx] = { ...ex[idx], [key]: value };
        setFormData({ ...formData, famousExamples: ex });
    };

    const addItem = field => {
        if (field === 'famousExamples') {
            setFormData({
                ...formData,
                famousExamples: [
                    ...formData.famousExamples,
                    { name: '', location: '', architect: '', year: '', imageUrl: '' }
                ]
            });
        } else {
            setFormData({ ...formData, [field]: [...formData[field], ''] });
        }
    };

    const removeItem = (field, idx) => {
        if (formData[field].length <= 1) return;
        const arr = formData[field].filter((_, i) => i !== idx);
        setFormData({ ...formData, [field]: arr });
    };

    const handleSubmit = async e => {
        e.preventDefault();
        setSubmitting(true);
        setError(null);

        const payload = {
            ...formData,
            characteristics: formData.characteristics.filter(c => c.trim()),
            mainFeatures: formData.mainFeatures.filter(f => f.trim()),
            famousExamples: formData.famousExamples.filter(
                ex => ex.name.trim() || ex.location.trim()
            )
        };

        try {
            if (isEditMode) {
                if (user && user._id !== styleCreator) {
                    setError('You are not authorized to edit this style');
                    setSubmitting(false);
                    return;
                }
                await styleAPI.updateStyle(id, payload);
                setSuccess('Updated successfully!');
                setTimeout(() => navigate('/styles'), 1200);
            } else {
                await styleAPI.createStyle(payload);
                setSuccess('Created successfully!');
                setTimeout(() => navigate('/styles'), 1200);
            }
        } catch (err) {
            setError(err.response?.data?.message || 'Save failed.');
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) return <div className="center">Loading...</div>;

    return (
        <div className="style-form-container">
            <h1 className="form-title">{isEditMode ? 'Edit' : 'Add New'} Architectural Style</h1>

            {error && <div className="alert alert-danger">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}

            <form onSubmit={handleSubmit} className="style-form">
                <div className="form-group">
                    <label htmlFor="name">Name*</label>
                    <input
                        id="name"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        className="form-control"
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="period">Time Period*</label>
                    <input
                        id="period"
                        name="period"
                        value={formData.period}
                        onChange={handleChange}
                        className="form-control"
                        placeholder="e.g. 1750–1850"
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="description">Description*</label>
                    <textarea
                        id="description"
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        className="form-control"
                        rows="4"
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Key Characteristics*</label>
                    {formData.characteristics.map((c, i) => (
                        <div key={i} className="array-input-group">
                            <input
                                value={c}
                                onChange={e => handleArrayChange('characteristics', i, e.target.value)}
                                className="form-control"
                                placeholder="e.g. Symmetrical facades"
                            />
                            <button
                                type="button"
                                onClick={() => removeItem('characteristics', i)}
                                className="btn btn-danger"
                            >
                                Remove
                            </button>
                        </div>
                    ))}
                    <button
                        type="button"
                        onClick={() => addItem('characteristics')}
                        className="btn btn-secondary btn-sm"
                    >
                        Add Characteristic
                    </button>
                </div>

                <div className="form-group">
                    <label>Main Features</label>
                    {formData.mainFeatures.map((f, i) => (
                        <div key={i} className="array-input-group">
                            <input
                                value={f}
                                onChange={e => handleArrayChange('mainFeatures', i, e.target.value)}
                                className="form-control"
                                placeholder="e.g. Domed roofs"
                            />
                            <button
                                type="button"
                                onClick={() => removeItem('mainFeatures', i)}
                                className="btn btn-danger"
                            >
                                Remove
                            </button>
                        </div>
                    ))}
                    <button
                        type="button"
                        onClick={() => addItem('mainFeatures')}
                        className="btn btn-secondary btn-sm"
                    >
                        Add Feature
                    </button>
                </div>

                <div className="form-group">
                    <label>Famous Examples</label>
                    {formData.famousExamples.map((ex, i) => (
                        <div key={i} className="example-inputs">
                            <h4>Example #{i + 1}</h4>
                            <div className="form-row">
                                <div className="form-group">
                                    <label>Building Name</label>
                                    <input
                                        value={ex.name}
                                        onChange={e => handleExampleChange(i, 'name', e.target.value)}
                                        className="form-control"
                                        placeholder="e.g. Taj Mahal"
                                    />
                                </div>

                                <div className="form-group">
                                    <label>Location</label>
                                    <input
                                        value={ex.location}
                                        onChange={e => handleExampleChange(i, 'location', e.target.value)}
                                        className="form-control"
                                        placeholder="e.g. Agra, India"
                                    />
                                </div>
                            </div>

                            <div className="form-row">
                                <div className="form-group">
                                    <label>Architect</label>
                                    <input
                                        value={ex.architect}
                                        onChange={e => handleExampleChange(i, 'architect', e.target.value)}
                                        className="form-control"
                                        placeholder="e.g. Ustad Ahmad Lahauri"
                                    />
                                </div>

                                <div className="form-group">
                                    <label>Year</label>
                                    <input
                                        value={ex.year}
                                        onChange={e => handleExampleChange(i, 'year', e.target.value)}
                                        className="form-control"
                                        placeholder="e.g. 1653"
                                    />
                                </div>
                            </div>

                            <div className="form-group">
                                <label>Image URL</label>
                                <input
                                    value={ex.imageUrl}
                                    onChange={e => handleExampleChange(i, 'imageUrl', e.target.value)}
                                    className="form-control"
                                    placeholder="https://example.com/image.jpg"
                                />
                            </div>

                            <button
                                type="button"
                                onClick={() => removeItem('famousExamples', i)}
                                className="btn btn-danger"
                            >
                                Remove Example
                            </button>
                        </div>
                    ))}
                    <button
                        type="button"
                        onClick={() => addItem('famousExamples')}
                        className="btn btn-secondary btn-sm"
                    >
                        Add Example
                    </button>
                </div>

                <div className="form-group">
                    <label htmlFor="imageUrl">Style Image URL</label>
                    <input
                        id="imageUrl"
                        name="imageUrl"
                        value={formData.imageUrl}
                        onChange={handleChange}
                        className="form-control"
                        placeholder="https://example.com/image.jpg"
                    />
                </div>

                <div className="form-actions">
                    <button
                        type="button"
                        onClick={() => navigate('/styles')}
                        className="btn btn-secondary"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        disabled={submitting}
                        className="btn btn-primary"
                    >
                        {submitting
                            ? isEditMode ? 'Updating...' : 'Creating...'
                            : isEditMode ? 'Update Style' : 'Create Style'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default StyleForm;