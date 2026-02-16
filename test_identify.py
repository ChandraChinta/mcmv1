"""
Test script for the new identify technology endpoint
"""
import requests
import json

API_BASE_URL = 'http://localhost:5000/api'

def test_identify_technology():
    """Test identifying third-party technologies"""
    
    test_cases = [
        "MongoDB",
        "Redis",
        "Apache Kafka",
        "Docker",
        "PostgreSQL",
        "RabbitMQ"
    ]
    
    print("="*80)
    print("Testing Technology Identification and Azure Mapping")
    print("="*80)
    
    for technology in test_cases[:2]:  # Test first 2 to save time
        print(f"\n\n{'='*80}")
        print(f"Testing: {technology}")
        print("="*80)
        
        try:
            response = requests.post(
                f'{API_BASE_URL}/identify',
                json={'technology_name': technology},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data['success']:
                    analysis = data['analysis']
                    print(f"\n✓ Successfully identified: {analysis['technology_name']}")
                    print(f"  Type: {analysis['technology_type']}")
                    print(f"  Provider: {analysis['provider']}")
                    print(f"  Cloud Native: {analysis['is_cloud_native']}")
                    print(f"\n  Azure Equivalents Found: {len(analysis['azure_equivalents'])}")
                    
                    if analysis['azure_equivalents']:
                        print("\n  Top Azure Services:")
                        for equiv in analysis['azure_equivalents'][:3]:
                            print(f"    - {equiv['azure_service']} ({equiv['match_type']}, {equiv['match_score']}%)")
                    
                    print(f"\n  Recommended: {analysis['recommended_azure_service']}")
                else:
                    print(f"\n✗ Error: {data.get('error', 'Unknown error')}")
            else:
                print(f"\n✗ HTTP Error: {response.status_code}")
                print(response.text)
                
        except requests.exceptions.ConnectionError:
            print(f"\n✗ Connection Error: Make sure Flask app is running on {API_BASE_URL}")
            break
        except Exception as e:
            print(f"\n✗ Error: {str(e)}")
    
    print("\n" + "="*80)
    print("Test completed!")
    print("="*80)

if __name__ == "__main__":
    test_identify_technology()
