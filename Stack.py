# for generics in Python 3.12, see:
# https://docs.python.org/3/library/typing.html#generics
# https://www.youtube.com/watch?v=q6ujWWaRdbA

from typing import TypeVar

T = TypeVar('T')

class EmptyError(Exception):
    ''' class extending Exception to better document stack errors '''
    def __init__(self, message: str):
        self.message = message

class Stack[T]:
    ''' class to implement a stack ADT using a Python list '''

    __slots__ = ("_data")

    def __init__(self):
        self._data: list[T] = []    # typing _data to be a list of type T

    def __len__(self) -> int:
        ''' allows the len function to be called using an ArrayStack object, e.g.,
               stack = ArrayStack()
               print(len(stack))
        Returns:
            number of elements in the stack, as an integer
        '''
        return len(self._data)

    def push(self, item: T) -> None: 
        ''' pushes a given item of arbitrary type onto the stack
        Parameters:
            item: an item of arbitrary type
        Returns:
            None
        Raises:
            TypeError if type pushed to non-empty stack does not match type
                of previously pushed element(s) (presumably type T)
        '''
        if len(self) > 0:
            t = type(self.top())
            if not isinstance(item, t):
                raise TypeError(f"cannot push {type(item).__name__} to stack of {t.__name__}")
        self._data.append(item)

    def pop(self) -> T:
        ''' removes the topmost element from the stack and returns that element
        Returns:
            the topmost item, of arbitrary type
        Raises:
            EmptyError exception if the stack is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in ArrayStack.pop(): stack is empty')
        return self._data.pop()  # calling Python list pop()

    def top(self) -> T:
        ''' returns the topmost element from the stack without modifying the stack
        Returns:
            the topmost item, of arbitrary type
        Raises:
            EmptyError exception if the stack is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in ArrayStack.top(): stack is empty')
        return self._data[-1]

    def is_empty(self) -> bool:
        ''' indicates whether the stack is empty
        Returns:
            True if the stack is empty, False otherwise
        '''
        return len(self._data) == 0

    def __str__(self) -> str:
        ''' creates a string representation of the data in the stack, using
            the maximum str length of any one datum as a centering guide
        Returns:
            string representation of the stack
        '''
        result = "--- top ---\n"
        if len(self._data) > 0:
            max_len    = max(len(str(datum)) for datum in self._data)
            half_width = max(0, (len(result) - max_len) // 2)
            # "\n".join creates a new string, deliminted by "\n" characters, where
            # the elements between each "\n" in the string are drawn from the
            # reverse of the data list so as to print the stack from top to bottom
            result += "\n".join(f"{datum:>{max_len + half_width}}" for datum in self._data[::-1])
            result += "\n--- bot ---"
        else:
            # stack is empty
            result += "--- bot ---"

        return result


###################
def main() -> None:
    empty = Stack[None]()
    print(empty)
    print('-' * 40)

    s = Stack[int]()
    for i in [8,6,7,5,3,0,9]: s.push(i)
    print(s)
    print('-' * 40)

    import string
    import random
    s2 = Stack[str]()
    for i in range(5):
        str_ = "".join(random.choice(string.ascii_letters) for i in range(7))
        s2.push(str_)
    print(s2)
    print('-' * 40)

    s3 = Stack[int]()
    s3.push(4)
    s3.push(5)
    try:
        s3.push('a')
    except TypeError as err:
        print(f"Successfully caught invalid push: {err}")



if __name__ == "__main__":
    main()
