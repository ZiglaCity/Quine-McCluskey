def to_binary(num, num_vars):
    return f"{num:0{num_vars}b}"

def count_ones(binary):
    return binary.count('1')

def combine_terms(term1, term2):
    diff_count = 0
    combined = []
    for bit1, bit2 in zip(term1, term2):
        if bit1 != bit2:
            diff_count += 1
            combined.append('-')
        else:
            combined.append(bit1)
    return ''.join(combined) if diff_count == 1 else None

def find_prime_implicants(minterms, num_vars):
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

def build_chart(minterms, prime_implicants):
    chart = {pi: [] for pi in prime_implicants}
    for minterm in minterms:
        binary = to_binary(minterm, len(next(iter(prime_implicants))))
        for pi in prime_implicants:
            if all(pi_bit == '-' or pi_bit == minterm_bit for pi_bit, minterm_bit in zip(pi, binary)):
                chart[pi].append(minterm)
    return chart

def extract_essential_prime_implicants(chart):
    essential_pis = []
    covered_minterms = []

    for pi, minterms in sorted(chart.items()):
        uncovered = [m for m in minterms if m not in covered_minterms]
        if len(uncovered) == 1:
            essential_pis.append(pi)
            covered_minterms.extend(minterms)
    return essential_pis, covered_minterms

def iterative_reduction(chart, essential_pis):
    covered_minterms = []
    for pi in essential_pis:
        covered_minterms.extend(chart[pi])
    covered_minterms = list(set(covered_minterms))

    remaining_chart = {}
    for pi, minterms in chart.items():
        remaining_minterms = [m for m in minterms if m not in covered_minterms]
        if remaining_minterms:
            remaining_chart[pi] = remaining_minterms

    while remaining_chart:
        max_pi = max(remaining_chart, key=lambda pi: len(remaining_chart[pi]))
        essential_pis.append(max_pi)
        covered_minterms.extend(remaining_chart[max_pi])
        covered_minterms = list(set(covered_minterms))

        new_remaining_chart = {}
        for pi, minterms in remaining_chart.items():
            remaining_minterms = [m for m in minterms if m not in covered_minterms]
            if remaining_minterms:
                new_remaining_chart[pi] = remaining_minterms
        remaining_chart = new_remaining_chart

    return essential_pis

def minimize_function(minterms, dont_cares, num_vars):
    all_terms = minterms + dont_cares
    prime_implicants = find_prime_implicants(all_terms, num_vars)
    chart = build_chart(minterms, prime_implicants)

    essential_pis, _ = extract_essential_prime_implicants(chart)
    final_pis = iterative_reduction(chart, essential_pis)

    return final_pis

def sop_expression(prime_implicants):
    # variables = ['A', 'B', 'C', 'D']  
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


def check_inputs(inputs):
    for item in inputs:
        if not item.isdigit():
            raise ValueError(f"Invalid input: {item}. All inputs should be integers.")
    return True
    
minterms = input("Enter minterms (e.g., 0, 1, 2): ")
dont_cares = input("Enter don't cares (e.g., 3, 4): ")
variables = input("Enter variables to change default (e.g., A, B, C, D): ")
num_vars = 3

# remove all white spaces and excess commas and remove all characters which are not numbers
minterms = minterms.replace(" ", "").strip(',')
minterms = [int(x) for x in minterms.split(',') if x.isdigit()]


if not dont_cares:
    dont_cares = []
else:
    dont_cares = dont_cares.replace(" ", "").strip(',')
    dont_cares = [int(x) for x in dont_cares.split(',') if x.isdigit()]

if not variables:
    variables = ['A', 'B', 'C', 'D']
    if int(max(minterms)) < 4:
        num_vars  = 2
    elif int(max(minterms)) < 8:
        num_vars = 3
    else:
        num_vars = 4

else:
    variables = variables.split(',')
    num_vars = len(variables)


# limiting the max minterm to just four variables
if int(max(minterms)) > 15:
    print("Minterm greater than expected!")


minterms.sort()
print(f"Minterms: {minterms}")
print(f"Don't Cares: {dont_cares}")
print(f"Variables: {variables}")
print(f"Number of variables: {num_vars}")


final_prime_implicants = minimize_function(minterms, dont_cares, num_vars)
final_expression = sop_expression(final_prime_implicants)

print("Minimized Boolean Function: F = ", final_expression)