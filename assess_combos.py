from combo_selection import dyn

detailed_output = False # Set to True to get detailed information on all score components
num_results = 6 # Maximum number of recommendations for each organization

def get_input(name):
    # Pre-process input from CSV files
    first = True
    keys = []
    results = {}
    with open(name) as f:
        for line in f:
            line = line.strip('\n')
            if first:
                # Split line of CSV by commas and store header as keys
                first = False
                keys = line.split(',')
            else:
                # Retrieve values for each column in CSV
                result = {}
                parts = line.split(',')
                for i, key in enumerate(keys):
                    # Convert numeric values or alternatively store values as strings
                    if parts[i].replace('.', '', 1).isdigit():
                        result[key] = float(parts[i])
                    else:
                        result[key] = parts[i]
                if 'det' in result:
                    # List of solutions separated by semi-colon
                    result['det'] = result['det'].split(';')
                results[result['id']] = result
    return results

# Load CSV files
techniques = get_input('techniques.txt')
solutions = get_input('solutions.txt')
organizations = get_input('organizations.txt')

# Create a dictionary storing solutions as keys and corresponding covered attack techniques as values
solutions_dict = {}
for sol_id, solution in solutions.items():
    techniques_covered = []
    for t_id, technique in techniques.items():
        for covered_technique in technique['det']:
            if covered_technique not in solutions and covered_technique != 'N/A':
                print('Unknown technique in ' + str(t_id) + ': ' + str(covered_technique))
        if sol_id in technique['det']:
            techniques_covered.append(technique)
            if sol_id in solutions_dict:
                solutions_dict[sol_id].add(technique['id'])
            else:
                solutions_dict[sol_id] = set([technique['id']])
    solutions[sol_id]['covered'] = techniques_covered

# Compute the maximum score that could theoretically be achieved by a solution covering all techniques for normalization
sum_techniques = 0
for t_id, technique in techniques.items():
    sum_techniques += technique['weight'] * technique['relevance']

# Get all combinations and covered techniques
solution_ids, techniques_result = dyn(0, solutions_dict, set(), set(), {})

# Create a list of combinations with aggregated values for price, complexity, etc. based on the indivdual solutions
combinations = {}
for solution_id_list in solution_ids:
    if len(solution_id_list) == 0:
        # Omit empty set
        continue
    combo_id_list = []
    combo_prices = []
    combo_complexities = []
    combo_covered = []
    combo_lml = []
    for solution_id in solution_id_list:
        combo_id_list.append(solution_id)
        combo_prices.append((solutions[solution_id]['price'], solutions[solution_id]['unit']))
        combo_complexities.append(solutions[solution_id]['complexity'])
        combo_lml.append(solutions[solution_id]['lml'])
        for covered_technique in solutions[solution_id]['covered']:
            if covered_technique not in combo_covered:
                combo_covered.append(covered_technique)
    combo = {}
    combo['id'] = combo_id_list
    combo['prices'] = combo_prices # Prices depend on employees and are thus organization-specific
    combo['complexity'] = max(combo_complexities) + (len(combo_complexities) - 1) / len(solutions) # Combined complexity is highest individual complexity and further increases when many solutions are involved
    combo['covered'] = combo_covered
    combo['lml'] = max(0, min(1, sum(combo_lml))) # LML is fulfilled by combination when at least one solution fulfills LML and no solution prevents LML
    combinations[frozenset(combo['id'])] = combo

def get_results(organizations):
    results = {}
    for org_id, organization in organizations.items():
        scores = {}
        for sol_id, solution in combinations.items():
            techniques_covered = solution['covered']
            # Compute cost based on solution price and organization properties
            sol_cost = 0
            for price in solution['prices']:
                if price[1] == 'usermonth':
                    sol_cost += price[0]
                elif price[1] == 'gb':
                    sol_cost += price[0] * organization['gbperempl']
                elif price[1] == 'month':
                    sol_cost += price[0] / organization['empl']
            # Compute score based on techniques covered by solution
            t_score = 0
            for t in techniques_covered:
                t_score += t['weight'] * t['relevance']
            # Compute score factor based on cost
            cost_score = 1
            if organization['cost'] < sol_cost: # Lower price is always acceptable
                cost_score = organization['cost'] / sol_cost
            cost_fact = 1
            if cost_score != 0 and organization['cost_importance']!= 0: # Avoid 0^0
                cost_fact = pow(cost_score, organization['cost_importance'])
            # Compute score factor based on complexity
            compl_score = 1
            if organization['complexity'] < solution['complexity']: # Lower complexity is always acceptable
                compl_score = organization['complexity'] / solution['complexity']
            compl_fact = 1
            if compl_score != 0 and organization['complexity_importance'] != 0: # Avoid 0^0
                compl_fact = pow(compl_score, organization['complexity_importance'])
            # Compute lml factor
            lml_fact = pow(solution['lml'], organization['lml'])
            # Combine score with factors
            score = t_score * cost_fact * compl_fact * lml_fact
            scores[sol_id] = {'score': score, 'covered': len(techniques_covered), 't_score': t_score, 'cost_score': cost_score, 'cost_fact': cost_fact, 'compl_score': compl_score, 'compl_fact': compl_fact, 'lml_fact': lml_fact}
        scores_sorted = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1]['score'], reverse=True)}
        results[org_id] = scores_sorted
    return results

# Print results
scores = get_results(organizations)
for org, score in scores.items():
    print('Recommended solutions for organization ' + org + ':')
    cnt = 1
    for sol, s in score.items():
        if cnt > num_results:
            break
        cnt += 1
        output = ' * ' + str('+'.join(list(sol))) + ': ' + str(round(s['score'] / sum_techniques, 3))
        if detailed_output:
            output += ' ('
            for k, v in s.items():
                output += str(k) + ': ' + str(v) + ', '
            output = output[:-2] + ')'
        print(output)
    print('')

