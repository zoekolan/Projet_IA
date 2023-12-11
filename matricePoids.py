matrice = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
def assign_weights(matrix, weights, locations):
    for location, weight in zip(locations, weights):
        row, col = location
        matrix[row][col] = weight

# Example usage
weights = [1, 2, 3]
locations = [(0, 0), (1, 1), (2, 2)]
#assign_weights(matrice, weights, locations)
#print(matrice)

def generate_hex_weights_with_cross(n):
    weights = [[0 for _ in range(n)] for _ in range(n)]

    # Poids pour les bords
    border_weight = 50
    for i in range(n):
        for j in range(n):
            if i == 0 or i == n - 1 or j == 0 or j == n - 1:
                weights[i][j] = border_weight

    # Poids pour le centre
    center_weight = 100
    if n % 2 != 0:
        weights[n // 2][n // 2] = center_weight
    else:
        weights[n // 2 - 1][n // 2 - 1] = center_weight
        weights[n // 2][n // 2] = center_weight

    # Poids pour la croix centrale
    cross_weight = 80
    for i in range(n):
        weights[i][n // 2] = cross_weight
        weights[n // 2][i] = cross_weight

    return weights

# Exemple d'utilisation avec une matrice de poids de taille 8x8
n = 11
weights_with_cross = generate_hex_weights_with_cross(n)

# Affichage de la matrice de poids générée avec la croix centrale
for row in weights_with_cross:
    print(row)
