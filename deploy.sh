#!/bin/bash

echo "🚀 AutoCDA Production Deployment Script"
echo "========================================"

# Check if environment is set
if [ -z "$DEPLOYMENT_TARGET" ]; then
    echo "Please set DEPLOYMENT_TARGET (heroku or railway)"
    exit 1
fi

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ Error: .env.production not found"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "🧪 Running basic tests..."
python -c "from backend.intent_extractor import IntentExtractor; print('✅ Intent extractor OK')"
python -c "from backend.dsl_generator import DSLGenerator; print('✅ DSL generator OK')"
python -c "from backend.circuit_validator import CircuitValidator; print('✅ Validator OK')"
python -c "from backend.skidl_generator import SKiDLGenerator; print('✅ SKiDL generator OK')"

if [ "$DEPLOYMENT_TARGET" == "heroku" ]; then
    echo "🔧 Deploying to Heroku..."
    
    # Create Heroku app if doesn't exist
    heroku create autocda-production || true
    
    # Set environment variables
    heroku config:set FLASK_ENV=production
    heroku config:set ANTHROPIC_API_KEY=$(grep ANTHROPIC_API_KEY .env.production | cut -d '=' -f2)
    heroku config:set SECRET_KEY=$(grep SECRET_KEY .env.production | cut -d '=' -f2)
    
    # Deploy
    git push heroku main
    
    echo "✅ Deployed to Heroku"
    heroku open

elif [ "$DEPLOYMENT_TARGET" == "railway" ]; then
    echo "🔧 Deploying to Railway..."
    
    # Install Railway CLI if not present
    if ! command -v railway &> /dev/null; then
        echo "Installing Railway CLI..."
        npm i -g @railway/cli
    fi
    
    # Login and deploy
    railway login
    railway up
    
    echo "✅ Deployed to Railway"
fi

echo "🎉 Deployment complete!"
