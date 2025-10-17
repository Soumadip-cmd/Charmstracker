import React from 'react';
import { Brain, Zap, Gem, ArrowRight } from 'lucide-react';
import { collectorReasons } from '../mockData';

const iconMap = {
  Brain: Brain,
  Zap: Zap,
  Gem: Gem
};

export const WhyCollectors = () => {
  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section
      id="why-collectors"
      className="py-24 lg:py-32"
      style={{ background: '#ffffff' }}
    >
      <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
        {/* Section Header */}
        <div className="max-w-3xl mx-auto text-center mb-16">
          <h2 className="heading-1 mb-6">
            Built for Accuracy, Speed, and Simplicity
          </h2>
          <p className="body-large" style={{ color: '#666666' }}>
            No logins, no ads, no noise — just clean data, quick search, and clear
            insight into the real charm market. Whether you're hunting for a rare
            retired piece or pricing a collection to sell, CharmTracker gives you a
            collector's edge.
          </p>
        </div>

        {/* Reasons Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 lg:gap-12 mb-12">
          {collectorReasons.map((reason, index) => {
            const IconComponent = iconMap[reason.icon];
            return (
              <div key={index} className="text-center">
                <div
                  className="w-16 h-16 mx-auto mb-6 flex items-center justify-center"
                  style={{
                    background: '#f6f5e8',
                    border: '1px solid #c9a94d',
                    borderRadius: '0px'
                  }}
                >
                  <IconComponent className="w-8 h-8" style={{ color: '#c9a94d' }} />
                </div>
                <h3 className="heading-3 mb-3">{reason.title}</h3>
                <p className="body-regular" style={{ color: '#666666' }}>
                  {reason.description}
                </p>
              </div>
            );
          })}
        </div>

        {/* CTA Button */}
        <div className="flex justify-center">
          <button
            onClick={() => scrollToSection('discover-market')}
            className="btn-primary group"
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
            Start Browsing Now
            <ArrowRight className="w-4 h-4 transition-smooth group-hover:translate-x-1" />
          </button>
        </div>
      </div>
    </section>
  );
};