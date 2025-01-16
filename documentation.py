# Function to convert a number to binary with leading zeros
def to_binary(num, num_vars):
    """
    Converts a number to its binary representation with leading zeros to match the number of variables.

    Args:
        num (int): The number to convert.
        num_vars (int): The number of binary digits (variables).

    Returns:
        str: Binary representation of the number with leading zeros.
    """
    return f"{num:0{num_vars}b}"

# Function to count the number of '1's in a binary string
def count_ones(binary):
    """
    Counts the number of '1's in a binary string.

    Args:
        binary (str): A binary string.

    Returns:
        int: The count of '1's in the binary string.
    """
    return binary.count('1')

# Function to combine two binary terms differing by one bit
def combine_terms(term1, term2):
    """
    Combines two binary terms if they differ by exactly one bit. Replaces the differing bit with a dash ('-').

    Args:
        term1 (str): The first binary term.
        term2 (str): The second binary term.

    Returns:
        str or None: The combined term with a dash for differing bits, or None if terms differ by more than one bit.
    """
    diff_count = 0
    combined = []
    for bit1, bit2 in zip(term1, term2):
        if bit1 != bit2:
            diff_count += 1
            combined.append('-')
        else:
            combined.append(bit1)
    return ''.join(combined) if diff_count == 1 else None

# Function to find all prime implicants
def find_prime_implicants(minterms, num_vars):
    """
    Finds all prime implicants from a given list of minterms using the Quine-McCluskey method.

    Args:
        minterms (list of int): List of minterms to minimize.
        num_vars (int): The number of variables in the Boolean function.

    Returns:
        list of str: A list of binary strings representing prime implicants.
    """
    groups = {i: [] for i in range(num_vars + 1)}
    for minterm in minterms:
        binary = to_binary(minterm, num_vars)
        groups[count_ones(binary)].append(binary)

    prime_implicants = []
    checked = []
    while any(groups.values()):
        next_groups = {i: [] for i in range(num_vars + 1)}
        for i in range(num_vars):
            for term1 in groups[i]:
                for term2 in groups[i + 1]:
                    combined = combine_terms(term1, term2)
                    if combined:
                        checked.append(term1)
                        checked.append(term2)
                        next_groups[count_ones(combined)].append(combined)
        prime_implicants.extend([term for group in groups.values() for term in group if term not in checked])
        groups = next_groups

    return prime_implicants

# Function to build a prime implicant chart
def build_chart(minterms, prime_implicants):
    """
    Constructs a prime implicant chart mapping prime implicants to the minterms they cover.

    Args:
        minterms (list of int): The list of minterms to cover.
        prime_implicants (list of str): List of prime implicants.

    Returns:
        dict: A dictionary where keys are prime implicants and values are lists of covered minterms.
    """
    chart = {pi: [] for pi in prime_implicants}
    for minterm in minterms:
        binary = to_binary(minterm, len(next(iter(prime_implicants))))
        for pi in prime_implicants:
            if all(pi_bit == '-' or pi_bit == minterm_bit for pi_bit, minterm_bit in zip(pi, binary)):
                chart[pi].append(minterm)
    return chart

# Function to extract essential prime implicants
def extract_essential_prime_implicants(chart):
    """
    Identifies and extracts essential prime implicants from the chart.

    Args:
        chart (dict): A prime implicant chart.

    Returns:
        tuple: A list of essential prime implicants and a list of covered minterms.
    """
    essential_pis = []
    covered_minterms = []

    for pi, minterms in sorted(chart.items()):
        uncovered = [m for m in minterms if m not in covered_minterms]
        if len(uncovered) == 1:
            essential_pis.append(pi)
            covered_minterms.extend(minterms)
    return essential_pis, covered_minterms

# Function for iterative reduction of remaining implicants
def iterative_reduction(chart, essential_pis):
    """
    Performs iterative reduction to select additional prime implicants and ensure all minterms are covered.

    Args:
        chart (dict): A prime implicant chart.
        essential_pis (list of str): List of already identified essential prime implicants.

    Returns:
        list of str: The final list of prime implicants covering all minterms.
    """
    covered_minterms = list(set(m for pi in essential_pis for m in chart[pi]))

    remaining_chart = {
        pi: [m for m in minterms if m not in covered_minterms]
        for pi, minterms in chart.items() if any(m not in covered_minterms for m in minterms)
    }

    while remaining_chart:
        max_pi = max(remaining_chart, key=lambda pi: len(remaining_chart[pi]))
        essential_pis.append(max_pi)
        covered_minterms.extend(remaining_chart[max_pi])
        covered_minterms = list(set(covered_minterms))

        remaining_chart = {
            pi: [m for m in minterms if m not in covered_minterms]
            for pi, minterms in remaining_chart.items() if any(m not in covered_minterms for m in minterms)
        }

    return essential_pis

# Function to minimize the Boolean function
def minimize_function(minterms, dont_cares, num_vars):
    """
    Minimizes a Boolean function using the Quine-McCluskey method.

    Args:
        minterms (list of int): List of minterms.
        dont_cares (list of int): List of don't-care conditions.
        num_vars (int): Number of variables.

    Returns:
        list of str: The minimized prime implicants.
    """
    all_terms = minterms + dont_cares
    prime_implicants = find_prime_implicants(all_terms, num_vars)
    chart = build_chart(minterms, prime_implicants)

    essential_pis, _ = extract_essential_prime_implicants(chart)
    final_pis = iterative_reduction(chart, essential_pis)

    return final_pis

# Function to generate SOP expression from prime implicants
def sop_expression(prime_implicants):
    """
    Converts prime implicants to a Sum of Products (SOP) expression.

    Args:
        prime_implicants (list of str): The prime implicants.

    Returns:
        str: The SOP expression.
    """
    variables = ['A', 'B', 'C', 'D']  # Extend this list for more variables
    terms = []

    for pi in sorted(prime_implicants):
        term = ''
        for idx, bit in enumerate(pi):
            if bit == '0':
                term += f"{variables[idx]}'"
            elif bit == '1':
                term += f"{variables[idx]}"
        terms.append(term)

    return ' + '.join(sorted(terms))


# Example input and execution
if __name__ == "__main__":
    # manually input the minterms and dont care values to run script directly... if not use use the cli script which allows users input values via command line
    minterms = [1,2,5,7]  # Minterms
    dont_cares = []  # Don't care conditions
    num_vars = 3  # Number of variables

    # Minimize function and generate SOP expression
    final_prime_implicants = minimize_function(minterms, dont_cares, num_vars)
    final_expression = sop_expression(final_prime_implicants)

    print("Minimized Boolean Function:", final_expression)
