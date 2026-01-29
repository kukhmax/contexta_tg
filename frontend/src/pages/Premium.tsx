import React from 'react';
import { useTranslation } from 'react-i18next';
import WebApp from '@twa-dev/sdk';

const Premium: React.FC = () => {
    const { t } = useTranslation();

    // В продакшене лучше получать статус подписки с бэкенда
    const user = WebApp.initDataUnsafe.user;

    const handleBuyPremium = () => {
        // Открываем инвойс через WebApp API
        // В реальном приложении мы бы сначала получили ссылку на инвойс от нашего бота 
        // через API бэкенда (createInvoiceLink), но для простоты можно использовать 
        // механику "напиши боту команду" или если бот умеет генерировать ссылку.

        // Способ 1: Прямое открытие инвойса (если есть ссылка)
        // WebApp.openInvoice(invoiceLink, (status) => { ... });

        // Способ 2 (MVP): Просим пользователя написать /buy боту, так как генерация ссылки требует бэкенда бота
        // Но WebApp умеет отправлять данные боту.

        // Лучший UX для Stars: WebApp.openInvoice, но нужна ссылка.
        // Ссылку генерирует бот методом createInvoiceLink.
        // Эндпоинта у нас пока нет для этого, бот только обрабатывает /buy.

        // Давайте попросим пользователя нажать кнопку в боте или реализуем эндпоинт генерации ссылки.
        // Для MVP проще всего закрыть WebApp и отправить команду.

        WebApp.close();
        // В идеале мы бы сделали API endpoint: POST /api/v1/payments/create-invoice -> returns link
        // Затем WebApp.openInvoice(link)
    };

    // Давайте лучше реализуем правильный флоу с openInvoice?
    // У нас нет эндпоинта API для генерации ссылки. 
    // Я добавлю простую заглушку пока.

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
                onClick={() => {
                    // Пока просто алерт, так как нужно получить ссылку от бота
                    alert("Please send /buy command to the bot to purchase!");
                    // Или можно использовать switchInlineQuery если бот поддерживает
                }}
            >
                Get Premium
            </button>

            <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', marginTop: '20px' }}>
                To buy stars, use Telegram's internal currency.
            </p>
        </div>
    );
};

export default Premium;
