"""
Flask API for Multicloud Mapper Service
Provides REST endpoints for the AI-powered cloud service mapping
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_agent import MulticloudMapperAgent
from bom_agent import BOMGeneratorAgent
from cloud_services_data import get_all_services, search_service_by_partial_name
import os
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize AI agents
agent = MulticloudMapperAgent()
bom_agent = BOMGeneratorAgent()


@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'service': 'Multicloud Mapper AI Service',
        'version': '1.0.0'
    })


@app.route('/api/services', methods=['GET'])
def list_services():
    """Get list of all available services"""
    try:
        result = agent.list_all_services()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search', methods=['GET'])
def search_services():
    """Search for services by partial name"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Query parameter "q" is required'
        }), 400
    
    try:
        matches = search_service_by_partial_name(query)
        return jsonify({
            'success': True,
            'query': query,
            'matches': matches,
            'count': len(matches)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/map', methods=['POST'])
def map_service():
    """
    Map a cloud service to equivalent services in other clouds
    
    Request body:
    {
        "service_name": "Azure Virtual Machines",
        "source_provider": "azure"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        service_name = data.get('service_name')
        source_provider = data.get('source_provider')
        
        if not service_name or not source_provider:
            return jsonify({
                'success': False,
                'error': 'Both service_name and source_provider are required'
            }), 400
        
        # Validate provider
        valid_providers = ['azure', 'aws', 'gcp']
        if source_provider.lower() not in valid_providers:
            return jsonify({
                'success': False,
                'error': f'Invalid provider. Must be one of: {", ".join(valid_providers)}'
            }), 400
        
        # Get mapping with AI analysis
        result = agent.analyze_service_mapping(service_name, source_provider.lower())
        
        if not result['success']:
            return jsonify(result), 404
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """
    Get AI-powered recommendations for cloud service selection
    
    Request body:
    {
        "service_name": "Amazon S3",
        "source_provider": "aws",
        "requirements": {
            "budget": "low",
            "usage": "high traffic"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        service_name = data.get('service_name')
        source_provider = data.get('source_provider')
        requirements = data.get('requirements')
        
        if not service_name or not source_provider:
            return jsonify({
                'success': False,
                'error': 'Both service_name and source_provider are required'
            }), 400
        
        result = agent.get_recommendations(service_name, source_provider.lower(), requirements)
        
        if not result['success']:
            return jsonify(result), 404
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/identify', methods=['POST'])
def identify_technology():
    """
    Identify third-party technology/product and suggest Azure equivalents
    
    Request body:
    {
        "technology_name": "MongoDB"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        technology_name = data.get('technology_name')
        
        if not technology_name:
            return jsonify({
                'success': False,
                'error': 'technology_name is required'
            }), 400
        
        # Identify and map to Azure
        result = agent.identify_and_map_to_azure(technology_name)
        
        if not result['success']:
            return jsonify(result), 404
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/bom/validate', methods=['POST'])
def validate_diagram():
    """
    Validate if uploaded image is an architecture diagram
    
    Request body:
    {
        "image": "base64 encoded image data"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'Image data is required'
            }), 400
        
        image_data = data['image']
        
        # Validate the diagram
        result = bom_agent.validate_architecture_diagram(image_data)
        
        return jsonify({
            'success': True,
            'validation': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/bom/analyze', methods=['POST'])
def analyze_diagram():
    """
    Analyze architecture diagram and generate BOM with costs
    
    Request body:
    {
        "image": "base64 encoded image data"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'Image data is required'
            }), 400
        
        image_data = data['image']
        
        # Process diagram: validate and analyze
        result = bom_agent.process_diagram(image_data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/bom/generate', methods=['POST'])
def generate_bom_only():
    """
    Generate BOM for a pre-validated diagram
    
    Request body:
    {
        "image": "base64 encoded image data"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'Image data is required'
            }), 400
        
        image_data = data['image']
        
        # Generate BOM directly
        result = bom_agent.analyze_diagram_and_generate_bom(image_data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print(f"\n{'='*60}")
    print(f"🚀 Multicloud Mapper AI Service Starting...")
    print(f"{'='*60}")
    print(f"📍 Running on: http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"📊 Services:")
    print(f"   - Multicloud Service Mapper")
    print(f"   - BOM Generator (Architecture Diagram Analysis)")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
