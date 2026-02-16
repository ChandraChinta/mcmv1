# Quick Deploy Script for Azure
# Run this after completing az login

param(
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroup,
    
    [Parameter(Mandatory=$false)]
    [string]$WebAppName,
    
    [Parameter(Mandatory=$false)]
    [string]$TenantId
)

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Azure App Service Deployment Fix" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if logged in
Write-Host "Checking Azure login status..." -ForegroundColor Yellow
$account = az account show 2>$null
if (-not $account) {
    Write-Host "Not logged in. Starting Azure login..." -ForegroundColor Red
    
    if ($TenantId) {
        Write-Host "Logging in with tenant: $TenantId" -ForegroundColor Yellow
        az login --tenant $TenantId
    } else {
        az login
    }
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Login failed. Please complete MFA in browser." -ForegroundColor Red
        exit 1
    }
}

Write-Host "✓ Logged in successfully" -ForegroundColor Green
Write-Host ""

# List subscriptions
Write-Host "Available subscriptions:" -ForegroundColor Yellow
az account list --query '[].{Name:name, ID:id, Default:isDefault}' --output table
Write-Host ""

# If no subscription found, set one
$subs = az account list --query '[].id' -o tsv
if (-not $subs) {
    Write-Host "✗ No subscriptions found. Please check your account permissions." -ForegroundColor Red
    exit 1
}

# Get or prompt for web app details if not provided
if (-not $WebAppName -or -not $ResourceGroup) {
    Write-Host "Searching for 'mcm' app service..." -ForegroundColor Yellow
    $webapps = az webapp list --query '[?contains(name, `mcm`)].{Name:name, ResourceGroup:resourceGroup, State:state, DefaultHostName:defaultHostName}' --output json | ConvertFrom-Json
    
    if ($webapps.Count -eq 0) {
        Write-Host "✗ No web apps found with 'mcm' in name" -ForegroundColor Red
        Write-Host ""
        Write-Host "All web apps:" -ForegroundColor Yellow
        az webapp list --output table
        exit 1
    }
    
    Write-Host "Found web apps:" -ForegroundColor Green
    $webapps | ForEach-Object { Write-Host "  - Name: $($_.Name), RG: $($_.ResourceGroup), URL: https://$($_.DefaultHostName)" -ForegroundColor Gray }
    Write-Host ""
    
    if (-not $WebAppName) {
        $WebAppName = $webapps[0].Name
        Write-Host "Using: $WebAppName" -ForegroundColor Cyan
    }
    
    if (-not $ResourceGroup) {
        $ResourceGroup = $webapps[0].ResourceGroup
        Write-Host "Using resource group: $ResourceGroup" -ForegroundColor Cyan
    }
}

Write-Host ""

# Update startup command
Write-Host "Updating startup command..." -ForegroundColor Yellow
az webapp config set `
    --resource-group $ResourceGroup `
    --name $WebAppName `
    --startup-file "startup.sh"

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to update startup command" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Startup command updated" -ForegroundColor Green
Write-Host ""

# Deploy application
Write-Host "Deploying application..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
az webapp up `
    --resource-group $ResourceGroup `
    --name $WebAppName `
    --runtime "PYTHON:3.11"

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Deployment failed" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Application deployed" -ForegroundColor Green
Write-Host ""

# Restart web app
Write-Host "Restarting web app..." -ForegroundColor Yellow
az webapp restart --resource-group $ResourceGroup --name $WebAppName

Write-Host "✓ Web app restarted" -ForegroundColor Green
Write-Host ""

# Show app URL
$appUrl = az webapp show --resource-group $ResourceGroup --name $WebAppName --query defaultHostName -o tsv
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Your app is available at: https://$appUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "To view logs, run:" -ForegroundColor Yellow
Write-Host "az webapp log tail --resource-group $ResourceGroup --name $WebAppName" -ForegroundColor Gray
Write-Host ""
