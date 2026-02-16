# BOM Generator - Architecture Diagram Analysis

## Overview

The **BOM (Bill of Materials) Generator** uses Azure OpenAI's GPT-4 Vision capabilities to analyze cloud architecture diagrams and automatically generate detailed cost estimates.

## Features

### 🔍 **Diagram Validation**
- AI validates if uploaded image is an architecture diagram
- Confidence score for validation
- Detects technical elements in the diagram

### 📊 **Bill of Materials Generation**
- Identifies all cloud components in the diagram
- Detects cloud providers (Azure, AWS, GCP)
- Categorizes components (Compute, Storage, Database, etc.)
- Estimates quantities and configurations

### 💰 **Cost Analysis**
- Provides monthly cost estimates for each component
- Breaks down costs by category
- Calculates total architecture cost
- Uses February 2026 pricing

### 💡 **Recommendations**
- AI-generated cost optimization suggestions
- Best practices for the architecture
- Alternative service recommendations

## How to Use

### 1. Start the Server

```powershell
.\venv\Scripts\python.exe app.py
```

### 2. Open BOM Generator

Open `bom.html` in your browser or navigate from the main page.

### 3. Upload Diagram

- **Drag and drop** your architecture diagram
- Or **click to browse** and select a file
- Supported formats: PNG, JPG, JPEG (Max 10MB)

### 4. Analyze

Click "Analyze Diagram & Generate BOM" and wait 15-30 seconds for AI analysis.

### 5. Review Results

The BOM will display:
- **Summary Cards**: Total components, providers, estimated cost
- **Architecture Summary**: Overview of the design
- **BOM Table**: Detailed list of all components with costs
- **Cost Breakdown**: Visual breakdown by category
- **Recommendations**: AI suggestions for optimization

## API Endpoints

### POST /api/bom/validate
Validate if an image is an architecture diagram.

**Request:**
```json
{
  "image": "data:image/jpeg;base64,..."
}
```

**Response:**
```json
{
  "success": true,
  "validation": {
    "is_valid": true,
    "diagram_type": "cloud architecture",
    "confidence": 0.95,
    "reason": "Contains cloud services...",
    "detected_elements": ["VMs", "Storage", "Database"]
  }
}
```

### POST /api/bom/analyze
Complete workflow: validate and generate BOM.

**Request:**
```json
{
  "image": "data:image/jpeg;base64,..."
}
```

**Response:**
```json
{
  "success": true,
  "validation": { ... },
  "bom": {
    "architecture_summary": "3-tier web application...",
    "cloud_providers": ["Azure"],
    "total_components": 8,
    "estimated_monthly_cost": 2450,
    "components": [
      {
        "id": 1,
        "name": "Web Tier VMs",
        "service_type": "Azure Virtual Machines",
        "provider": "Azure",
        "category": "Compute",
        "quantity": 2,
        "configuration": "Standard_D2s_v3",
        "monthly_cost": 140,
        "description": "Hosts web application"
      }
    ],
    "cost_breakdown": {
      "compute": 500,
      "storage": 200,
      "database": 1500,
      "networking": 150,
      "other": 100
    },
    "recommendations": [
      "Consider Azure Reserved Instances...",
      "Use Azure CDN to reduce bandwidth..."
    ]
  }
}
```

### POST /api/bom/generate
Generate BOM without validation (for pre-validated diagrams).

## Architecture Diagram Requirements

For best results, your diagram should:

✅ **Include labeled components** - Service names clearly visible
✅ **Show connections** - Lines/arrows between components
✅ **Use standard icons** - Official cloud provider icons when possible
✅ **Be clear and readable** - High resolution, minimal clutter
✅ **Show quantities** - Multiple instances clearly indicated

## Example Use Cases

### 1. **Cost Estimation**
Upload your proposed architecture to get instant cost estimates before deployment.

### 2. **Architecture Review**
Analyze existing diagrams to identify cost optimization opportunities.

### 3. **Multi-Cloud Comparison**
Compare costs across different cloud providers for the same architecture.

### 4. **Documentation**
Generate detailed component lists for architecture documentation.

### 5. **Budget Planning**
Get accurate monthly costs for financial planning and budgeting.

## Tips for Accurate Results

1. **Higher Resolution = Better Results**: Upload clear, high-quality diagrams
2. **Label Everything**: Include service names and configurations in your diagram
3. **Use Standard Symbols**: Azure/AWS/GCP official icons help AI recognition
4. **Show Redundancy**: Clearly indicate multiple instances (e.g., "x2", "x3")
5. **Include Context**: Text annotations help AI understand the purpose

## Limitations

- AI estimates are based on standard configurations
- Actual costs may vary based on usage patterns
- Complex licensing and discounts not included
- Network egress costs are approximated
- Assumes steady-state operation (24/7)

## Technology Stack

- **Azure OpenAI GPT-4 Vision**: Diagram analysis
- **Flask API**: Backend service
- **HTML/CSS/JavaScript**: Frontend interface
- **Base64 Encoding**: Image handling

## Troubleshooting

### "Not a valid architecture diagram"
- Ensure image contains technical cloud components
- Check image quality and clarity
- Verify it's an architecture diagram, not a flowchart or other diagram type

### Analysis takes too long
- Large images may take 30+ seconds
- Check your internet connection
- Verify Azure OpenAI service is responding

### Inaccurate cost estimates
- Add more detail to your diagram labels
- Include service tier/size information
- Specify regions for more accurate pricing

## Future Enhancements

- [ ] Support for whiteboard sketches
- [ ] Export BOM to Excel/CSV
- [ ] Side-by-side architecture comparisons
- [ ] Historical cost tracking
- [ ] Integration with Azure Cost Management
- [ ] PDF report generation
- [ ] Multi-region cost analysis

---

**Built with Azure OpenAI GPT-4 Vision** 🤖👁️
