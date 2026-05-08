#!/bin/bash
# VOID-SHELL Launch Script
# Automatically detects platform and launches the application

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[VOID-SHELL]${NC} $1"
}

success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

error() {
    echo -e "${RED}[✗]${NC} $1" >&2
    exit 1
}

warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        error "Python3 is not installed. Please install Python 3.8+ first."
    fi
    
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if [[ "$PYTHON_VERSION" < "3.8" ]]; then
        error "Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    fi
    
    success "Python $PYTHON_VERSION detected"
}

# Check dependencies
check_dependencies() {
    log "Checking dependencies..."
    
    # Install via pip if not present
    python3 -m pip install --upgrade pip > /dev/null 2>&1 || true
    
    # Check for required packages
    REQUIRED_PKGS=("requests" "rich" "click" "pyyaml")
    for pkg in "${REQUIRED_PKGS[@]}"; do
        if ! python3 -c "import $pkg" 2> /dev/null; then
            log "Installing $pkg..."
            python3 -m pip install "$pkg" --quiet || error "Failed to install $pkg"
        fi
    done
    
    success "All dependencies satisfied"
}

# Run setup wizard if needed
run_setup_wizard() {
    if [ ! -f ".void_shell_configured" ]; then
        log "First-time setup detected. Running configuration wizard..."
        python3 void_shell/utils/wizard.py --interactive
        touch .void_shell_configured
        success "Setup complete!"
    fi
}

# Run doctor check
run_doctor_check() {
    log "Running system diagnostics..."
    python3 void_shell/utils/doctor.py
}

# Launch the application
launch_application() {
    log "Launching VOID-SHELL..."
    python3 void_shell/main.py "$@"
}

# Main execution
main() {
    echo ""
    log "========================================"
    log "  VOID-SHELL Launch Script"
    log "========================================"
    echo ""
    
    check_python
    check_dependencies
    run_setup_wizard
    run_doctor_check
    launch_application "$@"
    
    echo ""
    success "VOID-SHELL launched successfully!"
    echo ""
}

main "$@"
