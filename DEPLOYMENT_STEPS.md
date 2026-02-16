# Deployment Steps - Azure MCM App Service

## Current Status
- Login attempted but MFA authentication is required
- Two tenants detected:
  - `0d1469f6-b977-4eb1-a160-c99b4bae5e4c` (Default Directory)
  - `ec42d4c9-b0e2-47dc-853a-85a9353b2863` (csazuread)

## Step-by-Step Deployment

### Step 1: Complete Azure Login with MFA
Open a **NEW PowerShell terminal** and run:

```powershell
# Login with the csazuread tenant (most likely has your subscriptions)
az login --tenant ec42d4c9-b0e2-47dc-853a-85a9353b2863

# Complete MFA in the browser that opens
# After completion, verify login:
az account show
```

If that doesn't work, try the other tenant:
```powershell
az login --tenant 0d1469f6-b977-4eb1-a160-c99b4bae5e4c
```

### Step 2: Verify Subscriptions
```powershell
az account list --output table
```

If you see subscriptions, set the default:
```powershell
az account set --subscription "YOUR_SUBSCRIPTION_NAME_OR_ID"
```

### Step 3: Find the MCM App Service
```powershell
az webapp list --query "[?contains(name, 'mcm')]" --output table
```

Note the `Name` and `ResourceGroup` values.

### Step 4: Deploy Using Automated Script
```powershell
# Navigate to your project directory
cd C:\mcm

# Run the deployment script
.\deploy-azure.ps1
```

The script will automatically:
- Find the MCM app service
- Update the startup command  
- Deploy the application
- Restart the service

**OR Manual Deployment:**

```powershell
# Replace with your actual values
$rg = "YOUR_RESOURCE_GROUP"
$app = "mcm"  # or your actual app name

# Update startup command
az webapp config set --resource-group $rg --name $app --startup-file "startup.sh"

# Deploy applicationaz webapp up --resource-group $rg --name $app --runtime "PYTHON:3.11"

# Restart
az webapp restart --resource-group $rg --name $app

# View logs
az webapp log tail --resource-group $rg --name $app
```

### Step 5: Verify Deployment
```powershell
# Get app URL
az webapp show --name $app --resource-group $rg --query defaultHostName -o tsv

# Test the endpoint
$url = "https://$(az webapp show --name $app --resource-group $rg --query defaultHostName -o tsv)"
curl "$url/api/services"
```

## What Was Fixed
✅ Added `gunicorn` to requirements.txt (production WSGI server)
✅ Created `startup.sh` with proper Azure App Service configuration
✅ Removed hardcoded virtual environment paths
✅ Configured proper port binding from Azure environment

## Troubleshooting

### If you get "No subscriptions found":
- Contact your Azure administrator to grant you subscription access
- Or login with a different account that has subscriptions

### If MFA keeps failing:
- Clear browser cache and try again
- Use `az login --use-device-code` for alternative auth method
- Contact your IT administrator about MFA settings

### If deployment fails:
- Check you have contributor access to the resource group
- Verify the app service exists: `az webapp show --name mcm --resource-group YOUR_RG`
- Check deployment logs: `az webapp log download --name mcm --resource-group YOUR_RG`
