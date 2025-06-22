#!/bin/bash

# SecureKB Demo Script

echo "===== SecureKB Demo ====="
echo ""
echo "This demo showcases the role-based access control capabilities of SecureKB."
echo "We'll run the same queries with different user roles to demonstrate how the system"
echo "filters information based on department and clearance level."
echo ""

# Activate virtual environment
source .venv/bin/activate

# Run queries with different user roles
echo "===== Query: What are our financial projections? ====="
echo ""

echo "1. Sales User (department: sales, clearance: internal)"
python test_query.py --department sales --clearance internal --query "What are our financial projections?"
echo ""

echo "2. Finance User (department: finance, clearance: confidential)"
python test_query.py --department finance --clearance confidential --query "What are our financial projections?"
echo ""

echo "3. Executive User (department: executive, clearance: restricted)"
python test_query.py --department executive --clearance restricted --query "What are our financial projections?"
echo ""

echo "===== Query: What are our HR policies? ====="
echo ""

echo "1. Public User (department: public, clearance: public)"
python test_query.py --department public --clearance public --query "What are our HR policies?"
echo ""

echo "2. HR User (department: hr, clearance: confidential)"
python test_query.py --department hr --clearance confidential --query "What are our HR policies?"
echo ""

echo "===== Query: What are our acquisition plans? ====="
echo ""

echo "1. Sales User (department: sales, clearance: internal)"
python test_query.py --department sales --clearance internal --query "What are our acquisition plans?"
echo ""

echo "2. Finance User (department: finance, clearance: confidential)"
python test_query.py --department finance --clearance confidential --query "What are our acquisition plans?"
echo ""

echo "3. Executive User (department: executive, clearance: restricted)"
python test_query.py --department executive --clearance restricted --query "What are our acquisition plans?"
echo ""

echo "===== Demo Complete ====="
