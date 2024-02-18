#I'm just keeping this here in case I need to get a list of VP IDs in the future. Can also be used as a basis for reading other loc files I guess.

numbers = []

with open('victory_points_l_english.yml', 'r', encoding='utf-8') as file:
    for line in file:
        if line[1:15] == "VICTORY_POINTS":
            parts = line.split(':')
            number_part = parts[0].split('_')[-1]       #Get everything between the colon and the underscore prior to the colon.
            if number_part.isnumeric():     #Some VPs have _RUS or _POL on the end, ignore them.
                numbers.append(int(number_part))
                
numbers.sort()

for i in range (0,len(numbers)):
    print("\tset_province_name = {} id = {} name = VICTORY_POINTS_{} {}".format(("{"),(numbers[i]),(numbers[i]),("}")))
