# ANSI escape color codes
RED='\e[31m'
YELLOW='\e[93m'
BLUE='\e[34m'
MAGENTA='\e[35m'
CYAN='\e[36m'
GREEN='\e[32m'
PURPLE='\e[38;5;129m'  # purple is not a standard 16-bit color so it needs to mix up custom RGB values
ORANGE='\e[38;5;208m'
NC='\e[00m'            # \e[m, \e[0m, \e[00m all serve the same purpose

function print_debug { local message=$1; echo -e "${PURPLE}[DEBUG]${NC} - ${message}"; }
function print_info  { local message=$1; echo -e "${CYAN}[INFO]${NC} - ${message}"; }
function print_warn  { local message=$1; echo -e "${ORANGE}[WARNING]${NC} - ${message}"; }
function print_error { local message=$1; echo -e "${RED}[ERROR]${NC} - ${message}"; }

export ATELIER_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && (pwd -W 2> /dev/null || pwd))"
export ATELIER_DOCS_ROOT="${ATELIER_ROOT}/docs"
export ATELIER_BIN_ROOT="${ATELIER_ROOT}/bin"
export PATH="${ATELIER_BIN_ROOT}:$PATH"

# make sure pip will not install packages outside a virtual environment
export PIP_REQUIRE_VIRTUALENV=true

function activate_venv
{
    cd ${ATELIER_ROOT}

    if [[ "$OSTYPE" == linux-gnu* ]]; then
        source .venv/bin/activate
        print_info "Activated virtual environment $VIRTUAL_ENV on Linux"
    elif [[ "$OSTYPE" == cygwin* || "$OSTYPE" == msys* || "$OSTYPE" == win32* ]]; then
        source .venv/Scripts/activate
        print_info "Activated virtual environment $VIRTUAL_ENV on Windows"
    else
        print_error "Unsupported OS type detected: $OSTYPE"
        exit 1
    fi
}

if [ ! -d "${ATELIER_ROOT}/.venv" ]; then
    cd ${ATELIER_ROOT}
    print_info "Creating virtual environment in ${ATELIER_ROOT}/.venv"
    python -m venv .venv

    activate_venv

    print_info "Installing packages to $VIRTUAL_ENV"
    print_info "Installing mkdocs-material..."
    pip install mkdocs-material

    mkdocs --version
    pip show mkdocs-material

    echo ""
    print_info "Setup Done!"
    print_info "Deactivated virtual environment"
    deactivate
fi
