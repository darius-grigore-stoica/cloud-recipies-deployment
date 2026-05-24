# 🍴 Récipes — Recipe Sharing App

A full-stack recipe sharing web app built with **FastAPI** + **Azure** (3 services).

---

## 🏗️ Azure Services Used

| Service | Purpose |
|---|---|
| **Azure App Service** | Hosts and runs the FastAPI backend + HTML frontend |
| **Azure SQL Database** | Stores all recipe data (titles, ingredients, steps, etc.) |
| **Azure Blob Storage** | Stores recipe photos uploaded by users |

---

## 📁 Project Structure

```
recipe-app/
├── main.py              ← FastAPI app entry point
├── database.py          ← Azure SQL connection
├── models.py            ← Database table definitions
├── schemas.py           ← Request/response data shapes
├── blob_storage.py      ← Azure Blob Storage helper
├── routers/
│   └── recipes.py       ← All /api/recipes endpoints
├── templates/
│   └── index.html       ← The whole frontend (HTML + CSS + JS)
├── requirements.txt     ← Python dependencies
├── startup.sh           ← Azure App Service startup command
├── .env.example         ← Template for your environment variables
└── .gitignore
```

---

## 🚀 Azure Setup (Step by Step)

### STEP 1 — Create an Azure Account
Go to https://azure.microsoft.com/free/students
Sign up with your school email → you get $100 free credit.

---

### STEP 2 — Create Azure SQL Database

1. In the Azure Portal (portal.azure.com), click **"Create a resource"**
2. Search for **"SQL Database"** → Click Create
3. Fill in:
   - **Resource Group**: Create new → name it `recipes-rg`
   - **Database name**: `recipes-db`
   - **Server**: Create new →
     - Server name: `recipes-server-YOURNAME` (must be globally unique)
     - Location: pick the closest to you
     - Authentication: **SQL Authentication**
     - Admin login: `recipeadmin`
     - Password: something strong (save this!)
   - **Compute + storage**: Click "Configure database" → pick **Basic** (cheapest, ~$5/mo or free tier)
4. Click **Review + Create** → **Create**

After it deploys:
- Go to the SQL Server → **Networking** → Add your current IP under "Firewall rules"
- Also check **"Allow Azure services and resources to access this server"**

Get the connection string:
- Go to your SQL Database → **Connection strings** → copy the values for:
  - Server: `your-server.database.windows.net`
  - Username and password you set above

---

### STEP 3 — Create Azure Blob Storage

1. Click **"Create a resource"** → Search **"Storage account"** → Create
2. Fill in:
   - **Resource Group**: same `recipes-rg`
   - **Storage account name**: `recipesphotosYOURNAME` (lowercase, no spaces, globally unique)
   - **Region**: same as your SQL server
   - **Performance**: Standard
   - **Redundancy**: LRS (cheapest)
3. Click **Review + Create** → **Create**

Get the connection string:
- Go to your Storage Account → **Access keys**
- Copy **Connection string** under key1

---

### STEP 4 — Set Up Your .env File

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```env
SQL_SERVER=recipes-server-YOURNAME.database.windows.net
SQL_DATABASE=recipes-db
SQL_USERNAME=recipeadmin
SQL_PASSWORD=YourPasswordHere

AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_STORAGE_CONTAINER=recipe-images

SECRET_KEY=pick-any-random-string-here
```

---

### STEP 5 — Test Locally

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the app
uvicorn main:app --reload

# Open your browser to:
# http://localhost:8000
```

The app will automatically create the database tables on first run.

---

### STEP 6 — Deploy to Azure App Service

#### Option A: Deploy from VS Code (easiest)
1. Install the **Azure App Service** extension in VS Code
2. Sign in to Azure
3. Right-click your project folder → **"Deploy to Web App"**
4. Choose **"Create new Web App"**
   - Name: `recipes-app-YOURNAME`
   - Runtime: **Python 3.11**
   - Pricing: **Free (F1)**

#### Option B: Deploy from GitHub (recommended for class)
1. Push your code to a GitHub repo (don't commit `.env`!)
2. In Azure Portal → App Service → **Deployment Center**
3. Source: **GitHub** → connect your repo → Save

#### After deploying — Set Environment Variables:
In Azure Portal → App Service → **Configuration** → **Application settings**
Add each variable from your `.env` file here (this is how Azure reads them instead of the .env file).

#### Set Startup Command:
In Azure Portal → App Service → **Configuration** → **General settings**
Startup command: `uvicorn main:app --host 0.0.0.0 --port 8000`

---

## 🔌 API Endpoints

| Method | URL | What it does |
|--------|-----|-------------|
| GET | `/api/recipes/` | List all recipes |
| GET | `/api/recipes/?category=Dinner` | Filter by category |
| GET | `/api/recipes/{id}` | Get one recipe |
| POST | `/api/recipes/` | Create a recipe (multipart form) |
| PUT | `/api/recipes/{id}` | Update a recipe |
| DELETE | `/api/recipes/{id}` | Delete a recipe |
| GET | `/health` | Health check (Azure uses this) |
| GET | `/docs` | Auto-generated API docs (Swagger UI) |

---

## 💡 Tips

- FastAPI auto-generates interactive API docs at `/docs` — great for testing!
- If images don't show up, make sure the Blob Storage container is set to **public access**
- If you get a connection error to SQL, double-check the firewall rules in Azure Portal
