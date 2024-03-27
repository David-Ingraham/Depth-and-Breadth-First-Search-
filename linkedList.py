from __future__ import annotations

######################################################################


def test_linked_list():
    ll = LinkedList[int]()

    # Test add_left and add_right
    ll.add_left(1)
    ll.add_left(2)
    ll.add_right(3)
    ll.add_right(4)
    assert str(ll) == 'head->[2]<->[1]<->[3]<->[4]<-tail', "add_left or add_right failed"

    # Test __len__
    assert len(ll) == 4, "__len__ failed"

    # Test front and back
    assert ll.front() == 2, print(f'front failed. Returned {ll.front()}')
    assert ll.back() == 4, print(f"back failed Returned {ll.back()}")

    # Test remove_left and remove_right
    assert ll.remove_left() == 2, "remove_left failed"
    assert ll.remove_right() == 4, "remove_right failed"
    assert str(ll) == 'head->[1]<->[3]<-tail', "remove_left or remove_right failed"

    # Add more tests as needed
    print("All tests passed!")



class EmptyError(Exception):
    ''' class to represent an empty list exception '''
    def __init__(self, message: str) -> None:
        self.message = message

######################################################################
class Node[T]:
    ''' class to represent a node in a doubly-linked list '''
    def __init__(self, data: T):
        self.data: T      = data
        self.prev: Node[T] = None  # pointer to the previous Node in the list
        self.next: Node[T] = None  # pointer to the next Node in the list

######################################################################
class LinkedList[T]:
    #''' class to implement a doubly-linked list '''
    __slots__ = ('_head', '_tail', '_size')

    def __init__(self) -> None:
        self._head: Node[T] = None   # the head pointer in the linked list
        self._tail: Node[T] = None   # the tail pointer in the linked list
        self._size: int     = 0      # number of entries in the list

    def __len__(self) -> int:
        ''' returns the number of entries in the linked list
        Returns:
            integer valued number of list entries
        '''
        return self._size

    def front(self) -> T:
        ''' method to return the data item at the front of the list without
            removing that node
        Returns:
            the T-valued item at the front of the list
        Raises:
            EmptyError if the list is empty
        '''

        if self._size == 0:
            raise EmptyError('List already empty')
        

        return self._head.data

    def back (self) -> T:
        ''' method to return the data item at the end of the list without
            removing that node
        Returns:
            the T-valued item at the end of the list
        Raises:
            EmptyError if the list is empty
        '''
        if self._size == 0:
            raise EmptyError('List already empty')
                
        return self._tail.data

    def add_left(self, item: T) -> None:
        ''' adds the given T-type data item as part of a new Node to the left
            of the linked list
        Parameters:
            item: a type T data item to be included as the data in the inserted Node
        Raises:
            TypeError if non-empty list and item type does not match list entry types
        '''


        if self._size != 0 and type(item) != type(self._head.data):
            msg = f'Only supporting list of single data type. Type of attmpeted add : {type(item)}. Type currently in list : {type(self._head.data)}'
            raise TypeError(msg)

        new_node = Node(item)

        if self._head is None:
           self._head = self._tail = new_node
           
           

        else:

            new_node.next = self._head
            self._head = new_node
            new_node.next.prev = new_node
            

        self._size+=1



        

    def add_right(self, item: T) -> None:
        ''' adds the given T-type data item as part of a new Node to the right 
            of the linked list
        Parameters:
            item: a type T data item to be included as the data in the inserted Node
        Raises:
            TypeError if non-empty list and item type does not match list entry types
        '''


        if self._size != 0 and type(item) != type(self._head.data):
            msg = f'Only supporting list of single data type. Type of attmpeted add : {type(item)}. Type currently in list : {type(self._head.data)}'
            raise TypeError(msg)

        new_node = Node(item)

        if self._head is None:
           self._head = self._tail = new_node
           

        else:

            self._tail.next = new_node
            new_node.prev = self._tail
            self._tail = new_node


        self._size +=1
            



     

    def remove_left(self) -> T:
        ''' removes the first Node in the linked list, returning the data item
            inside that Node
        Returns:
            a T type data item extracted from the removed Node
        Raises:
            EmptyError exception if list is empty
        '''



        if self._size == 0:
            raise EmptyError('cannot remove_left from an empty list')
        

        value : T = self._head.data

        if self._size == 1:
            self._head = self._tail = None

        else:
            self._head  = self._head.next 
            self._head.prev = None
        
        self._size -=1

        return value

    def remove_right(self) -> T:
        ''' removes the last Node in the linked list, returning the data item
            inside that Node
        Returns:
            a T type data item extracted from the removed Node
        Raises:
            EmptyError exception if list is empty
        '''



        if self._size == 0:
            raise EmptyError('cannot remove_left from an empty list')
        

        value : T = self._tail.data

        if self._size == 1:
            self._head = self._tail = None
           


        else:
            self._tail = self._tail.prev
            self._tail.next = None
        
        self._size-=1
        return value

    def __str__(self):
        ''' a str representation of the linked list data
        Returns:
            str representation of the linked list, showing head and tail
            pointers and list data items
        '''
        str_ = "head->"
        # start out at the head Node, and walk through Node by Node until we
        # reach the end of the linked list (i.e., the ._next entry is None)
        ptr_ = self._head
        while ptr_ is not None:
            str_ += "[" + str(ptr_.data) + "]<->" 
            ptr_ = ptr_.next  # move ptr_ to the next Node in the linked list

        if self._head != None: str_ = str_[:-3]  # remove the last "<->"
        str_ += "<-tail"
        return str_
        
###################
def main() -> None:
    # create a LinkedList and try out some various adds and removes
    ll = LinkedList()

    # your tests here...

    ll.add_left(10)

    print(ll)

    print(ll._size)
    print(ll.remove_right())

    print(ll)
  
    


    """ print(ll)

    for i in range(5):
        ll.add_left(i)

    print(ll)

    for i in range(1,5):
        ll.add_right(i)


    print(ll)


    print('*'*30)
    
    for i in range(5):
        a = ll.remove_left()
        print(ll)
        print(f'item removed : {a}')

    print('*'*30)
    print(ll)

    print('\n\n\n\n\n testing remove right')
    for i in range(5):
        ll.add_right(i)

    print(ll)
    

    for i in range(ll._size-1):
        print(f'the last item in the linked list is : {ll.remove_right()}')


    print(ll)
   
    print(ll)"""


    test_linked_list()
    print(f' front of the list : {ll.front()}')

    print(f' back of the list : {ll.back()}')




  

"""  ll.add_left(0)
    ll.add_left(1)

    print(ll)

    print(f' front of the list : {ll.front()}')

    print(f' back of the list : {ll.back()}')"""


    # Test add_left and add_right



   
    
        



if __name__ == "__main__":
    main()
