import React from 'react';
import WebApp from '@twa-dev/sdk';

const Premium: React.FC = () => {

    const handleBuyPremium = () => {
        // Способ 2 (MVP): Просим пользователя написать /buy боту
        WebApp.close();
    };

    return (
        <div className="container" style={{ textAlign: 'center', paddingTop: '40px' }}>
            <div style={{ fontSize: '48px', marginBottom: '20px' }}>⭐</div>
            <h2 style={{ color: 'var(--color-accent-primary)', marginBottom: '10px' }}>Premium Access</h2>
            <p style={{ color: 'var(--color-text-secondary)', marginBottom: '30px' }}>
                Unlock unlimited stories, audio generation, and vocabulary storage.
            </p>

            <div className="card" style={{ marginBottom: '20px', border: '1px solid var(--color-accent-primary)' }}>
                <h3 style={{ fontSize: '24px' }}>1 Month</h3>
                <p style={{ fontSize: '32px', fontWeight: 'bold', margin: '10px 0' }}>50 ⭐</p>
                <p style={{ fontSize: '14px', color: 'var(--color-text-secondary)' }}>approx. $1.00</p>
            </div>

            <button
                className="btn btn-primary"
                onClick={handleBuyPremium}
            >
                Get Premium
            </button>

            <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', marginTop: '20px' }}>
                Tap button to close app and send /buy to bot
            </p>
        </div>
    );
};

export default Premium;
