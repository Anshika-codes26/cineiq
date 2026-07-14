'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Play, Info } from 'lucide-react';
import Link from 'next/link';
import Image from 'next/image';

// Mock data
const heroMovie = {
  id: '1',
  title: 'Dune: Part Two',
  overview: 'Paul Atreides unites with Chani and the Fremen while on a warpath of revenge against the conspirators who destroyed his family.',
  backdrop: 'https://image.tmdb.org/t/p/original/8rpDcsfLJypbO6vtecsmHLsC88C.jpg',
  match: '98% Match'
};

const trendingMovies = [
  { id: '1', title: 'Dune: Part Two', poster: 'https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2JGqpTd4p.jpg' },
  { id: '2', title: 'Oppenheimer', poster: 'https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg' },
  { id: '3', title: 'Poor Things', poster: 'https://image.tmdb.org/t/p/w500/kCGlIMHnOm8PhcbTi03XQ5VGe1T.jpg' },
  { id: '4', title: 'Interstellar', poster: 'https://image.tmdb.org/t/p/w500/gEU2QlsE1ZEbKU01E8XgK31rGfQ.jpg' },
  { id: '5', title: 'Inception', poster: 'https://image.tmdb.org/t/p/w500/oYuLEt3zVCKqA3F0B7I2G0kE7Y.jpg' },
  { id: '6', title: 'Arrival', poster: 'https://image.tmdb.org/t/p/w500/x2FJsf1ElAgr63Y3PNPtJrcmpoe.jpg' }
];

export default function HomePage() {
  const [typedText, setTypedText] = useState('');
  const fullText = "Discover films that match your soul.";

  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      if (i <= fullText.length) {
        setTypedText(fullText.slice(0, i));
        i++;
      } else {
        clearInterval(interval);
      }
    }, 50);
    return () => clearInterval(interval);
  }, []);

  return (
    <main>
      {/* Hero Section */}
      <section className="hero-section">
        {/* Background Image & Gradient */}
        <div style={{
          position: 'absolute', inset: 0, zIndex: -1,
          backgroundImage: `url(${heroMovie.backdrop})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
        }} />
        <div style={{
          position: 'absolute', inset: 0, zIndex: -1,
          background: 'linear-gradient(to right, #05050A 20%, transparent 60%), linear-gradient(to top, #05050A 0%, transparent 30%)'
        }} />

        {/* Hero Content */}
        <div className="hero-content">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div style={{ color: 'var(--accent-primary)', fontWeight: 700, letterSpacing: '2px', marginBottom: '16px', fontSize: '14px' }}>
              CINEIQ PREMIERE
            </div>
            <h1 className="hero-title">
              {heroMovie.title}
            </h1>
            
            {/* Typewriter Effect */}
            <div style={{ fontSize: '18px', color: 'var(--text-secondary)', marginBottom: '8px', minHeight: '28px' }}>
              {typedText}<span style={{ opacity: 0.5 }}>|</span>
            </div>
            
            <p style={{ fontSize: '16px', color: '#D4D4D8', marginBottom: '32px', lineHeight: 1.6, textShadow: '0 2px 10px rgba(0,0,0,0.5)' }}>
              {heroMovie.overview}
            </p>

            <div className="hero-buttons">
              <button className="btn btn-primary" style={{ padding: '14px 32px', fontSize: '16px' }}>
                <Play size={20} fill="currentColor" /> Play Now
              </button>
              <button className="btn btn-glass" style={{ padding: '14px 32px', fontSize: '16px' }}>
                <Info size={20} /> More Info
              </button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Rows */}
      <section className="trending-section">
        <h3 style={{ fontSize: '24px', marginBottom: '20px' }}>Top Picks for You</h3>
        <div style={{ display: 'flex', gap: '16px', overflowX: 'auto', paddingBottom: '32px' }}>
          {trendingMovies.map((movie, i) => (
            <motion.div
              key={movie.id}
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1, duration: 0.5 }}
              style={{ flex: '0 0 auto', width: '220px' }}
            >
              <Link href={`/movie/${movie.id}`}>
                <div className="movie-card">
                  <Image src={movie.poster} alt={movie.title} className="movie-poster" width={220} height={330} />
                  <div className="movie-overlay">
                    <div className="movie-title">{movie.title}</div>
                    <div className="movie-meta">
                      <span style={{ color: '#22C55E', fontWeight: 600 }}>98% Match</span>
                      <span>2024</span>
                    </div>
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      </section>
    </main>
  );
}
