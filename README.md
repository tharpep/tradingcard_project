# Trading Card Collection Manager

A modern web application for managing your Pokemon trading card collection, built with React, FastAPI, and SQLite.

## Features

- **Collection Statistics** - Track total cards, quantity, and favorites
- **Smart Search** - Search by name, set, card number, or rarity
- **Favorites System** - Mark your favorite cards
- **Responsive Design** - Works on desktop and mobile
- **Modern UI** - Built with Shadcn UI components
- **Fast Performance** - Optimized with Vite and FastAPI

## Architecture

### Backend (FastAPI + SQLite)
- **FastAPI** - Modern Python web framework
- **SQLite** - Local database (easily migratable to Supabase)
- **Repository Pattern** - Clean data access layer
- **Service Layer** - Business logic separation
- **CLI Interface** - Test functionality via command line

### Frontend (React + TypeScript)
- **React 19** - Latest React with hooks
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Shadcn UI** - Beautiful, accessible components
- **Tailwind CSS** - Utility-first styling

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- pnpm (recommended) or npm

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd tradingcard_project
```

### 2. Backend Setup
```bash
cd backend
python run setup    # Creates venv and installs dependencies
python run start    # Starts FastAPI server on http://localhost:8000
```

### 3. Frontend Setup
```bash
cd frontend
pnpm install        # Install dependencies
pnpm dev           # Starts Vite dev server on http://localhost:5173
```

### 4. Access the Application
- **Web App**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## Usage

### Web Interface
1. **Add Cards** - Enter card name to add to collection
2. **View Collection** - Browse all cards in a responsive table
3. **Search & Filter** - Find cards by name, set, or rarity
4. **Manage Favorites** - Star/unstar cards
5. **View Statistics** - See collection overview

### CLI Commands (Backend)
```bash
cd backend

# Setup
python run setup

# Add cards
python run add "Charizard"
python run add "Pikachu" --set "Base Set" --rarity "Common"

# List all cards
python run list

# Search cards
python run search "Char"

# View statistics
python run stats

# Start API server
python run start

# Run tests
python run test

# Get help
python run help
```

## Project Structure

```
tradingcard_project/
├── backend/                 # FastAPI backend
│   ├── api/                # API routes and models
│   │   ├── routes/         # FastAPI route handlers
│   │   └── models/         # Pydantic response models
│   ├── database/           # Database connection and schema
│   ├── models/             # Pydantic data models
│   ├── repositories/       # Data access layer
│   ├── services/           # Business logic layer
│   ├── main.py            # FastAPI app entry point
│   ├── run                # CLI entry point
│   └── requirements.txt   # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   │   └── ui/        # Shadcn UI components
│   │   ├── services/       # API service layer
│   │   ├── App.tsx        # Main React component
│   │   └── index.css      # Global styles
│   ├── package.json       # Node.js dependencies
│   └── vite.config.ts     # Vite configuration
├── tests/                  # Test suite
├── PLAN.md                # Project planning document
├── QUICKSTART.md          # Quick start guide
└── README.md              # This file
```

## Development

### Backend Development
```bash
cd backend

# Install dependencies
python run setup

# Run tests
python run test

# Start development server
python run start

# Add new card via CLI
python run add "Test Card"
```

### Frontend Development
```bash
cd frontend

# Install dependencies
pnpm install

# Start development server
pnpm dev

# Build for production
pnpm build

# Preview production build
pnpm preview
```

### API Development
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **Health Check**: http://localhost:8000/health

## Testing

### Backend Tests
```bash
cd backend
python run test
```

### Manual Testing
1. Start backend: `cd backend && python run start`
2. Start frontend: `cd frontend && pnpm dev`
3. Open http://localhost:5173
4. Add some cards and test functionality

## Database Schema

### Cards Table
```sql
CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    set_name TEXT NOT NULL DEFAULT 'Unknown',
    card_number TEXT,
    rarity TEXT,
    quantity INTEGER NOT NULL DEFAULT 1,
    is_favorite BOOLEAN NOT NULL DEFAULT 0,
    date_added TEXT NOT NULL
);
```

## Configuration

### Backend Configuration
- **Database**: SQLite (`backend/cards.db`)
- **Port**: 8000
- **CORS**: Enabled for `http://localhost:5173`

### Frontend Configuration
- **Port**: 5173
- **API Base URL**: `http://localhost:8000`
- **Build Tool**: Vite
- **UI Library**: Shadcn UI

## Deployment

### Docker Deployment
```bash
# Build and run with Docker
docker build -t trading-card-app ./backend
docker run -p 8000:8000 trading-card-app
```

### Google Cloud Run
1. Build Docker image
2. Push to Google Container Registry
3. Deploy to Cloud Run
4. Configure environment variables

## Future Enhancements

- **Pokemon TCG API Integration** - Auto-fill card data
- **Card Images** - Display card artwork
- **Advanced Analytics** - Collection insights
- **Cloud Database** - Migrate to Supabase
- **Mobile App** - React Native version
- **Import/Export** - CSV/JSON data exchange
- **Multi-user** - User accounts and sharing

## Troubleshooting

### Common Issues

**Backend won't start:**
- Ensure Python 3.11+ is installed
- Run `python run setup` to create virtual environment
- Check if port 8000 is available

**Frontend won't compile:**
- Run `pnpm install` to install dependencies
- Check Node.js version (18+)
- Clear cache: `pnpm store prune`

**CORS errors:**
- Ensure backend is running on port 8000
- Check CORS configuration in `backend/main.py`
- Verify frontend is accessing correct API URL

**Database errors:**
- Delete `backend/cards.db` to reset database
- Run `python run setup` to reinitialize

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cards` | Get all cards |
| GET | `/cards/search?name={query}` | Search cards |
| GET | `/cards/favorites` | Get favorite cards |
| GET | `/cards/stats` | Get collection statistics |
| GET | `/cards/{id}` | Get specific card |
| POST | `/cards` | Add new card |
| PUT | `/cards/{id}` | Update card |
| DELETE | `/cards/{id}` | Delete card |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- **Shadcn UI** - Beautiful component library
- **FastAPI** - Modern Python web framework
- **React** - Frontend library
- **Tailwind CSS** - Utility-first CSS framework

---

For detailed setup instructions, see [QUICKSTART.md](QUICKSTART.md)
For project planning details, see [PLAN.md](PLAN.md)