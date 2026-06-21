# Finnova AI - Complete AI-Powered Financial Management Platform

A modern, full-stack financial management platform powered by artificial intelligence. Built with Next.js, FastAPI, and advanced ML models.

## 🚀 Features

### Core Features
- **Smart Expense Tracking** - Add, edit, and categorize expenses with ease
- **Receipt Scanner** - Upload receipts and automatically extract transaction data using OCR
- **AI Categorization** - Intelligent expense categorization using machine learning
- **Interactive Dashboard** - Beautiful, responsive dashboard with real-time analytics
- **Budget Management** - Create and track multiple budgets
- **Savings Goals** - Set and monitor savings goals
- **Financial Health Score** - Comprehensive financial health assessment

### Advanced Features
- **AI Financial Assistant** - Chat with AI about your finances using RAG
- **Expense Forecasting** - Predict future expenses using Prophet
- **Fraud Detection** - Identify suspicious transactions
- **Subscription Detection** - Automatically detect recurring payments
- **Financial Insights** - AI-generated personalized insights
- **Weekly Reports** - Automated PDF reports sent via email
- **Dark Mode** - Full dark mode support
- **PWA Support** - Install as a web app

### Tech Stack

**Frontend:**
- Next.js 15
- TypeScript
- Tailwind CSS
- React Query
- Zustand
- Framer Motion
- Recharts

**Backend:**
- FastAPI
- Python 3.12
- SQLAlchemy
- PostgreSQL (Neon)
- Redis
- Celery

**AI/ML:**
- Ollama
- Llama 3
- LangChain
- ChromaDB
- Prophet
- XGBoost
- Scikit-Learn

**OCR:**
- OpenCV
- Tesseract OCR
- pdfplumber

**Deployment:**
- Docker
- Docker Compose
- Vercel (Frontend)
- Railway (Backend)

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.12+
- Node.js 18+
- PostgreSQL 15+
- Redis
- Ollama (optional, for AI features)

## 🏗️ Project Structure

```
FINNOVA-AI/
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/            # Next.js app directory
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── lib/            # Utilities and helpers
│   │   ├── services/       # API services
│   │   ├── store/          # Zustand stores
│   │   └── types/          # TypeScript types
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration and security
│   │   ├── db/             # Database setup
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── ml/             # Machine learning modules
│   │   ├── ocr/            # OCR modules
│   │   └── main.py         # FastAPI app
│   ├── pyproject.toml
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
└── README.md

```

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository:**
```bash
cd FINNOVA-AI
```

2. **Copy environment file:**
```bash
cp backend/.env.example backend/.env
```

3. **Update environment variables:**
Edit `backend/.env` with your configuration

4. **Start all services:**
```bash
docker-compose up -d
```

5. **Initialize database:**
```bash
docker-compose exec backend python -m alembic upgrade head
```

6. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup

#### Backend Setup

1. **Create Python virtual environment:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
```

4. **Start PostgreSQL and Redis:**
```bash
# Using Docker
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:16
docker run -d -p 6379:6379 redis:7
```

5. **Run database migrations:**
```bash
alembic upgrade head
```

6. **Start the FastAPI server:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Set environment variables:**
```bash
# Create .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

3. **Start development server:**
```bash
npm run dev
```

4. **Open browser:**
Navigate to http://localhost:3000

## 🔐 Authentication

### JWT Authentication
- Access tokens: 30 minutes
- Refresh tokens: 7 days
- Secure password hashing with bcrypt

### Login/Register
- Email and password authentication
- Google OAuth (optional)
- Email verification (optional)
- Password reset via email

## 📊 Dashboard Features

### Analytics
- Monthly spending trends
- Income vs expenses chart
- Spending by category pie chart
- Financial health score
- Recent transactions list

### Transaction Management
- Add/edit/delete transactions
- Filter by date range, category, type
- Search functionality
- Tag support
- Receipt attachment

### Budgets
- Create category budgets
- Track budget progress
- Budget alerts
- Multiple budget types (50/30/20, zero-based, goal-based)

### Goals
- Create financial goals
- Track progress
- Calculate monthly savings needed
- Visualize goal timeline

## 🤖 AI Features

### Financial Assistant
- Chat interface for financial questions
- RAG (Retrieval Augmented Generation) integration
- Ollama local LLM support
- Context-aware responses using user data

### Receipt Scanner
- Upload JPG, PNG, or PDF receipts
- OCR text extraction
- Automatic data parsing
- Category suggestions
- Confidence score display

### Expense Categorization
- ML-based auto-categorization
- User feedback for training
- Support for custom categories

### Forecasting
- Monthly expense forecasting
- Income prediction
- Savings projection
- Confidence intervals

## 🛡️ Fraud Detection

- Duplicate transaction detection
- Anomaly detection using Isolation Forest
- Outlier detection using LOF
- Fraud alerts and notifications

## 📧 Email Notifications

- Budget alerts
- Fraud alerts
- Weekly summaries
- Goal reminders
- Integration with Resend email service

## 🌐 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout user

### Transactions
- `GET /api/v1/transactions` - Get all transactions
- `POST /api/v1/transactions` - Create transaction
- `GET /api/v1/transactions/{id}` - Get transaction
- `PUT /api/v1/transactions/{id}` - Update transaction
- `DELETE /api/v1/transactions/{id}` - Delete transaction
- `GET /api/v1/transactions/stats` - Get transaction stats
- `GET /api/v1/transactions/category-breakdown` - Category breakdown

### Analytics
- `GET /api/v1/analytics/financial-health` - Financial health score
- `GET /api/v1/analytics/spending-trends` - Spending trends
- `GET /api/v1/analytics/forecasts` - Expense forecasts
- `GET /api/v1/analytics/insights` - AI insights
- `GET /api/v1/analytics/subscriptions` - Subscriptions
- `GET /api/v1/analytics/fraud-alerts` - Fraud alerts

### Budgets
- `GET /api/v1/budgets` - Get all budgets
- `POST /api/v1/budgets` - Create budget
- `GET /api/v1/budgets/{id}` - Get budget
- `PUT /api/v1/budgets/{id}` - Update budget
- `DELETE /api/v1/budgets/{id}` - Delete budget

### Goals
- `GET /api/v1/goals` - Get all goals
- `POST /api/v1/goals` - Create goal
- `GET /api/v1/goals/{id}` - Get goal
- `PUT /api/v1/goals/{id}` - Update goal
- `DELETE /api/v1/goals/{id}` - Delete goal

### Receipts
- `POST /api/v1/receipts/upload` - Upload receipt
- `GET /api/v1/receipts` - Get all receipts
- `GET /api/v1/receipts/{id}` - Get receipt
- `DELETE /api/v1/receipts/{id}` - Delete receipt

### Chat
- `POST /api/v1/chat/message` - Send message
- `GET /api/v1/chat/history` - Get chat history
- `DELETE /api/v1/chat/history` - Clear history

## 🗄️ Database Schema

### Users
- id, email, name, hashed_password, avatar, role, is_active, is_verified

### Transactions
- id, user_id, type, amount, currency, category, merchant, description, date, tags, notes

### Budgets
- id, user_id, name, budget_type, amount, category, start_date, end_date

### Goals
- id, user_id, name, target_amount, current_amount, deadline, priority, status

### Receipts
- id, user_id, image_url, extracted_data, status, transaction_id

### Financial Health
- id, user_id, score, savings_rate, debt_ratio, income_stability, emergency_fund

### Chat History
- id, user_id, messages

## 📦 Deployment

### Frontend (Vercel)

1. **Connect repository to Vercel**
2. **Set environment variables:**
   - `NEXT_PUBLIC_API_URL` - Backend API URL
3. **Deploy**

### Backend (Railway)

1. **Connect repository to Railway**
2. **Add PostgreSQL service**
3. **Add Redis service**
4. **Set environment variables**
5. **Deploy**

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```
DATABASE_URL=postgresql://user:password@localhost/finnova_ai_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
RESEND_API_KEY=your-resend-api-key
OLLAMA_BASE_URL=http://localhost:11434
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📝 API Documentation

Swagger documentation available at: `http://localhost:8000/docs`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🙋 Support

For support, email support@finnovaai.com or create an issue in the repository.

## 🎯 Roadmap

- [ ] Multi-currency support
- [ ] Family/shared accounts
- [ ] Investment tracking
- [ ] Mobile app (React Native)
- [ ] Stock market integration
- [ ] Cryptocurrency tracking
- [ ] Tax optimization
- [ ] Bill payment integration
- [ ] Multi-language support

## 📚 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)
- [React Query Documentation](https://tanstack.com/query/latest)
- [Prophet Documentation](https://facebook.github.io/prophet)

---

**Finnova AI** - Empowering Financial Intelligence Through Technology
#   F I N N O V A - A I  
 #   F I N N O V A - A I  
 