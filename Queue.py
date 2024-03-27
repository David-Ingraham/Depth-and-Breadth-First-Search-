from typing import TypeVar

T= TypeVar('T')


from linkedList import *

class Queue():

    __slots__ = ('_data')

    def __init__ (self)-> None:
        self._data = LinkedList()

    def __len__(self)-> int:
        return len(self._data)
    
    def push(self, item: T)-> None:
        self._data.add_right(item)

    def pop(self)-> T:
       return self._data.remove_left()
    
    def top(self) -> T:
        return self._data.front()
    

    def isempty(self)-> bool:
        return len(self._data) ==0
  
    def __str__(self)-> str:
        ''' creates a string representation of the data in the queue, using
            the maximum str length of any one datum as a centering guide 
        Returns:
            string representation of the stack
        '''

        data_list = []
        ptr = self._data._head

        for i in range(self._data._size):
            data_list.append(ptr.data)

            ptr = ptr.next

        result     = "--- top ---\n"
        max_len    = max(len(str(datum)) for datum in data_list)
    
        half_width = max(0, (len(result) - max_len) // 2)
        # "\n".join creates a new string, deliminted by "\n" characters, where
        # the elements between each "\n" in the string are drawn from the
        # reverse of the data list so as to print the queue from top to bottom
        result += "\n".join(f"{datum:>{max_len + half_width}}" for datum in data_list)
        result += "\n--- bot ---"
        return result
    


def main():


    q = Queue()

    for i in range(10):
        q.push(i)

    
    print(q)
    print(q.isempty())

    print(q.pop())

    print(q)

    print(q.top())


if __name__ == '__main__':
    main()