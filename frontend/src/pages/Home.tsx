import React from 'react';
import { useTranslation } from 'react-i18next';
import WebApp from '@twa-dev/sdk';

const Home: React.FC = () => {
    const { t } = useTranslation();
    const user = WebApp.initDataUnsafe.user;

    return (
        <div className="home-page">
            <header style={{ marginBottom: '24px' }}>
                <h1 style={{ fontSize: '28px', color: 'var(--color-accent-primary)' }}>
                    Contexta
                </h1>
                <p style={{ color: 'var(--color-text-secondary)' }}>
                    {t('welcome')}, {user?.first_name || 'Guest'}!
                </p>
            </header>

            <div className="card" style={{ marginBottom: '20px' }}>
                <h2 style={{ marginBottom: '12px' }}>{t('start_learning')}</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    <select className="input">
                        <option value="en">English (US)</option>
                        <option value="pt">Português (EU)</option>
                        <option value="es">Español</option>
                        <option value="pl">Polski</option>
                    </select>

                    <input
                        type="text"
                        className="input"
                        placeholder={t('word_input_placeholder')}
                    />

                    <button className="btn btn-primary">
                        {t('generate_btn')}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Home;
