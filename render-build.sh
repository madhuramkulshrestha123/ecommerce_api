#!/usr/bin/env bash
# Build script for render.com deployment

# Exit on error
set -e

# Install production dependencies
echo "Installing production dependencies..."
pip install -r requirements-prod.txt

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

echo "Deployment preparation complete!" 