from spec.validator import validate_spec
from spec.enricher import enrich_spec


def process_spec(spec: dict) -> dict:

    validate_spec(spec)
    spec = enrich_spec(spec)

    return spec
