"""
Test script to verify real-time Azure OpenAI integration for service mapping
"""

import json
from cloud_services_data import get_service_mappings, search_service_by_partial_name

def test_realtime_ai_mapping():
    """Test the AI-powered service mapping"""
    
    print("="*70)
    print("Testing Real-Time AI Service Mapping with Azure OpenAI")
    print("="*70)
    print()
    
    # Test Case 1: Query a service with AI
    print("Test 1: Azure Virtual Machines (with AI)")
    print("-" * 70)
    result = get_service_mappings("Azure Virtual Machines", "azure", use_ai=True)
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("No result found")
    print()
    
    # Test Case 2: Query a custom/new service that's not in static data
    print("\nTest 2: Azure AI Search (new service, AI-generated)")
    print("-" * 70)
    result = get_service_mappings("Azure AI Search", "azure", use_ai=True)
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("No result found")
    print()
    
    # Test Case 3: AWS service
    print("\nTest 3: Amazon Lambda (with AI)")
    print("-" * 70)
    result = get_service_mappings("AWS Lambda", "aws", use_ai=True)
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("No result found")
    print()
    
    # Test Case 4: GCP service
    print("\nTest 4: Google Cloud Run (with AI)")
    print("-" * 70)
    result = get_service_mappings("Cloud Run", "gcp", use_ai=True)
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("No result found")
    print()
    
    # Test Case 5: Fallback to static data
    print("\nTest 5: Azure Functions (without AI, static data)")
    print("-" * 70)
    result = get_service_mappings("Azure Functions", "azure", use_ai=False)
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("No result found")
    print()
    
    print("="*70)
    print("Testing Complete!")
    print("="*70)


if __name__ == "__main__":
    test_realtime_ai_mapping()
