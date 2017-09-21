

__version__ = '0.0'
__all__ = [
    'AND',
    'OR',
    'EQ',
    'NE',
    'LT',
    'LE',
    'GT',
    'GE',
    'LIKE',
    'OPS',
    ]


DOT = '.'


class Where:

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __eq__(self, other):
        try:
            return (self.op == other.op and self.left == other.left and
                    self.right == other.right)
        except AttributeError:
            return False

    def __str__(self):
        if isinstance(self.left, tuple):
            left = DOT.join(self.left)
        elif isinstance(self.left, Where):
            left = str(self.left)
        else:
            left = '%s'
        if isinstance(self.right, tuple):
            right = DOT.join(self.right)
        elif isinstance(self.right, Where):
            right = str(self.right)
        else:
            right = '%s'
        return '(%s %s %s)' % (left, self.op, right)

    def params(self):
        buffer = []
        self._params(buffer)
        return tuple(buffer)

    def _params(self, buffer):
        if isinstance(self.left, Where):
            self.left._params(buffer)
        elif not isinstance(self.left, tuple):
            buffer.append(self.left)
        if isinstance(self.right, Where):
            self.right._params(buffer)
        elif not isinstance(self.right, tuple):
            buffer.append(self.right)

    def visit(self, f):
        f(self)
        if isinstance(self.left, Where):
            self.left.visit(f)
        if isinstance(self.right, Where):
            self.right.visit(f)

    def __iter__(self):
        yield self
        if isinstance(self.left, Where):
            for node in self.left:
                yield node
        if isinstance(self.right, Where):
            for node in self.right:
                yield node
        return

    def findall(self, f):
        stack = [self]
        while stack:
            node = stack.pop()
            try:
                if f(node):
                    yield node
            except:
                pass
            if isinstance(node, Where):
                stack.append(node.right)
                stack.append(node.left)
        return

    def remove(self, node):
        """This assumes that node is a child of this node."""
        if self.left == node:
            self.op = self.right.op
            self.left = self.right.left
            self.right = self.right.right
        elif self.right == node:
            self.op = self.left.op
            self.right = self.left.right
            self.left = self.left.left
        else:
            try:
                self.left.remove(node)
            except (AttributeError, ValueError):
                try:
                    self.right.remove(node)
                except (AttributeError, ValueError):
                    raise ValueError('%s is not a child of %s.' % (node, self))


def AND(left, right):
    return Where('AND', left, right)


def OR(left, right):
    return Where('OR', left, right)


def EQ(left, right):
    return Where('=', left, right)


def NE(left, right):
    return Where('<>', left, right)


def LT(left, right):
    return Where('<', left, right)


def LE(left, right):
    return Where('<=', left, right)


def GT(left, right):
    return Where('>', left, right)


def GE(left, right):
    return Where('>=', left, right)


def LIKE(left, right):
    return Where('LIKE', left, right)


def IN(left, right):
    right = right.replace('_', r'\_')
    right = right.replace('%', r'\%')
    right = '%%' + right + '%%'
    return LIKE(left, right)


OPS = {
    'AND' : AND,
    'OR'  : OR,
    'EQ'  : EQ,
    'NE'  : NE,
    'LT'  : LT,
    'LE'  : LE,
    'GT'  : GT,
    'GE'  : GE,
    'LIKE': LIKE,
    'IN'  : IN,
    }


def _make():
    '''A builder function for testing.'''
    return AND(
        EQ(('Informants', 'comid'), ('Communities', 'comid')),
        AND(
            EQ(('Informants', 'infid'), ('Responses', 'infid')),
            AND(
                EQ(('Responses', 'targetid'), 712),
                AND(
                    NE(('Responses', 'item'), 'NR'),
                    AND(EQ(('Responses', 'item'), 'NA'),
                        EQ(('Responses', 'item'), '-0-'))))))


