// Store configuration
const STORE_NAMES = {
    '001': '광화문점',
    '015': '강남점',
    '029': '잠실점',
    '058': '가든파이브점',
    '002': '영등포점',
    '003': '목동점',
    '004': '천호점',
    '005': '분당점',
    '006': '부천점',
    '007': '인천점',
    '008': '대구점',
    '009': '부산점',
    '010': '울산점',
    '011': '창원점',
    '012': '천안점',
    '013': '전주점',
    '014': '광주점'
};

// API base URL
const API_BASE_URL = 'http://localhost:5001/api';

// DOM elements
const storeSelect = document.getElementById('store-select');
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const loading = document.getElementById('loading');
const searchResults = document.getElementById('search-results');
const resultsList = document.getElementById('results-list');
const bookInfo = document.getElementById('book-info');
const bookDetails = document.getElementById('book-details');
const locationInfo = document.getElementById('location-info');
const locationDetails = document.getElementById('location-details');
const errorMessage = document.getElementById('error-message');
const errorText = document.getElementById('error-text');

// Current book data
let currentBook = null;

// Load saved store preference
window.addEventListener('DOMContentLoaded', () => {
    const savedStore = localStorage.getItem('preferredStore');
    if (savedStore) {
        storeSelect.value = savedStore;
    }
});

// Save store preference
storeSelect.addEventListener('change', () => {
    localStorage.setItem('preferredStore', storeSelect.value);
});

// Search on Enter key
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        performSearch();
    }
});

// Search button click
searchBtn.addEventListener('click', performSearch);

// Main search function
async function performSearch() {
    const query = searchInput.value.trim();

    if (!query) {
        showError('검색어를 입력해주세요.');
        return;
    }

    if (!storeSelect.value) {
        showError('매장을 먼저 선택해주세요.');
        return;
    }

    hideAllSections();
    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || '검색 중 오류가 발생했습니다');
        }

        if (data.books && data.books.length > 0) {
            displaySearchResults(data.books);
        } else {
            showError('검색 결과가 없습니다. 다른 검색어를 시도해보세요.');
        }

    } catch (error) {
        console.error('Search error:', error);
        showError(`검색 중 오류가 발생했습니다: ${error.message}<br><br>서버가 실행 중인지 확인해주세요.`);
    } finally {
        showLoading(false);
    }
}

// Display search results
function displaySearchResults(books) {
    resultsList.innerHTML = '';

    books.forEach(book => {
        const bookItem = document.createElement('div');
        bookItem.className = 'book-item';
        bookItem.innerHTML = `
            <h3>${escapeHtml(book.title)}</h3>
            <p>${escapeHtml(book.author)}${book.publisher ? ' | ' + escapeHtml(book.publisher) : ''}</p>
        `;
        bookItem.addEventListener('click', () => selectBook(book));
        resultsList.appendChild(bookItem);
    });

    searchResults.classList.remove('hidden');
}

// Select a book and get its details
async function selectBook(book) {
    hideAllSections();
    showLoading(true);

    try {
        // Get book details including barcode
        const response = await fetch(`${API_BASE_URL}/book/${book.product_id}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || '책 정보를 가져오는 중 오류가 발생했습니다');
        }

        currentBook = {
            ...book,
            barcode: data.barcode,
            title: data.title || book.title,
            author: data.author || book.author,
            publisher: data.publisher || book.publisher
        };

        // Display book details
        displayBookDetails(currentBook);

        // Automatically get location
        await getBookLocation(currentBook.barcode);

    } catch (error) {
        console.error('Book details error:', error);
        showError(`책 정보를 가져오는 중 오류가 발생했습니다: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// Display book details
function displayBookDetails(book) {
    bookDetails.innerHTML = `
        <div class="detail-item">
            <span class="detail-label">제목</span>
            <span class="detail-value">${escapeHtml(book.title)}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">저자</span>
            <span class="detail-value">${escapeHtml(book.author)}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">출판사</span>
            <span class="detail-value">${escapeHtml(book.publisher)}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">바코드</span>
            <span class="detail-value">${escapeHtml(book.barcode)}</span>
        </div>
    `;

    bookInfo.classList.remove('hidden');
}

// Get book location from backend
async function getBookLocation(barcode) {
    const storeCode = storeSelect.value;
    const storeName = STORE_NAMES[storeCode];

    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/location?barcode=${barcode}&store=${storeCode}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || '위치 정보를 가져오는 중 오류가 발생했습니다');
        }

        displayLocation({
            store: storeName,
            locations: data.locations || [],
            stock: data.stock,
            stockText: data.stock_text,
            kioskUrl: data.kiosk_url
        });

    } catch (error) {
        console.error('Location error:', error);
        showError(`위치 정보를 가져오는 중 오류가 발생했습니다: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// Display location information
function displayLocation(location) {
    // Format locations as a list
    const locationsHtml = location.locations.map(loc =>
        `<div class="location-entry">• ${escapeHtml(loc)}</div>`
    ).join('');

    locationDetails.innerHTML = `
        <div class="location-item">
            <div class="location-label">
                <span>🏪</span>
                <span>매장</span>
            </div>
            <div class="location-value">${escapeHtml(location.store)}</div>
        </div>
        <div class="location-item">
            <div class="location-label">
                <span>📍</span>
                <span>위치 정보</span>
            </div>
            <div class="location-list">
                ${locationsHtml}
            </div>
        </div>
        <div class="location-item">
            <div class="location-label">
                <span>📦</span>
                <span>재고</span>
            </div>
            <div>
                <span class="stock-info ${location.stock > 0 ? '' : 'no-stock'}">
                    ${location.stock > 0 ? `${location.stock}부` : '재고 정보 없음'}
                </span>
            </div>
        </div>
        <div class="location-item" style="margin-top: 1.5rem;">
            <a href="${location.kioskUrl}" target="_blank" style="display: inline-block; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">
                키오스크 페이지에서 확인 →
            </a>
        </div>
    `;

    locationInfo.classList.remove('hidden');
}

// UI helper functions
function showLoading(show) {
    loading.classList.toggle('hidden', !show);
}

function hideAllSections() {
    searchResults.classList.add('hidden');
    bookInfo.classList.add('hidden');
    locationInfo.classList.add('hidden');
    errorMessage.classList.add('hidden');
}

function showError(message) {
    errorText.innerHTML = message;
    errorMessage.classList.remove('hidden');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
