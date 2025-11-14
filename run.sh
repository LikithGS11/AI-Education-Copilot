#!/bin/bash

# AI Copilot System Startup Script
# Starts Flask backend and React frontend, then opens browser

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/flask-ai-copilot"
FRONTEND_DIR="$SCRIPT_DIR/react-ai-copilot"

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to cleanup on exit
cleanup() {
    print_info "Shutting down servers..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        print_info "Backend stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        print_info "Frontend stopped"
    fi
    exit 0
}

# Trap Ctrl+C and cleanup
trap cleanup SIGINT SIGTERM

echo "=========================================="
echo "  AI Copilot System Startup"
echo "=========================================="
echo ""

# Check if directories exist
if [ ! -d "$BACKEND_DIR" ]; then
    print_error "Backend directory not found: $BACKEND_DIR"
    exit 1
fi

if [ ! -d "$FRONTEND_DIR" ]; then
    print_error "Frontend directory not found: $FRONTEND_DIR"
    exit 1
fi

# Check if .env exists
if [ ! -f "$BACKEND_DIR/.env" ]; then
    print_warning ".env file not found in backend directory"
    print_info "Please create $BACKEND_DIR/.env with your API keys"
    print_info "See RUNNING_THE_PROJECT.md for details"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Start Flask backend
print_info "Starting Flask backend..."
cd "$BACKEND_DIR"

# Check for virtual environment
if [ -d "venv" ]; then
    print_info "Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    print_info "Activating virtual environment..."
    source .venv/bin/activate
fi

# Start backend in background
python app.py > backend.log 2>&1 &
BACKEND_PID=$!

print_info "Backend starting (PID: $BACKEND_PID)"
print_info "Logs: $BACKEND_DIR/backend.log"

# Wait for backend to be ready
print_info "Waiting for backend to be ready..."
MAX_ATTEMPTS=30
ATTEMPT=0
BACKEND_READY=false

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    sleep 2
    ATTEMPT=$((ATTEMPT + 1))
    
    if curl -s http://localhost:5000/check-keys > /dev/null 2>&1; then
        BACKEND_READY=true
        break
    fi
    
    echo -n "."
done
echo ""

if [ "$BACKEND_READY" = true ]; then
    print_success "Backend is running on http://localhost:5000"
    
    # Check API keys
    if curl -s http://localhost:5000/check-keys | grep -q '"generator_initialized":true'; then
        print_success "API keys loaded and generator initialized"
    else
        print_warning "Generator not initialized. Check API keys in .env file"
    fi
else
    print_error "Backend failed to start after $MAX_ATTEMPTS attempts"
    print_error "Check logs: $BACKEND_DIR/backend.log"
    cleanup
    exit 1
fi

# Start React frontend
print_info "Starting React frontend..."
cd "$FRONTEND_DIR"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    print_warning "node_modules not found. Installing dependencies..."
    npm install
fi

# Start frontend in background
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!

print_info "Frontend starting (PID: $FRONTEND_PID)"
print_info "Logs: $FRONTEND_DIR/frontend.log"

# Wait for frontend to be ready
print_info "Waiting for frontend to be ready..."
MAX_ATTEMPTS=30
ATTEMPT=0
FRONTEND_READY=false

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    sleep 2
    ATTEMPT=$((ATTEMPT + 1))
    
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        FRONTEND_READY=true
        break
    fi
    
    echo -n "."
done
echo ""

if [ "$FRONTEND_READY" = true ]; then
    print_success "Frontend is running on http://localhost:3000"
else
    print_warning "Frontend may still be starting. Check logs: $FRONTEND_DIR/frontend.log"
fi

# Open browser
print_info "Opening browser..."
sleep 2

if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:3000
elif command -v open > /dev/null; then
    open http://localhost:3000
elif command -v start > /dev/null; then
    start http://localhost:3000
else
    print_warning "Could not automatically open browser"
    print_info "Please open http://localhost:3000 manually"
fi

echo ""
echo "=========================================="
print_success "AI Copilot System is running!"
echo "=========================================="
echo ""
print_info "Backend:  http://localhost:5000"
print_info "Frontend: http://localhost:3000"
echo ""
print_info "Press Ctrl+C to stop all servers"
echo ""

# Wait for user interrupt
wait

