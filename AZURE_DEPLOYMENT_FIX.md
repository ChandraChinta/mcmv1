# Azure Deployment Fix Instructions

## Issue
Azure App Service is trying to find virtual environment at `/home/site/wwwroot/antenv` which doesn't exist.

## Solution

### Step 1: Complete Azure Login
If you haven't completed the Azure login yet, complete it in your browser.

### Step 2: Find Your Web App
```powershell
# List all web apps
az webapp list --output table

# Note your web app name and resource group
```

### Step 3: Update Startup Command
Replace `YOUR_WEBAPP_NAME` and `YOUR_RESOURCE_GROUP` with your actual values:

```powershell
# Update the startup command to use our new startup.sh script
az webapp config set --resource-group YOUR_RESOURCE_GROUP --name YOUR_WEBAPP_NAME --startup-file "startup.sh"

# Or use this command to let Azure auto-detect Python app
az webapp config set --resource-group YOUR_RESOURCE_GROUP --name YOUR_WEBAPP_NAME --startup-file "gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app"
```

### Step 4: Configure Environment Variables
Make sure your Azure Web App has the required environment variables set:

```powershell
az webapp config appsettings set --resource-group YOUR_RESOURCE_GROUP --name YOUR_WEBAPP_NAME --settings @appsettings.json
```

Or set them individually:
```powershell
az webapp config appsettings set --resource-group YOUR_RESOURCE_GROUP --name YOUR_WEBAPP_NAME --settings AZURE_OPENAI_ENDPOINT="your-endpoint"
az webapp config appsettings set --resource-group YOUR_RESOURCE_GROUP --name YOUR_WEBAPP_NAME --settings AZURE_OPENAI_API_KEY="your-key"
az webapp config appsettings set --resource-group YOUR_RESOURCE_GROUP --name YOUR_WEBAPP_NAME --settings AZURE_OPENAI_DEPLOYMENT_NAME="your-deployment"
```

### Step 5: Deploy the Application

#### Option A: Deploy using Azure CLI (Recommended)
```powershell
# Deploy from local Git or zip
az webapp up --resource-group YOUR_RESOURCE_GROUP --name YOUR_WEBAPP_NAME --runtime "PYTHON:3.11"
```

#### Option B: Deploy using Git
```powershell
# Configure deployment source
az webapp deployment source config-local-git --resource-group YOUR_RESOURCE_GROUP --name YOUR_WEBAPP_NAME

# Add Azure remote and push
git remote add azure <git-url-from-previous-command>
git add .
git commit -m "Fix virtual environment configuration"
git push azure main
```

#### Option C: Deploy using ZIP
```powershell
# Create deployment package (excluding venv and other unnecessary files)
$exclude = @('venv', '__pycache__', '.git', '.env')
Compress-Archive -Path * -DestinationPath deploy.zip -Force -CompressionLevel Optimal

# Deploy the ZIP file
az webapp deployment source config-zip --resource-group YOUR_RESOURCE_GROUP --name YOUR_WEBAPP_NAME --src deploy.zip
```

### Step 6: Restart the Web App
```powershell
az webapp restart --resource-group YOUR_RESOURCE_GROUP --name YOUR_WEBAPP_NAME
```

### Step 7: Check Logs
```powershell
# Stream logs
az webapp log tail --resource-group YOUR_RESOURCE_GROUP --name YOUR_WEBAPP_NAME

# Or download logs
az webapp log download --resource-group YOUR_RESOURCE_GROUP --name YOUR_WEBAPP_NAME
```

## Alternative: Fix in Azure Portal

1. Go to Azure Portal (portal.azure.com)
2. Navigate to your App Service
3. Go to **Configuration** → **General settings**
4. Find **Startup Command** field
5. Clear the old command or set it to: `startup.sh`
6. Click **Save**
7. Go to **Deployment Center** and trigger a new deployment

## Files Updated
- ✅ Added `gunicorn` to requirements.txt
- ✅ Created `startup.sh` with proper Azure App Service configuration
- ✅ Startup script automatically detects PORT from Azure environment

## Testing Locally
To test the gunicorn setup locally:
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install updated requirements
pip install -r requirements.txt

# Test gunicorn
gunicorn --bind=0.0.0.0:5000 --timeout 600 app:app
```
