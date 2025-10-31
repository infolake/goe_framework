#!/bin/bash
# Execute este script DENTRO do pod após conectar via SSH
# Automated GPU testing for RTX 4090

set -e
clear

echo "================================================================"
echo "GoE STATISTICAL TESTS - GPU ACCELERATED"
echo "================================================================"
echo ""
echo "Checking GPU..."
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
echo ""

echo "Installing dependencies..."
apt-get update -qq > /dev/null 2>&1
apt-get install -y -qq git python3-pip > /dev/null 2>&1

pip3 install -q numpy scipy matplotlib pandas seaborn
pip3 install -q torch torchvision --index-url https://download.pytorch.org/whl/cu121

echo "Cloning/updating repository..."
cd /workspace
if [ -d "goe_framework" ]; then
    cd goe_framework && git pull -q origin main && cd ..
else
    git clone -q https://github.com/infolake/goe_framework.git
fi

cd goe_framework/Shared_Resources/validation/fermion_models

echo ""
echo "================================================================"
echo "RUNNING GPU TESTS (100k Bootstrap + 100k Permutation)"
echo "================================================================"
echo ""

python3 goe_fermion_statistical_tests_gpu.py

echo ""
echo "================================================================"
echo "DONE! Results saved in:"
echo "$(pwd)"
echo ""
ls -lh goe_gpu_*.{pdf,png,json} 2>/dev/null
echo "================================================================"

