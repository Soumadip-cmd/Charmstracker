/**
 * API Service for CharmTracker Frontend
 * Handles all API calls to the backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Generic fetch wrapper with error handling
 */
async function apiFetch(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw error;
  }
}

/**
 * Charm API endpoints
 */
export const charmAPI = {
  /**
   * Get all charms with optional filters
   */
  getAllCharms: async (params = {}) => {
    const queryParams = new URLSearchParams();
    
    Object.keys(params).forEach(key => {
      if (params[key] !== undefined && params[key] !== null && params[key] !== '') {
        queryParams.append(key, params[key]);
      }
    });

    const endpoint = `/api/charms${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
    return await apiFetch(endpoint);
  },

  /**
   * Get charm by ID
   */
  getCharmById: async (id) => {
    return await apiFetch(`/api/charms/${id}`);
  },

  /**
   * Get trending charms
   */
  getTrending: async () => {
    return await apiFetch('/api/trending');
  },

  /**
   * Get market overview statistics
   */
  getMarketOverview: async () => {
    return await apiFetch('/api/market-overview');
  },

  /**
   * Trigger real-time update for a specific charm
   */
  updateCharm: async (charmId) => {
    return await apiFetch(`/api/scraper/update/${charmId}`, {
      method: 'POST',
    });
  },

  /**
   * Check marketplace availability for a charm
   */
  checkMarketplaceAvailability: async (charmName) => {
    const encodedName = encodeURIComponent(charmName);
    return await apiFetch(`/api/scraper/marketplace-check/${encodedName}`);
  },

  /**
   * Get scraper status
   */
  getScraperStatus: async () => {
    return await apiFetch('/api/scraper/status');
  },
};

/**
 * Watchlist utilities (localStorage-based)
 */
export const watchlistUtils = {
  STORAGE_KEY: 'charmtracker_watchlist',

  /**
   * Get all items in watchlist
   */
  getWatchlist: () => {
    try {
      const stored = localStorage.getItem(watchlistUtils.STORAGE_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.error('Error reading watchlist:', error);
      return [];
    }
  },

  /**
   * Add item to watchlist
   */
  addToWatchlist: (charmId) => {
    try {
      const watchlist = watchlistUtils.getWatchlist();
      if (!watchlist.includes(charmId)) {
        watchlist.push(charmId);
        localStorage.setItem(watchlistUtils.STORAGE_KEY, JSON.stringify(watchlist));
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error adding to watchlist:', error);
      return false;
    }
  },

  /**
   * Remove item from watchlist
   */
  removeFromWatchlist: (charmId) => {
    try {
      let watchlist = watchlistUtils.getWatchlist();
      watchlist = watchlist.filter(id => id !== charmId);
      localStorage.setItem(watchlistUtils.STORAGE_KEY, JSON.stringify(watchlist));
      return true;
    } catch (error) {
      console.error('Error removing from watchlist:', error);
      return false;
    }
  },

  /**
   * Check if item is in watchlist
   */
  isInWatchlist: (charmId) => {
    const watchlist = watchlistUtils.getWatchlist();
    return watchlist.includes(charmId);
  },

  /**
   * Clear entire watchlist
   */
  clearWatchlist: () => {
    try {
      localStorage.removeItem(watchlistUtils.STORAGE_KEY);
      return true;
    } catch (error) {
      console.error('Error clearing watchlist:', error);
      return false;
    }
  },
};

/**
 * Real-time data utilities
 */
export const realtimeUtils = {
  /**
   * Auto-refresh charm data
   * Polls for updates at specified interval
   */
  startAutoRefresh: (charmId, callback, intervalMs = 30000) => {
    const refresh = async () => {
      try {
        const data = await charmAPI.getCharmById(charmId);
        callback(data);
      } catch (error) {
        console.error('Auto-refresh error:', error);
      }
    };

    // Initial fetch
    refresh();

    // Set up interval
    const intervalId = setInterval(refresh, intervalMs);

    // Return cleanup function
    return () => clearInterval(intervalId);
  },

  /**
   * Check if data needs refresh (older than threshold)
   */
  needsRefresh: (lastUpdated, thresholdMinutes = 30) => {
    if (!lastUpdated) return true;
    
    const lastUpdateTime = new Date(lastUpdated).getTime();
    const now = Date.now();
    const thresholdMs = thresholdMinutes * 60 * 1000;
    
    return (now - lastUpdateTime) > thresholdMs;
  },

  /**
   * Format time since last update
   */
  timeSinceUpdate: (lastUpdated) => {
    if (!lastUpdated) return 'Never updated';
    
    const diff = Date.now() - new Date(lastUpdated).getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'Just now';
  },
};

/**
 * Price formatting utilities
 */
export const priceUtils = {
  /**
   * Format price as currency
   */
  formatPrice: (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  },

  /**
   * Format price change percentage
   */
  formatPriceChange: (change) => {
    const sign = change >= 0 ? '+' : '';
    return `${sign}${change.toFixed(1)}%`;
  },

  /**
   * Get price trend color
   */
  getPriceTrendColor: (change) => {
    if (change > 0) return '#2d8659'; // Green for positive
    if (change < 0) return '#ba3e2b'; // Red for negative
    return '#666666'; // Gray for no change
  },
};

export default {
  charmAPI,
  watchlistUtils,
  realtimeUtils,
  priceUtils,
};