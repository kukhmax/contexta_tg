import React, { useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import WebApp from '@twa-dev/sdk';

const Layout: React.FC = () => {
    const { i18n } = useTranslation();
    const navigate = useNavigate();

    useEffect(() => {
        // Инициализация Telegram WebApp
        WebApp.ready();
        WebApp.expand();

        // Установка цвета хедера
        const color = getComputedStyle(document.documentElement).getPropertyValue('--color-bg-primary').trim();
        if (color) {
            WebApp.setHeaderColor(color as any);
        } else {
            WebApp.setHeaderColor('#0F0F13');
        }

        // Адаптация языка приложения под язык Telegram
        if (WebApp.initDataUnsafe.user?.language_code === 'en') {
            i18n.changeLanguage('en');
        }
    }, [i18n]);

    return (
        <div className="app-wrapper">
            <main className="container" style={{ flex: 1, paddingBottom: '80px' }}>
                <Outlet />
            </main>

            {/* Нижняя навигация (простая реализация) */}
            <nav style={{
                position: 'fixed',
                bottom: 0,
                left: 0,
                right: 0,
                backgroundColor: 'var(--color-bg-secondary)',
                padding: '12px',
                display: 'flex',
                justifyContent: 'space-around',
                borderTop: '1px solid rgba(255,255,255,0.05)',
                zIndex: 100
            }}>
                <button onClick={() => navigate('/')} style={{ background: 'none', border: 'none', color: 'var(--color-text-primary)' }}>
                    🏠
                </button>
                <button onClick={() => navigate('/history')} style={{ background: 'none', border: 'none', color: 'var(--color-text-primary)' }}>
                    📜
                </button>
                <button onClick={() => navigate('/profile')} style={{ background: 'none', border: 'none', color: 'var(--color-text-primary)' }}>
                    👤
                </button>
            </nav>
        </div>
    );
};

export default Layout;
