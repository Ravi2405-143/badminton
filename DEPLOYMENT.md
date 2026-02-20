# Deploying to Vercel Guide

Follow these steps to deploy the Sportify Tournament Manager to Vercel.

## 1. Prerequisites
- Have a [Vercel account](https://vercel.com).
- Push your code to GitHub (already done).

## 2. Deploy on Vercel

1. Go to [vercel.com](https://vercel.com) → **Add New Project**
2. Import your GitHub repo (`Ravi2405-143/badminton`)
3. Set **Root Directory** to `backend`
4. Click **Deploy**

---

## 3. Fix Data Erasure — Add a Permanent Database ⚠️

> [!IMPORTANT]
> By default, Vercel uses serverless functions with an ephemeral filesystem.
> Data stored in SQLite (`/tmp`) is **wiped on every cold start**.
> You **must** connect a permanent database to persist your tournaments.

### Step-by-step: Vercel Postgres (Free)

1. Go to your Vercel project dashboard
2. Click **Storage** tab → **Create Database** → choose **Postgres**
3. Name it (e.g. `sportify-db`) and click **Create & Continue**
4. Vercel will add environment variables automatically. You're done!
5. Click **Redeploy** — your data will now persist permanently ✅

### Or: Use Supabase (also free)

1. Go to [supabase.com](https://supabase.com) → create a new project
2. Go to **Project Settings** → **Database** → copy the **Connection String (URI)**
3. In Vercel → your project → **Settings** → **Environment Variables**
4. Add: `DATABASE_URL` = `<your supabase connection string>`
5. Redeploy ✅

---

## 4. How It Works

The app automatically detects the database:
- If `DATABASE_URL` env var is set → uses **PostgreSQL** (permanent ✅)
- If not set → uses local **SQLite** (development only)
