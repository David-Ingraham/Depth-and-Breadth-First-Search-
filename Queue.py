from typing import TypeVar

T= TypeVar('T')

class Queue():

    __slots__ = ('_data')

    def __init__ (self)-> None:
        self._data = []

    def __len__(self)-> int:
        return len(self._data)
    
    def push(self, item: T)-> None:
        self._data.append(item)

    def pop(self)-> T:
        self._data = self._data[1:]
        return self._data
    
    def top(self) -> T:
        return self._data[1:]
    

    def isempty(self)-> bool:
        return len(self._data) ==0
    
    def __str__(self)-> str:
        ''' creates a string representation of the data in the queue, using
            the maximum str length of any one datum as a centering guide 
        Returns:
            string representation of the stack
        '''
        result     = "--- top ---\n"
        max_len    = max(len(str(datum)) for datum in self._data)
        half_width = max(0, (len(result) - max_len) // 2)
        # "\n".join creates a new string, deliminted by "\n" characters, where
        # the elements between each "\n" in the string are drawn from the
        # reverse of the data list so as to print the queue from top to bottom
        result += "\n".join(f"{datum:>{max_len + half_width}}" for datum in self._data)
        result += "\n--- bot ---"
        return result
    


def main():


    q = Queue()

    for i in range(10):
        q.push(i)

    
    print(q)
    print(q.isempty())


if __name__ == '__main__':
    main()