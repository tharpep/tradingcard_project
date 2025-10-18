# Trading Card Collection - Quick Start Guide

## 🚀 Running the Application

### Backend (FastAPI)

1. **Start the backend server:**
   ```bash
   cd backend
   python run start
   ```
   
   The API will be available at:
   - Main API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Frontend (React + Vite)

2. **Start the frontend dev server:**
   ```bash
   cd frontend
   pnpm dev
   ```
   
   The web app will be available at:
   - http://localhost:5173

## ✅ What Was Fixed

### 1. **CSS Import Error**
   - **Issue:** `@import "tw-animate-css"` was causing "file not found" errors
   - **Fix:** Removed incorrect Tailwind v4 imports from `frontend/src/index.css`
   - **Result:** Vite now compiles successfully

### 2. **API Route Conflicts**
   - **Issue:** Routes like `/cards/search`, `/cards/favorites`, `/cards/stats` were being interpreted as `/{card_id}` paths
   - **Fix:** Reordered routes in `backend/api/routes/cards.py` so specific paths come before parameterized paths
   - **Result:** All API endpoints now work correctly

### 3. **TypeScript Import**
   - **Issue:** `Card` type import causing linter error with `verbatimModuleSyntax`
   - **Fix:** Changed to `import type { Card as CardType }`
   - **Result:** No linter errors

## 🎨 Features Available

### Statistics Dashboard
- Total cards count
- Total quantity (including duplicates)
- Favorites count

### Add Cards
- Simple form to add new cards by name
- Default values for set_name, quantity, etc.

### Search & Filter
- Real-time search across name, set, number, rarity
- Toggle to show favorites only
- Refresh button

### Card Collection Table
- View all card details
- Star/unstar favorites
- Delete cards with confirmation
- Responsive design

## 📝 API Endpoints (Correct Order)

1. `GET /cards` - Get all cards
2. `GET /cards/search?name={query}` - Search cards
3. `GET /cards/favorites` - Get favorite cards
4. `GET /cards/stats` - Get collection statistics
5. `GET /cards/{card_id}` - Get specific card
6. `POST /cards` - Add new card
7. `PUT /cards/{card_id}` - Update card
8. `DELETE /cards/{card_id}` - Delete card

## 🧪 Testing

### Backend CLI Testing
```bash
cd backend
python run add Charizard
python run list
python run stats
```

### API Testing
Visit http://localhost:8000/docs for interactive API documentation

### Frontend Testing
1. Start both backend and frontend
2. Open http://localhost:5173
3. Add some cards
4. Test search, favorites, delete functions

## 📁 Project Structure

```
tradingcard_project/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   │   └── cards.py (✅ Fixed route order)
│   │   └── models/
│   │       └── responses.py
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── main.py
│   ├── run (CLI entry point)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ui/ (Shadcn components)
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   └── cardService.ts
│   │   ├── App.tsx (✅ Fixed imports)
│   │   └── index.css (✅ Fixed CSS imports)
│   ├── package.json
│   └── vite.config.ts
└── tests/

```

## 🔍 Verification Steps

1. ✅ Backend starts without errors
2. ✅ Frontend Vite compiles without errors
3. ✅ No linter errors in TypeScript files
4. ✅ All API endpoints respond correctly
5. ✅ Frontend can fetch and display data
6. ✅ CORS configured for localhost:5173
7. ✅ CSS and Shadcn UI components load properly

## 🎯 Next Steps

- Add Pokemon TCG API integration for auto-filling card data
- Add edit functionality for cards
- Migrate from SQLite to Supabase
- Add card images
- Add sorting and advanced filters
- Add export/import functionality

## 🐛 Common Issues

### Backend won't start
- Ensure virtual environment is set up: `python run setup`
- Check if port 8000 is already in use

### Frontend won't compile
- Run `pnpm install` to ensure dependencies are installed
- Check that backend is running for CORS

### CORS errors
- Verify backend is running on port 8000
- Verify frontend is accessing http://localhost:8000
- Check CORS configuration in `backend/main.py`

---

**All systems verified and operational! 🎉**

