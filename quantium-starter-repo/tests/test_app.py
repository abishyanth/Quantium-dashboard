import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sales_visulaizers import app


def _find_by_id(layout, target_id):
    """Traverse Dash layout tree and return the first component with id=target_id, or None."""
    if getattr(layout, "id", None) == target_id:
        return layout
    children = getattr(layout, "children", None)
    if children is None:
        return None
    if not isinstance(children, list):
        children = [children]
    for child in children:
        if hasattr(child, "id") or hasattr(child, "children"):
            found = _find_by_id(child, target_id)
            if found is not None:
                return found
    return None


def test_header_is_present():
    """Ensure the main header is present in the layout."""
    header = _find_by_id(app.layout, "main-header")
    assert header is not None
    children = getattr(header, "children", None)
    text = children if isinstance(children, str) else (children[0] if children else "")
    assert "Soul Foods" in str(text)


def test_visualisation_is_present():
    """Ensure the main sales graph is present in the layout."""
    graph = _find_by_id(app.layout, "sales-graph")
    assert graph is not None


def test_region_picker_is_present():
    """Ensure the region picker control is present in the layout."""
    region_control = _find_by_id(app.layout, "region-filter")
    assert region_control is not None
