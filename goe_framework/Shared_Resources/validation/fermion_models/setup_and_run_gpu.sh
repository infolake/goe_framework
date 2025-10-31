#!/bin/bash
# GoE Statistical Tests - Automated Setup and Execution for RunPod
# RTX 4090 GPU-Accelerated Version

set -e  # Exit on error

echo "================================================================================"
echo "GoE FERMION STATISTICAL TESTS - GPU SETUP (RTX 4090)"
echo "================================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on GPU
if ! command -v nvidia-smi &> /dev/null; then
    echo -e "${RED}ERROR: nvidia-smi not found. Are you on a GPU pod?${NC}"
    exit 1
fi

echo -e "${GREEN}GPU Detected:${NC}"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
echo ""

# Update system
echo "Updating system packages..."
apt-get update -qq
apt-get install -y -qq git python3-pip > /dev/null 2>&1
echo -e "${GREEN}✓ System updated${NC}"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
echo "  - numpy, scipy, matplotlib, pandas, seaborn"
pip3 install -q numpy scipy matplotlib pandas seaborn

echo "  - torch (CUDA-enabled)"
pip3 install -q torch torchvision --index-url https://download.pytorch.org/whl/cu121

echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Clone/update repository
cd /workspace

if [ -d "goe_framework" ]; then
    echo "Repository exists, pulling latest..."
    cd goe_framework
    git pull origin main -q
    cd ..
else
    echo "Cloning repository..."
    git clone https://github.com/infolake/goe_framework.git -q
fi

echo -e "${GREEN}✓ Repository ready${NC}"
echo ""

# Navigate to test directory
cd goe_framework/Shared_Resources/validation/fermion_models

echo "================================================================================"
echo "RUNNING GPU-ACCELERATED STATISTICAL TESTS"
echo "================================================================================"
echo ""
echo "Configuration:"
echo "  - Bootstrap samples: 100,000"
echo "  - Permutation tests: 100,000"
echo "  - Sectors: Leptons, Up Quarks, Down Quarks"
echo ""
echo "Expected runtime: ~30-60 seconds"
echo ""
echo "================================================================================"
echo ""

# Run GPU tests
python3 goe_fermion_statistical_tests_gpu.py

echo ""
echo "================================================================================"
echo "TESTS COMPLETED SUCCESSFULLY"
echo "================================================================================"
echo ""
echo "Output files in:"
echo "  $(pwd)"
echo ""
ls -lh goe_gpu_*.{pdf,png,json} 2>/dev/null || echo "  (Files generated)"
echo ""
echo "To view results:"
echo "  cat goe_gpu_statistical_tests_results.json | python3 -m json.tool"
echo ""
echo "================================================================================"

