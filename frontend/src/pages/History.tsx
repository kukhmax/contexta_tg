import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import WebApp from '@twa-dev/sdk';

const History: React.FC = () => {
    const { t } = useTranslation();
    const [stories, setStories] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [visibleTranslations, setVisibleTranslations] = useState<{ [key: number]: boolean }>({});

    useEffect(() => {
        fetchStories();
    }, []);

    const fetchStories = async () => {
        try {
            const telegramId = WebApp.initDataUnsafe.user?.id || 123456789;
            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

            const response = await fetch(`${API_URL}/api/v1/stories/?telegram_id=${telegramId}`);
            if (response.ok) {
                const data = await response.json();
                setStories(data);
            }
        } catch (error) {
            console.error("Failed to fetch stories", error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleDelete = async (storyId: number) => {
        if (!confirm(t('delete_story') + "?")) return;

        try {
            const telegramId = WebApp.initDataUnsafe.user?.id || 123456789;
            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

            await fetch(`${API_URL}/api/v1/stories/${storyId}?telegram_id=${telegramId}`, {
                method: 'DELETE'
            });

            setStories(stories.filter(s => s.id !== storyId));
        } catch (error) {
            console.error("Failed to delete", error);
        }
    };

    const toggleTranslation = (storyId: number) => {
        setVisibleTranslations(prev => ({
            ...prev,
            [storyId]: !prev[storyId]
        }));
    };

    return (
        <div className="container" style={{ paddingTop: '20px' }}>
            <h2 style={{ marginBottom: '20px', color: 'var(--color-accent-primary)' }}>{t('history')}</h2>

            {isLoading ? <p>{t('loading')}</p> : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                    {stories.length === 0 ? (
                        <p style={{ color: 'var(--color-text-secondary)' }}>No stories yet.</p>
                    ) : stories.map((story) => (
                        <div key={story.id} className="card">
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                                <h3 style={{ fontSize: '18px', color: 'var(--color-accent-primary)', margin: 0 }}>
                                    {story.input_word}
                                    {/* Placeholder for word translation if available later */}
                                </h3>
                                <button
                                    onClick={() => handleDelete(story.id)}
                                    style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '18px' }}
                                >
                                    🗑️
                                </button>
                            </div>

                            <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6', fontSize: '16px', marginBottom: '12px' }}>
                                {story.content.split(/(<b>.*?<\/b>)/g).map((part: string, index: number) => {
                                    if (part.startsWith('<b>') && part.endsWith('</b>')) {
                                        const cleanWord = part.replace(/<\/?b>/g, '');
                                        return (
                                            <span
                                                key={index}
                                                style={{
                                                    color: '#fbbf24',
                                                    fontWeight: 'bold',
                                                }}
                                            >
                                                {cleanWord}
                                            </span>
                                        );
                                    }
                                    return <span key={index}>{part}</span>;
                                })}
                            </div>

                            <button
                                className="btn btn-outline"
                                style={{ width: '100%', fontSize: '14px', padding: '8px' }}
                                onClick={() => toggleTranslation(story.id)}
                            >
                                {visibleTranslations[story.id] ? t('hide_translation') : t('show_translation')}
                            </button>

                            {visibleTranslations[story.id] && story.translation && (
                                <div style={{ marginTop: '12px', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '12px' }}>
                                    <p style={{ color: 'var(--color-text-secondary)', fontStyle: 'italic', whiteSpace: 'pre-wrap', fontSize: '14px' }}>
                                        {story.translation}
                                    </p>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default History;
