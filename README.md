Just small funny exercise. I do not claim that it is perfect soultion.

Traveler's Cards

You are given tickets (cards) for different means of transportation which deliver you from start A to destination B. Cards are shuffled. 
You do not know where your journey starts and ends. 
Every card contains information on starting and ending places of this piece of your route, mean of transportation (route numbe, seat number, etc.).
You have to provide Python API that will sort such a list of cards and return description in natural language how to make a journey.
API should accept unsorted list of cards as input. Input format you should devise yourself. 
The returned description should look like:
Take train 37A from Madrid to Barcelona. Seat 46C. 
Take the airport bus from Barcelona to Gerona Airport. No seat assignment. 
From Gerona Airport, take flight SK455 to Stockholm. Gate 45B. Seat 3A. Baggage drop at ticket counter 344. 
From Stockholm, take flight SK22 to New York JFK. Gate 22. Seat 7B. Baggage will be automatically transferred from your last leg.

Requirements:
Your algorithm should handle any number of cards if all the cards could be chained consecutively.
Arrival and departure times are unknown and unimportant. It is assumed that the next mean of transportation waits for you. 
Code structure should be extensible as different means of transportation with relative information could be utilized.
You should use object oriented programming.
You should use standards libraries only.
Describe input and output data formats.


Solution:
1. I have chosen JSON as input format. JSON represents list of cards. Every element of the list is a dictionary
key				value
from_place		starting point
to_place		destination
transport		mean of transportation
route_number	route number
seat			seat number
other_notes		other data (string, list or dictionary that contains strings with some other data)
gate			gate, platform, etc.

JSON has format: 
{
'cardname1' : {'from_place' : 'some_value1', 'to_place' : 'some_value2', 'transport' : 'some_value3', 'route_number' : 'some_value4', 'gate' : 'some_value5', 'seat' : 'some_value6', 'other_notes' : 'some_value7'}, 
'cardname2' : {'from_place' : 'some_value8', 'to_place' : 'some_value9', 'transport' : 'some_value10', 'route_number' : 'some_value11',  'gate' : 'some_value12', 'seat' : 'some_value13', 'other_notes' : 'some_value14'}, ...
}

2. A list of cards is created: instance of BundleOfCards class

3. Cards are loaded into instance of BundleOfCards with BundleOfCards.load_cards() method. Cards are not sorted at this point of time.

4. Method BundleOfCards.get_whole_route() sorts the cards and returns the string answer. 
If cards could be chained consecutively then answer contains it.
If there is no single route then string answer contains warning and unsorted (or partially sorted) cards.
Singly linked list is used as a base.
