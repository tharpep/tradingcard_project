# Database Schema Management

This folder contains SQL scripts and schema documentation for the Supabase database.

## 📁 Structure

- `SETUP_SUPABASE.sql` - **Main setup file (use this!)**
- `schema/` - Individual schema files (reference)
- `migrations/` - Migration files (reference)
- `seeds/` - Sample data for development
- `docs/` - Schema documentation and review

## 🚀 Quick Start (2 Steps!)

### **Step 1: Run Main Setup**
1. Open your Supabase project → SQL Editor
2. Copy entire contents of `SETUP_SUPABASE.sql`
3. Paste and click **Run**
4. Verify `cards` table appears in Table Editor

### **Step 2: Add Sample Data (Optional)**
1. Copy contents of `seeds/sample_cards.sql`
2. Paste into SQL Editor and click **Run**
3. See 30 sample cards in your database

**That's it!** Your database is ready.

## 🔧 Repository Integration

The existing repository pattern will be updated to use Supabase instead of SQLite:

- `CardRepository` → `SupabaseCardRepository`
- Keep same interface, change backend
- Easy migration path

## 📋 Schema Design Principles

1. **Modular**: Easy to add new features
2. **Scalable**: Ready for user authentication
3. **Consistent**: Follows Supabase best practices
4. **Secure**: Row Level Security (RLS) ready

## 🎯 Key Features

- ✅ **Duplicate Prevention**: Unique constraint on (name, set, number, user)
- ✅ **Auto Quantity Increment**: `add_or_increment_card()` function
- ✅ **Tag Searching**: PostgreSQL array with GIN index
- ✅ **Performance**: 14 indexes for fast queries
- ✅ **Safety**: Idempotent (safe to re-run)
