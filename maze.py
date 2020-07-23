class MazeError(Exception):
    pass


class Maze(object):
    def __init__(self, file_name):
        # def two attributes: the name of the file and conducted content of the file
        self.file_name = file_name
        with open(self.file_name, 'r') as f:
            file_content = f.read()
        self.content = self.conduct_file(file_content)

    # conduct the file, check whether it is satisfied with all requirements
    # if not, raise MazeError with specified exception
    def conduct_file(self, content):
        file_temp = content.split('\n')
        temp_1 = []
        temp_2 = []
        # delete extra spaces, record it, and then delete it
        for i in file_temp:
            if len(i) == 0 or not any(c.isdigit() for c in i):
                temp_1.append(i)
        for i in temp_1:
            file_temp.remove(i)
        for i in file_temp:
            if i.isdigit():
                i = [e for e in i]
            else:
                i = [r for r in i if r.isdigit()]
            # alter the type of every element into int
            g = list(map(int, i))
            temp_2.append(g)
        # check if it is satisfied with requirements and raise error massage
        for i in temp_2:
            if not all(j in {0, 1, 2, 3} for j in i) or len(i) < 2 or len(i) > 31:
                raise MazeError('Incorrect input.')
        if len(temp_2) < 2 or len(temp_2) > 41 or any(len(i) - len(temp_2[0]) for i in temp_2):
            raise MazeError('Incorrect input.')
        for e in temp_2:
            if e[-1] in {1, 3}:
                raise MazeError('Input does not represent a maze.')
        for g in temp_2[-1]:
            if g in {2, 3}:
                raise MazeError('Input does not represent a maze.')
        # add additional row and column at each edge of the maze to facilitate upcoming analysis
        for i in temp_2:
            i.insert(0, 0)
            i.append(0)
        additional_row = [0] * len(temp_2[0])
        temp_2.insert(0, additional_row)
        temp_2.append(additional_row)
        return temp_2

    def analyse(self):
        # print the number of gates
        nb_of_gates = self.count_gates()
        if nb_of_gates == 0:
            print('The maze has no gate.')
        elif nb_of_gates == 1:
            print('The maze has a single gate.')
        else:
            print(f'The maze has {nb_of_gates} gates.')

        # print the number of wall sets
        nb_of_wall_sets = self.count_walls()
        if nb_of_wall_sets == 0:
            print('The maze has no wall.')
        elif nb_of_wall_sets == 1:
            print('The maze has walls that are all connected.')
        else:
            print(f'The maze has {nb_of_wall_sets} sets of walls that are all connected.')

        # print the number of inaccessible inner point
        nb_of_inaccessible_inner_point = self.inaccessible_point()
        if nb_of_inaccessible_inner_point == 0:
            print('The maze has no inaccessible inner point.')
        elif nb_of_inaccessible_inner_point == 1:
            print('The maze has a unique inaccessible inner point.')
        else:
            print(f'The maze has {nb_of_inaccessible_inner_point} inaccessible inner points.')

        # print the number of accessible area
        nb_of_accessible_area = self.accessible_area()
        if nb_of_accessible_area == 0:
            print('The maze has no accessible area.')
        elif nb_of_accessible_area == 1:
            print('The maze has a unique accessible area.')
        else:
            print(f'The maze has {nb_of_accessible_area} accessible areas.')

        # print the number of cul-de-sacs
        nb_of_cds_set = self.count_cds_set()
        if nb_of_cds_set == 0:
            print('The maze has no accessible cul-de-sac.')
        elif nb_of_cds_set == 1:
            print('The maze has accessible cul-de-sacs that are all connected.')
        else:
            print(f'The maze has {nb_of_cds_set} sets of accessible cul-de-sacs that are all connected.')

        # print the number of entry-exit paths with no intersections not to cul-de-sacs
        nb_of_eep, path_record = self.count_eep()
        if nb_of_eep == 0:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        elif nb_of_eep == 1:
            print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print(f'The maze has {nb_of_eep} entry-exit paths with no intersections not to cul-de-sacs.')

    # calculate the number of gates
    def count_gates(self):
        nb = 0
        for i in range(1, len(self.content[1]) - 2):
            if self.content[1][i] == 0 or self.content[1][i] == 2:
                nb += 1
            if self.content[-2][i] == 0 or self.content[-2][i] == 2:
                nb += 1
        for i in range(1, len(self.content) - 2):
            if self.content[i][1] == 0 or self.content[i][1] == 1:
                nb += 1
            if self.content[i][-2] == 0 or self.content[i][-2] == 1:
                nb += 1
        return nb

    # count the number of sets of walls
    def count_walls(self):
        nb = 0
        wall = self.build_wall()
        number = self.recursive_wall(wall, nb)
        return number

    # build walls for recursive
    def build_wall(self):
        wall = []
        for _ in range(len(self.content)):
            wall.append([0] * len(self.content[0]))
        # mark this position as 1, as long as there is a wall connect to it
        for i in range(1, len(self.content)):
            for j in range(1, len(self.content[i])):
                if self.content[i][j] != 0 or self.content[i - 1][j] in {2, 3} or self.content[i][j - 1] in {1, 3}:
                    wall[i][j] = 1
        return wall

    # explore the wall grid recursively and return the number of sets
    def recursive_wall(self, w, nb):
        # if there is no more wall that has not been explored, end the recursion and return the number
        if sum(e.count(1) for e in w) == 0:
            return nb
        # This is a flag, means whether find a new wall connected to current wall
        find_new_wall = False
        # already in a set of walls, find a wall connected, then mark it as 'wall'
        for i in range(1, len(w) - 1):
            for j in range(1, len(w[i]) - 1):
                if not w[i][j] in {'start', 'wall'}:
                    if w[i + 1][j] in {'start', 'wall'} \
                            and any([self.content[i][j] == 2, self.content[i][j] == 3]):
                        w[i][j] = 'wall'
                        find_new_wall = True
                    elif w[i][j + 1] in {'start', 'wall'} \
                            and any([self.content[i][j] == 1, self.content[i][j] == 3]):
                        w[i][j] = 'wall'
                        find_new_wall = True
                    elif w[i - 1][j] in {'start', 'wall'} \
                            and any([self.content[i - 1][j] == 2, self.content[i - 1][j] == 3]):
                        w[i][j] = 'wall'
                        find_new_wall = True
                    elif w[i][j - 1] in {'start', 'wall'} \
                            and any([self.content[i][j - 1] == 1, self.content[i][j - 1] == 3]):
                        w[i][j] = 'wall'
                        find_new_wall = True
        # if there is no wall connected, find a new start in wall grid mark it as 'start'
        if not find_new_wall:
            for e in w:
                # find 1 means find a new wall
                if 1 in e:
                    e[e.index(1)] = 'start'
                    nb += 1
                    break
        return self.recursive_wall(w, nb)

    # mark every point in the maze with its direction, which presents a path map
    def build_path(self, cont):
        path_direction = [[set([]) for _ in range(len(self.content[0]) - 3)] for _ in range(len(self.content) - 3)]
        for e in range(len(path_direction)):
            for r in range(len(path_direction[e])):
                if cont[e + 1][r + 1] == 0 or cont[e + 1][r + 1] == 2:
                    path_direction[e][r].add('N')
                if cont[e + 2][r + 1] == 0 or cont[e + 2][r + 1] == 2:
                    path_direction[e][r].add('S')
                if cont[e + 1][r + 1] == 0 or cont[e + 1][r + 1] == 1:
                    path_direction[e][r].add('W')
                if cont[e + 1][r + 2] == 0 or cont[e + 1][r + 2] == 1:
                    path_direction[e][r].add('E')
        return path_direction

    # find all gates with its directions
    # gates record the position of every gate
    # gate_direction record a grid with the open direction of each gate
    def find_gates_and_direction(self):
        gates = []
        path_direction = self.build_path(self.content)
        gate_direction = [[set([]) for _ in range(len(path_direction[0]))] for _ in range(len(path_direction))]
        # find gates, while the direction of the position towards outside of the grid, means that it is a gate
        for v in range(len(path_direction)):
            if 'W' in path_direction[v][0]:
                gates.append((v, 0))
            if 'E' in path_direction[v][-1]:
                gates.append((v, -1))
        for j in range(len(path_direction[0])):
            if 'N' in path_direction[0][j]:
                gates.append((0, j))
            if 'S' in path_direction[-1][j]:
                gates.append((-1, j))
        gates = list(set(gates))
        # build a grid to record the direction of gates in each position
        for e in gates:
            path_direction[e[0]][e[1]].add('G')
            if e[0] == 0:
                if 'N' in path_direction[e[0]][e[1]]:
                    path_direction[e[0]][e[1]].discard('N')
                    if not len(gate_direction[e[0]][e[1]]) == 0:
                        gate_direction[e[0]][e[1]].update({'GN'})
                    else:
                        gate_direction[e[0]][e[1]] = {'GN'}
            if e[0] == -1 or e[0] == len(path_direction) - 1:
                if 'S' in path_direction[e[0]][e[1]]:
                    path_direction[e[0]][e[1]].discard('S')
                    if not len(gate_direction[e[0]][e[1]]) == 0:
                        gate_direction[e[0]][e[1]].update({'GS'})
                    else:
                        gate_direction[e[0]][e[1]] = {'GS'}
            if e[1] == 0:
                if 'W' in path_direction[e[0]][e[1]]:
                    path_direction[e[0]][e[1]].discard('W')
                    if not len(gate_direction[e[0]][e[1]]) == 0:
                        gate_direction[e[0]][e[1]].update({'GW'})
                    else:
                        gate_direction[e[0]][e[1]] = {'GW'}
            if e[1] == -1 or e[1] == len(path_direction[0]) - 1:
                if 'E' in path_direction[e[0]][e[1]]:
                    path_direction[e[0]][e[1]].discard('E')
                    if not len(gate_direction[e[0]][e[1]]) == 0:
                        gate_direction[e[0]][e[1]].update({'GE'})
                    else:
                        gate_direction[e[0]][e[1]] = {'GE'}
        return gate_direction, gates, path_direction

    # access the maze recursively, mark every footprint as 'A'
    # return the number of accessible areas
    def access_recursive(self, nb, accessed_path, gates):
        # This is a flag, means that it is available to go next position
        continue_explore = False
        # mark every accessed position with 'A'
        for i in range(len(accessed_path)):
            for j in range(len(accessed_path[i])):
                if 'A' not in accessed_path[i][j]:
                    if 'N' in accessed_path[i][j]:
                        if i > 0:
                            if 'A' in accessed_path[i - 1][j]:
                                accessed_path[i][j].update('A')
                                continue_explore = True
                    if 'W' in accessed_path[i][j]:
                        if j > 0:
                            if 'A' in accessed_path[i][j - 1]:
                                accessed_path[i][j].update('A')
                                continue_explore = True
                    if 'S' in accessed_path[i][j]:
                        if i < len(accessed_path) - 1:
                            if 'A' in accessed_path[i + 1][j]:
                                accessed_path[i][j].update('A')
                                continue_explore = True
                    if 'E' in accessed_path[i][j]:
                        if j < len(accessed_path[i]) - 1:
                            if 'A' in accessed_path[i][j + 1]:
                                accessed_path[i][j].update('A')
                                continue_explore = True
        if not continue_explore:
            new_area_exist = False
            # find a gate which has not been accessed, start recursion
            for e in gates:
                if 'A' not in accessed_path[e[0]][e[1]]:
                    accessed_path[e[0]][e[1]].add('A')
                    nb += 1
                    new_area_exist = True
                    break
            # Here means every gate has been accessed, end the recursion
            if not new_area_exist:
                return nb, accessed_path
        return self.access_recursive(nb, accessed_path, gates)

    # count the number of accessible areas
    def accessible_area(self):
        nb_of_accessible_area = 0
        gate_direction, gates, path_direction = self.find_gates_and_direction()
        accessed_path = self.build_path(self.content)
        nb_of_accessible_area, access_path = self.access_recursive(nb_of_accessible_area, accessed_path, gates)
        return nb_of_accessible_area

    # inspect the accessed maze, find all position that has not been acceesed
    def inaccessible_point(self):
        nb_of_inaccessible_inner_point = 0
        gate_direction, gates, path_direction = self.find_gates_and_direction()
        accessed_path = self.build_path(self.content)
        a, accessed_area = self.access_recursive(0, accessed_path, gates)
        # if not find 'A' in position, means that it can not been accessed
        for i in range(len(accessed_area)):
            for j in range(len(accessed_area[i])):
                if 'A' not in accessed_area[i][j]:
                    nb_of_inaccessible_inner_point += 1
        return nb_of_inaccessible_inner_point

    # start with a point which has one direction to go,
    # find its next point until next point has more than two directions to go
    def find_cds(self, path_cds, gate_direction, cds_points, access_path):
        cds_exist = False  # this is a flag, presenting whether find a cds
        cds = []
        for i in range(len(path_cds)):
            for j in range(len(path_cds[i])):
                if len(path_cds[i][j]) == 1 and 'C' not in path_cds[i][j] and 'A' in access_path[i][j]:
                    # loop the path_cds to find a point which only has one direction to go
                    cds_exist = True  # find a cds, mark this flag as True
                    a = i
                    b = j  # record i and j as a and b, presenting the position in path_cds
                    while len(path_cds[a][b]) < 2:
                        #    inaccessible_area = True  # end with nowhere to go, means that this is an inaccessible area
                        #    break
                        if {'G'}.issubset(path_cds[a][b]):
                            if len(gate_direction[a][b]) == 1:  # and this gate only open to one direction
                                cds += [(a, b)]  # if reach a gate with only one direction to go, record this position
                        else:
                            cds += [(a, b)]
                        A = a
                        B = b  # A B present the current position, same as below
                        if {'W'}.issubset(path_cds[a][b]) and b > 0:
                            b -= 1  # let a and b be the next position, same as below
                            path_cds[A][B] -= {'W'}
                            path_cds[a][b] -= {'E'}  # delete the direction towards each other, same as below
                        elif {'E'}.issubset(path_cds[a][b]) and b < len(path_cds[a]) - 1:
                            b += 1
                            path_cds[A][B] -= {'E'}
                            path_cds[a][b] -= {'W'}
                        elif {'N'}.issubset(path_cds[a][b]) and a > 0:
                            a -= 1
                            path_cds[A][B] -= {'N'}
                            path_cds[a][b] -= {'S'}
                        elif {'S'}.issubset(path_cds[a][b]) and a < len(path_cds) - 1:
                            a += 1
                            path_cds[A][B] -= {'S'}
                            path_cds[a][b] -= {'N'}
                        elif {'G'}.issubset(path_cds[a][b]):
                            path_cds[A][B] -= {'G'}
                            break  # if reach a gate, end the loop
                    for e in cds:
                        path_cds[e[0]][e[1]] = {'C'}
                    cds_points += cds  # record all points that are accessible
                    return self.find_cds(path_cds, gate_direction, cds_points, access_path)
        if not cds_exist:
            return cds_points, path_cds
            # if there is no cds, end recursive and return cds_points and modified path_cds

    # start with a cds, find the next position is also cds, mark as 'A', accessed
    # until cannot reach any cds, start a new set
    def cds_recursive(self, nb, path_cds, access_path):
        if not sum([e.count({'C'}) for e in path_cds]):
            return nb  # if there is no cds have not be accessed, return the number of cds_sets
        continue_explore = False  # This is a flag, meaning that whether to start a new set
        for i in range(1, len(path_cds) - 1):
            for j in range(1, len(path_cds[i]) - 1):
                if path_cds[i][j] == {'C'}:
                    if {'N'}.issubset(access_path[i][j]) and path_cds[i - 1][j] == 'A':
                        # if find a cds next to accessed point, mark it as 'A' accessed, and continue explore
                        # same as below
                        path_cds[i][j] = 'A'
                        continue_explore = True
                    if {'S'}.issubset(access_path[i][j]) and path_cds[i + 1][j] == 'A':
                        path_cds[i][j] = 'A'
                        continue_explore = True
                    if {'W'}.issubset(access_path[i][j]) and path_cds[i][j - 1] == 'A':
                        path_cds[i][j] = 'A'
                        continue_explore = True
                    if {'E'}.issubset(access_path[i][j]) and path_cds[i][j + 1] == 'A':
                        path_cds[i][j] = 'A'
                        continue_explore = True
        if not continue_explore:
            for i in path_cds:
                if {'C'} in i:  # find a new set
                    i[i.index({'C'})] = 'A'  # mark it as accessed
                    nb += 1
                    break
        return self.cds_recursive(nb, path_cds, access_path)

    # count the number of cds_sets
    def count_cds_set(self):
        nb = 0
        cds_points = []
        gate_direction, gates, path_direction = self.find_gates_and_direction()
        accessed_path = self.build_path(self.content)
        x, access_path = self.access_recursive(0, accessed_path, gates)
        cds_points, path_cds = self.find_cds(path_direction, gate_direction, cds_points, access_path)
        a, accessed_path = self.access_recursive(0, access_path, gates)
        # add extra 0 in the start and end of each row
        # then add extra column in start and end of path_cds and access_path
        # for better loop
        for i in path_cds:
            i.insert(0, 0)
            i.append(0)
        e = [0] * len(path_cds[0])
        path_cds.insert(0, e)
        path_cds.append(e)
        for i in accessed_path:
            i.insert(0, 0)
            i.append(0)
        g = [0] * len(access_path[0])
        accessed_path.insert(0, g)
        accessed_path.append(g)
        nb = self.cds_recursive(nb, path_cds, accessed_path)
        return nb

    # access the maze recursively, not to somewhere is either cds or more than 2 direction to go
    def eep_recursive(self, path_cds_eep, path_record, path):
        # This is a flag, True means that we already enter the maze from one gate
        # False means that we should find a new gate to start
        in_path = False
        # enter the maze from a gate
        for i in range(len(path_cds_eep)):
            for j in range(len(path_cds_eep[i])):
                if 'P' in path_cds_eep[i][j]:
                    # check whether it has next position to go, and only one direction to go
                    if 'N' in path_cds_eep[i][j] and 'S' in path_cds_eep[i - 1][j]:
                        if len(path_cds_eep[i - 1][j]) == 2:
                            path_cds_eep[i][j].remove('N')
                            path_cds_eep[i - 1][j].remove('S')
                            path_cds_eep[i - 1][j].add('P')
                            in_path = True
                            # find a path, record it in temp recorder 'path'
                            # same as below
                            path.append((i, j))
                        else:
                            # if there are more than 2 direction in next position
                            # means that it is not satisfied with requirements
                            # clear temp recorder 'path'
                            # same as below
                            in_path = False
                            path_cds_eep[i][j].remove('P')
                            path.clear()
                            break
                    if 'S' in path_cds_eep[i][j] and 'N' in path_cds_eep[i + 1][j]:
                        if len(path_cds_eep[i + 1][j]) == 2:
                            path_cds_eep[i][j].remove('S')
                            path_cds_eep[i + 1][j].remove('N')
                            path_cds_eep[i + 1][j].add('P')
                            in_path = True
                            path.append((i, j))
                        else:
                            in_path = False
                            path_cds_eep[i][j].remove('P')
                            path.clear()
                            break
                    if 'W' in path_cds_eep[i][j] and 'E' in path_cds_eep[i][j - 1]:
                        if len(path_cds_eep[i][j - 1]) == 2:
                            path_cds_eep[i][j].remove('W')
                            path_cds_eep[i][j - 1].remove('E')
                            path_cds_eep[i][j - 1].add('P')
                            in_path = True
                            path.append((i, j))
                        else:
                            in_path = False
                            path_cds_eep[i][j].remove('P')
                            path.clear()
                            break
                    if 'E' in path_cds_eep[i][j] and 'W' in path_cds_eep[i][j + 1]:
                        if len(path_cds_eep[i][j + 1]) == 2:
                            path_cds_eep[i][j].remove('E')
                            path_cds_eep[i][j + 1].remove('W')
                            path_cds_eep[i][j + 1].add('P')
                            in_path = True
                            path.append((i, j))
                        else:
                            in_path = False
                            path_cds_eep[i][j].remove('P')
                            path.clear()
                            break
                    if 'G' in path_cds_eep[i][j]:
                        path_cds_eep[i][j].remove('G')
                        path_cds_eep[i][j].add('P')
                        in_path = False
                        path.append((i, j))
                        # enter by a gate, exit by a gate, record the path
                        path_record.append(path)
        if not in_path:
            # build a temp path record
            path = []
            # find a gate, marking it as 'P' to start recursion
            for i in range(len(path_cds_eep)):
                for j in range(len(path_cds_eep[i])):
                    if 'G' in path_cds_eep[i][j]:
                        path_cds_eep[i][j].remove('G')
                        path_cds_eep[i][j].add('P')
                        return self.eep_recursive(path_cds_eep, path_record, path)
            # if code reach here, means that there is no gate left to access
            # end the recursion
            return path_cds_eep, path_record
        return self.eep_recursive(path_cds_eep, path_record, path)

    def count_eep(self):
        gate_direction, gates, path_direction = self.find_gates_and_direction()
        cds_points = []
        accessed_path = self.build_path(self.content)
        x, access_path = self.access_recursive(0, accessed_path, gates)
        cds_points, path_cds_eep = self.find_cds(path_direction, gate_direction, cds_points, access_path)
        for e in path_cds_eep:
            e.insert(0, set([]))
            e.append(set([]))
        path_cds_eep.insert(0, [set([]) for _ in range(len(path_cds_eep[0]))])
        path_cds_eep.append([set([]) for _ in range(len(path_cds_eep[0]))])
        for i in range(1, len(path_cds_eep) - 1):
            for j in range(1, len(path_cds_eep[i]) - 1):
                if path_cds_eep[i][j] == set([]) and len(gate_direction[i - 1][j - 1]):
                    if 'GN' in gate_direction[i - 1][j - 1]:
                        path_cds_eep[i][j].add('N')
                        path_cds_eep[i - 1][j].update('SG')
                    if 'GS' in gate_direction[i - 1][j - 1]:
                        path_cds_eep[i][j].add('S')
                        path_cds_eep[i + 1][j].update('NG')
                    if 'GW' in gate_direction[i - 1][j - 1]:
                        path_cds_eep[i][j].add('W')
                        path_cds_eep[i][j - 1].update('EG')
                    if 'GE' in gate_direction[i - 1][j - 1]:
                        path_cds_eep[i][j].add('E')
                        path_cds_eep[i][j + 1].update('WG')
                if 'G' in path_cds_eep[i][j]:
                    path_cds_eep[i][j].remove('G')
                    if 'GN' in gate_direction[i - 1][j - 1]:
                        path_cds_eep[i][j].add('N')
                        path_cds_eep[i - 1][j].update('SG')
                    if 'GS' in gate_direction[i - 1][j - 1]:
                        path_cds_eep[i][j].add('S')
                        path_cds_eep[i + 1][j].update('NG')
                    if 'GW' in gate_direction[i - 1][j - 1]:
                        path_cds_eep[i][j].add('W')
                        path_cds_eep[i][j - 1].update('EG')
                    if 'GE' in gate_direction[i - 1][j - 1]:
                        path_cds_eep[i][j].add('E')
                        path_cds_eep[i][j + 1].update('WG')
        path_record = []
        path = []
        path_cds_eep, path_record = self.eep_recursive(path_cds_eep, path_record, path)
        nb = len(path_record)
        return nb, path_record

    def display(self):
        with open(self.file_name.replace('.txt', '.tex'), 'w') as tex:
            tex.write('\\documentclass[10pt]{article}\n'
                      '\\usepackage{tikz}\n'
                      '\\usetikzlibrary{shapes.misc}\n'
                      '\\usepackage[margin=0cm]{geometry}\n'
                      '\\pagestyle{empty}\n'
                      '\\tikzstyle{every node}=[cross out, draw, red]\n'
                      '\n'
                      '\\begin{document}\n'
                      '\n'
                      '\\vspace*{\\fill}\n'
                      '\\begin{center}\n'
                      '\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n'
                      '% Walls\n')
            # draw the horizon walls
            i = 1
            while i < len(self.content) - 1:
                j = 0
                while j < len(self.content[i]) - 1:
                    if self.content[i][j] != 1 and self.content[i][j] != 3:
                        j += 1
                        continue
                    start = j
                    stop = j + 1
                    while self.content[i][stop] == 1 or self.content[i][stop] == 3:
                        stop += 1
                    j = stop
                    tex.write(f'    \\draw ({start - 1},{i - 1}) -- ({stop - 1},{i - 1});\n')
                i += 1
            # draw the vertical walls
            j = 1
            while j < len(self.content[0]):
                i = 0
                while i < len(self.content):
                    if self.content[i][j] != 2 and self.content[i][j] != 3:
                        i += 1
                        continue
                    start = i
                    stop = i + 1
                    while self.content[i + 1][j] == 2 or self.content[i + 1][j] == 3:
                        stop += 1
                        i += 1
                    i = stop
                    tex.write(f'    \\draw ({j - 1},{start - 1}) -- ({j - 1},{stop - 1});\n')
                j += 1
            # draw pillars
            tex.write('% Pillars\n')
            for i in range(1, len(self.content) - 1):
                for j in range(1, len(self.content[i]) - 1):
                    if not self.content[i][j]:
                        if self.content[i - 1][j] == 0 or self.content[i - 1][j] == 1:
                            if self.content[i][j - 1] == 0 or self.content[i][j - 1] == 2:
                                tex.write(f'    \\fill[green] ({j - 1},{i - 1}) circle(0.2);\n')
            # draw accessible cds
            tex.write('% Inner points in accessible cul-de-sacs\n')
            cds_points = []
            gate_direction, gates, path_direction = self.find_gates_and_direction()
            accessed_path = self.build_path(self.content)
            x, access_path = self.access_recursive(0, accessed_path, gates)
            cds_points, path_cds = self.find_cds(path_direction, gate_direction, cds_points, access_path)
            cds_points = sorted(cds_points, key=lambda x: (x[0], x[1]))
            for e in cds_points:
                tex.write(f'    \\node at ({e[1] + 0.5},{e[0] + 0.5}) {{}};\n')
            # draw the eep
            tex.write('% Entry-exit paths without intersections\n')
            nb, path_record = self.count_eep()
            horizon_of_eep = []
            vertical_of_eep = []
            # separate the eep path into two parts: horizontal and vertical
            # every element presents its start position and stop position
            # order these tuple by position, place the smaller number in advance
            for i in range(len(path_record)):
                for j in range(1, len(path_record[i])):
                    if path_record[i][j][0] == path_record[i][j - 1][0] + 1:
                        vertical_of_eep.append((path_record[i][j - 1][0], path_record[i][j - 1][1],
                                                path_record[i][j][0], path_record[i][j][1]))
                    if path_record[i][j][0] == path_record[i][j - 1][0] - 1:
                        vertical_of_eep.append((path_record[i][j][0], path_record[i][j][1],
                                                path_record[i][j - 1][0], path_record[i][j - 1][1]))
                    if path_record[i][j][1] == path_record[i][j - 1][1] + 1:
                        horizon_of_eep.append((path_record[i][j - 1][0], path_record[i][j - 1][1],
                                               path_record[i][j][0], path_record[i][j][1]))
                    if path_record[i][j][1] == path_record[i][j - 1][1] - 1:
                        horizon_of_eep.append((path_record[i][j][0], path_record[i][j][1],
                                               path_record[i][j - 1][0], path_record[i][j - 1][1]))
            # sort these paths by its position, together with same level
            horizon_of_eep = sorted(horizon_of_eep, key=lambda x: (x[0], x[1]))
            vertical_of_eep = sorted(vertical_of_eep, key=lambda x: (x[1], x[0]))
            # draw the horizontal eep path
            i = 0
            while i < len(horizon_of_eep):
                start = [horizon_of_eep[i][0], horizon_of_eep[i][1]]
                stop = [horizon_of_eep[i][2], horizon_of_eep[i][3]]
                mark = i
                while mark < len(horizon_of_eep) - 1:
                    # if the start position of next path is same as the stop position of current path
                    # the new stop should be the same as the stop position of next path
                    if horizon_of_eep[mark + 1][0] == horizon_of_eep[mark][2] \
                            and horizon_of_eep[mark + 1][1] == horizon_of_eep[mark][3]:
                        stop = [horizon_of_eep[mark + 1][2], horizon_of_eep[mark + 1][3]]
                        mark += 1
                        continue
                    break
                tex.write(f'    \\draw[dashed, yellow] ({start[1] - 0.5},{start[0] - 0.5}) -- '
                          f'({stop[1] - 0.5},{stop[0] - 0.5});\n')
                if not i == mark:
                    i = mark + 1
                    continue  # until reach a path which is not connected, continue with next path
                i += 1
            # draw the vertical eep path
            i = 0
            while i < len(vertical_of_eep):
                start = [vertical_of_eep[i][0], vertical_of_eep[i][1]]
                stop = [vertical_of_eep[i][2], vertical_of_eep[i][3]]
                mark = i
                while mark < len(vertical_of_eep) - 1:
                    # if the start position of next path is same as the stop position of current path
                    # the new stop should be the same as the stop position of next path
                    if vertical_of_eep[mark + 1][0] == vertical_of_eep[mark][2] \
                            and vertical_of_eep[mark + 1][1] == vertical_of_eep[mark][3]:
                        stop = [vertical_of_eep[mark + 1][2], vertical_of_eep[mark + 1][3]]
                        mark += 1
                        continue
                    break
                tex.write(f'    \\draw[dashed, yellow] ({start[1] - 0.5},{start[0] - 0.5}) -- '
                          f'({stop[1] - 0.5},{stop[0] - 0.5});\n')
                if not i == mark:
                    i = mark + 1
                    continue  # until reach a path which is not connected, continue with next path
                i += 1
            tex.write('\\end{tikzpicture}\n'
                      '\\end{center}\n'
                      '\\vspace*{\\fill}\n'
                      '\n'
                      '\\end{document}\n'
                      '')


maze = Maze('Ricky_24.txt')
maze.analyse()
maze.display()