import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, TrendingUp, TrendingDown } from 'lucide-react';
import { charmAPI } from '../services/api';

export const DiscoverMarket = () => {
  const navigate = useNavigate();
  const [trendingCharms, setTrendingCharms] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTrendingCharms();
  }, []);

  const fetchTrendingCharms = async () => {
    try {
      setLoading(true);
      const data = await charmAPI.getTrending();
      setTrendingCharms(data.trending);
    } catch (error) {
      console.error('Error fetching trending charms:', error);
    } finally {
      setLoading(false);
    }
  };

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  if (loading) {
    return (
      <section
        id="discover-market"
        className="py-24 lg:py-32"
        style={{ background: '#f3f3f3' }}
      >
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="max-w-3xl mx-auto text-center mb-16">
            <h2 className="heading-1 mb-6">
              Find Out What's Trending Among Collectors
            </h2>
            <p className="body-regular" style={{ color: '#666666' }}>
              Stay ahead of the market with insights showing which charms are climbing
              in value and which are cooling off.
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="animate-pulse bg-white" style={{ borderRadius: '0px' }}>
                <div className="h-64 bg-gray-200" />
                <div className="p-6">
                  <div className="h-4 bg-gray-200 mb-3" />
                  <div className="h-6 bg-gray-200 mb-2" />
                  <div className="h-4 bg-gray-200" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    );
  }

  return (
    <section
      id="discover-market"
      className="py-24 lg:py-32"
      style={{ background: '#f3f3f3' }}
    >
      <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
        {/* Section Header */}
        <div className="max-w-3xl mx-auto text-center mb-16">
          <h2 className="heading-1 mb-6">
            Find Out What's Trending Among Collectors
          </h2>
          <p className="body-regular" style={{ color: '#666666' }}>
            Stay ahead of the market with insights showing which charms are climbing
            in value and which are cooling off.
          </p>
        </div>

        {/* Trending Charms Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8 mb-12">
          {trendingCharms.map((charm) => (
            <button
              key={charm.id}
              onClick={() => navigate(`/charm/${charm.id}`)}
              className="bg-white overflow-hidden transition-smooth cursor-pointer group text-left"
              style={{
                border: 'none',
                borderRadius: '0px'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px)';
                e.currentTarget.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.12)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              {/* Image */}
              <div className="w-full h-64 overflow-hidden">
                <img
                  src={charm.image}
                  alt={charm.name}
                  className="w-full h-full object-cover transition-smooth group-hover:scale-105"
                />
              </div>

              {/* Content */}
              <div className="p-6">
                <h3 className="heading-3 mb-2">{charm.name}</h3>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-2xl font-semibold" style={{ color: '#333333' }}>
                    ${charm.avg_price.toFixed(2)}
                  </span>
                  <div
                    className="flex items-center gap-1 text-sm font-medium"
                    style={{
                      color: charm.price_change >= 0 ? '#2d8659' : '#ba3e2b'
                    }}
                  >
                    {charm.price_change >= 0 ? (
                      <TrendingUp className="w-4 h-4" />
                    ) : (
                      <TrendingDown className="w-4 h-4" />
                    )}
                    {Math.abs(charm.price_change)}%
                  </div>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span style={{ color: '#666666' }}>Material: {charm.material}</span>
                  <span
                    className="px-3 py-1"
                    style={{
                      background: charm.status === 'Retired' ? '#f6f5e8' : 'transparent',
                      border: `1px solid ${charm.status === 'Retired' ? '#bcbcbc' : '#c9a94d'}`,
                      color: '#333333',
                      fontSize: '12px',
                      borderRadius: '0px'
                    }}
                  >
                    {charm.status}
                  </span>
                </div>
              </div>
            </button>
          ))}
        </div>

        {/* CTA Button */}
        <div className="flex justify-center">
          <button
            onClick={() => navigate('/browse')}
            className="group inline-flex items-center gap-2"
            style={{
              background: 'none',
              border: 'none',
              padding: '12px 0',
              fontSize: '16px',
              fontWeight: '400',
              color: '#333333',
              cursor: 'pointer',
              textDecoration: 'none',
              position: 'relative'
            }}
          >
            Explore Full Market
            <ArrowRight
              className="w-5 h-5 transition-smooth group-hover:translate-x-1"
              style={{ color: '#c9a94d' }}
            />
          </button>
        </div>
      </div>
    </section>
  );
};