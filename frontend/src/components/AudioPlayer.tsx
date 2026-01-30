import React, { useState, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import WebApp from '@twa-dev/sdk';

interface AudioPlayerProps {
    storyId: number;
    targetLang: string; // используется чтобы показать язык
}

const AudioPlayer: React.FC<AudioPlayerProps> = ({ storyId }) => {
    const { t } = useTranslation();
    const [isPlaying, setIsPlaying] = useState(false);
    const audioRef = useRef<HTMLAudioElement | null>(null);
    const [audioSrc, setAudioSrc] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    const togglePlay = async () => {
        if (!audioSrc) {
            // First time play: fetch audio
            setIsLoading(true);
            try {
                const telegramId = WebApp.initDataUnsafe.user?.id || 123456789;
                const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

                // Используем blob для воспроизведения
                const response = await fetch(`${API_URL}/api/v1/stories/${storyId}/audio?telegram_id=${telegramId}`);
                if (!response.ok) throw new Error("Audio fetch failed");

                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                setAudioSrc(url);

                // Небольшая задержка чтобы стейт обновился и элемент создался (если бы он был условным)
                setTimeout(() => {
                    if (audioRef.current) {
                        audioRef.current.play();
                        setIsPlaying(true);
                    }
                }, 100);
            } catch (error) {
                console.error("Audio error:", error);
                alert("Failed to load audio");
            } finally {
                setIsLoading(false);
            }
        } else {
            // Just toggle
            if (audioRef.current) {
                if (isPlaying) {
                    audioRef.current.pause();
                } else {
                    audioRef.current.play();
                }
                setIsPlaying(!isPlaying);
            }
        }
    };

    return (
        <div style={{ marginTop: '16px', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <button
                className="btn btn-primary"
                onClick={togglePlay}
                style={{ width: 'auto', padding: '8px 16px', fontSize: '14px', borderRadius: '20px' }}
                disabled={isLoading}
            >
                {isLoading ? '⏳ ...' : (isPlaying ? '⏸ Pause' : `▶️ ${t('listen')}`)}
            </button>

            {audioSrc && (
                <audio
                    ref={audioRef}
                    src={audioSrc}
                    onEnded={() => setIsPlaying(false)}
                    onPause={() => setIsPlaying(false)}
                    onPlay={() => setIsPlaying(true)}
                    style={{ display: 'none' }}
                />
            )}
        </div>
    );
};

export default AudioPlayer;
