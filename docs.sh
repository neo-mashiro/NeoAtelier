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

export MANA_OASIS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && (pwd -W 2> /dev/null || pwd))"
export PATH=${MANA_OASIS_ROOT}/bin:$PATH
cd ${MANA_OASIS_ROOT}

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

cd ${MANA_OASIS_ROOT}/docs

print_info "Cleaning up existing doc builds..."
# rm -R ${MANA_OASIS_ROOT}/docs/docs
print_info "Building documentation..."
# mkdocs serve --open ???
mkdocs serve --open

