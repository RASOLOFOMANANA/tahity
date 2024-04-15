from itertools import product

def truth_table(func, variables):
    """Calculates the truth table for a given function."""
    table = []
    for vals in product([0, 1], repeat=len(variables)):
        row = list(vals)
        row.append(func(*vals))
        table.append(row)
    return table

def generate_karnaugh_map(variables, table):
    """Generates the Karnaugh map."""
    num_rows = 2 ** len(variables)
    num_cols = len(variables)
    karnaugh_map = [['-' for _ in range(num_cols)] for _ in range(num_rows)]
    for row in table:
        index = 0
        for i, val in enumerate(row[:-1]):
            if val:
                index += 2 ** (num_cols - i - 1)
        karnaugh_map[index][:-1] = row[:-1]
    return karnaugh_map

def find_groups(karnaugh_map):
    """Finds groups of 1s in the Karnaugh map."""
    groups = []
    visited = set()
    for i in range(len(karnaugh_map)):
        for j in range(len(karnaugh_map[0])):
            if karnaugh_map[i][j] == 1 and (i, j) not in visited:
                group = []
                dfs(karnaugh_map, i, j, visited, group)
                groups.append(group)
    return groups

def dfs(karnaugh_map, i, j, visited, group):
    """Depth-first search to find connected components."""
    if (i, j) in visited or karnaugh_map[i][j] == 0:
        return
    visited.add((i, j))
    group.append((i, j))
    if i > 0:
        dfs(karnaugh_map, i - 1, j, visited, group)
    if i < len(karnaugh_map) - 1:
        dfs(karnaugh_map, i + 1, j, visited, group)
    if j > 0:
        dfs(karnaugh_map, i, j - 1, visited, group)
    if j < len(karnaugh_map[0]) - 1:
        dfs(karnaugh_map, i, j + 1, visited, group)

def simplify_group(group, variables):
    """Simplifies a group of 1s."""
    terms = []
    for cell in group:
        term = ""
        for i, val in enumerate(cell):
            if val == 0:
                term += variables[i] + "'"
            elif val == 1:
                term += variables[i]
        terms.append(term)
    return " + ".join(terms)

def minimize_function(groups, variables):
    """Minimizes the function using the simplified groups."""
    terms = []
    for group in groups:
        terms.append(simplify_group(group, variables))
    return " * ".join(terms)

def main():
    expression = input("Entrez la fonction logique (utilisez les opérateurs logiques 'and', 'or', 'not' et les variables en minuscules) : ")
    variables = sorted(set([char for char in expression if char.isalpha()]))
    func = eval(f"lambda {', '.join(variables)}: {expression}")
    
    print("\nTable de vérité :")
    table = truth_table(func, variables)
    for row in table:
        print(row)
    
    karnaugh_map = generate_karnaugh_map(variables, table)
    
    print("\nCarte de Karnaugh :")
    for row in karnaugh_map:
        print(row)
    
    groups = find_groups(karnaugh_map)
    
    print("\nGroupes de 1s :")
    for group in groups:
        print(group)
    
    minimized_function = minimize_function(groups, variables)
    
    print("\nFonction minimisée :")
    print(minimized_function)

if __name__ == "__main__":
    main()