#!/usr/bin/env bash
# Build script for render.com deployment

# Exit on error
set -e

# Set temporary writable paths to avoid "read-only file system" errors with Rust crates
export CARGO_HOME=$(mktemp -d)
export RUSTUP_HOME=$(mktemp -d)

echo "🔧 Installing pip and build tools..."
pip install --upgrade pip setuptools wheel

echo "📦 Installing production dependencies from requirements-prod.txt..."
pip install --no-cache-dir --no-binary :all: -r requirements-prod.txt || pip install --no-cache-dir -r requirements-prod.txt

echo "🔁 Replacing v1 files with Pydantic v2 compatible versions if they exist..."

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

echo "🚀 Deployment preparation complete!"
