import maze


class MazeDataStorage:

    FILE_NAME = "saved_mazes_data.txt"
    DATA_SEPARATOR = ","
    MATRIX_SEPARATOR = "|"

    def save_maze_data(self, maze_obj, maze_id):

        start_x, start_y = maze_obj.start
        end_x, end_y = maze_obj.end

        matrix_data = []
        for row in maze_obj.matrix:
            for cell in row:
                matrix_data.append(str(cell))

        line = self.DATA_SEPARATOR.join([
            maze_id,
            str(start_x),
            str(start_y),
            str(end_x),
            str(end_y),
            self.MATRIX_SEPARATOR.join(matrix_data)
        ])

        with open(self.FILE_NAME, "a") as file:
            file.write(line + "\n")


    def load_maze_data(self, maze_id):

        try:
            with open(self.FILE_NAME, "r") as file:
                for line in file:
                    parts = line.strip().split(self.DATA_SEPARATOR)

                    if parts[0] != maze_id:
                        continue

                    start = (int(parts[1]), int(parts[2]))
                    end = (int(parts[3]), int(parts[4]))

                    matrix_data = parts[5].split(self.MATRIX_SEPARATOR)

                    dim = int(len(matrix_data) ** 0.5)

                    matrix = []
                    for i in range(dim):
                        row = []
                        for j in range(dim):
                            row.append(matrix_data[i * dim + j])
                        matrix.append(row)

                    return maze.Maze(matrix, start, end)

        except FileNotFoundError:
            return None

        return None


    def delete_maze_data(self, maze_id):

        try:
            with open(self.FILE_NAME, "r") as file:
                lines = file.readlines()

            new_lines = []
            found = False

            for line in lines:
                parts = line.strip().split(self.DATA_SEPARATOR)

                if parts[0] == maze_id:
                    found = True
                    continue

                new_lines.append(line)

            with open(self.FILE_NAME, "w") as file:
                file.writelines(new_lines)

            return found

        except FileNotFoundError:
            return False