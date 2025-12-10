# Production-Grade Authentication System

A complete authentication system built from scratch with FastAPI (backend) and Next.js (frontend).

## 🚀 Features

- ✅ User Registration & Login
- ✅ JWT Token Authentication (Access + Refresh)
- ✅ Bcrypt Password Hashing (12 rounds)
- ✅ Rate Limiting (5 requests/minute)
- ✅ Account Lockout (5 failed attempts)
- ✅ Audit Logging
- ✅ PostgreSQL Database
- ✅ CORS Protection
- ✅ Security Headers
- ✅ Password Strength Validation

## 📁 Project Structure

```
auth-system/
├── backend/          # FastAPI application
├── frontend/         # Next.js application
└── docker-compose.yml
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL (or use Docker)

---

### Step 1: Clone and Setup

```bash
# Create project directory
mkdir auth-system
cd auth-system

# Create backend and frontend directories with the files provided
```

---

### Step 2: Setup PostgreSQL Database

**Option A: Using Docker (Recommended)**

```bash
# Start PostgreSQL with Docker Compose
docker-compose up -d

# Wait for database to be ready (check with)
docker-compose logs postgres
```

**Option B: Local PostgreSQL**

```bash
# Create database
createdb authdb

# Create user
psql -d authdb -c "CREATE USER authuser WITH PASSWORD 'authpassword';"
psql -d authdb -c "GRANT ALL PRIVILEGES ON DATABASE authdb TO authuser;"

# Run migrations
psql -d authdb -U authuser -f backend/migrations/init.sql
```

---

### Step 3: Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env file if needed (optional)
# nano .env

# Run migrations (if not done in Step 2)
psql -h localhost -U authuser -d authdb -f migrations/init.sql

# Start backend server
python run.py
```

Backend will run on: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

---

### Step 4: Setup Frontend

**Open a new terminal window**

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: **http://localhost:3000**

---

## 🧪 Testing the Application

### 1. Register a New User

- Go to: http://localhost:3000/register
- Fill in the form:
  - Email: `test@example.com`
  - Username: `testuser`
  - Password: `Test@12345678` (must meet requirements)
- Click "Register"

### 2. Login

- Go to: http://localhost:3000/login
- Enter your credentials
- Click "Login"

### 3. Access Dashboard

- After login, you'll be redirected to the dashboard
- You'll see your user information
- Click "Test Protected API" to test token authentication

### 4. Test API Directly

```bash
# Register user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "api@example.com",
    "username": "apiuser",
    "password": "ApiTest@12345"
  }'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email_or_username": "apiuser",
    "password": "ApiTest@12345"
  }'

# Save the access_token from response, then:

# Access protected route
curl -X GET http://localhost:8000/auth/protected \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

---

## 📊 Database Schema

The system uses 4 main tables:

1. **users** - User accounts
2. **sessions** - Refresh token storage
3. **verification_tokens** - Email verification (future)
4. **audit_logs** - Security audit trail

View the complete schema in `backend/migrations/init.sql`

---

## 🔐 Security Features

### Password Security
- Minimum 12 characters
- Must include: uppercase, lowercase, number, special character
- Bcrypt hashing with cost factor 12

### Token Security
- Access tokens: 15 minutes expiry
- Refresh tokens: 7 days expiry
- Token rotation on refresh

### Account Protection
- Rate limiting: 5 attempts per minute
- Account lockout: 5 failed login attempts → 30 min lock
- Audit logging: All auth activities logged

### API Security
- CORS protection
- Security headers (XSS, Clickjacking protection)
- SQL injection prevention (parameterized queries)

---

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check if PostgreSQL is running
docker-compose ps

# Check database connection
psql -h localhost -U authuser -d authdb -c "SELECT 1;"

# Check Python version
python --version  # Should be 3.10+
```

### Frontend won't start

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Should be 18+
```

### CORS errors

Make sure `FRONTEND_URL` in `backend/.env` matches your frontend URL:
```
FRONTEND_URL=http://localhost:3000
```

### Database connection errors

1. Check if PostgreSQL is running: `docker-compose ps`
2. Check credentials in `backend/.env`
3. Ensure database is initialized: `docker-compose logs postgres`

---

## 📝 Environment Variables

### Backend (.env)

```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=authdb
DATABASE_USER=authuser
DATABASE_PASSWORD=authpassword

JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

ENVIRONMENT=development
API_HOST=0.0.0.0
API_PORT=8000

FRONTEND_URL=http://localhost:3000
```

### Generate Secure Keys

```bash
# Generate JWT secret
openssl rand -hex 32

# Or use Python
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🚀 Production Deployment

### Backend

1. Set `ENVIRONMENT=production` in `.env`
2. Use strong secret keys
3. Enable HTTPS
4. Use environment variables for secrets
5. Set up proper logging
6. Use production WSGI server (Gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Frontend

```bash
npm run build
npm start
```

### Database

1. Use managed PostgreSQL (AWS RDS, Google Cloud SQL)
2. Enable SSL connections
3. Set up automated backups
4. Configure connection pooling

---

## 📚 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/register` | POST | Register new user |
| `/auth/login` | POST | Login user |
| `/auth/refresh` | POST | Refresh access token |
| `/auth/logout` | POST | Logout user |
| `/auth/me` | GET | Get current user (protected) |
| `/auth/protected` | GET | Example protected route |
| `/health` | GET | Health check |
| `/docs` | GET | API documentation |

---

## 🎓 Learning Resources

This project demonstrates:

- RESTful API design
- JWT authentication flow
- Password hashing best practices
- Database design and indexing
- Security headers and CORS
- Rate limiting implementation
- Audit logging
- Frontend-backend integration

---

## 📄 License

MIT License - Feel free to use for learning and interviews!

---

## 🤝 Contributing

This is a learning project. Feel free to:
- Add features (email verification, password reset)
- Improve security
- Optimize performance
- Add tests

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the logs: `docker-compose logs`
3. Ensure all dependencies are installed
4. Verify database is running

Happy coding! 🚀