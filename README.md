# Multicloud Mapper - AI-Powered Cloud Service Comparison Tool

An intelligent cloud service mapping tool that helps you find equivalent services across Azure, AWS, and GCP with AI-powered cost analysis using Azure OpenAI.

## 🎯 Features

### 🔄 **Multicloud Service Mapper**
- 🤖 **AI-Powered Analysis**: Uses Azure OpenAI to provide intelligent insights on cloud service mappings
- ☁️ **Multi-Cloud Support**: Compare services across Azure, AWS, and Google Cloud Platform
- 💰 **Cost Comparison**: View pricing models and cost ranges for equivalent services
- 🎨 **Modern UI**: Clean, responsive web interface with intuitive search
- 📊 **Detailed Mappings**: Comprehensive service details including category, description, and pricing

### 📊 **BOM Generator (NEW!)**
- 🔍 **Diagram Validation**: AI validates if uploaded images are architecture diagrams
- 📋 **Bill of Materials**: Automatically generates component lists from diagrams
- 💵 **Cost Estimation**: AI-powered cost estimates for each component (Feb 2026 pricing)
- 🎯 **Component Detection**: Identifies cloud services from Azure, AWS, and GCP
- 💡 **Optimization Tips**: AI-generated recommendations for cost savings
- 📊 **Visual Reports**: Interactive tables and cost breakdowns

## Architecture

### Backend (Python Flask)
- **app.py**: Main Flask API server with REST endpoints
- **ai_agent.py**: Azure OpenAI agent for intelligent service analysis
- **bom_agent.py**: Azure OpenAI GPT-4 Vision agent for diagram analysis
- **cloud_services_data.py**: Database of cloud service mappings across providers

### Frontend (HTML/CSS/JavaScript)
- **index.html**: Multicloud service mapper interface
- **bom.html**: BOM generator for architecture diagram analysis

## Prerequisites

- Python 3.8 or higher
- Azure OpenAI Service access
- pip (Python package manager)

## Setup Instructions

### 1. Clone or Navigate to the Project
```bash
cd c:\mcm
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Azure OpenAI

1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` and add your Azure OpenAI credentials:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

**To get Azure OpenAI credentials:**
- Go to [Azure Portal](https://portal.azure.com/)
- Navigate to your Azure OpenAI resource
- Under "Keys and Endpoint", copy the endpoint and one of the keys
- Under "Model deployments", note your deployment name

### 5. Start the Backend Server
```bash
python app.py
```

The API server will start on `http://localhost:5000`

### 6. Open the Frontend

Open `index.html` or `bom.html` in your web browser:
```bash
start index.html
# or
start bom.html
```

Or simply double-click the HTML files.

## Usage

### 🔄 Multicloud Service Mapper (index.html)

1. **Select Cloud Provider**: Choose the source cloud provider (Azure, AWS, or GCP)
2. **Enter Service Name**: Type the name of the cloud service you want to map
   - Examples: "Azure Virtual Machines", "Amazon S3", "Cloud Functions"
3. **Click Search**: The AI agent will analyze and find equivalent services
4. **View Results**: See detailed comparison table with costs and AI insights

### 📊 BOM Generator (bom.html)

1. **Upload Diagram**: Drag and drop or select your architecture diagram
   - Supported: PNG, JPG, JPEG (Max 10MB)
2. **Preview**: Review the uploaded diagram
3. **Analyze**: Click "Analyze Diagram & Generate BOM"
4. **View BOM**: See detailed component list with cost estimates
5. **Review Recommendations**: Check AI-generated cost optimization tips

📖 **Detailed BOM Documentation**: See [BOM_README.md](BOM_README.md)

## API Endpoints

### Service Mapper Endpoints

### GET /api/services
List all available services grouped by category.

### GET /api/search?q=query
Search for services by partial name match.

### POST /api/map
Map a service to equivalent services in other clouds.

**Request Body:**
```json
{
  "service_name": "Azure Virtual Machines",
  "source_provider": "azure"
}
```

### POST /api/recommendations
Get AI-powered recommendations for service selection.

**Request Body:**
```json
{
  "service_name": "Amazon S3",
  "source_provider": "aws",
  "requirements": {
    "budget": "low",
    "usage": "high traffic"
  }
}
```

### BOM Generator Endpoints

### POST /api/bom/validate
Validate if an image is an architecture diagram.

**Request Body:**
```json
{
  "image": "data:image/jpeg;base64,..."
}
```

### POST /api/bom/analyze
Complete workflow: validate diagram and generate BOM with costs.

**Request Body:**
```json
{
  "image": "data:image/jpeg;base64,..."
}
```

**Response includes:**
- Validation results with confidence score
- Architecture summary
- Complete BOM with components and costs
- Cost breakdown by category
- AI-generated recommendations

### POST /api/bom/generate
Generate BOM for pre-validated diagrams (skip validation step).

## Supported Services

### Compute
- Virtual Machines (Azure VMs, EC2, Compute Engine)
- Kubernetes (AKS, EKS, GKE)
- Serverless Functions (Azure Functions, Lambda, Cloud Functions)

### Storage
- Object Storage (Blob Storage, S3, Cloud Storage)

### Database
- Relational (Azure SQL, RDS, Cloud SQL)
- NoSQL (Cosmos DB, DynamoDB, Firestore)

### Networking
- Load Balancers
- CDN Services

*More services can be added to `cloud_services_data.py`*

## Project Structure

```
c:\mcm\
├── app.py                      # Flask API server (both services)
├── ai_agent.py                 # Azure OpenAI service mapper agent
├── bom_agent.py                # Azure OpenAI BOM generator agent
├── cloud_services_data.py      # Service mappings database
├── index.html                  # Service Mapper UI
├── bom.html                    # BOM Generator UI
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── .env.example               # Example environment configuration
├── README.md                   # Main documentation
├── BOM_README.md              # BOM Generator detailed docs
└── test_realtime_ai.py        # Test scripts
└── .env.example               # Example environment configuration
```

## Troubleshooting

### "AI analysis unavailable" error
- Check that your `.env` file has correct Azure OpenAI credentials
- Verify your Azure OpenAI deployment is active and accessible
- Ensure you have sufficient quota in your Azure OpenAI resource

### CORS errors in browser
- Make sure the Flask server is running on `http://localhost:5000`
- Check browser console for specific error messages
- Verify CORS is enabled in `app.py` (already configured)

### Service not found
- Check the exact service name in `cloud_services_data.py`
- The tool will suggest similar services if an exact match isn't found
- Service names are case-sensitive

## Extending the Tool

### Adding New Services

Edit `cloud_services_data.py` and add entries to the `CLOUD_SERVICES_MAP` dictionary:

```python
"Your Service Name": {
    "azure": {
        "name": "Azure Service Name",
        "category": "Category",
        "description": "Description",
        "cost_range": "$X - $Y",
        "pricing_model": "Pricing details"
    },
    "aws": { ... },
    "gcp": { ... }
}
```

### Customizing AI Behavior

Modify the system prompt in `ai_agent.py` > `create_system_prompt()` to change how the AI analyzes services.

## Technologies Used

- **Backend**: Python 3, Flask, Azure OpenAI SDK
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI Models**: 
  - Azure OpenAI GPT-4 (Service mapping and analysis)
  - Azure OpenAI GPT-4 Vision (Architecture diagram analysis)
- **API**: RESTful architecture with JSON
- **Image Processing**: Base64 encoding for diagram uploads
- **API**: RESTful architecture with JSON

## Security Notes

- Never commit your `.env` file to version control
- Keep your Azure OpenAI API keys secure
- Use environment variables for all sensitive configuration
- Consider implementing authentication for production use

## License

This project is provided as-is for demonstration purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Azure OpenAI service status
3. Verify all configuration settings

## Future Enhancements

### Service Mapper
- [ ] Add more cloud services (networking, AI/ML, IoT, etc.)
- [ ] Implement caching for faster responses
- [ ] Add user authentication
- [ ] Export results to PDF/Excel
- [ ] Cost calculator based on usage patterns
- [ ] Migration planning assistant
- [ ] Multi-language support

### BOM Generator
- [ ] Support for whiteboard sketches and hand-drawn diagrams
- [ ] Export BOM to Excel/CSV/PDF
- [ ] Side-by-side architecture comparisons
- [ ] Historical cost tracking
- [ ] Integration with Azure Cost Management
- [ ] Multi-region cost analysis
- [ ] Drag-and-drop architecture builder
- [ ] Template library for common architectures

---

**Built with ❤️ using Azure OpenAI GPT-4 and GPT-4 Vision**
