import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${API_BASE_URL}/api`;

// Charm API
export const charmAPI = {
  // Get all charms with filtering and sorting
  getAllCharms: async (params = {}) => {
    try {
      const response = await axios.get(`${API}/charms`, { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching charms:', error);
      throw error;
    }
  },

  // Get charm by ID
  getCharmById: async (id) => {
    try {
      const response = await axios.get(`${API}/charms/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching charm ${id}:`, error);
      throw error;
    }
  },

  // Get trending charms
  getTrending: async () => {
    try {
      const response = await axios.get(`${API}/trending`);
      return response.data;
    } catch (error) {
      console.error('Error fetching trending charms:', error);
      throw error;
    }
  },

  // Get market overview
  getMarketOverview: async () => {
    try {
      const response = await axios.get(`${API}/market-overview`);
      return response.data;
    } catch (error) {
      console.error('Error fetching market overview:', error);
      throw error;
    }
  }
};

// Watchlist utilities (localStorage-based)
export const watchlistUtils = {
  // Get watchlist from localStorage
  getWatchlist: () => {
    try {
      const watchlist = localStorage.getItem('charmtracker_watchlist');
      return watchlist ? JSON.parse(watchlist) : [];
    } catch (error) {
      console.error('Error reading watchlist:', error);
      return [];
    }
  },

  // Add charm to watchlist
  addToWatchlist: (charmId) => {
    try {
      const watchlist = watchlistUtils.getWatchlist();
      if (!watchlist.includes(charmId)) {
        watchlist.push(charmId);
        localStorage.setItem('charmtracker_watchlist', JSON.stringify(watchlist));
      }
      return watchlist;
    } catch (error) {
      console.error('Error adding to watchlist:', error);
      return [];
    }
  },

  // Remove charm from watchlist
  removeFromWatchlist: (charmId) => {
    try {
      const watchlist = watchlistUtils.getWatchlist();
      const filtered = watchlist.filter(id => id !== charmId);
      localStorage.setItem('charmtracker_watchlist', JSON.stringify(filtered));
      return filtered;
    } catch (error) {
      console.error('Error removing from watchlist:', error);
      return [];
    }
  },

  // Check if charm is in watchlist
  isInWatchlist: (charmId) => {
    const watchlist = watchlistUtils.getWatchlist();
    return watchlist.includes(charmId);
  }
};