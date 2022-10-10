# This file contains a function that returns all combinations of keys that have no redundant values. Consider the following example. Key "k1" has values ["v1", "v2"], key "k2" has
# values ["v1", "v3"], and key "k3" has values ["v2", "v3"]. Then, the combination of keys ["k1", "k2"] is valid as both keys together cover more values than each of the keys
# individually, in particular, the values ["v1", "v2", "v3"]. On the other hand, the combination ["k1", "k2", "k3"] is not valid as key "k3" does not add any new values to combination
# ["k1", "k2"] or any other valid combination such as ["k1", "k3"] or ["k2", "k3"]. We provide two ways to implement this function: Simple recursive (rec) and based on dynamic
# programming and memoization (dyn).

def rec(n, d, selected_keys, covered_values):
    # This function recursively selects all combinations of keys in d that yield unique combinations of corresponding values.
    if n == 0:
        # Make sure that keys in d are sorted by length of value list, because values that are supersets of already processed entries results in redundant key combinations
        d = {k: v for k, v in sorted(d.items(), key=lambda item: len(item[1]), reverse=True)}
    key_list = list(d.keys())
    if n == len(key_list):
        # Reached a leave of the binary tree, return key combinations and corresponding values
        return [selected_keys], [covered_values]
    else:
        key = key_list[n]
        values = d[key]
        if values.issubset(covered_values):
            # n-th key does not add any new values to set of values associated with selected_keys-> do not add to selected_keys
            return rec(n+1, d, selected_keys, covered_values)
        else:
            # n-th key adds new values to set of values associated with selected_keys -> onsider both cases where n-th key is added and not added
            keys_no, values_no = rec(n+1, d, selected_keys, covered_values)
            updated_keys = selected_keys.union(set([key]))
            updated_values = covered_values.union(values)
            keys_yes, values_yes = rec(n+1, d, updated_keys, updated_values)
            return keys_no + keys_yes, values_no + values_yes

def dyn(n, d, selected_keys, covered_values, memo_dict):
    # This function recursively selects all combinations of keys in d that yield unique combinations of corresponding values using memoization.
    if n == 0:
        # Make sure that keys in d are sorted by length of value list, because values that are supersets of already processed entries results in redundant key combinations
        d = {k: v for k, v in sorted(d.items(), key=lambda item: len(item[1]), reverse=True)}
    key_list = list(d.keys())
    if n == len(key_list):
        # Reached a leave of the binary tree, return key combinations and corresponding values
        return [selected_keys], [covered_values]
    else:
        if (n, frozenset(covered_values)) in memo_dict:
            # Set of values already processed before on this level of the tree -> retrieve key combinations from that node and replace keys used at that decision with currently used keys
            known_keys, known_values, memo_keys = memo_dict[(n, frozenset(covered_values))]
            new_keys = known_keys.copy() # Need to copy list to avoid changing by reference; not needed for values as they are not changed
            for i in range(len(new_keys)):
                # For each retrieved combination, remove keys used up until that node and replace them with keys used up until currently processed node
                new_keys[i] = new_keys[i].difference(memo_keys)
                new_keys[i].update(selected_keys)
            return new_keys, known_values
        else:
            key = key_list[n]
            values = d[key]
            if values.issubset(covered_values):
                # n-th key does not add any new values to set of values associated with selected_keys-> do not add to selected_keys
                keys_no, values_no = dyn(n+1, d, selected_keys, covered_values, memo_dict)
                memo_dict[(n, frozenset(covered_values))] = (keys_no, values_no, selected_keys) # Store resulting keys, resulting values, and keys used at this node to reuse it on other nodes at this level of the tree
                return keys_no, values_no
            else:
                # n-th key adds new values to set of values associated with selected_keys -> onsider both cases where n-th key is added and not added
                updated_keys = selected_keys.union(set([key]))
                updated_values = covered_values.union(values)
                keys_yes, values_yes = dyn(n+1, d, updated_keys, updated_values, memo_dict)
                keys_no, values_no = dyn(n+1, d, selected_keys, covered_values, memo_dict)
                memo_dict[(n, frozenset(covered_values))] = (keys_no + keys_yes, values_no + values_yes, selected_keys) # Store resulting keys, resulting values, and keys used at this node to reuse it on other nodes at this level of the tree
                return keys_no + keys_yes, values_no + values_yes

if __name__ == "__main__":
    def get_output(d):
        print('Combinations for ' + str(d) + ':')
        key_combos_dyn, covered_values_dyn = dyn(0, d, set(), set(), {})
        for i in range(len(key_combos_dyn)):
            print(' * ' + str(key_combos_dyn[i]) + ': ' + str(covered_values_dyn[i]))
        key_combos_rec, covered_values_rec = rec(0, d, set(), set())
        if key_combos_dyn != key_combos_rec or covered_values_dyn != covered_values_rec:
            print('WARNING: MISMATCHING RESULTS!')
            print(' * ' + str(key_combos_rec[i]) + ': ' + str(covered_values_rec[i]))
        set_of_sets = set()
        for set_element in key_combos_dyn:
            set_of_sets.add(frozenset(set_element))
        if len(set_of_sets) != len(key_combos_dyn):
            print('WARNING: DUPLICATED KEY COMBOS!')
        print('Selected ' + str(len(key_combos_rec)) + ' out of possible 2^' + str(len(d)) + '=' + str(pow(2, len(d))) + ' combinations')
        print('')

    d = {}
    d["k1"] = set(["v1", "v2", "v3", "v4", "v9"])
    d["k2"] = set(["v2", "v4", "v6", "v8"])
    d["k3"] = set(["v3", "v4", "v7", "v9"])
    d["k4"] = set(["v1", "v2", "v5", "v6"])
    d["k6"] = set(["v3", "v6", "v8"])
    d["k7"] = set(["v2", "v7", "v8"])
    d["k8"] = set(["v5", "v9"])
    d["k9"] = set(["v1", "v8"])
    get_output(d)

    d = {}
    d["k1"] = set(["v1", "v2"])
    d["k2"] = set(["v1", "v3"])
    d["k3"] = set(["v2", "v3"])
    d["k4"] = set(["v1", "v4"])
    get_output(d)
