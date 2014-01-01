class Empty(Exception):
    pass

    
class NotSorted(Exception):
    pass


class BundleOfCards():
    """ Representation of travel cards' pile. 
        Initial data is given in JSON format:
        {'cardname1' : {'from_place' : 'some_value1', 'to_place' : 'some_value2', 
        'transport' : 'some_value3', 'route_number' : 'some_value4', 'gate' : 'some_value5', 
        'seat' : 'some_value6', 'other_notes' : 'some_value7'}, 
        'cardname2' : {'from_place' : 'some_value8', 'to_place' : 'some_value9', 
        'transport' : 'some_value10', 'route_number' : 'some_value11',  
        'gate' : 'some_value12', 'seat' : 'some_value13', 'other_notes' : 'some_value14'}, ...}
        Output: string containing description of the whole route which is close to 
        natural language.
    """

    class _Card():
        def __init__(self, card_name, from_place, to_place, transport, route_number, 
                    gate, seat, other_notes, next = None):
            self._card_name = card_name
            self._from = from_place
            self._to = to_place 
            self._transport = transport
            self._route_number = route_number 
            self._gate = gate
            self._seat = seat
            self._other_notes = other_notes
            self._next = next
            
            
        def get_representation(self):
            """
            Returns string representation of route's part that is defined by the given card
            """
            basic_text = 'Take %s %s from %s to %s. ' % (self._transport, self._route_number, self._from, self._to)
                
            if self._gate:
                gate_text = 'Gate %s. ' % (self._gate)
            else:
                gate_text = ''
                
            if self._seat:
                seat_text = 'Seat %s. ' % (self._seat)
            else:
                seat_text = 'No seat assignment. '    
            
            if isinstance(self._other_notes, basestring): #we deal with string
                other_notes_text = self._other_notes
            
            if isinstance(self._other_notes, dict): #we deal with dictionary:
                other_notes_text = ''.join(self._other_notes.values(), '. ')
                
            if isinstance(self._other_notes, (list, tuple)): # we deal with list or tuple
                other_notes_text = ''.join(self._other_notes, '. ')
                
            return ''.join([basic_text, gate_text, seat_text, other_notes_text])
            
    
    def __init__(self):
        self._head = None # reference to the head node
        self._tail = None # reference to the tail node
        self._size = 0
        self._issorted = False
    
    
    def _insert_card(self, card_name, from_place, to_place, transport, route_number, 
                    gate, seat, other_notes):
        new_card = self._Card(card_name, from_place, to_place, transport, route_number,
                    gate, seat, other_notes)
        if self.is_empty(): # if our bundle is empty yet
            self._head = new_card
            self._tail = new_card
            self._size += 1
        else:
            self._tail._next = new_card
            self._tail = new_card
            self._size +=1
    
    
    def _sort_cards(self):
        """
        Sorting procedure. It sorts cards to make continuous way. It returns True
        if sorting is successful, otherwise, we are given False. 
        """
        if self._size == 1: #  no need to sort 
            return True
        else:
            marker = self._head
            pivot = marker._next # next item to analyze
            before_pivot = marker
            while marker is not self._tail:
                if marker._to == pivot._from: # pivot is the end of the route 
                    if marker._next is pivot: # if marker and pivot are adjacent
                        marker = pivot
                        before_pivot = marker
                        pivot = marker._next

                    else:                    # if marker and pivot are not adjacent
                        temp = marker._next
                        
                        marker._next = pivot
                        before_pivot._next = pivot._next
                        pivot._next = temp
                        
                        marker = pivot
                        before_pivot = marker
                        pivot = marker._next 

                elif self._head._from == pivot._to: # if we can travel from pivot to head
                    before_pivot._next = pivot._next
                    pivot._next = self._head
                    self._head = pivot  #pivot becomes head
                    
                    pivot = marker._next
                    before_pivot = marker

                else:                      # if pivot can not be added neither to start nor to end
                    before_pivot = pivot
                    pivot = pivot._next
                    if pivot is None:
                        return False # there is no continuous way 
            return True
                
    def __len__(self):
        return self._size

        
    def is_empty(self):
        return self._size == 0

        
    def first_card(self):
        if self.is_empty():
            raise Empty('No cards are present.')
        if not self._issorted:
            raise NotSorted('Cards are not sorted. ')
        return self._head.get_representation()
    
    
    def last_card(self):
        if self.is_empty():
            raise Empty('No cards are present.')
        if not self._issorted:
            raise NotSorted('Cards are not sorted. ')
        return self._tail.get_representation()
    
    
    def load_cards(self, file_name, format_type):
        if format_type == 'json': #we deal with json
            import json
            cards = json.load(file_name)
        #elif format_type == 'xml'   # if we implement xml support in future
        if len(cards) == 0:
            raise Empty('There is no travel cards in file you specified')
        for card_name, v in cards.iteritems():
            self._insert_card(card_name, v['from_place'], v['to_place'], v['transport'], 
                            v['route_number'], v['gate'], v['seat'], v['other_notes'])
           
            
    def get_whole_route(self):
        if self.is_empty():
            raise Empty('No cards are present.')

        self._issorted = self._sort_cards()
        
        whole_route = []
        marker = self._head
        while marker is not None:
            whole_route.append(marker.get_representation())
            marker = marker._next
        result = ''.join(whole_route, '\n')
        
        if self._issorted:    
            return result
        else:
            return ''.join(['It is impossible to create continuous route from the given cards.', 
                            'Therefore, parts below are given in arbitrary way.',
                             result], '\n')