# polynomial.py


class Polynomial:
    def __init__(self, *coefficients):
        """ self.c contains list of coefficients from power = 0
            Polynom can have 0 coefficients in the end of self.c
        """
        self.c = list(coefficients)
        if isinstance(coefficients[0], dict):
            self.c = [0] * (max(coefficients[0].keys()) + 1)
            for k, v in coefficients[0].items():
                self.c[k] = v
        elif isinstance(coefficients[0], Polynomial):
            self.c = coefficients[0].c.copy()
        elif isinstance(coefficients[0], list):
            self.c = coefficients[0]

    def __repr__(self):
        i = len(self.c) - 1
        while self.c[i] == 0:
            i -= 1
        return 'Polynomial ' + str(self.c[:i + 1])

    def __str__(self):
        def get_str_by_i_c(i, c):
            space = '' if i == self.degree() else ' '
            sign = '+' * (self.degree() != i) if c > 0 else '-'
            coef = str(abs(c)) * (abs(c) != 1 or i == 0)
            power = '' if i == 0 else 'x' + ('^' + str(i)) * (i != 1)
            return sign + space + coef + power
        if self == 0:
            return '0'
        rev_c = reversed(list(enumerate(self.c)))
        str_rep = [get_str_by_i_c(i, c) for i, c in rev_c if c != 0]
        return ' '.join(str_rep)

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            if len(self.c) > len(other.c):
                return other == self
            for i, c in enumerate(self.c):
                if other.c[i] != c:
                    return False
            no_zeroes = len([c for c in other.c[len(self.c):] if c != 0]) == 0
            return True if no_zeroes else False
        return other == self.c[0] and self.degree() == 0

    def __add__(self, other):
        if isinstance(other, Polynomial):
            coefs1 = self.c
            coefs2 = other.c
            answer = [0] * max(len(coefs1), len(coefs2))
            for i in range(min(len(coefs1), len(coefs2))):
                answer[i] = coefs1[i] + coefs2[i]
            if len(coefs1) > len(coefs2):
                answer[i + 1:] = coefs1[i + 1:]
            if len(coefs1) < len(coefs2):
                answer[i + 1:] = coefs2[i + 1:]
        else:
            answer = self.c[:]
            answer[0] += other
        return Polynomial(answer)

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return self * (-1)

    def __sub__(self, other):
        return self + other * (-1)

    def __rsub__(self, other):
        return (-1) * (self - other)

    def __call__(self, x):
        answer = 0
        for i in range(len(self.c)):
            answer += x ** i * self.c[i]
        return answer

    def degree(self):
        if len([c for c in self.c if c != 0]) == 0:
            return 0
        l = len(self.c) - 1
        f, k = 0, 0
        while f == 0:
            f = self.c[l - k]
            k += 1
        return l - k + 1

    def der(self, d=1):
        n = self.c.copy()
        for x in range(d):
            k = 0
            for k in range(len(n[:-1])):
                n[k] = n[k + 1] * (k + 1)
            n[-1] = 0
        return Polynomial(n)

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            l = (len(self.c)) * (len(other.c) - 1) + 1
            answer = [0 for i in range(l)]
            for i in range(len(self.c)):
                mult = self.c[i]
                for j in range(len(other.c)):
                    answer[i + j] += other.c[j] * mult
        else:
            answer = [x * other for x in self.c]
        return Polynomial(answer)

    def __rmul__(self, other):
        return self * other

    def __iter__(self):
        return enumerate(self.c[:self.degree() + 1])

    def __next__(self):
        return next(self)


class DegreeIsTooBigException(Exception):
    def __init__(self, text):
        self.text = 'DegreeIsTooBigException'


class NotOddDegreeException(Exception):
    def __init__(self, text):
        self.text = 'NotOddDegreeException'


class RealPolynomial(Polynomial):
    def __init__(self, *coefficients):
        Polynomial.__init__(self, *coefficients)
        if self.degree() % 2 == 0:
            raise NotOddDegreeException()

    def find_root(self):
        a = 1
        while True:
            if self(-a) * self(a) < 0:
                break
            else:
                a = a * 2
        a, b = -a, a
        while True:
            if abs(self(a)) < 1e-6:
                return a
            if abs(self(b)) < 1e-6:
                return b
            c = (a + b) / 2
            if abs(self(c)) < 1e-6:
                return c
            else:
                if self(a) * self(c) < 0:
                    a, b = a, c
                else:
                    a, b = c, b


class QuadraticPolynomial(Polynomial):
    def __init__(self, *coefficients):
        Polynomial.__init__(self, *coefficients)
        if self.degree() > 2:
            raise Exception('')

    def solve(self):
        n = self.c.copy()
        if n[2] != 0:
            deskr = n[1] ** 2 - 4 * n[0] * n[2]
            if deskr < 0:
                answer = []
            elif deskr == 0:
                answer = [-n[1] / (2 * n[2])]
            else:
                answer = [(-n[1] - deskr ** (1 / 2)) / (2 * n[2]),
                          (-n[1] + deskr ** (1 / 2)) / (2 * n[2])]
        elif n[2] == 0:
            if n[1] != 0:
                answer = [n[0] / n[1]]
            else:
                answer = []
        return answer
