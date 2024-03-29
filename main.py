def get_data():
    data = []
    with open("input.txt") as iFile:
        while True:
            line = iFile.readline()
            if not line:
                break
            temp = list(map(int, (line[:len(line)] + line[len(line) + 1:]).split()))
            data.append(temp)
    return data


def create_adjacency_matrix(idata):
    matrix = [0] * idata[0][0]
    for x in range(idata[0][0]):
        matrix[x] = [0] * idata[0][0]

    for y in range(1, len(idata)):
        matrix[idata[y][0] - 1][idata[y][1] - 1] = 1
        matrix[idata[y][1] - 1][idata[y][0] - 1] = 1
    return matrix


def get_power_matrix(adjacency_matrix):
    matrix_of_power = []
    for x in range(len(adjacency_matrix)):
        total = 0
        for y in range(len(adjacency_matrix)):
            total += adjacency_matrix[x][y]
        matrix_of_power.append(total)
    return matrix_of_power


def get_maximum_index(colour_of_nodes, matrix_power):
    max_index = -1
    maximum = -1
    for x in range(len(matrix_power)):
        if colour_of_nodes[x] == -1 and matrix_power[x] > maximum:
            maximum = matrix_power[x]
            max_index = x
    return max_index


def colour_graph(adjacency_matrix):
    colour_of_nodes = [-1] * len(adjacency_matrix)
    counter = 1
    matrix_power = get_power_matrix(adjacency_matrix)
    maximum_index = get_maximum_index(colour_of_nodes, matrix_power)
    while maximum_index != -1:
        will_be_coloured = [maximum_index]
        unvisited = True
        while unvisited:
            unvisited = False
            colour_of_nodes[will_be_coloured[-1]] = counter
            for x in range(len(adjacency_matrix)):
                if colour_of_nodes[x] == -1:
                    unvisited = True
                    for y in will_be_coloured:
                        if adjacency_matrix[x][y] == 1:
                            unvisited = False
                            break
                    if unvisited:
                        will_be_coloured.append(x)
                        break
        counter += 1
        maximum_index = get_maximum_index(colour_of_nodes, matrix_power)
    return colour_of_nodes


def show_coloured_graph(colour):
    maximum = max(colour)
    for x in range(1, maximum + 1):
        print("Колір %d" % x, end=": ")
        for y in range(len(colour)):
            if colour[y] == x:
                print(y + 1, end=", ")
        print()


def create_matching_solving_matrix(colour, adjacency_matrix):
    maximum = max(colour)
    if maximum != 2:
        print("Не можливо побудувати досконале паросполучення")
        exit(1)
    counter = 0
    for y in range(len(colour)):
        if colour[y] == 1:
            counter += 1
    if counter != len(adjacency_matrix) / 2:
        print("Не можливо побудувати досконале паросполучення")
        exit(1)

    colour_ordered = []
    for x in range(1, 3):
        group_colour = []
        for y in range(len(colour)):
            if colour[y] == x:
                group_colour.append(y)
        colour_ordered.append(group_colour)
    matrix = ['*'] * (int(len(adjacency_matrix) / 2))
    for x in range(int(len(adjacency_matrix) / 2)):
        matrix[x] = ['*'] * (int(len(adjacency_matrix) / 2))
    for i in range(int(len(adjacency_matrix) / 2)):
        for j in range(int(len(adjacency_matrix) / 2)):
            if adjacency_matrix[colour_ordered[0][i]][colour_ordered[1][j]] == 1:
                matrix[i][j] = 0
            else:
                matrix[i][j] = 'x'
    return colour_ordered, matrix


def search_all_matching_matrix(matching_matrix_skeleton, row=0):
    counter = 0
    if row == len(matching_matrix_skeleton):
        print_matrix(matching_matrix_skeleton)
        counter += 1
    else:
        for x in range(len(matching_matrix_skeleton)):
            is_added_already = False
            for y in range(0, row):
                if matching_matrix_skeleton[y][x] == 1:
                    is_added_already = True
                    break
            if not is_added_already and matching_matrix_skeleton[row][x] != 'x':
                matching_matrix_skeleton[row][x] = 1
                counter += search_all_matching_matrix(matching_matrix_skeleton, row + 1)
                matching_matrix_skeleton[row][x] = 0
    return counter


def print_matrix(matrix):
    for i in matrix:
        for j in i:
            print(j, end=" ")
        print()
    print()


adjacencyMatrix = create_adjacency_matrix(get_data())
myColour = colour_graph(adjacencyMatrix)
show_coloured_graph(myColour)
print("Колір 1 відповідає за позначення біля рядків")
print("Колір 2 за позначення біля стовпців")
colourOrdered, myMatrix = create_matching_solving_matrix(myColour, adjacencyMatrix)
counter = search_all_matching_matrix(myMatrix)
print("Всього можливих варіантів паросполучення " + str(counter))
