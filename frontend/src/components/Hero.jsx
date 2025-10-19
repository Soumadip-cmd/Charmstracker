import React from 'react';
import { Search, TrendingUp } from 'lucide-react';

export const Hero = () => {
  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section
      id="hero"
      className="relative pt-32 pb-24 lg:pt-40 lg:pb-32 overflow-hidden"
      style={{ background: '#f3f3f3' }}
    >
      {/* Background pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="grid grid-cols-6 gap-4 h-full p-8">
          {[...Array(24)].map((_, i) => (
            <div key={i} className="bg-[#bcbcbc] rounded-full aspect-square" />
          ))}
        </div>
      </div>

      <div className="max-w-[1400px] mx-auto px-6 lg:px-12 relative z-10">
        <div className="max-w-4xl mx-auto">
          {/* Main Headline */}
          <h1 className="hero-large text-center mb-6 animate-fade-in">
            Track the Real Market Value of Individual James Avery Charms
          </h1>

          {/* Subheadline */}
          <p className="body-large text-center mb-12 max-w-3xl mx-auto" style={{ color: '#666666' }}>
            CharmTracker aggregates prices for individual silver and gold charms from eBay, Poshmark, Etsy, and more — helping
            collectors discover true market value for single charm pieces instantly.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              onClick={() => scrollToSection('discover-market')}
              className="btn-primary group w-full sm:w-auto"
              style={{
                background: 'transparent',
                color: '#333333',
                border: '1px solid #333333',
                borderRadius: '0px',
                padding: '19px 23px',
                minWidth: '210px',
                height: '60px',
                fontSize: '14px',
                fontWeight: '700',
                cursor: 'pointer',
                textDecoration: 'none',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = '#333333';
                e.currentTarget.style.color = '#f3f3f3';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'transparent';
                e.currentTarget.style.color = '#333333';
              }}
            >
              <Search className="w-4 h-4" />
              Start Browsing
            </button>

            <button
              onClick={() => scrollToSection('discover-market')}
              className="btn-secondary group w-full sm:w-auto"
              style={{
                background: 'none',
                border: 'none',
                padding: '12px 16px',
                fontSize: '14px',
                fontWeight: '400',
                color: '#333333',
                cursor: 'pointer',
                textDecoration: 'none',
                position: 'relative',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px'
              }}
            >
              <TrendingUp className="w-4 h-4" />
              See Trending Charms
              <span
                className="absolute bottom-2 left-4 h-[1px] bg-[#333333] transition-slow"
                style={{ width: '0' }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.width = 'calc(100% - 32px)';
                }}
              />
            </button>
          </div>

          {/* Trust indicators */}
          <div className="mt-16 flex flex-wrap items-center justify-center gap-8 text-sm" style={{ color: '#666666' }}>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full" style={{ background: '#c9a94d' }} />
              <span>Updated Daily</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full" style={{ background: '#c9a94d' }} />
              <span>Multiple Marketplaces</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full" style={{ background: '#c9a94d' }} />
              <span>Real Sale Data</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};