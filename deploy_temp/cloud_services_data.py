"""
Multicloud Service Mapping Database
Contains mappings between Azure, AWS, and GCP services with cost information
"""

import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI client for real-time queries
try:
    _openai_client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    _deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    _openai_available = True
except Exception as e:
    print(f"if any qustions: Contact AI and developer {e}")
    _openai_client = None
    _openai_available = False

CLOUD_SERVICES_MAP = {
    # Compute Services
    "Azure Virtual Machines": {
        "azure": {
            "name": "Azure Virtual Machines",
            "category": "Compute",
            "description": "Scalable computing capacity in the cloud",
            "cost_range": "$0.008 - $13.34/hour",
            "pricing_model": "Pay per use (hourly)"
        },
        "aws": {
            "name": "Amazon EC2",
            "category": "Compute",
            "description": "Scalable computing capacity in the cloud",
            "cost_range": "$0.0047 - $13.338/hour",
            "pricing_model": "Pay per use (hourly)"
        },
        "gcp": {
            "name": "Google Compute Engine",
            "category": "Compute",
            "description": "Scalable computing capacity in the cloud",
            "cost_range": "$0.006 - $11.77/hour",
            "pricing_model": "Pay per use (per second, 1 min minimum)"
        }
    },
    "Amazon EC2": {
        "azure": {
            "name": "Azure Virtual Machines",
            "category": "Compute",
            "description": "Scalable computing capacity in the cloud",
            "cost_range": "$0.008 - $13.34/hour",
            "pricing_model": "Pay per use (hourly)"
        },
        "aws": {
            "name": "Amazon EC2",
            "category": "Compute",
            "description": "Scalable computing capacity in the cloud",
            "cost_range": "$0.0047 - $13.338/hour",
            "pricing_model": "Pay per use (hourly)"
        },
        "gcp": {
            "name": "Google Compute Engine",
            "category": "Compute",
            "description": "Scalable computing capacity in the cloud",
            "cost_range": "$0.006 - $11.77/hour",
            "pricing_model": "Pay per use (per second, 1 min minimum)"
        }
    },
    "Google Compute Engine": {
        "azure": {
            "name": "Azure Virtual Machines",
            "category": "Compute",
            "description": "Scalable computing capacity in the cloud",
            "cost_range": "$0.008 - $13.34/hour",
            "pricing_model": "Pay per use (hourly)"
        },
        "aws": {
            "name": "Amazon EC2",
            "category": "Compute",
            "description": "Scalable computing capacity in the cloud",
            "cost_range": "$0.0047 - $13.338/hour",
            "pricing_model": "Pay per use (hourly)"
        },
        "gcp": {
            "name": "Google Compute Engine",
            "category": "Compute",
            "description": "Scalable computing capacity in the cloud",
            "cost_range": "$0.006 - $11.77/hour",
            "pricing_model": "Pay per use (per second, 1 min minimum)"
        }
    },
    
    # Container Services
    "Azure Kubernetes Service": {
        "azure": {
            "name": "Azure Kubernetes Service (AKS)",
            "category": "Containers",
            "description": "Managed Kubernetes service",
            "cost_range": "$0.10/hour + VM costs",
            "pricing_model": "Free cluster management + node costs"
        },
        "aws": {
            "name": "Amazon EKS",
            "category": "Containers",
            "description": "Managed Kubernetes service",
            "cost_range": "$0.10/hour + EC2 costs",
            "pricing_model": "Pay per cluster hour + node costs"
        },
        "gcp": {
            "name": "Google Kubernetes Engine (GKE)",
            "category": "Containers",
            "description": "Managed Kubernetes service",
            "cost_range": "$0.10/hour + compute costs",
            "pricing_model": "Pay per cluster hour + node costs"
        }
    },
    "Amazon EKS": {
        "azure": {
            "name": "Azure Kubernetes Service (AKS)",
            "category": "Containers",
            "description": "Managed Kubernetes service",
            "cost_range": "$0.10/hour + VM costs",
            "pricing_model": "Free cluster management + node costs"
        },
        "aws": {
            "name": "Amazon EKS",
            "category": "Containers",
            "description": "Managed Kubernetes service",
            "cost_range": "$0.10/hour + EC2 costs",
            "pricing_model": "Pay per cluster hour + node costs"
        },
        "gcp": {
            "name": "Google Kubernetes Engine (GKE)",
            "category": "Containers",
            "description": "Managed Kubernetes service",
            "cost_range": "$0.10/hour + compute costs",
            "pricing_model": "Pay per cluster hour + node costs"
        }
    },
    "Google Kubernetes Engine": {
        "azure": {
            "name": "Azure Kubernetes Service (AKS)",
            "category": "Containers",
            "description": "Managed Kubernetes service",
            "cost_range": "$0.10/hour + VM costs",
            "pricing_model": "Free cluster management + node costs"
        },
        "aws": {
            "name": "Amazon EKS",
            "category": "Containers",
            "description": "Managed Kubernetes service",
            "cost_range": "$0.10/hour + EC2 costs",
            "pricing_model": "Pay per cluster hour + node costs"
        },
        "gcp": {
            "name": "Google Kubernetes Engine (GKE)",
            "category": "Containers",
            "description": "Managed Kubernetes service",
            "cost_range": "$0.10/hour + compute costs",
            "pricing_model": "Pay per cluster hour + node costs"
        }
    },
    
    # Storage Services
    "Azure Blob Storage": {
        "azure": {
            "name": "Azure Blob Storage",
            "category": "Storage",
            "description": "Object storage for unstructured data",
            "cost_range": "$0.0184 - $0.15/GB/month",
            "pricing_model": "Pay per GB stored + operations"
        },
        "aws": {
            "name": "Amazon S3",
            "category": "Storage",
            "description": "Object storage for unstructured data",
            "cost_range": "$0.021 - $0.023/GB/month",
            "pricing_model": "Pay per GB stored + requests"
        },
        "gcp": {
            "name": "Google Cloud Storage",
            "category": "Storage",
            "description": "Object storage for unstructured data",
            "cost_range": "$0.020 - $0.026/GB/month",
            "pricing_model": "Pay per GB stored + operations"
        }
    },
    "Amazon S3": {
        "azure": {
            "name": "Azure Blob Storage",
            "category": "Storage",
            "description": "Object storage for unstructured data",
            "cost_range": "$0.0184 - $0.15/GB/month",
            "pricing_model": "Pay per GB stored + operations"
        },
        "aws": {
            "name": "Amazon S3",
            "category": "Storage",
            "description": "Object storage for unstructured data",
            "cost_range": "$0.021 - $0.023/GB/month",
            "pricing_model": "Pay per GB stored + requests"
        },
        "gcp": {
            "name": "Google Cloud Storage",
            "category": "Storage",
            "description": "Object storage for unstructured data",
            "cost_range": "$0.020 - $0.026/GB/month",
            "pricing_model": "Pay per GB stored + operations"
        }
    },
    "Google Cloud Storage": {
        "azure": {
            "name": "Azure Blob Storage",
            "category": "Storage",
            "description": "Object storage for unstructured data",
            "cost_range": "$0.0184 - $0.15/GB/month",
            "pricing_model": "Pay per GB stored + operations"
        },
        "aws": {
            "name": "Amazon S3",
            "category": "Storage",
            "description": "Object storage for unstructured data",
            "cost_range": "$0.021 - $0.023/GB/month",
            "pricing_model": "Pay per GB stored + requests"
        },
        "gcp": {
            "name": "Google Cloud Storage",
            "category": "Storage",
            "description": "Object storage for unstructured data",
            "cost_range": "$0.020 - $0.026/GB/month",
            "pricing_model": "Pay per GB stored + operations"
        }
    },
    
    # Database Services
    "Azure SQL Database": {
        "azure": {
            "name": "Azure SQL Database",
            "category": "Database",
            "description": "Managed relational database service",
            "cost_range": "$5 - $29,127/month",
            "pricing_model": "DTU or vCore based pricing"
        },
        "aws": {
            "name": "Amazon RDS",
            "category": "Database",
            "description": "Managed relational database service",
            "cost_range": "$15 - $28,000/month",
            "pricing_model": "Pay per instance hour"
        },
        "gcp": {
            "name": "Cloud SQL",
            "category": "Database",
            "description": "Managed relational database service",
            "cost_range": "$7.67 - $25,000/month",
            "pricing_model": "Pay per use or per instance"
        }
    },
    "Amazon RDS": {
        "azure": {
            "name": "Azure SQL Database",
            "category": "Database",
            "description": "Managed relational database service",
            "cost_range": "$5 - $29,127/month",
            "pricing_model": "DTU or vCore based pricing"
        },
        "aws": {
            "name": "Amazon RDS",
            "category": "Database",
            "description": "Managed relational database service",
            "cost_range": "$15 - $28,000/month",
            "pricing_model": "Pay per instance hour"
        },
        "gcp": {
            "name": "Cloud SQL",
            "category": "Database",
            "description": "Managed relational database service",
            "cost_range": "$7.67 - $25,000/month",
            "pricing_model": "Pay per use or per instance"
        }
    },
    "Cloud SQL": {
        "azure": {
            "name": "Azure SQL Database",
            "category": "Database",
            "description": "Managed relational database service",
            "cost_range": "$5 - $29,127/month",
            "pricing_model": "DTU or vCore based pricing"
        },
        "aws": {
            "name": "Amazon RDS",
            "category": "Database",
            "description": "Managed relational database service",
            "cost_range": "$15 - $28,000/month",
            "pricing_model": "Pay per instance hour"
        },
        "gcp": {
            "name": "Cloud SQL",
            "category": "Database",
            "description": "Managed relational database service",
            "cost_range": "$7.67 - $25,000/month",
            "pricing_model": "Pay per use or per instance"
        }
    },
    
    # NoSQL Database
    "Azure Cosmos DB": {
        "azure": {
            "name": "Azure Cosmos DB",
            "category": "Database",
            "description": "Globally distributed NoSQL database",
            "cost_range": "$0.008/hour per 100 RU/s",
            "pricing_model": "Request Units (RU) based pricing"
        },
        "aws": {
            "name": "Amazon DynamoDB",
            "category": "Database",
            "description": "Fully managed NoSQL database",
            "cost_range": "$0.00065 per read + $0.00325 per write",
            "pricing_model": "On-demand or provisioned capacity"
        },
        "gcp": {
            "name": "Cloud Firestore",
            "category": "Database",
            "description": "Flexible, scalable NoSQL database",
            "cost_range": "$0.06/100k reads + $0.18/100k writes",
            "pricing_model": "Pay per operation + storage"
        }
    },
    "Amazon DynamoDB": {
        "azure": {
            "name": "Azure Cosmos DB",
            "category": "Database",
            "description": "Globally distributed NoSQL database",
            "cost_range": "$0.008/hour per 100 RU/s",
            "pricing_model": "Request Units (RU) based pricing"
        },
        "aws": {
            "name": "Amazon DynamoDB",
            "category": "Database",
            "description": "Fully managed NoSQL database",
            "cost_range": "$0.00065 per read + $0.00325 per write",
            "pricing_model": "On-demand or provisioned capacity"
        },
        "gcp": {
            "name": "Cloud Firestore",
            "category": "Database",
            "description": "Flexible, scalable NoSQL database",
            "cost_range": "$0.06/100k reads + $0.18/100k writes",
            "pricing_model": "Pay per operation + storage"
        }
    },
    "Cloud Firestore": {
        "azure": {
            "name": "Azure Cosmos DB",
            "category": "Database",
            "description": "Globally distributed NoSQL database",
            "cost_range": "$0.008/hour per 100 RU/s",
            "pricing_model": "Request Units (RU) based pricing"
        },
        "aws": {
            "name": "Amazon DynamoDB",
            "category": "Database",
            "description": "Fully managed NoSQL database",
            "cost_range": "$0.00065 per read + $0.00325 per write",
            "pricing_model": "On-demand or provisioned capacity"
        },
        "gcp": {
            "name": "Cloud Firestore",
            "category": "Database",
            "description": "Flexible, scalable NoSQL database",
            "cost_range": "$0.06/100k reads + $0.18/100k writes",
            "pricing_model": "Pay per operation + storage"
        }
    },
    
    # Serverless Functions
    "Azure Functions": {
        "azure": {
            "name": "Azure Functions",
            "category": "Serverless",
            "description": "Event-driven serverless compute",
            "cost_range": "$0.20 per million executions",
            "pricing_model": "Pay per execution + compute time"
        },
        "aws": {
            "name": "AWS Lambda",
            "category": "Serverless",
            "description": "Event-driven serverless compute",
            "cost_range": "$0.20 per million requests",
            "pricing_model": "Pay per request + compute time"
        },
        "gcp": {
            "name": "Cloud Functions",
            "category": "Serverless",
            "description": "Event-driven serverless compute",
            "cost_range": "$0.40 per million invocations",
            "pricing_model": "Pay per invocation + compute time"
        }
    },
    "AWS Lambda": {
        "azure": {
            "name": "Azure Functions",
            "category": "Serverless",
            "description": "Event-driven serverless compute",
            "cost_range": "$0.20 per million executions",
            "pricing_model": "Pay per execution + compute time"
        },
        "aws": {
            "name": "AWS Lambda",
            "category": "Serverless",
            "description": "Event-driven serverless compute",
            "cost_range": "$0.20 per million requests",
            "pricing_model": "Pay per request + compute time"
        },
        "gcp": {
            "name": "Cloud Functions",
            "category": "Serverless",
            "description": "Event-driven serverless compute",
            "cost_range": "$0.40 per million invocations",
            "pricing_model": "Pay per invocation + compute time"
        }
    },
    "Cloud Functions": {
        "azure": {
            "name": "Azure Functions",
            "category": "Serverless",
            "description": "Event-driven serverless compute",
            "cost_range": "$0.20 per million executions",
            "pricing_model": "Pay per execution + compute time"
        },
        "aws": {
            "name": "AWS Lambda",
            "category": "Serverless",
            "description": "Event-driven serverless compute",
            "cost_range": "$0.20 per million requests",
            "pricing_model": "Pay per request + compute time"
        },
        "gcp": {
            "name": "Cloud Functions",
            "category": "Serverless",
            "description": "Event-driven serverless compute",
            "cost_range": "$0.40 per million invocations",
            "pricing_model": "Pay per invocation + compute time"
        }
    },
    
    # Load Balancer
    "Azure Load Balancer": {
        "azure": {
            "name": "Azure Load Balancer",
            "category": "Networking",
            "description": "Layer 4 load balancing service",
            "cost_range": "$0.025/hour + $0.005/GB processed",
            "pricing_model": "Pay per hour + data processed"
        },
        "aws": {
            "name": "AWS Elastic Load Balancing",
            "category": "Networking",
            "description": "Automatic traffic distribution",
            "cost_range": "$0.025/hour + $0.008/GB",
            "pricing_model": "Pay per hour + data processed"
        },
        "gcp": {
            "name": "Cloud Load Balancing",
            "category": "Networking",
            "description": "Global load balancing service",
            "cost_range": "$0.025/hour + $0.008/GB",
            "pricing_model": "Pay per hour + data processed"
        }
    },
    "AWS Elastic Load Balancing": {
        "azure": {
            "name": "Azure Load Balancer",
            "category": "Networking",
            "description": "Layer 4 load balancing service",
            "cost_range": "$0.025/hour + $0.005/GB processed",
            "pricing_model": "Pay per hour + data processed"
        },
        "aws": {
            "name": "AWS Elastic Load Balancing",
            "category": "Networking",
            "description": "Automatic traffic distribution",
            "cost_range": "$0.025/hour + $0.008/GB",
            "pricing_model": "Pay per hour + data processed"
        },
        "gcp": {
            "name": "Cloud Load Balancing",
            "category": "Networking",
            "description": "Global load balancing service",
            "cost_range": "$0.025/hour + $0.008/GB",
            "pricing_model": "Pay per hour + data processed"
        }
    },
    "Cloud Load Balancing": {
        "azure": {
            "name": "Azure Load Balancer",
            "category": "Networking",
            "description": "Layer 4 load balancing service",
            "cost_range": "$0.025/hour + $0.005/GB processed",
            "pricing_model": "Pay per hour + data processed"
        },
        "aws": {
            "name": "AWS Elastic Load Balancing",
            "category": "Networking",
            "description": "Automatic traffic distribution",
            "cost_range": "$0.025/hour + $0.008/GB",
            "pricing_model": "Pay per hour + data processed"
        },
        "gcp": {
            "name": "Cloud Load Balancing",
            "category": "Networking",
            "description": "Global load balancing service",
            "cost_range": "$0.025/hour + $0.008/GB",
            "pricing_model": "Pay per hour + data processed"
        }
    },
    
    # CDN Services
    "Azure CDN": {
        "azure": {
            "name": "Azure CDN",
            "category": "Networking",
            "description": "Content delivery network",
            "cost_range": "$0.081 - $0.18/GB",
            "pricing_model": "Pay per GB transferred"
        },
        "aws": {
            "name": "Amazon CloudFront",
            "category": "Networking",
            "description": "Content delivery network",
            "cost_range": "$0.085 - $0.20/GB",
            "pricing_model": "Pay per GB transferred + requests"
        },
        "gcp": {
            "name": "Cloud CDN",
            "category": "Networking",
            "description": "Content delivery network",
            "cost_range": "$0.08 - $0.20/GB",
            "pricing_model": "Pay per GB transferred + requests"
        }
    },
    "Amazon CloudFront": {
        "azure": {
            "name": "Azure CDN",
            "category": "Networking",
            "description": "Content delivery network",
            "cost_range": "$0.081 - $0.18/GB",
            "pricing_model": "Pay per GB transferred"
        },
        "aws": {
            "name": "Amazon CloudFront",
            "category": "Networking",
            "description": "Content delivery network",
            "cost_range": "$0.085 - $0.20/GB",
            "pricing_model": "Pay per GB transferred + requests"
        },
        "gcp": {
            "name": "Cloud CDN",
            "category": "Networking",
            "description": "Content delivery network",
            "cost_range": "$0.08 - $0.20/GB",
            "pricing_model": "Pay per GB transferred + requests"
        }
    },
    "Cloud CDN": {
        "azure": {
            "name": "Azure CDN",
            "category": "Networking",
            "description": "Content delivery network",
            "cost_range": "$0.081 - $0.18/GB",
            "pricing_model": "Pay per GB transferred"
        },
        "aws": {
            "name": "Amazon CloudFront",
            "category": "Networking",
            "description": "Content delivery network",
            "cost_range": "$0.085 - $0.20/GB",
            "pricing_model": "Pay per GB transferred + requests"
        },
        "gcp": {
            "name": "Cloud CDN",
            "category": "Networking",
            "description": "Content delivery network",
            "cost_range": "$0.08 - $0.20/GB",
            "pricing_model": "Pay per GB transferred + requests"
        }
    },
}


def get_all_services():
    """Return list of all service names"""
    return list(CLOUD_SERVICES_MAP.keys())


def get_service_mappings(service_name, source_provider, use_ai=True):
    """
    Get service mappings for other cloud providers using Azure OpenAI in real-time
    
    Args:
        service_name: Name of the service to map
        source_provider: Source cloud provider (azure, aws, or gcp)
        use_ai: If True, use Azure OpenAI for real-time intelligent mapping (default: True)
    
    Returns:
        Dictionary with mappings to other providers or None if not found
    """
    # Normalize provider name
    source_provider = source_provider.lower()
    
    # Try AI-powered real-time mapping first if available and requested
    if use_ai and _openai_available and _openai_client:
        try:
            ai_result = _get_ai_service_mappings(service_name, source_provider)
            if ai_result:
                return ai_result
        except Exception as e:
            print(f"AI mapping failed, falling back to static data: {e}")
    
    # Fallback to static data
    if service_name not in CLOUD_SERVICES_MAP:
        return None
    
    mapping = CLOUD_SERVICES_MAP[service_name]
    
    # Get the other two providers
    providers = ['azure', 'aws', 'gcp']
    other_providers = [p for p in providers if p != source_provider]
    
    result = {
        'source': mapping.get(source_provider),
        'mappings': {
            provider: mapping.get(provider)
            for provider in other_providers
        }
    }
    
    return result


def _get_ai_service_mappings(service_name, source_provider):
    """
    Use Azure OpenAI to generate real-time service mappings with cost analysis
    
    Args:
        service_name: Name of the cloud service
        source_provider: Source cloud provider
        
    Returns:
        Dictionary with AI-generated mappings or None if failed
    """
    if not _openai_client:
        return None
    
    prompt = f"""You are a cloud architecture expert. validate  the cloud service "{service_name}" available from {source_provider.upper()} 
    and if it is available, provide equivalent services in the other two major cloud providers (Azure, AWS, GCP). if not available, indicate that the service is not available.
    
For each cloud provider (including the source), provide:
1. Service name (official name)
2. Category (Compute, Storage, Database, Networking, Serverless, Containers, etc.)
3. Description (brief, 1 sentence)
4. Cost range (approximate pricing with units)
5. Pricing model (how it's billed)

Return the response as a valid JSON object with this exact structure:
{{
  "source": {{
    "name": "service name",
    "category": "category",
    "description": "description",
    "cost_range": "cost range",
    "pricing_model": "pricing model"
  }},
  "mappings": {{
    "azure": {{
      "name": "service name",
      "category": "category",
      "description": "description",
      "cost_range": "cost range",
      "pricing_model": "pricing model"
    }},
    "aws": {{
      "name": "service name",
      "category": "category",
      "description": "description",
      "cost_range": "cost range",
      "pricing_model": "pricing model"
    }},
    "gcp": {{
      "name": "service name",
      "category": "category",
      "description": "description",
      "cost_range": "cost range",
      "pricing_model": "pricing model"
    }}
  }}
}}

Note: The "mappings" should NOT include the source provider. Only include the other two providers.
Provide accurate, up-to-date pricing information for February 2026."""

    try:
        response = _openai_client.chat.completions.create(
            model=_deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a cloud services expert specializing in multicloud architecture and cost optimization. Provide accurate, factual information about cloud services."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature for more factual responses
            max_tokens=1500,
            response_format={"type": "json_object"}
        )
        
        # Parse the AI response
        ai_response = response.choices[0].message.content
        result = json.loads(ai_response)
        
        # Validate the structure
        if 'source' in result and 'mappings' in result:
            # Remove source provider from mappings if it exists
            if source_provider in result['mappings']:
                del result['mappings'][source_provider]
            
            return result
        else:
            print("AI response missing required structure")
            return None
            
    except Exception as e:
        print(f"Error calling Azure OpenAI: {e}")
        return None


def search_service_by_partial_name(partial_name):
    """
    Search for services by partial name match
    
    Args:
        partial_name: Partial service name to search for
    
    Returns:
        List of matching service names
    """
    partial_lower = partial_name.lower()
    matches = [
        service for service in CLOUD_SERVICES_MAP.keys()
        if partial_lower in service.lower()
    ]
    return matches
