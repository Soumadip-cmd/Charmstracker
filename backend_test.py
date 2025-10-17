#!/usr/bin/env python3
"""
CharmTracker Backend API Testing Suite
Tests all backend endpoints for Milestone 2 completion
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

# Backend URL from environment
BACKEND_URL = "https://charm-prices.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

class CharmTrackerAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.test_results = []
        self.failed_tests = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        if response_data:
            result['response_sample'] = str(response_data)[:200] + "..." if len(str(response_data)) > 200 else str(response_data)
        
        self.test_results.append(result)
        if not success:
            self.failed_tests.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        
    def test_api_root(self):
        """Test API root endpoint"""
        try:
            response = self.session.get(f"{API_BASE}/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    self.log_test("API Root", True, f"Status: {response.status_code}, Message: {data['message']}")
                else:
                    self.log_test("API Root", False, f"Missing message field in response: {data}")
            else:
                self.log_test("API Root", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("API Root", False, f"Exception: {str(e)}")

    def test_get_all_charms_basic(self):
        """Test GET /api/charms basic functionality"""
        try:
            response = self.session.get(f"{API_BASE}/charms")
            if response.status_code == 200:
                data = response.json()
                required_fields = ['charms', 'total', 'page', 'total_pages']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("GET /api/charms - Basic", False, f"Missing fields: {missing_fields}")
                    return
                
                charms = data['charms']
                if not isinstance(charms, list):
                    self.log_test("GET /api/charms - Basic", False, "Charms field is not a list")
                    return
                
                if len(charms) == 0:
                    self.log_test("GET /api/charms - Basic", False, "No charms returned")
                    return
                
                # Check charm structure
                charm = charms[0]
                required_charm_fields = ['id', 'name', 'material', 'status', 'avg_price', 'price_change_7d', 'popularity', 'images']
                missing_charm_fields = [field for field in required_charm_fields if field not in charm]
                
                if missing_charm_fields:
                    self.log_test("GET /api/charms - Basic", False, f"Missing charm fields: {missing_charm_fields}")
                    return
                
                self.log_test("GET /api/charms - Basic", True, 
                            f"Returned {len(charms)} charms, Total: {data['total']}, Page: {data['page']}")
                
            else:
                self.log_test("GET /api/charms - Basic", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("GET /api/charms - Basic", False, f"Exception: {str(e)}")

    def test_get_charms_pagination(self):
        """Test GET /api/charms with pagination parameters"""
        try:
            response = self.session.get(f"{API_BASE}/charms?page=1&limit=20&sort=popularity")
            if response.status_code == 200:
                data = response.json()
                charms = data['charms']
                
                if len(charms) > 20:
                    self.log_test("GET /api/charms - Pagination", False, f"Returned {len(charms)} charms, expected max 20")
                    return
                
                if data['page'] != 1:
                    self.log_test("GET /api/charms - Pagination", False, f"Page should be 1, got {data['page']}")
                    return
                
                self.log_test("GET /api/charms - Pagination", True, 
                            f"Pagination working: {len(charms)} charms on page {data['page']}")
                
            else:
                self.log_test("GET /api/charms - Pagination", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/charms - Pagination", False, f"Exception: {str(e)}")

    def test_get_charms_filtering(self):
        """Test GET /api/charms with filtering"""
        filters_to_test = [
            ("material=Silver", "material filter"),
            ("status=Active", "status filter"),
            ("min_price=50&max_price=100", "price range filter")
        ]
        
        for filter_param, filter_name in filters_to_test:
            try:
                response = self.session.get(f"{API_BASE}/charms?{filter_param}")
                if response.status_code == 200:
                    data = response.json()
                    charms = data['charms']
                    
                    # Validate filter is applied
                    if "material=Silver" in filter_param and charms:
                        if not all(charm['material'] == 'Silver' for charm in charms):
                            self.log_test(f"GET /api/charms - {filter_name}", False, "Material filter not applied correctly")
                            continue
                    
                    if "status=Active" in filter_param and charms:
                        if not all(charm['status'] == 'Active' for charm in charms):
                            self.log_test(f"GET /api/charms - {filter_name}", False, "Status filter not applied correctly")
                            continue
                    
                    if "min_price=50&max_price=100" in filter_param and charms:
                        if not all(50 <= charm['avg_price'] <= 100 for charm in charms):
                            self.log_test(f"GET /api/charms - {filter_name}", False, "Price range filter not applied correctly")
                            continue
                    
                    self.log_test(f"GET /api/charms - {filter_name}", True, 
                                f"Filter working: {len(charms)} charms returned")
                else:
                    self.log_test(f"GET /api/charms - {filter_name}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"GET /api/charms - {filter_name}", False, f"Exception: {str(e)}")

    def test_get_charms_sorting(self):
        """Test GET /api/charms with different sorting options"""
        sort_options = ["price_asc", "price_desc", "name", "popularity"]
        
        for sort_option in sort_options:
            try:
                response = self.session.get(f"{API_BASE}/charms?sort={sort_option}&limit=5")
                if response.status_code == 200:
                    data = response.json()
                    charms = data['charms']
                    
                    if len(charms) >= 2:
                        # Validate sorting
                        if sort_option == "price_asc":
                            is_sorted = all(charms[i]['avg_price'] <= charms[i+1]['avg_price'] for i in range(len(charms)-1))
                        elif sort_option == "price_desc":
                            is_sorted = all(charms[i]['avg_price'] >= charms[i+1]['avg_price'] for i in range(len(charms)-1))
                        elif sort_option == "name":
                            is_sorted = all(charms[i]['name'] <= charms[i+1]['name'] for i in range(len(charms)-1))
                        elif sort_option == "popularity":
                            is_sorted = all(charms[i]['popularity'] >= charms[i+1]['popularity'] for i in range(len(charms)-1))
                        
                        if is_sorted:
                            self.log_test(f"GET /api/charms - Sort {sort_option}", True, 
                                        f"Sorting working correctly")
                        else:
                            self.log_test(f"GET /api/charms - Sort {sort_option}", False, 
                                        f"Sorting not applied correctly")
                    else:
                        self.log_test(f"GET /api/charms - Sort {sort_option}", True, 
                                    f"Sort parameter accepted, {len(charms)} charms returned")
                else:
                    self.log_test(f"GET /api/charms - Sort {sort_option}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"GET /api/charms - Sort {sort_option}", False, f"Exception: {str(e)}")

    def test_get_trending_charms(self):
        """Test GET /api/trending"""
        try:
            response = self.session.get(f"{API_BASE}/trending")
            if response.status_code == 200:
                data = response.json()
                
                if 'trending' not in data:
                    self.log_test("GET /api/trending", False, "Missing 'trending' field in response")
                    return
                
                trending = data['trending']
                if not isinstance(trending, list):
                    self.log_test("GET /api/trending", False, "Trending field is not a list")
                    return
                
                if len(trending) > 6:
                    self.log_test("GET /api/trending", False, f"Expected max 6 trending charms, got {len(trending)}")
                    return
                
                if len(trending) > 0:
                    charm = trending[0]
                    required_fields = ['id', 'name', 'avg_price', 'price_change', 'material', 'status', 'image']
                    missing_fields = [field for field in required_fields if field not in charm]
                    
                    if missing_fields:
                        self.log_test("GET /api/trending", False, f"Missing trending charm fields: {missing_fields}")
                        return
                
                self.log_test("GET /api/trending", True, 
                            f"Returned {len(trending)} trending charms")
                
            else:
                self.log_test("GET /api/trending", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("GET /api/trending", False, f"Exception: {str(e)}")

    def test_get_market_overview(self):
        """Test GET /api/market-overview"""
        try:
            response = self.session.get(f"{API_BASE}/market-overview")
            if response.status_code == 200:
                data = response.json()
                
                required_fields = ['average_price', 'total_charms', 'active_charms', 'retired_charms', 
                                 'top_gainers', 'top_losers', 'recently_sold']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("GET /api/market-overview", False, f"Missing fields: {missing_fields}")
                    return
                
                # Validate data types
                if not isinstance(data['average_price'], (int, float)):
                    self.log_test("GET /api/market-overview", False, "average_price should be numeric")
                    return
                
                if not isinstance(data['total_charms'], int):
                    self.log_test("GET /api/market-overview", False, "total_charms should be integer")
                    return
                
                for array_field in ['top_gainers', 'top_losers', 'recently_sold']:
                    if not isinstance(data[array_field], list):
                        self.log_test("GET /api/market-overview", False, f"{array_field} should be a list")
                        return
                
                self.log_test("GET /api/market-overview", True, 
                            f"Market overview: {data['total_charms']} total charms, avg price: ${data['average_price']:.2f}")
                
            else:
                self.log_test("GET /api/market-overview", False, f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test("GET /api/market-overview", False, f"Exception: {str(e)}")

    def test_get_charm_by_id(self):
        """Test GET /api/charms/{id}"""
        # First get a charm ID from the list
        try:
            response = self.session.get(f"{API_BASE}/charms?limit=1")
            if response.status_code != 200:
                self.log_test("GET /api/charms/{id} - Setup", False, "Could not get charm list for ID")
                return
            
            data = response.json()
            if not data['charms']:
                self.log_test("GET /api/charms/{id} - Setup", False, "No charms available for ID test")
                return
            
            charm_id = data['charms'][0]['id']
            
            # Test getting specific charm
            response = self.session.get(f"{API_BASE}/charms/{charm_id}")
            if response.status_code == 200:
                charm_data = response.json()
                
                required_fields = ['id', 'name', 'description', 'material', 'status', 'avg_price', 
                                 'price_change_7d', 'popularity', 'images', 'listings', 'price_history', 
                                 'related_charm_ids']
                missing_fields = [field for field in required_fields if field not in charm_data]
                
                if missing_fields:
                    self.log_test("GET /api/charms/{id}", False, f"Missing fields: {missing_fields}")
                    return
                
                if charm_data['id'] != charm_id:
                    self.log_test("GET /api/charms/{id}", False, f"ID mismatch: requested {charm_id}, got {charm_data['id']}")
                    return
                
                self.log_test("GET /api/charms/{id}", True, 
                            f"Charm details retrieved: {charm_data['name']}")
                
            else:
                self.log_test("GET /api/charms/{id}", False, f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            self.log_test("GET /api/charms/{id}", False, f"Exception: {str(e)}")

    def test_invalid_charm_id(self):
        """Test GET /api/charms/{id} with invalid ID"""
        try:
            response = self.session.get(f"{API_BASE}/charms/invalid_charm_id_12345")
            if response.status_code == 404:
                self.log_test("GET /api/charms/{invalid_id}", True, "Correctly returns 404 for invalid ID")
            else:
                self.log_test("GET /api/charms/{invalid_id}", False, 
                            f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/charms/{invalid_id}", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all API tests"""
        print(f"🚀 Starting CharmTracker API Tests")
        print(f"📍 Backend URL: {BACKEND_URL}")
        print(f"📍 API Base: {API_BASE}")
        print("=" * 60)
        
        # Run all tests
        self.test_api_root()
        self.test_get_all_charms_basic()
        self.test_get_charms_pagination()
        self.test_get_charms_filtering()
        self.test_get_charms_sorting()
        self.test_get_trending_charms()
        self.test_get_market_overview()
        self.test_get_charm_by_id()
        self.test_invalid_charm_id()
        
        # Print summary
        print("=" * 60)
        print(f"📊 TEST SUMMARY")
        print(f"Total Tests: {len(self.test_results)}")
        print(f"Passed: {len(self.test_results) - len(self.failed_tests)}")
        print(f"Failed: {len(self.failed_tests)}")
        
        if self.failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in self.failed_tests:
                print(f"  - {test['test']}: {test['details']}")
        else:
            print("\n🎉 ALL TESTS PASSED!")
        
        return len(self.failed_tests) == 0

if __name__ == "__main__":
    tester = CharmTrackerAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)