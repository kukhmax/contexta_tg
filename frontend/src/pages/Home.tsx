import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import WebApp from '@twa-dev/sdk';
import AudioPlayer from '../components/AudioPlayer';

const Home: React.FC = () => {
    const { t, i18n } = useTranslation();
    const [word, setWord] = useState('');
    const [level, setLevel] = useState('B1');
    const [targetLang, setTargetLang] = useState('en');
    const [isLoading, setIsLoading] = useState(false);
    const [story, setStory] = useState<any>(null); // TODO: Type properly
    const [error, setError] = useState<string | null>(null);
    const [showTranslation, setShowTranslation] = useState(false);

    const handleGenerate = async () => {
        if (!word) return;

        setIsLoading(true);
        setError(null);
        setStory(null);
        setShowTranslation(false);

        try {
            const telegramId = WebApp.initDataUnsafe.user?.id || 123456789; // Fallback for dev

            // В продакшене используем относительный путь /api/v1... если прокси настроен
            // Или полный URL из env
            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

            const response = await fetch(`${API_URL}/api/v1/stories/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    word,
                    level,
                    target_language: targetLang,
                    native_language: i18n.language,
                    telegram_id: telegramId
                })
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || 'Failed to generate');
            }

            const data = await response.json();
            setStory(data);

        } catch (err: any) {
            setError(err.message || t('error'));
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="home-page">
            {/* Header with Language Switcher */}
            <header style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <h1 style={{ fontSize: '28px', color: 'var(--color-accent-primary)', margin: 0 }}>
                        Contexta
                    </h1>
                    <p style={{ color: 'var(--color-text-secondary)', margin: 0 }}>
                        {t('welcome')}, {WebApp.initDataUnsafe.user?.first_name || 'Guest'}!
                    </p>
                </div>
                <button
                    onClick={() => i18n.changeLanguage(i18n.language === 'en' ? 'ru' : 'en')}
                    style={{ background: 'none', border: 'none', fontSize: '24px', cursor: 'pointer' }}
                >
                    {i18n.language === 'en' ? '🇺🇸' : '🇷🇺'}
                </button>
            </header>

            {!story ? (
                <div className="card" style={{ marginBottom: '20px' }}>
                    <h2 style={{ marginBottom: '12px' }}>{t('start_learning')}</h2>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                        <label style={{ fontSize: '14px', color: 'var(--color-text-secondary)' }}>{t('select_language')}</label>
                        <select
                            className="input"
                            value={targetLang}
                            onChange={(e) => setTargetLang(e.target.value)}
                        >
                            <option value="en">English (US)</option>
                            <option value="pt">Português (EU)</option>
                            <option value="es">Español</option>
                            <option value="pl">Polski</option>
                        </select>

                        {/* ... rest of the form ... */}

                        <label style={{ fontSize: '14px', color: 'var(--color-text-secondary)' }}>{t('select_level')}</label>
                        <select
                            className="input"
                            value={level}
                            onChange={(e) => setLevel(e.target.value)}
                        >
                            <option value="A1">A1 (Beginner)</option>
                            <option value="A2">A2 (Elementary)</option>
                            <option value="B1">B1 (Intermediate)</option>
                            <option value="B2">B2 (Upper Intermediate)</option>
                            <option value="C1">C1 (Advanced)</option>
                        </select>

                        <input
                            type="text"
                            className="input"
                            placeholder={t('word_input_placeholder')}
                            value={word}
                            onChange={(e) => setWord(e.target.value)}
                        />

                        {error && <p style={{ color: 'var(--color-error)' }}>{error}</p>}

                        <button
                            className="btn btn-primary"
                            onClick={handleGenerate}
                            disabled={isLoading}
                        >
                            {isLoading ? t('loading') : t('generate_btn')}
                        </button>
                    </div>
                </div>
            ) : (
                <div className="story-container">
                    <button
                        onClick={() => setStory(null)}
                        className="btn"
                        style={{ marginBottom: '12px', background: 'rgba(255,255,255,0.1)' }}
                    >
                        ← Back
                    </button>

                    <div className="card">
                        <h3 style={{ color: 'var(--color-accent-primary)', marginBottom: '8px' }}>
                            {story.input_word} ({story.language_level})
                        </h3>
                        <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6', fontSize: '18px' }}>
                            {/* Render content with <b> tags */}
                            {story.content.split(/(<b>.*?<\/b>)/g).map((part: string, index: number) => {
                                if (part.startsWith('<b>') && part.endsWith('</b>')) {
                                    const cleanWord = part.replace(/<\/?b>/g, '');
                                    return (
                                        <span
                                            key={index}
                                            onClick={async () => {
                                                if (confirm(`Save "${cleanWord}" to vocabulary?`)) {
                                                    try {
                                                        const telegramId = WebApp.initDataUnsafe.user?.id || 123456789;
                                                        const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
                                                        await fetch(`${API_URL}/api/v1/words/`, {
                                                            method: 'POST',
                                                            headers: { 'Content-Type': 'application/json' },
                                                            body: JSON.stringify({
                                                                word: cleanWord,
                                                                context: story.content.replace(/<\/?b>/g, ''), // Store without tags
                                                                telegram_id: telegramId
                                                            })
                                                        });
                                                        alert("Saved!");
                                                    } catch (e) {
                                                        alert("Error saving");
                                                    }
                                                }
                                            }}
                                            style={{
                                                color: '#fbbf24',
                                                fontWeight: 'bold',
                                                textShadow: '0 0 5px rgba(251, 191, 36, 0.3)',
                                                cursor: 'pointer',
                                                borderBottom: '1px dashed #fbbf24'
                                            }}
                                        >
                                            {cleanWord}
                                        </span>
                                    );
                                }
                                return <span key={index}>{part}</span>;
                            })}
                        </div>

                        <AudioPlayer storyId={story.id} targetLang={story.target_language} />

                        {story.translation && (
                            <div style={{ marginTop: '20px', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '16px' }}>
                                <button
                                    className="btn btn-outline"
                                    style={{ width: '100%', marginBottom: '12px' }}
                                    onClick={() => setShowTranslation(!showTranslation)}
                                >
                                    {showTranslation ? t('hide_translation') : t('show_translation')}
                                </button>

                                {showTranslation && (
                                    <p style={{ color: 'var(--color-text-secondary)', fontStyle: 'italic', whiteSpace: 'pre-wrap' }}>
                                        {story.translation}
                                    </p>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Home;
