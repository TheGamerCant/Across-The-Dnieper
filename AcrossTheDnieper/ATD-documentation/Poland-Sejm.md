Parties: LEFT, PO, PSL, PiS, RIGHT and OTHER
Any array will be of length six and have variables corresponding to the parties in that order unless stated otherwise.
E.G POL.generic_party_array^0 = LEFT, POL.generic_party_array^1 = PO ... POL.generic_party_array^5 = OTHER

List of states that are 'election states' - These states have the variables related to each voivodeships' political status:

427	- Mazowieckie
34	- Podlaskie
31	- Warmińsko-Mazurskie
51	- Lubelskie
19	- Pomorskie
38	- Kujawsko-Pomorskie
47	- Łódźkie
22	- Zachodniopomorskie
36	- Wielkopolskie
40	- Lubuskie
64	- Świętokrzyskie (Holy Cross)
49	- Dolnośląskie (Lower Silesia)
62	- Opolskie 				//Opolskie has a German minority party that does well
67	- Śląskie
81	- Małopolskie
76	- Podkarpackie (Sub-Carpathia)

Each one of these election states have the following variables / arrays:

THIS.number_of_seats_in_sejm	- Integer variable. Determines how many times the D'Hont method is used to divide up MPs
THIS.election_turnout 			- Float variable.
THIS.PREV_election_turnout 		- Float variable.
THIS.party_seat_count			- Integer array. Each integer is the number of seats won by a party
THIS.PREV_party_seat_count		- Integer array
THIS.party_vote_count			- Float array. Number of votes won by party in that voivodeship. Stored in thousands (E.G a variable of 10.050 == 10,050 votes)
THIS.PREV_party_vote_count		- Float array
THIS.party_vote_percentage		- Float array. Percentage of votes won by party, =/= current party popularity
THIS.PREV_party_vote_percentage	- Float array