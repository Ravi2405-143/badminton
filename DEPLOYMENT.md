# Deploying to Vercel Guide

Follow these steps to deploy the Sportify Tournament Manager to Vercel.

## 1. Prerequisites
- Have a [Vercel account](https://vercel.com).
- Install the [Vercel CLI](https://vercel.com/docs/cli) (optional, but recommended) or connect your GitHub repository.

## 2. Deployment Steps

### Option A: Vercel CLI (Fastest)
1. Open your terminal in the `backend` directory.
2. Run the command:
   ```bash
   vercel
   ```
3. Follow the prompts (Select "Yes" for "Link to existing project?" if applicable).
4. When asked for the build command, leave it blank (Vercel will detect FastAPI).

### Option B: GitHub Integration
1. Push your code to a GitHub repository.
2. Go to the Vercel Dashboard and click "Add New" > "Project".
3. Import your repository.
4. Set the **Root Directory** to `backend`.
5. Click **Deploy**.

## 3. Important Notes on Data ⚠️

> [!WARNING]
> **Data Resets on Restart**
> Because Vercel uses serverless functions, the `tournament.db` file will be **cleared** every time the app redeploys or restarts. 

### To persist data permanently:
1. Create a **Vercel Postgres** database in your Vercel project dashboard.
2. Vercel will automatically add a `POSTGRES_URL` environment variable.
3. In your Vercel Project Settings, add an Environment Variable named `DATABASE_URL` and copy the value from `POSTGRES_URL`.
4. The app will automatically switch to the permanent database on next deploy!
