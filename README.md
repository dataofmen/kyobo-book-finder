# 📚 Kyobo Book Finder

교보문고 매장에서 원하는 책의 위치를 쉽게 찾아주는 웹 애플리케이션입니다.

## ✨ Features

- 🔍 **책 검색**: 제목으로 교보문고 책 검색
- 📖 **상세 정보**: ISBN, 저자, 출판사 등 책 정보 확인
- 📍 **위치 찾기**: 선택한 매장에서 책의 정확한 위치 확인
- 📦 **재고 확인**: 실시간 재고 수량 확인
- 🏪 **매장 선택**: 전국 주요 교보문고 매장 지원

## 🚀 Tech Stack

### Backend
- **Flask**: Python web framework
- **Playwright**: JavaScript-rendered content scraping
- **BeautifulSoup4**: HTML parsing
- **Gunicorn**: Production WSGI server

### Frontend
- **HTML/CSS/JavaScript**: Vanilla web technologies
- **Responsive Design**: Mobile-friendly interface

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/kyobo-book-finder.git
cd kyobo-book-finder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

4. Run the server:
```bash
python server.py
```

5. Open `index.html` in your browser or visit `http://localhost:5001`

## 🌐 Deployment

### Railway

This application is configured for easy deployment on Railway:

1. Push your code to GitHub
2. Connect your GitHub repository to Railway
3. Railway will automatically detect the configuration from `railway.json`
4. The application will be deployed with Playwright support

### Environment Variables

No environment variables are required for basic functionality.

## 📖 Usage

1. **Select Store**: Choose your preferred Kyobo bookstore from the dropdown
2. **Search Book**: Enter the book title in the search box
3. **View Details**: Click on a search result to see book details
4. **Check Location**: The app automatically shows the book's location and stock in the selected store

## 🏗️ Project Structure

```
kyobo-book-finder/
├── server.py           # Flask backend server
├── index.html          # Main HTML page
├── app.js              # Frontend JavaScript
├── style.css           # Styling
├── requirements.txt    # Python dependencies
├── Procfile           # Railway deployment config
├── railway.json       # Railway build settings
└── README.md          # This file
```

## 🔧 API Endpoints

### Search Books
```
GET /api/search?q={query}
```

### Get Book Details
```
GET /api/book/{product_id}
```

### Get Book Location
```
GET /api/location?barcode={isbn}&store={store_code}
```

## ⚠️ Disclaimer

이 도구는 교보문고 공식 서비스가 아닙니다. 정보는 참고용으로만 사용하세요.

This tool is not an official Kyobo bookstore service. Information is for reference only.

## 📝 License

MIT License

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 👨‍💻 Author

Created with ❤️ for book lovers
