from utils.exceptions import *


class Matrix:
    def __init__(self, rows, columns, default=None):
        self.__rows = rows
        self.__columns = columns

        if rows < 1 or columns < 1:
            raise InvalidSize((rows, columns))

        self.__matrix = [[default for _ in range(columns)]
                         for _ in range(rows)]

    def set_element(self, position, element):
        self.__matrix[position[0]][position[1]] = element

    @property
    def rows(self):
        return self.__rows

    @rows.setter
    def rows(self, rows):
        if rows < 1:
            raise InvalidSize((rows, self.__columns))

        default = self.__matrix[0][0]
        difference = rows - self.__rows

        if difference:
            if rows > self.__rows:
                self.__matrix += [[default for _ in range(self.__columns)]
                                  for _ in range(difference)]
            else:
                self.__matrix = self.__matrix[:rows]

            self.__rows = rows

    @property
    def columns(self):
        return self.__columns

    @columns.setter
    def columns(self, columns):
        if columns < 1:
            raise InvalidSize((self.__rows, columns))

        default = self.__matrix[0][0]
        difference = columns - self.__columns

        if difference:
            if columns > self.__columns:
                for i in range(self.__rows):
                    self.__matrix[i] += [default for _ in range(difference)]
            else:
                for i in range(self.__rows):
                    self.__matrix[i] = self.__matrix[i][:columns]

            self.__columns = columns

    @property
    def matrix(self):
        return [[x for x in row] for row in self.__matrix]

    @matrix.setter
    def matrix(self, matrix):
        rows = len(matrix)

        if not rows:
            raise InvalidMatrix

        columns = len(matrix[0])

        if not columns:
            raise InvalidSize((len(matrix), columns))

        total = 0
        copy = []

        for row in matrix:
            copyRow = []

            for element in row:
                copyRow.append(element)
                total += 1

            if (total % columns):
                raise InvalidMatrix

            copy.append(copyRow)

        self.__columns = columns
        self.__rows = rows
        self.__matrix = copy

    def __repr__(self):
        string = f'Dimensions: {self.__rows} x {self.__columns}\n'

        for row in self.__matrix:
            string += str(row) + '\n'

        return string
