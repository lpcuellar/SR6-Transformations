##
##  UNIVERSIDAD DEL VALLE DE GUATEMALA
##  GRÁFICAS POR COMPUTADORA
##  SECCIÓN 20
##
##  SR6: TRANSFORMATIONS
##  LUIS PEDRO CUÉLLAR - 18220
##

class MathGl(object):
    ##  this function does the cross of two arrays
    def cross(self, a, b):
        length = len(a)
        c = []

        if length == 2 :
            c.append((a[0] * b[1]) - (a[1] * b[0]))

        elif length == 3 :
            c.append((a[1] * b[2]) - (a[2] * b[1]))
            c.append(-((a[0] * b[2]) - (a[2] * b[0])))
            c.append((a[0] * b[1]) - (a[1] * b[0]))

        return c

    ## this function does the difference between two arrays
    def subtract(self, a, b):
        length = len(a)
        c = []

        if length == 2 :
            c.append(a[0] - b[0])
            c.append(a[1] - b[1])

        elif length == 3 :
            c.append(a[0] - b[0])
            c.append(a[1] - b[1])
            c.append(a[2] - b[2])

        return c

    ##  this fucntion does the norm of a vector
    def norm(self, a):
        length = len(a)
        c = 0

        if length == 2 :
            c = (a[0] ** 2) + (a[1] ** 2)
            c = c ** 0.5


        elif length == 3 :
            c = (a[0] ** 2) + (a[1] ** 2) + (a[2] ** 2)
            c = c ** 0.5

        return c

    ##  this function does the dot product between two arrays or numbers
    def dot(self, a, b):
        is_a_Array = isinstance(a, list)
        is_b_Array = isinstance(b, list)
        c = 0

        if (is_a_Array == True) and (is_b_Array == True) :
            length = len(a)

            if length == 2:
                c = (a[0] * b[0]) + (a[1] * b[1])

            else :
                c = (a[0] * b[0]) + (a[1] * b[1]) + (a[2] * b[2])

        else:
            c = a * b

        return c

    ##  this function calculates the barycentric coordinates
    def barycentric_coords(self, a, b, c, p):
        ##  u => a
        ##  v => b
        ##  w => c
        try:
            u = (((b[1] - c[1]) * (p[0] - c[0]) + (c[0] - b[0]) * (p[1] - c[1])) /
                  ((b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])))

            v = (((c[1] - a[1]) * (p[0] - c[0]) + (a[0] - c[0]) * (p[1] - c[1])) /
                  ((b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])))

            w = 1 - u - v
        except:
            return -1, -1, -1

        return u, v, w




    ##  THE CODE BELOW IS COPIED FROM:
    ##  https://github.com/ThomIves/BasicLinearAlgebraToolsPurePy/blob/master/LinearAlgebraPurePython.py

    ##  this function does a matrix with 0s.
    def zeros_matrix(self, rows, cols):
        M = []
        while len(M) < rows:
            M.append([])
            while len(M[-1]) < cols:
                M[-1].append(0.0)

        return M

    ##  this function does the identity matrix
    def identity_matrix(self, n):
        IdM = self.zeros_matrix(n, n)
        for i in range(n):
            IdM[i][i] = 1.0

        return IdM

    ##  this function cpoies a matrix
    def copy_matrix(self, M):
        # Section 1: Get matrix dimensions
        rows = len(M)
        cols = len(M[0])

        # Section 2: Create a new matrix of zeros
        MC = self.zeros_matrix(rows, cols)

        # Section 3: Copy values of M into the copy
        for i in range(rows):
            for j in range(cols):
                MC[i][j] = M[i][j]

        return MC

    ##  this function prints a matrix
    def print_matrix(self, M, decimals=3):
        for row in M:
            print([round(x, decimals)+0 for x in row])

    ##  this function does the transpose of a matrix
    def transpose(self, M):
        # Section 1: if a 1D array, convert to a 2D array = matrix
        if not isinstance(M[0], list):
            M = [M]

        # Section 2: Get dimensions
        rows = len(M)
        cols = len(M[0])

        # Section 3: MT is zeros matrix with transposed dimensions
        MT = self.zeros_matrix(cols, rows)

        # Section 4: Copy values from M to it's transpose MT
        for i in range(rows):
            for j in range(cols):
                MT[j][i] = M[i][j]

        return MT

    ##  this function does the addition of two matrices
    def matrix_addition(self, A, B):
        # Section 1: Ensure dimensions are valid for matrix addition
        rowsA = len(A)
        colsA = len(A[0])
        rowsB = len(B)
        colsB = len(B[0])
        if rowsA != rowsB or colsA != colsB:
            raise ArithmeticError('Matrices are NOT the same size.')

        # Section 2: Create a new matrix for the matrix sum
        C = self.zeros_matrix(rowsA, colsB)

        # Section 3: Perform element by element sum
        for i in range(rowsA):
            for j in range(colsB):
                C[i][j] = A[i][j] + B[i][j]

        return C

    ##  this function does the subtraction of two matrices
    def matrix_subtraction(self, A, B):
        # Section 1: Ensure dimensions are valid for matrix subtraction
        rowsA = len(A)
        colsA = len(A[0])
        rowsB = len(B)
        colsB = len(B[0])
        if rowsA != rowsB or colsA != colsB:
            raise ArithmeticError('Matrices are NOT the same size.')

        # Section 2: Create a new matrix for the matrix difference
        C = self.zeros_matrix(rowsA, colsB)

        # Section 3: Perform element by element subtraction
        for i in range(rowsA):
            for j in range(colsB):
                C[i][j] = A[i][j] - B[i][j]

        return C

    ##  this function multiplies two matrices
    def matrix_multiply(self, A, B):
        # Section 1: Ensure A & B dimensions are correct for multiplication
        rowsA = len(A)
        colsA = len(A[0])
        rowsB = len(B)
        colsB = len(B[0])
        if colsA != rowsB:
            raise ArithmeticError(
                'Number of A columns must equal number of B rows.')

        # Section 2: Store matrix multiplication in a new matrix
        C = self.zeros_matrix(rowsA, colsB)
        for i in range(rowsA):
            for j in range(colsB):
                total = 0
                for ii in range(colsA):
                    total += A[i][ii] * B[ii][j]
                C[i][j] = total

        return C

    def multiply_matrices(self, list):
        # Section 1: Start matrix product using 1st matrix in list
        matrix_product = list[0]

        # Section 2: Loop thru list to create product
        for matrix in list[1:]:
            matrix_product = self.matrix_multiply(matrix_product, matrix)

        return matrix_product

    def check_matrix_equality(self, A, B, tol=None):
        # Section 1: First ensure matrices have same dimensions
        if len(A) != len(B) or len(A[0]) != len(B[0]):
            return False

        # Section 2: Check element by element equality
        #            use tolerance if given
        for i in range(len(A)):
            for j in range(len(A[0])):
                if tol is None:
                    if A[i][j] != B[i][j]:
                        return False
                else:
                    if round(A[i][j], tol) != round(B[i][j], tol):
                        return False

        return True

    def dot_product(self, A, B):
        # Section 1: Ensure A and B dimensions are the same
        rowsA = len(A)
        colsA = len(A[0])
        rowsB = len(B)
        colsB = len(B[0])
        if rowsA != rowsB or colsA != colsB:
            raise ArithmeticError('Matrices are NOT the same size.')

        # Section 2: Sum the products
        total = 0
        for i in range(rowsA):
            for j in range(colsB):
                total += A[i][j] * B[i][j]

        return total

    def unitize_vector(self, vector):
        # Section 1: Ensure that a vector was given
        if len(vector) > 1 and len(vector[0]) > 1:
            raise ArithmeticError(
                'Vector must be a row or column vector.')

        # Section 2: Determine vector magnitude
        rows = len(vector)
        cols = len(vector[0])
        mag = 0
        for row in vector:
            for value in row:
                mag += value ** 2
        mag = mag ** 0.5

        # Section 3: Make a copy of vector
        new = self.copy_matrix(vector)

        # Section 4: Unitize the copied vector
        for i in range(rows):
            for j in range(cols):
                new[i][j] = new[i][j] / mag

        return new


    def check_squareness(self, A):
        if len(A) != len(A[0]):
            raise ArithmeticError("Matrix must be square to inverse.")

    def determinant_recursive(self, A, total=0):
        # Section 1: store indices in list for flexible row referencing
        indices = list(range(len(A)))

        # Section 2: when at 2x2 submatrices recursive calls end
        if len(A) == 2 and len(A[0]) == 2:
            val = A[0][0] * A[1][1] - A[1][0] * A[0][1]
            return val

        # Section 3: define submatrix for focus column and call this function
        for fc in indices:  # for each focus column, find the submatrix ...
            As = self.copy_matrix(A)  # make a copy, and ...
            As = As[1:]  # ... remove the first row
            height = len(As)

            for i in range(height):  # for each remaining row of submatrix ...
                As[i] = As[i][0:fc] + As[i][fc+1:]  # zero focus column elements

            sign = (-1) ** (fc % 2)  # alternate signs for submatrix multiplier
            sub_det = self.determinant_recursive(As)  # pass submatrix recursively
            total += sign * A[0][fc] * sub_det  # total all returns from recursion

        return total

    def determinant_fast(self, A):
        # Section 1: Establish n parameter and copy A
        n = len(A)
        AM = self.copy_matrix(A)

        # Section 2: Row manipulate A into an upper triangle matrix
        for fd in range(n):  # fd stands for focus diagonal
            if AM[fd][fd] == 0:
                AM[fd][fd] = 1.0e-18  # Cheating by adding zero + ~zero
            for i in range(fd+1, n):  # skip row with fd in it.
                crScaler = AM[i][fd] / AM[fd][fd]  # cr stands for "current row".
                for j in range(n):  # cr - crScaler * fdRow, one element at a time.
                    AM[i][j] = AM[i][j] - crScaler * AM[fd][j]

        # Section 3: Once AM is in upper triangle form ...
        product = 1.0
        for i in range(n):
            product *= AM[i][i]  # ... product of diagonals is determinant

        return product

    def check_non_singular(self, A):
        det = self.determinant_fast(A)
        if det != 0:
            return det
        else:
            raise ArithmeticError("Singular Matrix!")

    def invert_matrix(A, tol=None):
        try:
            # Section 2: Make copies of A & I, AM & IM, to use for row ops
            n = len(A)
            AM = self.copy_matrix(A)
            I = self.identity_matrix(n)
            IM = self.copy_matrix(I)

            # Section 3: Perform row operations
            indices = list(range(n)) # to allow flexible row referencing ***
            for fd in range(n): # fd stands for focus diagonal
                fdScaler = 1.0 / AM[fd][fd]
                # FIRST: scale fd row with fd inverse.
                for j in range(n): # Use j to indicate column looping.
                    AM[fd][j] *= fdScaler
                    IM[fd][j] *= fdScaler
                # SECOND: operate on all rows except fd row as follows:
                for i in indices[0:fd] + indices[fd+1:]:
                    # *** skip row with fd in it.
                    crScaler = AM[i][fd] # cr stands for "current row".
                    for j in range(n):
                        # cr - crScaler * fdRow, but one element at a time.
                        AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
                        IM[i][j] = IM[i][j] - crScaler * IM[fd][j]

            # Section 4: Make sure IM is an inverse of A with specified tolerance
            if check_matrix_equality(I, self.matrix_multiply(A, IM), tol):
                return IM
            else:
                raise ArithmeticError("Matrix inverse out of tolerance.")
        except:
            pass

    def vector_matrix(self, m, v):
        return[self.dot_product(row, v) for row in m]
