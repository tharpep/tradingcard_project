# Trading Card Collection Manager

A modern web application for managing Pokemon trading card collections, built with React, FastAPI, and Supabase. Features multi-user support with admin CLI for system management.

## Features

- **Multi-User Support** - User authentication and data isolation
- **Admin CLI** - Full system management via command line
- **Collection Statistics** - Track total cards, quantity, and favorites
- **Smart Search** - Search by name, set, card number, or rarity
- **Favorites System** - Mark your favorite cards
- **Responsive Design** - Works on desktop and mobile
- **Modern UI** - Built with Shadcn UI components
- **Fast Performance** - Optimized with Vite and FastAPI
- **Cloud Database** - Supabase PostgreSQL with Row Level Security

## Architecture

### Backend (FastAPI + Supabase)
- **FastAPI** - Modern Python web framework
- **Supabase** - Cloud PostgreSQL database with Row Level Security
- **Repository Pattern** - Clean data access layer with REST API
- **Service Layer** - Business logic separation with user context
- **Admin CLI** - Full system management via command line
- **Authentication** - Supabase Auth integration

### Frontend (React + TypeScript)
- **React 19** - Latest React with hooks
- **TypeScript** - Type-safe development with UUID support
- **Vite** - Fast build tool and dev server
- **Shadcn UI** - Beautiful, accessible components
- **Tailwind CSS** - Utility-first styling
- **User Authentication** - Supabase Auth integration (planned)

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- pnpm (recommended) or npm
- Supabase account and project

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd tradingcard_project
```

### 2. Backend Setup
```bash
cd backend

# Set up Supabase environment variables
# Create .env file in project root with:
# SUPABASE_URL=your_supabase_url
# SUPABASE_KEY=your_supabase_anon_key
# 
# Get these values from your Supabase project dashboard

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

# Regular Commands
python run add "Charizard"
python run add "Pikachu" --set "Base Set" --rarity "Common"
python run list
python run search "Char"
python run stats
python run start
python run test
python run help

# Admin Commands (Full System Access)
python run users                    # List all users
python run cards all               # Show ALL cards from ALL users
python run cards user <user_id>    # Show cards for specific user
python run stats all               # System-wide statistics
python run clear                   # Delete all cards (admin only)
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

### Cards Table (Supabase)
```sql
CREATE TABLE cards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    set_name VARCHAR(255) NOT NULL DEFAULT 'Unknown',
    card_number VARCHAR(50),
    rarity VARCHAR(50),
    quantity INTEGER NOT NULL DEFAULT 1,
    is_favorite BOOLEAN NOT NULL DEFAULT false,
    date_added TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES auth.users(id)
);

-- Row Level Security
ALTER TABLE cards ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can only access their own cards" ON cards
FOR ALL USING (user_id = auth.uid() OR user_id IS NULL);
```

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Configuration

### Backend Configuration
- **Database**: Supabase PostgreSQL (cloud)
- **Port**: 8000
- **CORS**: Enabled for `http://localhost:5173`
- **Authentication**: Supabase Auth integration
- **Admin CLI**: Full system access via API keys

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
- **Frontend Authentication** - User signup/signin
- **Mobile App** - React Native version
- **Import/Export** - CSV/JSON data exchange
- **Admin Dashboard** - Web-based admin interface
- **Card Trading** - User-to-user card exchanges

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
- Check Supabase connection and API keys
- Verify environment variables in `.env` file
- Run `python run test test_supabase_connection` to test connection

## Multi-User Architecture

### User Data Isolation
- **Row Level Security (RLS)**: Users can only access their own cards
- **Admin Override**: CLI has full system access for management
- **Anonymous Cards**: Visible to all users (for testing/sharing)

### Admin CLI Features
- **System Management**: View all users and cards across the system
- **User Administration**: List users, view user-specific data
- **Data Analytics**: System-wide statistics and insights
- **Batch Operations**: Clear all data, manage collections

### Authentication Flow
- **Frontend Users**: Will use Supabase Auth (signup/signin)
- **Admin CLI**: Bypasses authentication (uses API keys)
- **Data Security**: RLS policies ensure proper data isolation

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