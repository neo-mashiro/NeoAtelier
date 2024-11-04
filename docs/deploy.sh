THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && (pwd -W 2> /dev/null || pwd))"
source "${THIS_DIR}/../setup.sh"

cd ${ATELIER_DOCS_ROOT}
mkdocs gh-deploy --no-history