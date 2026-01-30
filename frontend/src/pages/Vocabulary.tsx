import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import WebApp from '@twa-dev/sdk';

const Vocabulary: React.FC = () => {
    const { t } = useTranslation();
    const [words, setWords] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        fetchWords();
    }, []);

    const fetchWords = async () => {
        try {
            const telegramId = WebApp.initDataUnsafe.user?.id || 123456789;
            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

            const response = await fetch(`${API_URL}/api/v1/words/?telegram_id=${telegramId}`);
            if (response.ok) {
                const data = await response.json();
                setWords(data);
            }
        } catch (error) {
            console.error("Failed to fetch words", error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleDelete = async (wordId: number) => {
        if (!confirm("Delete word?")) return;

        try {
            const telegramId = WebApp.initDataUnsafe.user?.id || 123456789;
            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

            await fetch(`${API_URL}/api/v1/words/${wordId}?telegram_id=${telegramId}`, {
                method: 'DELETE'
            });

            setWords(words.filter(w => w.id !== wordId));
        } catch (error) {
            console.error("Failed to delete", error);
        }
    };

    return (
        <div className="container" style={{ paddingTop: '20px' }}>
            <h2 style={{ marginBottom: '20px', color: 'var(--color-accent-primary)' }}>{t('my_vocabulary')}</h2>

            {isLoading ? <p>{t('loading')}</p> : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    {words.length === 0 ? (
                        <p style={{ color: 'var(--color-text-secondary)' }}>No words saved yet.</p>
                    ) : words.map((w) => (
                        <div key={w.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <div>
                                <h3 style={{ fontSize: '18px', marginBottom: '4px' }}>{w.word}</h3>
                                {w.translation && <p style={{ color: 'var(--color-text-secondary)', fontSize: '14px' }}>{w.translation}</p>}
                                {w.context && <p style={{ color: 'var(--color-text-secondary)', fontSize: '12px', fontStyle: 'italic', marginTop: '4px' }}>"{w.context}"</p>}
                            </div>
                            <button
                                onClick={() => handleDelete(w.id)}
                                style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '18px' }}
                            >
                                🗑️
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Vocabulary;
