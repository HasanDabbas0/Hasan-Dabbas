def validate_relation(relation):
    """Validate that the relation is a set of tuples with two elements."""
    if not isinstance(relation, set):
        raise ValueError("The relation must be a set.")
    if not all(isinstance(pair, tuple) and len(pair) == 2 for pair in relation):
        raise ValueError("Each element in the relation must be a tuple of two elements.")


def is_reflexive(relation, elements):
    """Check reflexivity of a relation."""
    for e in elements:
        if (e, e) not in relation:
            print(f"Missing reflexive pair: ({e}, {e})")
            return False
    return True


def is_symmetric(relation):
    """Check symmetry of a relation."""
    for a, b in relation:
        if (b, a) not in relation:
            print(f"Missing symmetric pair for: ({a}, {b})")
            return False
    return True


def is_transitive(relation, elements):
    """Check transitivity of a relation."""
    for a, b in relation:
        for c in elements:
            if (b, c) in relation and (a, c) not in relation:
                print(f"Missing transitive pair: ({a}, {c})")
                return False
    return True


def check_properties(relation):
    """Check properties of the relation."""
    validate_relation(relation)

    # Extract elements from the relation
    elements = set(e for pair in relation for e in pair)

    # Check properties
    reflexive = is_reflexive(relation, elements)
    symmetric = is_symmetric(relation)
    transitive = is_transitive(relation, elements)

    return reflexive, symmetric, transitive


if __name__ == "__main__":
    # Example usage: dynamic input from the user
    relation = set()
    n = int(input("Enter the number of pairs in the relation: "))
    print("Enter the pairs (format: a b):")
    for _ in range(n):
        a, b = map(int, input().split())
        relation.add((a, b))

    reflexive, symmetric, transitive = check_properties(relation)

    print(f"\nResults:")
    print(f"Reflexive: {reflexive}")
    print(f"Symmetric: {symmetric}")
    print(f"Transitive: {transitive}")
