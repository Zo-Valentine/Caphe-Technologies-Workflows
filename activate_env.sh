#!/bin/bash
# Activation script for caphe.env virtual environment

echo "🚀 Activating caphe.env virtual environment..."
source caphe.env/bin/activate

echo "✅ Virtual environment activated!"
echo ""
echo "Python version: $(python --version)"
echo "Python location: $(which python)"
echo ""
echo "To deactivate, run: deactivate"
