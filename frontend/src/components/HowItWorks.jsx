import React from 'react';
import { TrendingUp, Search, Clock, Activity } from 'lucide-react';
import { features } from '../mockData';

const iconMap = {
  TrendingUp: TrendingUp,
  Search: Search,
  Clock: Clock,
  Activity: Activity
};

export const HowItWorks = () => {
  return (
    <section
      id="how-it-works"
      className="py-24 lg:py-32"
      style={{ background: '#ffffff' }}
    >
      <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
        {/* Section Header */}
        <div className="max-w-3xl mx-auto text-center mb-16">
          <h2 className="heading-1 mb-6">
            Real Market Data — Updated Daily
          </h2>
          <p className="body-regular" style={{ color: '#666666' }}>
            CharmTracker pulls pricing and listing data from trusted marketplaces
            every few hours. Each charm's page shows an average price based on sold
            listings, not just what sellers are asking.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-12">
          {features.map((feature, index) => {
            const IconComponent = iconMap[feature.icon];
            return (
              <div
                key={index}
                className="bg-white p-8 transition-smooth hover:shadow-lg"
                style={{
                  border: '1px solid #bcbcbc',
                  borderRadius: '0px'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = '#c9a94d';
                  e.currentTarget.style.transform = 'translateY(-2px)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = '#bcbcbc';
                  e.currentTarget.style.transform = 'translateY(0)';
                }}
              >
                <div
                  className="w-12 h-12 mb-6 flex items-center justify-center"
                  style={{
                    background: '#f6f5e8',
                    border: '1px solid #bcbcbc',
                    borderRadius: '0px'
                  }}
                >
                  <IconComponent className="w-6 h-6" style={{ color: '#c9a94d' }} />
                </div>
                <h3 className="heading-3 mb-3">{feature.title}</h3>
                <p className="body-regular" style={{ color: '#666666' }}>
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};