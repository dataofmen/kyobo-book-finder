import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
import os

app = Flask(__name__, static_folder='.', static_url_path='')
# Enable CORS for all routes, including file:// protocol
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# User agent to mimic a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Serve frontend files
@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

# Digital Asset Links for TWA
@app.route('/.well-known/assetlinks.json')
def asset_links():
    """Serve Digital Asset Links for Android TWA"""
    return send_from_directory('.well-known', 'assetlinks.json')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory('.', path)


@app.route('/api/search', methods=['GET'])
def search_books():
    """Search for books on Kyobo website"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'error': '검색어를 입력해주세요'}), 400
    
    try:
        # Search on Kyobo
        search_url = f'https://search.kyobobook.co.kr/search?keyword={quote(query)}'
        response = requests.get(search_url, headers=HEADERS, timeout=10, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Find book items - using correct selector for Kyobo website
        books = []
        book_items = soup.select('li.prod_item')
        
        for item in book_items[:10]:  # Limit to 10 results
            try:
                # Extract title
                title_elem = item.select_one('a.prod_info')
                if not title_elem:
                    continue
                
                # Get title text (may contain category prefix like [국내도서])
                title_spans = title_elem.find_all('span')
                if title_spans and len(title_spans) > 1:
                    # Skip category prefix, get actual title
                    title = title_spans[1].get_text(strip=True)
                else:
                    title = title_elem.get_text(strip=True)
                
                # Extract product URL and ID
                product_url = title_elem.get('href', '')
                product_id_match = re.search(r'/detail/([A-Z0-9]+)', product_url)
                if not product_id_match:
                    continue
                product_id = product_id_match.group(1)
                
                # Extract authors
                author_elems = item.select('.prod_author_info a.author')
                authors = [a.get_text(strip=True) for a in author_elems]
                author = ', '.join(authors) if authors else ''
                
                # Extract publisher
                publisher_elem = item.select_one('.prod_publish a.text')
                publisher = publisher_elem.get_text(strip=True) if publisher_elem else ''
                
                books.append({
                    'title': title,
                    'author': author,
                    'publisher': publisher,
                    'product_id': product_id,
                    'url': f'https://product.kyobobook.co.kr{product_url}' if product_url.startswith('/') else product_url
                })
            except Exception as e:
                print(f"Error parsing book item: {e}")
                continue
        
        return jsonify({
            'success': True,
            'query': query,
            'count': len(books),
            'books': books
        })
        
    except requests.RequestException as e:
        return jsonify({'error': f'검색 중 오류가 발생했습니다: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'처리 중 오류가 발생했습니다: {str(e)}'}), 500


@app.route('/api/book/<product_id>', methods=['GET'])
def get_book_details(product_id):
    """Get detailed information about a book including barcode"""
    from playwright.sync_api import sync_playwright
    
    try:
        with sync_playwright() as p:
            browser = None
            page = None
            try:
                # Launch browser
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Navigate to book detail page
                detail_url = f'https://product.kyobobook.co.kr/detail/{product_id}'
                page.goto(detail_url, wait_until='networkidle', timeout=15000)
                
                # Extract ISBN using JavaScript
                barcode = page.evaluate("""
                    () => {
                        const th = Array.from(document.querySelectorAll('th'))
                            .find(el => el.textContent.trim() === 'ISBN');
                        return th?.nextElementSibling?.textContent.trim() || null;
                    }
                """)
                
                if not barcode:
                    return jsonify({'error': '바코드(ISBN)를 찾을 수 없습니다'}), 404
                
                # Extract title
                title = page.evaluate("""
                    () => {
                        const elem = document.querySelector('h1.prod_title, div.prod_title, .prod_info h1');
                        return elem?.textContent.trim() || '';
                    }
                """)
                
                # Extract author
                author = page.evaluate("""
                    () => {
                        const elem = document.querySelector('span.author a, div.author, .prod_author a');
                        return elem?.textContent.trim() || '';
                    }
                """)
                
                # Extract publisher
                publisher = page.evaluate("""
                    () => {
                        const elem = document.querySelector('span.publisher a, div.publisher, .prod_publish a');
                        return elem?.textContent.trim() || '';
                    }
                """)
                
                return jsonify({
                    'success': True,
                    'product_id': product_id,
                    'barcode': barcode,
                    'title': title,
                    'author': author,
                    'publisher': publisher
                })
            
            finally:
                # Ensure proper cleanup
                if page:
                    try:
                        page.close()
                    except:
                        pass
                if browser:
                    try:
                        browser.close()
                    except:
                        pass
        
    except Exception as e:
        return jsonify({'error': f'처리 중 오류가 발생했습니다: {str(e)}'}), 500




@app.route('/api/location', methods=['GET'])
def get_location():
    """Get book location in a specific store"""
    from playwright.sync_api import sync_playwright
    
    barcode = request.args.get('barcode', '')
    store_code = request.args.get('store', '')
    
    if not barcode or not store_code:
        return jsonify({'error': '바코드와 매장 코드가 필요합니다'}), 400
    
    try:
        with sync_playwright() as p:
            browser = None
            page = None
            try:
                # Launch browser
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Navigate to kiosk page
                kiosk_url = f'https://kiosk.kyobobook.co.kr/bookInfoInk?site={store_code}&barcode={barcode}&ejkGb=KOR'
                page.goto(kiosk_url, wait_until='networkidle', timeout=15000)
                
                # Extract all text from the page
                page_text = page.evaluate("() => document.body.innerText")
                
                # Parse the text to extract location and stock information
                lines = [line.strip() for line in page_text.split('\n') if line.strip()]
                
                # Extract stock information
                stock = 0
                stock_text = ''
                for line in lines:
                    if line.startswith('재고:'):
                        stock_text = line
                        # Extract number from "재고: 22부(*재고는 실시간으로 변경)"
                        stock_match = re.search(r'재고:\s*(\d+)부', line)
                        if stock_match:
                            stock = int(stock_match.group(1))
                        break
                
                # Extract location information
                # Location entries appear between the stock line and "도서위치:" marker
                # They come in pairs: first line has [X관 Y] 평대, second line has description
                locations = []
                in_location_section = False
                temp_lines = []
                
                for i, line in enumerate(lines):
                    # Start collecting after stock line
                    if line.startswith('재고:'):
                        in_location_section = True
                        continue
                    
                    # Stop at the location marker or ISBN
                    if line.startswith('도서위치:') or line.startswith('ISBN'):
                        break
                    
                    # Collect location entries
                    if in_location_section:
                        # Skip empty lines
                        if not line:
                            continue
                        
                        # Add to temp lines
                        temp_lines.append(line)
                
                # Combine pairs of lines into single location entries
                # Format: "[K관 6] 평대 : 심리학"
                i = 0
                while i < len(temp_lines):
                    if i + 1 < len(temp_lines):
                        # Check if first line looks like a location marker (contains '[' and ']')
                        if '[' in temp_lines[i] and ']' in temp_lines[i]:
                            # Combine with next line
                            combined = f"{temp_lines[i]} : {temp_lines[i + 1]}"
                            locations.append(combined)
                            i += 2
                        else:
                            # Single line entry
                            locations.append(temp_lines[i])
                            i += 1
                    else:
                        # Last line, add as is
                        locations.append(temp_lines[i])
                        i += 1
                
                # If no locations found, return error
                if not locations:
                    return jsonify({
                        'success': False,
                        'error': '위치 정보를 찾을 수 없습니다',
                        'barcode': barcode,
                        'store_code': store_code,
                        'kiosk_url': kiosk_url
                    }), 404
                
                return jsonify({
                    'success': True,
                    'barcode': barcode,
                    'store_code': store_code,
                    'locations': locations,
                    'stock': stock,
                    'stock_text': stock_text,
                    'kiosk_url': kiosk_url
                })
            
            finally:
                # Ensure proper cleanup
                if page:
                    try:
                        page.close()
                    except:
                        pass
                if browser:
                    try:
                        browser.close()
                    except:
                        pass
        
    except Exception as e:
        return jsonify({'error': f'처리 중 오류가 발생했습니다: {str(e)}'}), 500




@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})


if __name__ == '__main__':
    print("🚀 교보문고 책 위치 찾기 서버 시작")
    print("📍 서버 주소: http://localhost:5001")
    print("💡 프론트엔드에서 http://localhost:5001/api/* 로 접근하세요")
    app.run(debug=True, host='0.0.0.0', port=5001)
