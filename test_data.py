"""
Quick test script to verify the multicloud mapper setup
Run this to test the data layer without Azure OpenAI
"""

from cloud_services_data import (
    get_all_services, 
    get_service_mappings, 
    search_service_by_partial_name
)
import json


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def test_all_services():
    """Test getting all services"""
    print_section("TEST 1: List All Services")
    services = get_all_services()
    print(f"Total services in database: {len(services)}")
    print("\nFirst 10 services:")
    for i, service in enumerate(services[:10], 1):
        print(f"  {i}. {service}")


def test_service_mapping():
    """Test service mapping"""
    print_section("TEST 2: Service Mapping - Azure Virtual Machines")
    
    result = get_service_mappings("Azure Virtual Machines", "azure")
    
    if result:
        print(f"Source Service: {result['source']['name']}")
        print(f"Category: {result['source']['category']}")
        print(f"Cost Range: {result['source']['cost_range']}")
        print(f"\nEquivalent Services:")
        
        for provider, details in result['mappings'].items():
            print(f"\n  {provider.upper()}:")
            print(f"    Name: {details['name']}")
            print(f"    Cost: {details['cost_range']}")
            print(f"    Pricing: {details['pricing_model']}")
    else:
        print("Service not found!")


def test_search():
    """Test service search"""
    print_section("TEST 3: Search Services - 'Storage'")
    
    matches = search_service_by_partial_name("storage")
    print(f"Found {len(matches)} matches:")
    for match in matches:
        print(f"  - {match}")


def test_cross_provider():
    """Test cross-provider mapping"""
    print_section("TEST 4: Cross-Provider Mapping")
    
    test_cases = [
        ("Azure Functions", "azure"),
        ("AWS Lambda", "aws"),
        ("Cloud Functions", "gcp")
    ]
    
    for service, provider in test_cases:
        result = get_service_mappings(service, provider)
        if result:
            print(f"\n{service} ({provider.upper()}):")
            for other_provider, details in result['mappings'].items():
                print(f"  → {other_provider.upper()}: {details['name']}")


def test_cost_comparison():
    """Test cost comparison"""
    print_section("TEST 5: Cost Comparison - Database Services")
    
    databases = [
        "Azure SQL Database",
        "Amazon RDS",
        "Cloud SQL"
    ]
    
    print("Database Service Cost Ranges:")
    for db in databases:
        # Find which provider this belongs to
        for provider in ['azure', 'aws', 'gcp']:
            result = get_service_mappings(db, provider)
            if result and result['source']:
                print(f"\n{db}:")
                print(f"  Cost Range: {result['source']['cost_range']}")
                print(f"  Pricing Model: {result['source']['pricing_model']}")
                break


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  MULTICLOUD MAPPER - DATA LAYER TEST")
    print("="*70)
    
    try:
        test_all_services()
        test_service_mapping()
        test_search()
        test_cross_provider()
        test_cost_comparison()
        
        print_section("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("Data layer is working correctly!")
        print("\nNext steps:")
        print("1. Configure Azure OpenAI in .env file")
        print("2. Run: python app.py")
        print("3. Open index.html in your browser")
        
    except Exception as e:
        print_section("❌ TEST FAILED")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
