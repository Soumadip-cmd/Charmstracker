import React, { useEffect, useState, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, TrendingUp, TrendingDown, Heart, ExternalLink, 
  RefreshCw, Clock, CheckCircle, AlertCircle 
} from 'lucide-react';
import { charmAPI, watchlistUtils, realtimeUtils } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export const CharmDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [charm, setCharm] = useState(null);
  const [relatedCharms, setRelatedCharms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [isInWatchlist, setIsInWatchlist] = useState(false);
  const [selectedImage, setSelectedImage] = useState(0);
  const [marketplaceStatus, setMarketplaceStatus] = useState(null);
  const [lastUpdateTime, setLastUpdateTime] = useState(null);

  useEffect(() => {
    fetchCharmDetail();
    
    // Auto-refresh every 30 seconds
    const cleanup = realtimeUtils.startAutoRefresh(
      id, 
      (data) => {
        setCharm(data);
        setLastUpdateTime(data.last_updated);
      },
      30000
    );
    
    return cleanup;
  }, [id]);

  useEffect(() => {
    if (charm) {
      setIsInWatchlist(watchlistUtils.isInWatchlist(charm.id));
      setLastUpdateTime(charm.last_updated);
    }
  }, [charm]);

  const fetchCharmDetail = async () => {
    try {
      setLoading(true);
      const data = await charmAPI.getCharmById(id);
      setCharm(data);

      // Fetch related charms
      if (data.related_charm_ids && data.related_charm_ids.length > 0) {
        const relatedPromises = data.related_charm_ids.slice(0, 4).map(relatedId =>
          charmAPI.getCharmById(relatedId).catch(() => null)
        );
        const related = await Promise.all(relatedPromises);
        setRelatedCharms(related.filter(c => c !== null));
      }

      // Check marketplace availability
      checkMarketplaceAvailability(data.name);
    } catch (error) {
      console.error('Error fetching charm detail:', error);
    } finally {
      setLoading(false);
    }
  };

  const checkMarketplaceAvailability = async (charmName) => {
    try {
      const status = await charmAPI.checkMarketplaceAvailability(charmName);
      setMarketplaceStatus(status);
    } catch (error) {
      console.error('Error checking marketplace:', error);
    }
  };

  const handleForceUpdate = async () => {
    try {
      setUpdating(true);
      await charmAPI.updateCharm(id);
      
      // Wait a few seconds then refresh
      setTimeout(async () => {
        await fetchCharmDetail();
        setUpdating(false);
      }, 3000);
    } catch (error) {
      console.error('Error updating charm:', error);
      setUpdating(false);
    }
  };

  const toggleWatchlist = () => {
    if (isInWatchlist) {
      watchlistUtils.removeFromWatchlist(charm.id);
      setIsInWatchlist(false);
    } else {
      watchlistUtils.addToWatchlist(charm.id);
      setIsInWatchlist(true);
    }
  };

  const chartData = useMemo(() => {
    if (!charm || !charm.price_history || charm.price_history.length === 0) return [];
    
    const last30Days = charm.price_history.slice(-30);
    
    return last30Days.map((entry, index) => {
      let dateStr = `Day ${index + 1}`;
      
      try {
        if (entry.date) {
          const date = new Date(entry.date);
          if (!isNaN(date.getTime())) {
            dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
          }
        }
      } catch (e) {
        // Use fallback
      }
      
      return {
        date: dateStr,
        price: Number(entry.price) || 0
      };
    });
  }, [charm]);

  const needsUpdate = charm ? realtimeUtils.needsRefresh(charm.last_updated, 30) : false;

  if (loading) {
    return (
      <div className="min-h-screen pt-24 pb-16" style={{ background: '#f3f3f3' }}>
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <div className="animate-pulse">
            <div className="h-96 bg-gray-200 mb-8" />
            <div className="h-8 bg-gray-200 w-1/3 mb-4" />
            <div className="h-4 bg-gray-200 w-2/3" />
          </div>
        </div>
      </div>
    );
  }

  if (!charm) {
    return (
      <div className="min-h-screen pt-24 pb-16" style={{ background: '#f3f3f3' }}>
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12 text-center">
          <h2 className="heading-1 mb-4">Charm Not Found</h2>
          <button
            onClick={() => navigate('/browse')}
            className="btn-primary"
            style={{
              background: 'transparent',
              color: '#333333',
              border: '1px solid #333333',
              borderRadius: '0px',
              padding: '19px 23px',
              minWidth: '210px',
              height: '60px'
            }}
          >
            Browse All Charms
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-24 pb-16" style={{ background: '#f3f3f3' }}>
      <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
        {/* Back Button */}
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 mb-8 body-regular transition-smooth hover:text-[#c9a94d]"
          style={{ color: '#666666' }}
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </button>

        {/* Update Status Bar */}
        <div className="mb-6 p-4 bg-white flex items-center justify-between" style={{ border: '1px solid #bcbcbc' }}>
          <div className="flex items-center gap-3">
            <Clock className="w-5 h-5" style={{ color: '#666666' }} />
            <span className="body-small" style={{ color: '#666666' }}>
              Last updated: {realtimeUtils.timeSinceUpdate(lastUpdateTime)}
            </span>
            {needsUpdate && (
              <span className="flex items-center gap-1 body-small" style={{ color: '#c9a94d' }}>
                <AlertCircle className="w-4 h-4" />
                Data may be outdated
              </span>
            )}
          </div>
          <button
            onClick={handleForceUpdate}
            disabled={updating}
            className="flex items-center gap-2 px-4 py-2 transition-smooth"
            style={{
              background: updating ? '#f3f3f3' : '#c9a94d',
              color: '#ffffff',
              border: 'none',
              borderRadius: '0px',
              opacity: updating ? 0.6 : 1,
              cursor: updating ? 'wait' : 'pointer'
            }}
          >
            <RefreshCw className={`w-4 h-4 ${updating ? 'animate-spin' : ''}`} />
            {updating ? 'Updating...' : 'Refresh Data'}
          </button>
        </div>

        {/* Marketplace Availability */}
        {marketplaceStatus && (
          <div className="mb-6 p-4 bg-white" style={{ border: '1px solid #bcbcbc' }}>
            <h3 className="heading-3 mb-3">Marketplace Availability</h3>
            <div className="grid grid-cols-3 gap-4">
              {Object.entries(marketplaceStatus.availability).map(([platform, status]) => (
                <div key={platform} className="flex items-center gap-2">
                  {status.available ? (
                    <CheckCircle className="w-5 h-5" style={{ color: '#2d8659' }} />
                  ) : (
                    <AlertCircle className="w-5 h-5" style={{ color: '#ba3e2b' }} />
                  )}
                  <div>
                    <p className="body-small font-semibold capitalize">{platform}</p>
                    <p className="text-xs" style={{ color: '#666666' }}>
                      {status.listing_count} listings
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">
          {/* Image Gallery */}
          <div>
            <div className="bg-white p-4 mb-4" style={{ border: 'none', borderRadius: '0px' }}>
              <img
                src={charm.images[selectedImage]}
                alt={charm.name}
                className="w-full h-96 object-cover"
              />
            </div>
            {charm.images.length > 1 && (
              <div className="grid grid-cols-4 gap-4">
                {charm.images.map((img, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedImage(index)}
                    className="transition-smooth"
                    style={{
                      border: selectedImage === index ? '2px solid #c9a94d' : '1px solid #bcbcbc',
                      borderRadius: '0px',
                      overflow: 'hidden'
                    }}
                  >
                    <img
                      src={img}
                      alt={`${charm.name} ${index + 1}`}
                      className="w-full h-20 object-cover"
                    />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Charm Details */}
          <div>
            <div className="flex items-start justify-between mb-4">
              <div>
                <h1 className="heading-1 mb-2">{charm.name}</h1>
                <div className="flex items-center gap-4 mb-4">
                  <span className="body-regular" style={{ color: '#666666' }}>
                    Material: {charm.material}
                  </span>
                  <span
                    className="px-3 py-1 text-sm"
                    style={{
                      background: charm.status === 'Retired' ? '#f6f5e8' : 'transparent',
                      border: `1px solid ${charm.status === 'Retired' ? '#bcbcbc' : '#c9a94d'}`,
                      borderRadius: '0px',
                      color: '#333333'
                    }}
                  >
                    {charm.status}
                  </span>
                </div>
              </div>
              <button
                onClick={toggleWatchlist}
                className="p-3 transition-smooth"
                style={{
                  background: isInWatchlist ? '#c9a94d' : 'transparent',
                  border: '1px solid #c9a94d',
                  borderRadius: '0px'
                }}
              >
                <Heart
                  className="w-6 h-6"
                  style={{ color: isInWatchlist ? '#ffffff' : '#c9a94d' }}
                  fill={isInWatchlist ? '#ffffff' : 'none'}
                />
              </button>
            </div>

            <div className="mb-6">
              <div className="flex items-baseline gap-4 mb-2">
                <span className="text-4xl font-semibold" style={{ color: '#333333' }}>
                  ${charm.avg_price.toFixed(2)}
                </span>
                <div
                  className="flex items-center gap-1 text-lg font-medium"
                  style={{ color: charm.price_change_7d >= 0 ? '#2d8659' : '#ba3e2b' }}
                >
                  {charm.price_change_7d >= 0 ? (
                    <TrendingUp className="w-5 h-5" />
                  ) : (
                    <TrendingDown className="w-5 h-5" />
                  )}
                  {Math.abs(charm.price_change_7d)}% (7d)
                </div>
              </div>
              <p className="body-small" style={{ color: '#666666' }}>
                Average market price from live listings
              </p>
            </div>

            <p className="body-regular mb-8" style={{ color: '#666666' }}>
              {charm.description}
            </p>

            {/* Price Changes */}
            <div className="grid grid-cols-3 gap-4 mb-8">
              <div className="p-4" style={{ background: '#ffffff', borderRadius: '0px' }}>
                <p className="body-small mb-1" style={{ color: '#666666' }}>
                  7 Days
                </p>
                <p
                  className="text-lg font-semibold"
                  style={{ color: charm.price_change_7d >= 0 ? '#2d8659' : '#ba3e2b' }}
                >
                  {charm.price_change_7d >= 0 ? '+' : ''}{charm.price_change_7d}%
                </p>
              </div>
              <div className="p-4" style={{ background: '#ffffff', borderRadius: '0px' }}>
                <p className="body-small mb-1" style={{ color: '#666666' }}>
                  30 Days
                </p>
                <p
                  className="text-lg font-semibold"
                  style={{ color: charm.price_change_30d >= 0 ? '#2d8659' : '#ba3e2b' }}
                >
                  {charm.price_change_30d >= 0 ? '+' : ''}{charm.price_change_30d}%
                </p>
              </div>
              <div className="p-4" style={{ background: '#ffffff', borderRadius: '0px' }}>
                <p className="body-small mb-1" style={{ color: '#666666' }}>
                  90 Days
                </p>
                <p
                  className="text-lg font-semibold"
                  style={{ color: charm.price_change_90d >= 0 ? '#2d8659' : '#ba3e2b' }}
                >
                  {charm.price_change_90d >= 0 ? '+' : ''}{charm.price_change_90d}%
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Price History Chart */}
        {charm && charm.price_history && charm.price_history.length > 0 && (
          <div className="mb-16 bg-white p-8" style={{ border: '2px solid #c9a94d', borderRadius: '0px' }}>
            <h2 className="heading-2 mb-6">Price History (Last 30 Days)</h2>
            <div style={{ width: '100%', height: '400px' }}>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart 
                  data={chartData}
                  margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Line 
                    type="monotone" 
                    dataKey="price" 
                    stroke="#c9a94d" 
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <p className="text-center mt-4 body-small" style={{ color: '#999999' }}>
              Real-time aggregated pricing from eBay, Etsy, Poshmark and more
            </p>
          </div>
        )}

        {/* Active Listings */}
        {charm.listings && charm.listings.length > 0 && (
          <div className="mb-16">
            <div className="flex items-center justify-between mb-6">
              <h2 className="heading-2">Active Listings ({charm.listings.length})</h2>
              <span className="body-small" style={{ color: '#666666' }}>
                Updated {realtimeUtils.timeSinceUpdate(charm.last_updated)}
              </span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {charm.listings.slice(0, 9).map((listing, index) => (
                <a
                  key={index}
                  href={listing.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-white p-6 transition-smooth hover:shadow-lg"
                  style={{ border: '1px solid #bcbcbc', borderRadius: '0px', textDecoration: 'none' }}
                >
                  <div className="flex items-center justify-between mb-3">
                    <span className="body-regular font-semibold" style={{ color: '#333333' }}>
                      {listing.platform}
                    </span>
                    <ExternalLink className="w-4 h-4" style={{ color: '#c9a94d' }} />
                  </div>
                  <div className="flex items-baseline gap-2 mb-2">
                    <span className="text-2xl font-semibold" style={{ color: '#333333' }}>
                      ${listing.price.toFixed(2)}
                    </span>
                    {listing.shipping > 0 && (
                      <span className="body-small" style={{ color: '#666666' }}>
                        +${listing.shipping} shipping
                      </span>
                    )}
                  </div>
                  <p className="body-small" style={{ color: '#666666' }}>
                    Condition: {listing.condition}
                  </p>
                  {listing.seller && (
                    <p className="body-small" style={{ color: '#999999' }}>
                      Seller: {listing.seller}
                    </p>
                  )}
                </a>
              ))}
            </div>
          </div>
        )}

        {/* Related Charms */}
        {relatedCharms.length > 0 && (
          <div>
            <h2 className="heading-2 mb-6">Related Charms</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {relatedCharms.map((relatedCharm) => (
                <button
                  key={relatedCharm.id}
                  onClick={() => navigate(`/charm/${relatedCharm.id}`)}
                  className="bg-white overflow-hidden transition-smooth hover:shadow-lg text-left"
                  style={{ border: 'none', borderRadius: '0px' }}
                >
                  <img
                    src={relatedCharm.images[0]}
                    alt={relatedCharm.name}
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-4">
                    <h3 className="heading-3 mb-2">{relatedCharm.name}</h3>
                    <p className="text-lg font-semibold" style={{ color: '#333333' }}>
                      ${relatedCharm.avg_price.toFixed(2)}
                    </p>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};