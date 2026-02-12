def enrich_spec(spec: dict):

    for block in spec["flow"]:
        if "steps" in block:
            for step in block["steps"]:
                step.setdefault("timeout", 5000)

    return spec
