#!/usr/bin/env bash
# Build script for render.com deployment

# Exit on error
set -e

# Install dependencies with binary wheels
echo "Installing base packages..."
pip install --upgrade pip setuptools wheel

# Install minimal dependencies without any Rust components
echo "Installing minimal dependencies..."
pip install fastapi==0.103.1 uvicorn==0.22.0 motor==3.1.2 pymongo==4.3.3 pydantic==2.4.2 python-dotenv==1.0.0

# Replace Pydantic v1 files with v2 compatible versions
echo "Replacing Pydantic v1 files with v2 compatible versions..."

# Replace models/order.py with models/order_v2.py
if [ -f models/order_v2.py ]; then
    cp models/order_v2.py models/order.py
    echo "✅ Replaced models/order.py with v2 version"
fi

# Replace schemas/common.py with schemas/common_v2.py
if [ -f schemas/common_v2.py ]; then
    cp schemas/common_v2.py schemas/common.py
    echo "✅ Replaced schemas/common.py with v2 version"
fi

# Replace schemas/order.py with schemas/order_v2.py
if [ -f schemas/order_v2.py ]; then
    cp schemas/order_v2.py schemas/order.py
    echo "✅ Replaced schemas/order.py with v2 version"
fi

# Use simplified main file for production
if [ -f main_prod.py ]; then
    cp main_prod.py main_deploy.py
    echo "✅ Using simplified main file for deployment"
fi

echo "Deployment preparation complete!" 