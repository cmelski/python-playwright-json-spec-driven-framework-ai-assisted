def validate_spec(spec: dict):

    if "flow" not in spec:
        raise ValueError("Spec missing 'flow'")

    for block in spec["flow"]:
        if not ("steps" in block or "assertions" in block):
            raise ValueError("Invalid flow block")
