# 📚 교보문고 책 위치 찾기 - 릴리즈 노트

## 버전 1.0.0 - 첫 번째 테스트 버전 (2025-12-22)

### 🎉 새로운 기능

교보문고 매장에서 원하는 책의 위치를 쉽게 찾아주는 웹 애플리케이션이 출시되었습니다!

#### 핵심 기능
- **📖 책 검색**: 제목으로 교보문고 도서를 빠르게 검색할 수 있습니다
- **📍 위치 찾기**: 선택한 매장에서 책의 정확한 위치를 확인할 수 있습니다
  - 관별 위치 정보 (예: [K관 6] 평대)
  - 섹션별 분류 정보 (예: 심리학, 자기계발 등)
- **📦 실시간 재고 확인**: 선택한 매장의 실시간 재고 수량을 확인할 수 있습니다
- **🏪 전국 매장 지원**: 광화문점, 강남점, 잠실점 등 주요 교보문고 매장 지원

#### 상세 정보 제공
- ISBN 바코드 정보
- 저자 및 출판사 정보
- 도서 상세 페이지 링크

#### 사용자 경험
- **반응형 디자인**: 모바일, 태블릿, 데스크톱 모든 기기에서 최적화된 화면
- **직관적인 인터페이스**: 간단한 3단계로 책 위치 확인
  1. 매장 선택
  2. 책 제목 검색
  3. 검색 결과에서 원하는 책 선택
- **빠른 검색**: 실시간 검색 결과 제공

### 🔧 기술 스택

#### 백엔드
- Flask 웹 프레임워크
- Playwright를 활용한 동적 콘텐츠 스크래핑
- BeautifulSoup4 HTML 파싱
- Gunicorn 프로덕션 서버

#### 프론트엔드
- 순수 HTML/CSS/JavaScript
- 모바일 최적화 반응형 디자인
- 직관적인 사용자 인터페이스

### 🌐 배포
- Railway 플랫폼을 통한 클라우드 배포
- 안정적인 24/7 서비스 제공
- 자동 재시작 및 오류 복구 기능

### ⚠️ 알려진 제한사항
- 이 도구는 교보문고 공식 서비스가 아닙니다
- 정보는 참고용으로만 사용하시기 바랍니다
- 실시간 재고는 변동될 수 있습니다

### 📝 향후 계획
- 즐겨찾기 기능 추가
- 검색 기록 저장
- 여러 매장 동시 재고 확인
- PWA(Progressive Web App) 지원으로 앱처럼 설치 가능

---

## Release Notes (English)

## Version 1.0.0 - First Test Release (2025-12-22)

### 🎉 New Features

Introducing the Kyobo Book Finder - a web application that helps you easily locate books in Kyobo bookstores!

#### Core Features
- **📖 Book Search**: Quickly search for books by title
- **📍 Location Finder**: Find exact book locations in your selected store
  - Building and section information (e.g., [K Building 6] Display)
  - Category classification (e.g., Psychology, Self-help)
- **📦 Real-time Stock Check**: View current stock levels at selected stores
- **🏪 Nationwide Coverage**: Support for major Kyobo stores including Gwanghwamun, Gangnam, Jamsil, and more

#### Detailed Information
- ISBN barcode information
- Author and publisher details
- Direct links to book detail pages

#### User Experience
- **Responsive Design**: Optimized for mobile, tablet, and desktop
- **Intuitive Interface**: Find books in 3 simple steps
  1. Select a store
  2. Search by book title
  3. Choose your book from results
- **Fast Search**: Real-time search results

### 🔧 Technology Stack

#### Backend
- Flask web framework
- Playwright for dynamic content scraping
- BeautifulSoup4 for HTML parsing
- Gunicorn production server

#### Frontend
- Vanilla HTML/CSS/JavaScript
- Mobile-optimized responsive design
- Intuitive user interface

### 🌐 Deployment
- Cloud deployment via Railway platform
- Reliable 24/7 service availability
- Automatic restart and error recovery

### ⚠️ Known Limitations
- This is not an official Kyobo bookstore service
- Information is for reference purposes only
- Real-time stock may vary

### 📝 Future Plans
- Bookmark functionality
- Search history
- Multi-store stock comparison
- PWA (Progressive Web App) support for app-like installation

---

**Created with ❤️ for book lovers**
