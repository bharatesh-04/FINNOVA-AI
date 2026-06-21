# Finnova AI - Getting Started Guide

## Quick Start (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- Git installed
- ~5GB free disk space

### Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd FINNOVA-AI
```

2. **Run setup script**

**On macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**On Windows:**
```bash
setup.bat
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

4. **Create an account**
- Click "Sign Up" on the login page
- Enter your email and password
- Start tracking expenses!

---

## Manual Setup

### Backend Setup

1. **Install Python 3.12+**

2. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
```

5. **Install PostgreSQL and Redis**

**Using Docker:**
```bash
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:16
docker run -d -p 6379:6379 redis:7
```

**Or install locally from:**
- PostgreSQL: https://www.postgresql.org/download/
- Redis: https://redis.io/download

6. **Start backend**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install Node.js 18+**

2. **Install dependencies**
```bash
cd frontend
npm install
```

3. **Create .env.local**
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

4. **Start development server**
```bash
npm run dev
```

5. **Open in browser**
Navigate to http://localhost:3000

---

## Features to Explore

### Dashboard
- View your financial overview
- See spending trends
- Check recent transactions

### Transactions
- Add expenses and income
- Categorize transactions
- Search and filter

### Budgets
- Create monthly budgets
- Track spending against budgets
- Get alerts when over budget

### Goals
- Set savings goals
- Track progress
- Get timeline predictions

### Receipt Scanner
- Upload receipt photos
- Automatic data extraction
- Create transactions from receipts

### AI Assistant
- Chat about your finances
- Ask spending questions
- Get personalized advice

### Reports
- Generate financial reports
- Export to PDF/CSV
- Get weekly summaries

---

## Troubleshooting

### Port already in use
If port 3000 or 8000 is already in use:
```bash
# Find and kill process on port
# On macOS/Linux:
lsof -ti:3000 | xargs kill -9

# On Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Database connection error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database credentials

### Redis connection error
- Ensure Redis is running
- Check REDIS_URL in .env

### Module not found errors
- Reinstall dependencies: `pip install -r requirements.txt`
- Or: `npm install`

### API not responding
- Check backend logs
- Verify NEXT_PUBLIC_API_URL in frontend .env.local
- Ensure CORS is properly configured

---

## First Steps

1. **Create an account**
   - Go to http://localhost:3000
   - Click "Sign Up"
   - Enter your details

2. **Add your first transaction**
   - Click "Add Transaction" on dashboard
   - Fill in the details
   - Click "Add Transaction"

3. **Set a budget**
   - Go to Budgets
   - Click "Add Budget"
   - Set your budget limits

4. **Explore AI features**
   - Go to "AI Assistant"
   - Ask a question about your finances

---

## Common Questions

**Q: Can I use this offline?**
A: No, the application requires internet connection and running backend.

**Q: Is my data encrypted?**
A: Data is transmitted via HTTPS and passwords are hashed with bcrypt.

**Q: Can I export my data?**
A: Yes, you can export transactions as CSV from the transactions page.

**Q: How do I reset my password?**
A: Use the "Forgot Password" link on the login page (email service required).

---

## Next Steps

- Read the [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Explore the API documentation at http://localhost:8000/docs
- Join the community and contribute!

---

## Support

For issues or questions:
1. Check the [README.md](README.md)
2. Check existing issues on GitHub
3. Create a new issue with details

Happy tracking! 🎉
