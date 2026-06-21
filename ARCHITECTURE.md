# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Dashboard   │  │ Transactions │  │  Analytics   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                  │                  │               │
│         └──────────────────┼──────────────────┘               │
│                            │                                  │
│                  ┌─────────▼─────────┐                        │
│                  │  API Client (Axios)                       │
│                  └─────────┬─────────┘                        │
└─────────────────────────────┼─────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   CORS Middleware  │
                    └─────────┬─────────┘
                              │
┌─────────────────────────────┼─────────────────────────────────┐
│                    Backend (FastAPI)                          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Route Handlers                            │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │ │
│  │  │  Auth    │  │  Trans   │  │Analytics │             │ │
│  │  └──────────┘  └──────────┘  └──────────┘             │ │
│  └──────────┬───────────┬───────────┬────────────────────┘ │
│             │           │           │                       │
│  ┌──────────▼──────┬────▼──────┬────▼───────────────────┐   │
│  │  Service Layer  │            │                       │   │
│  │  - UserService  │            │                       │   │
│  │  - TransService │            │                       │   │
│  │  - Analytics    │            │                       │   │
│  └──────────┬──────┴────┬───────┴────────────────────┬──┘   │
│             │           │                            │       │
│  ┌──────────▼──────┬────▼──────┬──────────────────┬─▼────┐  │
│  │   ML Modules    │ OCR       │ AI Assistant    │Utils  │  │
│  │ - Categorizer   │ - Tesseract - LangChain    │       │  │
│  │ - Forecaster    │ - OpenCV  │ - Ollama       │       │  │
│  │ - FraudDetect   │ - pdfplumber              │       │  │
│  └─────────────────┴───────────┴─────────────────┴───────┘  │
│             │                         │                      │
│  ┌──────────▼───────────────────────────▼──────────────┐    │
│  │         SQLAlchemy ORM                             │    │
│  └──────────┬─────────────────────────┬────────────────┘    │
└─────────────┼───────────────────────────┼────────────────────┘
              │                           │
         ┌────▼──────────┐        ┌──────▼───┐
         │  PostgreSQL   │        │  Redis   │
         │  (Data Store) │        │  (Cache) │
         └───────────────┘        └──────────┘

         ┌────────────────┐
         │  Ollama (LLM)  │
         │  Local Models  │
         └────────────────┘

         ┌─────────────────────┐
         │  External Services  │
         │  - Cloudinary       │
         │  - Resend (Email)   │
         │  - Google OAuth     │
         └─────────────────────┘
```

## Data Flow

### 1. User Authentication
```
User Input (Email/Password)
        ↓
[Frontend Form] → POST /auth/login
        ↓
[Backend Auth Service]
        ↓
[Password Verification] (bcrypt)
        ↓
[JWT Token Generation]
        ↓
[Store Token in Client]
```

### 2. Transaction Flow
```
User Input (Expense Details)
        ↓
[Frontend Form] → POST /transactions
        ↓
[Authorization Check]
        ↓
[Input Validation] (Pydantic)
        ↓
[Service Layer Processing]
        ↓
[ML Categorization] (Optional)
        ↓
[Database Insert] (SQLAlchemy)
        ↓
[Return Response]
        ↓
[Frontend Update] (React Query)
```

### 3. Receipt Processing
```
User Uploads Receipt
        ↓
[File Upload Handler]
        ↓
[Image Preprocessing] (OpenCV)
        ↓
[OCR Extraction] (Tesseract)
        ↓
[Data Parsing] (Regex)
        ↓
[Confidence Scoring]
        ↓
[Transaction Suggestion]
        ↓
[User Confirmation]
        ↓
[Database Store]
```

### 4. Analytics Flow
```
Dashboard Request
        ↓
[Query Recent Transactions]
        ↓
[Calculate Stats]
        ↓
[Generate Forecasts] (Prophet)
        ↓
[Detect Anomalies] (Isolation Forest)
        ↓
[Generate Insights]
        ↓
[Cache Results] (Redis)
        ↓
[Return to Frontend]
```

## Database Schema

### Core Tables

**users**
- id (PK)
- email (UNIQUE)
- name
- hashed_password
- avatar
- role
- is_active
- is_verified
- created_at
- updated_at

**transactions**
- id (PK)
- user_id (FK)
- type (expense/income)
- amount
- currency
- category
- merchant
- description
- date
- tags (JSON)
- notes
- receipt_id (FK)
- is_recurring
- recurring_frequency
- created_at
- updated_at

**budgets**
- id (PK)
- user_id (FK)
- name
- budget_type
- amount
- currency
- category
- start_date
- end_date
- created_at
- updated_at

**goals**
- id (PK)
- user_id (FK)
- name
- target_amount
- current_amount
- currency
- deadline
- priority
- status
- created_at
- updated_at

**receipts**
- id (PK)
- user_id (FK)
- image_url
- extracted_data (JSON)
- status (pending/processed/failed)
- transaction_id (FK)
- created_at
- updated_at

**financial_health**
- id (PK)
- user_id (FK)
- score
- savings_rate
- debt_ratio
- income_stability
- emergency_fund
- budget_adherence
- last_updated

**chat_history**
- id (PK)
- user_id (FK)
- messages (JSON)
- created_at
- updated_at

## Component Architecture

### Frontend Components

```
App
├── Layout
│   ├── Sidebar
│   └── Header
├── Pages
│   ├── Auth
│   │   ├── Login
│   │   └── Register
│   └── Dashboard
│       ├── Dashboard (Main)
│       ├── Transactions
│       ├── Budgets
│       ├── Goals
│       ├── Reports
│       ├── Insights
│       ├── Receipts
│       ├── Chat
│       ├── Health
│       ├── Subscriptions
│       ├── Fraud
│       └── Settings
└── Components
    ├── UI
    │   ├── Button
    │   ├── Card
    │   └── ...
    ├── Dashboard
    │   ├── StatCard
    │   ├── Charts
    │   ├── TransactionsTable
    │   └── ...
    └── Forms
        ├── TransactionForm
        └── ...
```

### Backend Architecture

```
FastAPI App
├── Middleware
│   ├── CORS
│   ├── Auth
│   └── Logging
├── Routes
│   ├── Auth (/auth)
│   ├── Transactions (/transactions)
│   ├── Budgets (/budgets)
│   ├── Goals (/goals)
│   ├── Receipts (/receipts)
│   ├── Analytics (/analytics)
│   └── Chat (/chat)
├── Services
│   ├── UserService
│   ├── TransactionService
│   └── AnalyticsService
├── Models
│   ├── SQLAlchemy ORM Models
│   └── Database Schema
├── Schemas
│   ├── Pydantic Validation Schemas
│   └── Response Models
├── ML
│   ├── ExpenseCategorizer
│   ├── ExpenseForecaster
│   └── FraudDetector
└── OCR
    ├── ImageProcessor
    └── OCRProcessor
```

## Technology Stack Details

### Frontend
- **Next.js 15**: React framework with file-based routing
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **React Query**: Server state management
- **Zustand**: Client state management
- **Framer Motion**: Animation library
- **Recharts**: Data visualization

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and serialization
- **JWT**: Token-based authentication
- **Celery**: Async task queue (optional)

### ML/AI
- **Prophet**: Time series forecasting
- **Scikit-Learn**: Machine learning algorithms
- **XGBoost**: Gradient boosting
- **LangChain**: LLM framework
- **Ollama**: Local LLM support

### OCR/Vision
- **Tesseract**: OCR engine
- **OpenCV**: Image processing
- **Pillow**: Image manipulation
- **pdfplumber**: PDF text extraction

### Database
- **PostgreSQL**: Primary database
- **Redis**: Caching and session store

### Deployment
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Vercel**: Frontend hosting
- **Railway**: Backend hosting

## Scaling Strategy

### Horizontal Scaling
- Load balancer for multiple backend instances
- Database replication
- Redis clustering
- CDN for static assets

### Vertical Scaling
- Increase CPU/Memory allocation
- Upgrade database tier
- Increase cache size

### Caching Strategy
- Session caching (Redis)
- Query result caching
- Static asset caching (CDN)
- API response caching

## Security Architecture

```
Request
├── HTTPS (TLS/SSL)
├── CORS Validation
├── Rate Limiting
├── Input Validation (Pydantic)
├── SQL Injection Prevention (SQLAlchemy ORM)
├── XSS Protection
├── CSRF Protection
├── JWT Validation
├── Role-Based Access Control
└── Secure Password Storage (bcrypt)

Response
├── HTTPS (TLS/SSL)
├── Security Headers
├── Secure Cookies
├── XSS Protection
└── CSRF Tokens
```

## Performance Optimization

### Frontend
- Code splitting
- Lazy loading
- Image optimization
- CSS-in-JS optimization
- React Query caching

### Backend
- Database indexing
- Query optimization
- Redis caching
- Connection pooling
- Response compression

### General
- CDN for static assets
- Gzip compression
- Minification
- Pagination for large datasets
