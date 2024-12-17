import csv
import itertools
import sys

PROBS = {
    # Unconditional probabilities for having gene
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        # Probability of trait given two copies of gene
        2: {True: 0.65, False: 0.35},
        # Probability of trait given one copy of gene
        1: {True: 0.56, False: 0.44},
        # Probability of trait given no gene
        0: {True: 0.01, False: 0.99},
    },
    # Mutation probability
    "mutation": 0.01,
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):
        # Check if current set of people violates known information
        fails_evidence = any(
            (
                people[person]["trait"] is not None
                and people[person]["trait"] != (person in have_trait)
            )
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (
                    True
                    if row["trait"] == "1"
                    else False
                    if row["trait"] == "0"
                    else None
                ),
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s)
        for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def parent(one_gene, two_genes, mother, father):
    """
    this function returns the probability with which a person inherits the gene from their mother and father.
    """
    mother_side = 1
    father_side = 1
    if mother not in one_gene and mother not in two_genes:
        mother_side *= PROBS["mutation"]
    elif mother in two_genes:
        mother_side *= 1 - PROBS["mutation"]
    elif mother in one_gene:
        mother_side *= 0.5
    if father not in one_gene and father not in two_genes:
        father_side *= PROBS["mutation"]
    elif father in two_genes:
        father_side *= 1 - PROBS["mutation"]
    elif father in one_gene:
        father_side *= 0.5
    return mother_side, father_side


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    vals = dict()
    for person in people:
        prob = 0
        number = 0
        mother = people[person]["mother"]
        father = people[person]["father"]
        if mother != None and father != None:
            mother_side, father_side = parent(one_gene, two_genes, mother, father)
            if person not in one_gene and person not in two_genes:
                prob = (1 - mother_side) * (1 - father_side)
                number = 0
            elif person in one_gene:
                prob = ((1 - mother_side) * father_side) + (
                    (1 - father_side) * mother_side
                )
                number = 1
            elif person in two_genes:
                prob = mother_side * father_side
                number = 2
        elif mother == None and father == None:
            if person not in one_gene and person not in two_genes:
                prob = PROBS["gene"][0]
                number = 0
            elif person in one_gene:
                prob = PROBS["gene"][1]
                number = 1
            elif person in two_genes:
                prob = PROBS["gene"][2]
                number = 2
        vals[person] = [prob, number]
        value = []
    for person in people:
        traitcheck = False
        if person in have_trait:
            traitcheck = True
        val = float(vals[person][0])
        val *= float(PROBS["trait"][int(vals[person][1])][traitcheck])
        value.append(val)
    joint_probability = 1
    for v in value:
        joint_probability *= v
    return joint_probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person not in one_gene and person not in two_genes:
            probabilities[person]["gene"][0] += p
        elif person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        v = []
        for value in probabilities[person]["gene"]:
            v.append(probabilities[person]["gene"][value])
        for value in probabilities[person]["gene"]:
            probabilities[person]["gene"][value] /= sum(v)

        v = []
        for value in probabilities[person]["trait"]:
            v.append(probabilities[person]["trait"][value])
        for value in probabilities[person]["trait"]:
            probabilities[person]["trait"][value] /= sum(v)


if __name__ == "__main__":
    main()
