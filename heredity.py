import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
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
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


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
    joint_p = 1  # Initial joint probability (unknown)
    for person in people:
        person_dict = people[person]  # Find person's info

        # Assign number of genes if known
        if person_dict["mother"] == None and person_dict["father"] == None:
            if person in two_genes:
                gene_number = 2
            elif person in one_gene:
                gene_number = 1
            else:
                gene_number = 0

            p = PROBS["gene"][gene_number]  # Contribute to joint probability

        # If a child
        else:
            # Probabilities of mother passing on the gene
            if person_dict["mother"] in two_genes:
                mprob_pass = 1 - PROBS["mutation"]
            elif person_dict["mother"] in one_gene:
                mprob_pass = 0.5
            else:
                mprob_pass = PROBS["mutation"]

            # Probabilities of father passing on the gene
            if person_dict["father"] in two_genes:
                fprob_pass = 1 - PROBS["mutation"]
            elif person_dict["father"] in one_gene:
                fprob_pass = 0.5
            else:
                fprob_pass = PROBS["mutation"]

            # Calculate joint probabilities for gene passing
            if person in two_genes:  # Mother and Father pass
                gene_number = 2
                p = mprob_pass * fprob_pass
            elif person in one_gene:  # Mother pass Xor Father pass
                gene_number = 1
                p = mprob_pass * (1 - fprob_pass) + fprob_pass * (1 - mprob_pass)
            else:  # No pass
                gene_number = 0
                p = (1 - mprob_pass) * (1 - fprob_pass)
            
        # Add trait probabilities for child to joint probability
        if person in have_trait:
            has_trait = True
        else:
            has_trait = False

        p *= PROBS["trait"][gene_number][has_trait]
        joint_p *= p
    
    return joint_p


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        person_dict = probabilities[person]

        # Gene number check
        if person in two_genes:
            gene_number = 2
        elif person in one_gene:
            gene_number = 1
        else:
            gene_number = 0

        # Trait check
        if person in have_trait:
            has_trait = True
        else:
            has_trait = False

        # Add new joint probability
        person_dict["gene"][gene_number] += p
        person_dict["trait"][has_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        person_dict = probabilities[person]

        # Normalise gene probabilities
        n = 0
        for probability in person_dict["gene"].values():
            n += probability  # Sum probs
        for gene in person_dict["gene"]:
            person_dict["gene"][gene] /= n  # Divide each by sum

        # Normalise trait probabilities
        n = 0
        for probability in person_dict["trait"].values():
            n += probability  # Sum probs
        for trait in person_dict["trait"]:
            person_dict["trait"][trait] /= n  # Divide each by sum


if __name__ == "__main__":
    main()
