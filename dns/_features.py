import importlib.metadata
import itertools
import string
from typing import Dict, List, Tuple

def _tuple_from_text(text: str) -> Tuple[int, ...]:
    """Convert version text like '1.2.3' or '1.2rc1' to a tuple of integers.
    
    Only includes numeric components, so '1.2rc1' becomes (1, 2).
    """
    if not text:
        return ()
    parts = []
    for part in text.split('.'):
        # Extract leading digits
        digits = ''
        for c in part:
            if c.isdigit():
                digits += c
            else:
                break
        if digits:
            parts.append(int(digits))
    return tuple(parts)

def _version_check(requirement: str) -> bool:
    """Is the requirement fulfilled?

    The requirement must be of the form

        package>=version
    """
    try:
        package, version = requirement.split('>=')
        installed_version = importlib.metadata.version(package)
        # Convert versions to tuples for comparison
        installed = tuple(int(x) for x in installed_version.split('.'))
        required = tuple(int(x) for x in version.split('.'))
        return installed >= required
    except (importlib.metadata.PackageNotFoundError, ValueError):
        return False
_cache: Dict[str, bool] = {}

def have(feature: str) -> bool:
    """Is *feature* available?

    This tests if all optional packages needed for the
    feature are available and recent enough.

    Returns ``True`` if the feature is available,
    and ``False`` if it is not or if metadata is
    missing.
    """
    if feature in _cache:
        return _cache[feature]
    if feature not in _requirements:
        return False
    result = all(_version_check(requirement) for requirement in _requirements[feature])
    _cache[feature] = result
    return result

def force(feature: str, enabled: bool) -> None:
    """Force the status of *feature* to be *enabled*.

    This method is provided as a workaround for any cases
    where importlib.metadata is ineffective, or for testing.
    """
    _cache[feature] = enabled
_requirements: Dict[str, List[str]] = {'dnssec': ['cryptography>=41'], 'doh': ['httpcore>=1.0.0', 'httpx>=0.26.0', 'h2>=4.1.0'], 'doq': ['aioquic>=0.9.25'], 'idna': ['idna>=3.6'], 'trio': ['trio>=0.23'], 'wmi': ['wmi>=1.5.1']}