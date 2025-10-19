import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, TrendingUp, TrendingDown, Filter, X } from 'lucide-react';
import { charmAPI } from '../services/api';

export const Browse = () => {
  const navigate = useNavigate();
  const [charms, setCharms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    sort: 'popularity',
    material: '',
    status: '',
    minPrice: '',
    maxPrice: ''
  });
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 12,
    total: 0,
    totalPages: 0
  });
  const [searchTerm, setSearchTerm] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    fetchCharms();
  }, [filters, pagination.page]);

  const fetchCharms = async () => {
    try {
      setLoading(true);
      const params = {
        ...filters,
        page: pagination.page,
        limit: pagination.limit,
        min_price: filters.minPrice || undefined,
        max_price: filters.maxPrice || undefined
      };
      
      // Remove empty filters
      Object.keys(params).forEach(key => {
        if (params[key] === '' || params[key] === undefined) {
          delete params[key];
        }
      });

      const data = await charmAPI.getAllCharms(params);
      setCharms(data.charms);
      setPagination(prev => ({
        ...prev,
        total: data.total,
        totalPages: data.total_pages
      }));
    } catch (error) {
      console.error('Error fetching charms:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const clearFilters = () => {
    setFilters({
      sort: 'popularity',
      material: '',
      status: '',
      minPrice: '',
      maxPrice: ''
    });
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const filteredCharms = charms.filter(charm =>
    charm.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const hasActiveFilters = filters.material || filters.status || filters.minPrice || filters.maxPrice;

  return (
    <div className="min-h-screen pt-24 pb-16" style={{ background: '#f3f3f3' }}>
      <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
        {/* Header */}
        <div className="mb-12">
          <h1 className="heading-1 mb-4">Browse All Charms</h1>
          <p className="body-regular" style={{ color: '#666666' }}>
            Explore our complete collection of James Avery charms with real-time market data.
          </p>
        </div>

        {/* Search and Filters */}
        <div className="mb-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-4">
            {/* Search */}
            <div className="lg:col-span-2 relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5" style={{ color: '#666666' }} />
              <input
                type="text"
                placeholder="Search charms by name..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full h-14 pl-12 pr-4 body-regular"
                style={{
                  background: '#ffffff',
                  border: '1px solid #bcbcbc',
                  borderRadius: '0px',
                  outline: 'none'
                }}
              />
            </div>

            {/* Sort */}
            <select
              value={filters.sort}
              onChange={(e) => handleFilterChange('sort', e.target.value)}
              className="h-14 px-4 body-regular cursor-pointer"
              style={{
                background: '#ffffff',
                border: '1px solid #bcbcbc',
                borderRadius: '0px',
                outline: 'none'
              }}
            >
              <option value="popularity">Most Popular</option>
              <option value="price_asc">Price: Low to High</option>
              <option value="price_desc">Price: High to Low</option>
              <option value="name">Name: A to Z</option>
            </select>
          </div>

          {/* Filter Toggle Button */}
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center gap-2 px-4 py-2 transition-smooth"
            style={{
              background: showFilters ? '#c9a94d' : 'transparent',
              border: '1px solid #c9a94d',
              borderRadius: '0px',
              color: showFilters ? '#ffffff' : '#333333'
            }}
          >
            <Filter className="w-4 h-4" />
            {showFilters ? 'Hide Filters' : 'Show Filters'}
            {hasActiveFilters && !showFilters && (
              <span className="ml-2 px-2 py-0.5 text-xs" style={{ background: '#c9a94d', color: '#ffffff' }}>
                Active
              </span>
            )}
          </button>

          {/* Filters Panel */}
          {showFilters && (
            <div className="mt-4 p-6 bg-white" style={{ border: '1px solid #bcbcbc', borderRadius: '0px' }}>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                {/* Material Filter */}
                <div>
                  <label className="body-small font-semibold mb-2 block" style={{ color: '#333333' }}>
                    Material
                  </label>
                  <select
                    value={filters.material}
                    onChange={(e) => handleFilterChange('material', e.target.value)}
                    className="w-full h-10 px-3 body-small"
                    style={{
                      background: '#ffffff',
                      border: '1px solid #bcbcbc',
                      borderRadius: '0px',
                      outline: 'none'
                    }}
                  >
                    <option value="">All Materials</option>
                    <option value="Silver">Silver</option>
                    <option value="Gold">Gold</option>
                  </select>
                </div>

                {/* Status Filter */}
                <div>
                  <label className="body-small font-semibold mb-2 block" style={{ color: '#333333' }}>
                    Status
                  </label>
                  <select
                    value={filters.status}
                    onChange={(e) => handleFilterChange('status', e.target.value)}
                    className="w-full h-10 px-3 body-small"
                    style={{
                      background: '#ffffff',
                      border: '1px solid #bcbcbc',
                      borderRadius: '0px',
                      outline: 'none'
                    }}
                  >
                    <option value="">All Status</option>
                    <option value="Active">Active</option>
                    <option value="Retired">Retired</option>
                  </select>
                </div>

                {/* Min Price */}
                <div>
                  <label className="body-small font-semibold mb-2 block" style={{ color: '#333333' }}>
                    Min Price ($)
                  </label>
                  <input
                    type="number"
                    placeholder="0"
                    value={filters.minPrice}
                    onChange={(e) => handleFilterChange('minPrice', e.target.value)}
                    className="w-full h-10 px-3 body-small"
                    style={{
                      background: '#ffffff',
                      border: '1px solid #bcbcbc',
                      borderRadius: '0px',
                      outline: 'none'
                    }}
                  />
                </div>

                {/* Max Price */}
                <div>
                  <label className="body-small font-semibold mb-2 block" style={{ color: '#333333' }}>
                    Max Price ($)
                  </label>
                  <input
                    type="number"
                    placeholder="500"
                    value={filters.maxPrice}
                    onChange={(e) => handleFilterChange('maxPrice', e.target.value)}
                    className="w-full h-10 px-3 body-small"
                    style={{
                      background: '#ffffff',
                      border: '1px solid #bcbcbc',
                      borderRadius: '0px',
                      outline: 'none'
                    }}
                  />
                </div>
              </div>

              {/* Clear Filters */}
              {hasActiveFilters && (
                <button
                  onClick={clearFilters}
                  className="mt-4 flex items-center gap-2 px-4 py-2 transition-smooth"
                  style={{
                    background: 'transparent',
                    border: '1px solid #ba3e2b',
                    borderRadius: '0px',
                    color: '#ba3e2b'
                  }}
                >
                  <X className="w-4 h-4" />
                  Clear All Filters
                </button>
              )}
            </div>
          )}
        </div>

        {/* Results Count */}
        <div className="mb-6">
          <p className="body-regular" style={{ color: '#666666' }}>
            Showing {filteredCharms.length} of {pagination.total} charms
          </p>
        </div>

        {/* Charms Grid */}
        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="animate-pulse bg-white" style={{ borderRadius: '0px' }}>
                <div className="h-64 bg-gray-200" />
                <div className="p-4">
                  <div className="h-4 bg-gray-200 mb-2" />
                  <div className="h-6 bg-gray-200" />
                </div>
              </div>
            ))}
          </div>
        ) : filteredCharms.length === 0 ? (
          <div className="text-center py-16">
            <p className="heading-2 mb-4">No charms found</p>
            <p className="body-regular" style={{ color: '#666666' }}>
              Try adjusting your filters or search term
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-12">
            {filteredCharms.map((charm) => (
              <button
                key={charm.id}
                onClick={() => navigate(`/charm/${charm.id}`)}
                className="bg-white overflow-hidden transition-smooth hover:shadow-lg text-left"
                style={{ border: 'none', borderRadius: '0px' }}
              >
                <div className="w-full h-64 overflow-hidden">
                  <img
                    src={charm.images[0]}
                    alt={charm.name}
                    className="w-full h-full object-cover transition-smooth hover:scale-105"
                  />
                </div>
                <div className="p-4">
                  <h3 className="heading-3 mb-2 line-clamp-1">{charm.name}</h3>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xl font-semibold" style={{ color: '#333333' }}>
                      ${charm.avg_price.toFixed(2)}
                    </span>
                    <div
                      className="flex items-center gap-1 text-sm font-medium"
                      style={{ color: charm.price_change_7d >= 0 ? '#2d8659' : '#ba3e2b' }}
                    >
                      {charm.price_change_7d >= 0 ? (
                        <TrendingUp className="w-4 h-4" />
                      ) : (
                        <TrendingDown className="w-4 h-4" />
                      )}
                      {Math.abs(charm.price_change_7d)}%
                    </div>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span style={{ color: '#666666' }}>{charm.material}</span>
                    <span
                      className="px-2 py-1"
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
              </button>
            ))}
          </div>
        )}

        {/* Pagination */}
        {pagination.totalPages > 1 && (
          <div className="flex items-center justify-center gap-2">
            <button
              onClick={() => setPagination(prev => ({ ...prev, page: Math.max(1, prev.page - 1) }))}
              disabled={pagination.page === 1}
              className="px-6 py-3 transition-smooth disabled:opacity-50 disabled:cursor-not-allowed"
              style={{
                background: 'transparent',
                border: '1px solid #333333',
                borderRadius: '0px',
                color: '#333333'
              }}
            >
              Previous
            </button>
            <span className="px-4 body-regular" style={{ color: '#666666' }}>
              Page {pagination.page} of {pagination.totalPages}
            </span>
            <button
              onClick={() => setPagination(prev => ({ ...prev, page: Math.min(pagination.totalPages, prev.page + 1) }))}
              disabled={pagination.page === pagination.totalPages}
              className="px-6 py-3 transition-smooth disabled:opacity-50 disabled:cursor-not-allowed"
              style={{
                background: 'transparent',
                border: '1px solid #333333',
                borderRadius: '0px',
                color: '#333333'
              }}
            >
              Next
            </button>
          </div>
        )}
      </div>
    </div>
  );
};