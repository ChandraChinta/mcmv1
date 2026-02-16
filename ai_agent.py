"""
Azure Agentic AI Service for Multicloud Service Mapping
This service uses Azure OpenAI to provide intelligent cloud service mapping
with cost analysis across Azure, AWS, and GCP
"""

import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
from cloud_services_data import get_service_mappings, search_service_by_partial_name, CLOUD_SERVICES_MAP

# Load environment variables
load_dotenv()


class MulticloudMapperAgent:
    """AI Agent for mapping cloud services across providers"""
    
    def __init__(self):
        """Initialize the Azure OpenAI client"""
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    def create_system_prompt(self):
        """Create system prompt for the AI agent"""
        return """You are an expert cloud architecture consultant specializing in multicloud strategies.
Your role is to help users understand equivalent services across Azure, AWS, and GCP cloud providers.

When analyzing service mappings, consider:
1. Functional equivalence - services that provide similar capabilities
2. Cost comparison - pricing models and cost ranges
3. Key differences - unique features or limitations
4. Migration considerations - what to watch out for when moving between clouds

Provide concise, actionable insights that help users make informed decisions about cloud service selection.
Focus on practical advice and cost implications."""

    def analyze_service_mapping(self, service_name, source_provider):
        """
        Use AI to analyze service mapping and provide insights
        
        Args:
            service_name: Name of the cloud service
            source_provider: Source cloud provider (azure, aws, gcp)
            
        Returns:
            Dictionary with AI analysis and service mappings
        """
        # First, get the structured data using AI-powered real-time mapping
        mapping_data = get_service_mappings(service_name, source_provider, use_ai=True)
        
        if not mapping_data:
            # Try to find similar services
            similar = search_service_by_partial_name(service_name)
            return {
                'success': False,
                'error': f'Service "{service_name}" not found',
                'suggestions': similar[:5] if similar else [],
                'ai_insight': None
            }
        
        # Prepare context for AI
        context = f"""
Source Service: {service_name}
Source Provider: {source_provider.upper()}

Service Details:
{json.dumps(mapping_data, indent=2)}

Analyze this multicloud service mapping and provide:
1. A brief summary of the source service
2. Key similarities and differences with equivalent services in other clouds
3. Cost comparison insights
4. Recommendation on which alternative might be more cost-effective and why
"""

        try:
            # Call Azure OpenAI for analysis
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": self.create_system_prompt()},
                    {"role": "user", "content": context}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            ai_insight = response.choices[0].message.content
            
            return {
                'success': True,
                'service_name': service_name,
                'source_provider': source_provider,
                'source_details': mapping_data['source'],
                'mappings': mapping_data['mappings'],
                'ai_insight': ai_insight
            }
            
        except Exception as e:
            print(f"AI analysis error: {str(e)}")
            # Fallback to structured data without AI insights
            return {
                'success': True,
                'service_name': service_name,
                'source_provider': source_provider,
                'source_details': mapping_data['source'],
                'mappings': mapping_data['mappings'],
                'ai_insight': f'AI analysis unavailable. Error: {str(e)}',
                'fallback': True
            }
    
    def get_recommendations(self, service_name, source_provider, requirements=None):
        """
        Get AI-powered recommendations for cloud service selection
        
        Args:
            service_name: Name of the cloud service
            source_provider: Source provider
            requirements: Optional dict with specific requirements (budget, performance, etc.)
            
        Returns:
            AI-generated recommendations
        """
        mapping_data = get_service_mappings(service_name, source_provider)
        
        if not mapping_data:
            return {'success': False, 'error': 'Service not found'}
        
        requirements_context = ""
        if requirements:
            requirements_context = f"\n\nUser Requirements:\n{json.dumps(requirements, indent=2)}"
        
        prompt = f"""
Given the following cloud service mapping:

Source: {service_name} on {source_provider.upper()}
{json.dumps(mapping_data, indent=2)}
{requirements_context}

Provide specific recommendations on:
1. Which cloud provider offers the best value for this service type
2. Cost optimization strategies
3. Any potential migration challenges
4. Best use case for each provider's equivalent service
"""

        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": self.create_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            return {
                'success': True,
                'recommendations': response.choices[0].message.content
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to generate recommendations: {str(e)}'
            }
    
    def identify_and_map_to_azure(self, technology_name):
        """
        Identify third-party technology or product and suggest Azure equivalent services
        
        Args:
            technology_name: Name of the technology, product, or service
            
        Returns:
            Dictionary with technology identification and Azure service mappings
        """
        identification_prompt = f"""Analyze this technology/product/service: "{technology_name}"

Provide a comprehensive analysis and Azure mapping in JSON format:

{{
  "technology_name": "exact name",
  "technology_type": "category (e.g., Database, Message Queue, Container Platform, etc.)",
  "provider": "vendor/provider name (e.g., MongoDB, Kafka, Redis, Docker, Kubernetes, etc.)",
  "description": "brief description of what this technology does",
  "primary_use_cases": ["use case 1", "use case 2"],
  "is_cloud_native": true/false,
  "azure_equivalents": [
    {{
      "azure_service": "Azure service name",
      "match_type": "Direct/Similar/Alternative",
      "match_score": 0-100,
      "category": "service category",
      "description": "how this Azure service matches",
      "cost_range": "estimated cost range",
      "pricing_model": "pricing model",
      "migration_complexity": "Low/Medium/High",
      "key_differences": "important differences to note",
      "advantages": "advantages of using this Azure service"
    }}
  ],
  "migration_considerations": ["consideration 1", "consideration 2"],
  "recommended_azure_service": "top recommended Azure service",
  "recommendation_reason": "why this is the best match"
}}

Be specific about Azure services and provide accurate information based on February 2026 Azure offerings."""

        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert Azure cloud architect and technology consultant.
You specialize in identifying technologies, products, and services, then mapping them to appropriate Azure services.
You have deep knowledge of Azure services, third-party technologies, databases, messaging systems, container platforms, and enterprise software.
Provide accurate, detailed mappings with practical migration advice."""
                    },
                    {
                        "role": "user",
                        "content": identification_prompt
                    }
                ],
                temperature=0.4,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return {
                'success': True,
                'technology_name': technology_name,
                'analysis': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to analyze technology: {str(e)}',
                'technology_name': technology_name
            }
    
    def list_all_services(self):
        """Get list of all available services"""
        services_by_category = {}
        
        for service_name, details in CLOUD_SERVICES_MAP.items():
            # Get category from any provider (they should be the same)
            category = details.get('azure', {}).get('category', 'Other')
            
            if category not in services_by_category:
                services_by_category[category] = []
            
            services_by_category[category].append(service_name)
        
        return {
            'success': True,
            'services_by_category': services_by_category,
            'total_services': len(CLOUD_SERVICES_MAP)
        }


def test_agent():
    """Test the agent functionality"""
    agent = MulticloudMapperAgent()
    
    # Test 1: Analyze a service mapping
    print("Test 1: Analyzing Azure Virtual Machines mapping...")
    result = agent.analyze_service_mapping("Azure Virtual Machines", "azure")
    print(json.dumps(result, indent=2))
    print("\n" + "="*80 + "\n")
    
    # Test 2: Get recommendations
    print("Test 2: Getting recommendations...")
    recommendations = agent.get_recommendations(
        "Amazon S3", 
        "aws",
        requirements={"budget": "low", "usage": "high traffic"}
    )
    print(json.dumps(recommendations, indent=2))
    print("\n" + "="*80 + "\n")
    
    # Test 3: List all services
    print("Test 3: Listing all services...")
    services = agent.list_all_services()
    print(json.dumps(services, indent=2))


if __name__ == "__main__":
    test_agent()
