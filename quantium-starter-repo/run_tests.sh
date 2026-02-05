set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ -f "$PROJECT_ROOT/venv/Scripts/activate" ]; then

    source "$PROJECT_ROOT/venv/Scripts/activate"
elif [ -f "$PROJECT_ROOT/venv/bin/activate" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
elif [ -f "$SCRIPT_DIR/venv/Scripts/activate" ]; then
    source "$SCRIPT_DIR/venv/Scripts/activate"
elif [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo "Error: Could not find virtual environment (looked in $PROJECT_ROOT/venv and $SCRIPT_DIR/venv)." >&2
    exit 1
fi

cd "$SCRIPT_DIR"
if pytest; then
    exit 0
else
    exit 1
fi
