"""
Azure OpenAI BOM (Bill of Materials) Agent
Analyzes architecture diagrams and generates cost estimates for cloud components
"""

import os
import json
import base64
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BOMGeneratorAgent:
    """AI Agent for analyzing architecture diagrams and generating BOM with costs"""
    
    def __init__(self):
        """Initialize the Azure OpenAI client with vision capabilities"""
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
        
    def validate_architecture_diagram(self, image_data):
        """
        Validate if the uploaded image is an architecture diagram
        
        Args:
            image_data: Base64 encoded image data or file path
            
        Returns:
            dict: {'is_valid': bool, 'reason': str, 'confidence': float}
        """
        try:
            # Prepare image for GPT-4 Vision
            if isinstance(image_data, str) and image_data.startswith('data:image'):
                # Already base64 data URI
                image_content = image_data
            else:
                # Assume it's raw base64
                image_content = f"data:image/jpeg;base64,{image_data}"
            
            validation_prompt = """Analyze this image and determine if it is a cloud architecture diagram or IT infrastructure diagram.

Return your analysis as a JSON object with this structure:
{
  "is_valid": true/false,
  "diagram_type": "cloud architecture" or "on-premise architecture" or  "network diagram" or "not a diagram",
  "confidence": 0.0-1.0,
  "reason": "explanation of why this is or isn't an architecture diagram",
  "detected_elements": ["list of technical elements you can see"]
}

An architecture diagram should contain cloud services, components, connections, or infrastructure elements."""

            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing technical diagrams and cloud architecture."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": validation_prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_content}
                            }
                        ]
                    }
                ],
                temperature=0.3,
                max_tokens=800,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return {
                'is_valid': False,
                'reason': f'Error validating diagram: {str(e)}',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def analyze_diagram_and_generate_bom(self, image_data):
        """
        Analyze architecture diagram and generate Bill of Materials with costs
        
        Args:
            image_data: Base64 encoded image data
            
        Returns:
            dict: BOM with components and costs
        """
        try:
            # Prepare image
            if isinstance(image_data, str) and image_data.startswith('data:image'):
                image_content = image_data
            else:
                image_content = f"data:image/jpeg;base64,{image_data}"
            
            analysis_prompt = """Analyze this cloud architecture diagram in detail and generate a comprehensive Bill of Materials (BOM).

For each component/service you identify in the diagram, provide:
1. Component name (specific service name)
2. Cloud provider (Azure, AWS, GCP, or Multi-cloud)
3. Category (Compute, Storage, Database, Networking, Security, etc.)
4. Quantity/Count (how many instances visible)
5. Configuration/Size (estimated tier: small/medium/large or specific SKU if visible)
6. Estimated monthly cost in USD
7. Description of its role in the architecture

Return a JSON object with this structure:
{
  "architecture_summary": "Brief description of the overall architecture",
  "cloud_providers": ["list of cloud providers used"],
  "total_components": number,
  "estimated_monthly_cost": total cost in USD,
  "components": [
    {
      "id": 1,
      "name": "component name",
      "service_type": "specific service",
      "provider": "Azure/AWS/GCP",
      "category": "category",
      "quantity": number,
      "configuration": "size/tier",
      "monthly_cost": cost in USD,
      "description": "role in architecture"
    }
  ],
  "cost_breakdown": {
    "compute": cost,
    "storage": cost,
    "database": cost,
    "networking": cost,
    "other": cost
  },
  "recommendations": ["cost optimization suggestions"]
}

Use February 2026 pricing. Be specific about service names and provide realistic cost estimates."""

            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert cloud architect and cost analyst. Analyze diagrams accurately and provide detailed cost estimates based on current 2026 pricing."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": analysis_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_content,
                                    "detail": "high"  # High detail for better analysis
                                }
                            }
                        ]
                    }
                ],
                temperature=0.4,
                max_tokens=3000,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return {
                'success': True,
                'bom': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error analyzing diagram: {str(e)}'
            }
    
    def generate_azure_equivalent_bom(self, original_bom):
        """
        Generate Azure equivalent BOM for non-Azure architectures
        
        Args:
            original_bom: The original BOM from the diagram analysis
            
        Returns:
            dict: Azure equivalent BOM with service mappings
        """
        try:
            bom_json = json.dumps(original_bom, indent=2)
            
            conversion_prompt = f"""Given this Bill of Materials from a cloud architecture diagram, generate an equivalent Azure-based BOM.

Original BOM:
{bom_json}

Create a new BOM that maps each non-Azure service to its Azure equivalent. Provide:
1. The original service name and provider
2. The recommended Azure service equivalent
3. Why this Azure service is the best match
4. Any architecture changes needed
5. Estimated Azure monthly cost (February 2026 pricing)

Return a JSON object with this structure:
{{
  "conversion_summary": "Brief description of the Azure conversion",
  "original_providers": ["list of original providers"],
  "total_components": number,
  "estimated_monthly_cost": total Azure cost in USD,
  "service_mappings": [
    {{
      "id": 1,
      "original_service": "original service name",
      "original_provider": "AWS/GCP/etc",
      "azure_equivalent": "Azure service name",
      "azure_category": "category",
      "quantity": number,
      "configuration": "recommended tier/size",
      "monthly_cost": Azure cost in USD,
      "mapping_reason": "why this Azure service is equivalent",
      "migration_notes": "any important considerations"
    }}
  ],
  "azure_cost_breakdown": {{
    "compute": cost,
    "storage": cost,
    "database": cost,
    "networking": cost,
    "other": cost
  }},
  "cost_comparison": {{
    "original_estimate": original cost,
    "azure_estimate": Azure cost,
    "difference": difference,
    "difference_percentage": percentage
  }},
  "migration_recommendations": ["Azure-specific recommendations and best practices"],
  "architecture_changes": ["any significant architectural changes needed for Azure"]
}}

Be specific about Azure service names (e.g., Azure App Service, Azure SQL Database, Azure Blob Storage) and provide accurate cost estimates."""

            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Azure cloud architect specializing in cloud migration and Azure service mapping. Provide accurate Azure service equivalents and cost estimates based on February 2026 Azure pricing."
                    },
                    {
                        "role": "user",
                        "content": conversion_prompt
                    }
                ],
                temperature=0.4,
                max_tokens=3000,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return {
                'success': True,
                'azure_bom': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error generating Azure equivalent BOM: {str(e)}'
            }
    
    def process_diagram(self, image_data):
        """
        Complete workflow: validate and analyze diagram
        
        Args:
            image_data: Base64 encoded image data
            
        Returns:
            dict: Complete analysis results including Azure equivalent if non-Azure
        """
        # Step 1: Validate
        validation = self.validate_architecture_diagram(image_data)
        
        if not validation.get('is_valid', False):
            return {
                'success': False,
                'stage': 'validation',
                'error': 'Not a valid architecture diagram',
                'validation': validation
            }
        
        # Step 2: Analyze and generate BOM
        bom_result = self.analyze_diagram_and_generate_bom(image_data)
        
        if not bom_result.get('success', False):
            return {
                'success': False,
                'stage': 'analysis',
                'error': bom_result.get('error', 'Analysis failed'),
                'validation': validation
            }
        
        original_bom = bom_result['bom']
        
        # Step 3: Check if architecture uses non-Azure services
        cloud_providers = original_bom.get('cloud_providers', [])
        has_non_azure = any(
            provider.upper() not in ['AZURE', 'MICROSOFT AZURE'] 
            for provider in cloud_providers 
            if provider.upper() != 'MULTI-CLOUD'
        )
        
        result = {
            'success': True,
            'validation': validation,
            'bom': original_bom,
            'is_azure': not has_non_azure
        }
        
        # Step 4: If non-Azure, generate Azure equivalent BOM
        if has_non_azure:
            print(f"Detected non-Azure services: {cloud_providers}")
            print("Generating Azure equivalent BOM...")
            
            azure_bom_result = self.generate_azure_equivalent_bom(original_bom)
            
            if azure_bom_result.get('success', False):
                result['azure_equivalent'] = azure_bom_result['azure_bom']
                result['has_azure_alternative'] = True
            else:
                result['azure_equivalent_error'] = azure_bom_result.get('error', 'Failed to generate Azure equivalent')
                result['has_azure_alternative'] = False
        
        return result


def test_bom_agent():
    """Test the BOM agent with a sample scenario"""
    agent = BOMGeneratorAgent()
    
    print("="*70)
    print("BOM Generator Agent - Test")
    print("="*70)
    print("\nAgent initialized successfully!")
    print("Ready to analyze architecture diagrams.")
    print("\nCapabilities:")
    print("  ✓ Validate architecture diagrams")
    print("  ✓ Identify cloud components")
    print("  ✓ Generate Bill of Materials")
    print("  ✓ Estimate costs (February 2026 pricing)")
    print("  ✓ Generate Azure equivalent BOM for non-Azure architectures")
    print("  ✓ Provide service mapping and migration recommendations")
    print("="*70)


if __name__ == "__main__":
    test_bom_agent()
