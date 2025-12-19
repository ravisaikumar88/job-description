#!/bin/bash
# Setup script for Streamlit Cloud deployment
# This installs Playwright browsers during build time

echo "📦 Installing Playwright browsers..."
python -m playwright install chromium
python -m playwright install-deps chromium

echo "✅ Playwright setup complete!"

