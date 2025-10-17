import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TrendingUp, TrendingDown, ArrowRight } from 'lucide-react';
import { charmAPI } from '../services/api';

export const MarketDataTable = () => {
  const navigate = useNavigate();
  const [charms, setCharms] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMarketData();
  }, []);

  const fetchMarketData = async () => {
    try {
      setLoading(true);
      const data = await charmAPI.getAllCharms({
        page: 1,
        limit: 20,
        sort: 'popularity'
      });
      setCharms(data.charms || []);
    } catch (error) {
      console.error('Error fetching market data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <section className="py-24 lg:py-32 bg-white">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="max-w-3xl mx-auto text-center mb-16">
            <h2 className="heading-1 mb-6">Live Market Data</h2>
            <p className="body-regular" style={{ color: '#666666' }}>
              Real-time pricing and trends from trusted marketplaces across the web.
            </p>
          </div>
          <div className="animate-pulse">
            <div className="h-12 bg-gray-200 mb-4" style={{ borderRadius: '0px' }} />
            {[...Array(10)].map((_, i) => (
              <div key={i} className="h-16 bg-gray-100 mb-2" style={{ borderRadius: '0px' }} />
            ))}
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-24 lg:py-32 bg-white">
      <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
        {/* Section Header */}
        <div className="max-w-3xl mx-auto text-center mb-16">
          <h2 className="heading-1 mb-6">Live Market Data</h2>
          <p className="body-regular" style={{ color: '#666666' }}>
            Real-time pricing and trends from trusted marketplaces across the web.
          </p>
        </div>

        {/* Table Container - Horizontal scroll on mobile */}
        <div className="overflow-x-auto mb-12" style={{ 
          border: '1px solid #e5e5e5',
          borderRadius: '0px'
        }}>
          <table className="w-full min-w-[900px]">
            {/* Table Header */}
            <thead>
              <tr style={{ background: '#f9f9f9', borderBottom: '2px solid #e5e5e5' }}>
                <th className="text-left px-6 py-4 body-small font-semibold" style={{ color: '#333333', width: '80px' }}>
                  Image
                </th>
                <th className="text-left px-6 py-4 body-small font-semibold" style={{ color: '#333333' }}>
                  Name
                </th>
                <th className="text-left px-6 py-4 body-small font-semibold" style={{ color: '#333333', width: '120px' }}>
                  Avg Price
                </th>
                <th className="text-left px-6 py-4 body-small font-semibold" style={{ color: '#333333', width: '120px' }}>
                  7d Change
                </th>
                <th className="text-left px-6 py-4 body-small font-semibold" style={{ color: '#333333', width: '120px' }}>
                  Status
                </th>
                <th className="text-left px-6 py-4 body-small font-semibold" style={{ color: '#333333', width: '120px' }}>
                  Material
                </th>
                <th className="text-right px-6 py-4 body-small font-semibold" style={{ color: '#333333', width: '100px' }}>
                  Popularity
                </th>
              </tr>
            </thead>

            {/* Table Body */}
            <tbody>
              {charms.map((charm, index) => (
                <tr
                  key={charm.id}
                  onClick={() => navigate(`/charm/${charm.id}`)}
                  className="cursor-pointer transition-smooth hover:bg-gray-50"
                  style={{ 
                    borderBottom: index < charms.length - 1 ? '1px solid #e5e5e5' : 'none'
                  }}
                >
                  {/* Thumbnail */}
                  <td className="px-6 py-4">
                    <div className="w-14 h-14 overflow-hidden" style={{ borderRadius: '0px' }}>
                      <img
                        src={charm.images[0]}
                        alt={charm.name}
                        className="w-full h-full object-cover"
                      />
                    </div>
                  </td>

                  {/* Name */}
                  <td className="px-6 py-4">
                    <span className="body-regular font-medium" style={{ color: '#333333' }}>
                      {charm.name}
                    </span>
                  </td>

                  {/* Avg Price */}
                  <td className="px-6 py-4">
                    <span className="text-lg font-semibold" style={{ color: '#333333' }}>
                      ${charm.avg_price.toFixed(2)}
                    </span>
                  </td>

                  {/* 7d Change */}
                  <td className="px-6 py-4">
                    <div
                      className="inline-flex items-center gap-1 px-3 py-1.5 body-small font-medium"
                      style={{
                        background: charm.price_change_7d >= 0 ? '#e8f5e9' : '#ffebee',
                        color: charm.price_change_7d >= 0 ? '#2d8659' : '#ba3e2b',
                        borderRadius: '0px'
                      }}
                    >
                      {charm.price_change_7d >= 0 ? (
                        <TrendingUp className="w-4 h-4" />
                      ) : (
                        <TrendingDown className="w-4 h-4" />
                      )}
                      {Math.abs(charm.price_change_7d).toFixed(1)}%
                    </div>
                  </td>

                  {/* Status */}
                  <td className="px-6 py-4">
                    <span
                      className="inline-block px-3 py-1.5 body-small font-medium"
                      style={{
                        background: charm.status === 'Retired' ? '#f6f5e8' : 'transparent',
                        border: `1px solid ${charm.status === 'Retired' ? '#bcbcbc' : '#c9a94d'}`,
                        color: '#333333',
                        borderRadius: '0px'
                      }}
                    >
                      {charm.status}
                    </span>
                  </td>

                  {/* Material */}
                  <td className="px-6 py-4">
                    <span className="body-regular" style={{ color: '#666666' }}>
                      {charm.material}
                    </span>
                  </td>

                  {/* Popularity */}
                  <td className="px-6 py-4 text-right">
                    <div className="inline-flex items-center gap-2">
                      <div 
                        className="h-2 bg-gray-200 relative overflow-hidden" 
                        style={{ width: '60px', borderRadius: '0px' }}
                      >
                        <div
                          className="h-full transition-all"
                          style={{
                            width: `${charm.popularity}%`,
                            background: charm.popularity >= 80 ? '#c9a94d' : charm.popularity >= 50 ? '#bcbcbc' : '#e5e5e5'
                          }}
                        />
                      </div>
                      <span className="body-small font-medium" style={{ color: '#666666' }}>
                        {charm.popularity}
                      </span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Mobile Scroll Hint */}
        <p className="text-center mb-8 body-small lg:hidden" style={{ color: '#999999' }}>
          ← Scroll horizontally to view all columns →
        </p>

        {/* See All Button */}
        <div className="flex justify-center">
          <button
            onClick={() => navigate('/browse')}
            className="group inline-flex items-center gap-3 px-8 py-4 transition-smooth"
            style={{
              background: 'transparent',
              border: '2px solid #333333',
              borderRadius: '0px',
              color: '#333333',
              fontSize: '16px',
              fontWeight: '500',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#333333';
              e.currentTarget.style.color = '#ffffff';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent';
              e.currentTarget.style.color = '#333333';
            }}
          >
            See All Market Data
            <ArrowRight className="w-5 h-5 transition-smooth group-hover:translate-x-1" />
          </button>
        </div>
      </div>
    </section>
  );
};
