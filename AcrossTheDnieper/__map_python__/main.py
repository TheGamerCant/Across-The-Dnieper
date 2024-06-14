import os
import subprocess
import re
import tkinter as tk
import shutil
import codecs

try:
	import numpy as np
	has_numpy = True
except ImportError:
	has_numpy = False
try:
	from PIL import ImageTk, Image, ImageOps
	has_pil = True
except ImportError:
	has_pil = False


class provinceClass:
    def __init__(self, ID, red, green, blue, type, coastal, terrain, continent, stateID, victoryPoints, strategicRegion, names, buildings):
        self.ID = int(ID)
        self.red = int(red)
        self.green = int(green)
        self.blue = int(blue)
        self.type = str(type)
        self.coastal = str(coastal)
        self.terrain = str(terrain)
        self.continent = int(continent)
        self.stateID = int(stateID)
        self.victoryPoints = int(victoryPoints)
        self.strategicRegion = int(strategicRegion)
        self.names = names if isinstance(names, list) else [names]
        self.buildings = buildings if isinstance(buildings, list) else [buildings]

    def __repr__(self):
        return f"Province(ID={self.ID}, red={self.red}, green={self.green}, blue={self.blue}, type={self.type}, coastal={self.coastal}, terrain={self.terrain}, stateID={self.stateID}, victoryPoints={self.victoryPoints}, strategicRegion={self.strategicRegion}, names={self.names}, buildings={self.buildings})"
    
class stateClass:
    def __init__(self, ID, population, category, owner, provinces, names, buildings, resources, dateInfo, cores, claims, stateFlags, impassable):
        self.ID = int(ID)
        self.population = int(population)
        self.category = str(category)
        self.owner = str(owner)
        self.provinces = provinces if isinstance(provinces, list) else [provinces]
        self.names = names if isinstance(names, list) else [names]
        self.buildings = buildings if isinstance(buildings, list) else [buildings]
        self.resources = resources if isinstance(resources, list) else [resources]
        self.dateInfo = dateInfo if isinstance(dateInfo, list) else [dateInfo]
        self.cores = cores if isinstance(cores, list) else [cores]
        self.claims = claims if isinstance(claims, list) else [claims]
        self.stateFlags = stateFlags if isinstance(stateFlags, list) else [stateFlags]
        self.impassable = int(impassable)
    
    def __repr__(self):
        return f"State(ID={self.ID}, population={self.population}, category={self.category}, owner={self.owner}, provinces={self.provinces}, names={self.names}, buildings={self.buildings}, resources={self.resources}, dateInfo={self.dateInfo}, cores={self.cores}, claims={self.claims}, stateFlags={self.stateFlags}, impassable={self.impassable}"
    
class strategicRegionClass:
    def __init__(self, ID, name, provinces):
        self.ID = int(ID)
        self.name = str(name)
        self.provinces = provinces if isinstance(provinces, list) else [provinces]

def parse_buildings_string(buildings_string):
    # Find all key=value pairs in the string and convert to 2d string
    matches = re.findall(r'(\w+)\s*=\s*(\d+)', buildings_string)
    buildings_array = [[match[0], int(match[1])] for match in matches]
    
    return buildings_array

def isolate_province_buildings(buildings_string):
    bracketed_matches = re.findall(r'(\d+)\s*=\s*\{[^}]+\}', buildings_string)
    other_matches = re.findall(r'(\w+)\s*=\s*(\d+)', buildings_string)
    provinceBuildings= []
    for match in re.finditer(r'(\d+)\s*=\s*\{[^}]+\}', buildings_string):
        provinceBuildings.append(match.group(0))
    stateBuildingsString = re.sub(r'(\d+)\s*=\s*\{[^}]+\}', '', buildings_string).strip()

    return stateBuildingsString, provinceBuildings

def parse_province_buildings_array(buildings_array):
    for item in buildings_array:
        province_id_match = re.match(r'(\d+)\s*=\s*\{', item)
        if province_id_match:
            provinceID = int(province_id_match.group(1))
            buildings_match = re.search(r'\{([^}]+)\}', item)
            if buildings_match:
                buildings_string = buildings_match.group(1).strip()
                provinceBuildingsArray = []
                buildings_pairs = re.findall(r'(\w+)\s*=\s*(\d+)', buildings_string)
                for building, count in buildings_pairs:
                    provinceBuildingsArray.append([building, int(count)])
                

                provincesArray[provinceID].buildings.clear()
                provincesArray[provinceID].buildings = provinceBuildingsArray

def return_close_bracket_location_string(openBracketLocation, localString):
    returnString = localString[openBracketLocation:]
    bracketBalance = 1
    currentParseLocation = openBracketLocation+1

    while bracketBalance != 0:
        if localString[currentParseLocation] == "{":
            bracketBalance+=1
        elif localString[currentParseLocation] == "}":
               bracketBalance-=1

        currentParseLocation += 1
            
    CloseBracketLocation = currentParseLocation-1
    
    return localString[openBracketLocation:CloseBracketLocation]

#AcrossTheDnieper/__map_python__
current_directory = os.getcwd()

#AcrossTheDnieper
base_directory = os.path.dirname(current_directory)

#AcrossTheDnieper/map
map_folder_path = os.path.join(base_directory, "map")

#AcrossTheDnieper/map/definition.csv
definitions_csv_file_path = os.path.join(map_folder_path, "definition.csv")

#AcrossTheDnieper/map/strategicregions
strategic_regions_folder_path = os.path.join(map_folder_path, "strategicregions")

#Load provinces
provincesArray = []
with open(definitions_csv_file_path, 'r') as file:
    for line in file:
        parts = line.strip().split(';')
        # and parts[0] != "0"       <-- Add this to the line below if you don't want an initial province class with everything set to 0
        if len(parts) >= 4:
            ID, red, green, blue, type, coastal, terrain = parts[:7]
            province = provinceClass(ID, red, green, blue, type, coastal, terrain, 1, 0, 0, 0, 0, 0)     #Read definitions.csv and create a new province class with ID and rgb values, set all other values to 0
            provincesArray.append(province)

provincesArray.sort(key=lambda x: x.ID)

#AcrossTheDnieper/history/states
history_states_folder_path = os.path.join(base_directory, "history", "states")
os.chdir(history_states_folder_path) 
statesArray = []
statesArray.append(stateClass(0,0,"","",0,0,0,0,0,0,0,0,-1))

def return_state_file_values(file_path): 
    with open(file_path, 'r', errors='ignore') as f: 
        stateData = f.read()
        stateData = re.sub(r'\s+', ' ', stateData).strip()
        stateData.lower()                                   #Read the file, collapse into a single string and convert to lower case

        id_match = re.search(r'id\s*=\s*(\d+)', stateData)
        if id_match:
            ID = id_match.group(1)
        else:
            ID = None

        impassable = stateData.find('impassable')

        manpower_match = re.search(r'manpower\s*=\s*(\d+)', stateData)
        if manpower_match:
            population = manpower_match.group(1)
        else:
            population = None
        
        category_match = re.search(r'state_category\s*=\s*(\w+)', stateData)
        if category_match:
            category = category_match.group(1)
        else:
            category = None

        owner_match = re.search(r'owner\s*=\s*(\w+)', stateData)
        if owner_match:
            owner = owner_match.group(1)
        else:
            owner = None

        provinces_match = re.search(r'provinces=\{(.*?)\}', stateData, re.DOTALL)
        if provinces_match:
            provinces = re.findall(r'(\d+)', provinces_match.group(1))
        else:
            provinces = []

        victory_points = re.findall(r'victory_points\s*=\s*\{\s*(\d+)\s+(\d+)\s*\}', stateData)
        victory_points = [[int(vp[0]), int(vp[1])] for vp in victory_points]
        if victory_points:
            for i in range (0,len(victory_points)):
                provincesArray[victory_points[i][0]].victoryPoints = victory_points[i][1]

        date_pattern = re.compile(r'\b(\d{4})\.(\d{1,2})\.(\d{1,2})\b')
        dates = date_pattern.findall(stateData)
        dates = [f"{year}.{month}.{day}" for year, month, day in dates]
        dateInfo = [0]
        if dates:
            dateInfo.clear()
            for i in range(0,len(dates)):
                datesLocation = stateData.find(dates[i])

                openBracketLocation = stateData[datesLocation:].find('{')
                if openBracketLocation != -1:
                    openBracketLocation += datesLocation+1
                    dateString = return_close_bracket_location_string(openBracketLocation,stateData)
                    dateString = str(dates[i]) + " = {" + dateString + "}"
                    dateInfo.append(dateString)

        buildings = [0]
        buildingsLocation = stateData.find('buildings')
        openBracketLocation = stateData[buildingsLocation:].find('{')
        if openBracketLocation != -1:
            buildings.clear()
            openBracketLocation += buildingsLocation+1

            buildingsString = return_close_bracket_location_string(openBracketLocation,stateData)

            openBracketLocation = buildingsString.find('{')
            if openBracketLocation != -1:       #Has province buildings
                provinceBuildings = []
                buildingsString, provinceBuildings = isolate_province_buildings(buildingsString)
                #print(ID, ", State buildings: ", buildingsString, ", Province buildings: ", provinceBuildings)

                parse_province_buildings_array(provinceBuildings)        
            
            buildings = parse_buildings_string(buildingsString)
        

        resources = [0]
        resourcesLocation = stateData.find('resources')
        openBracketLocation = stateData[resourcesLocation:].find('{')
        if openBracketLocation != -1:
            resources.clear()
            openBracketLocation += resourcesLocation+1
            resourcesString = return_close_bracket_location_string(openBracketLocation,stateData)
            resources = parse_buildings_string(resourcesString)     #Code for parse buildings string works for this too

        cores = re.findall(r'add_core_of\s*=\s*(\w+)', stateData)
        if cores:
            cores = [[str(coreCountry)] for coreCountry in cores]
            for i in range(0,len(cores)):
                for j in range(0,len(dateInfo)):
                    if dateInfo[j] != 0:
                        addCoreOfString = 'add_core_of = ' + str(cores[i][j])
                        coresAtLaterStart = str(dateInfo[j]).find(addCoreOfString)
                        #print (ID, " - ", dateInfo[j], " - ", addCoreOfString, " - ", coresAtLaterStart, "\n")
                        if coresAtLaterStart != -1:
                            cores.pop(i)
        else:
            cores.clear()
            cores = [0]

        claims = re.findall(r'add_claim_by\s*=\s*(\w+)', stateData)
        if claims:
            claims = [[str(claimCountry)] for claimCountry in claims]
            for i in range(0,len(claims)):
                for j in range(0,len(dateInfo)):
                    if dateInfo[j] != 0:
                        addClaimByString = 'add_claim_by = ' + str(claims[i][j])
                        claimsAtLaterStart = str(dateInfo[j]).find(addClaimByString)
                        if claimsAtLaterStart != -1:
                            claims.pop(i)
        else:
            claims.clear()
            claims = [0]



        stateFlags = re.findall(r'set_state_flag\s*=\s*(\w+)', stateData)
        if stateFlags:
            stateFlags = [[str(i)] for i in stateFlags]
            for i in range(0,len(stateFlags)):
                for j in range(0,len(dateInfo)):
                    if dateInfo[j] != 0:
                        addFlagByString = 'set_state_flag = ' + str(stateFlags[i][j])
                        stateFlagsAtLaterStart = str(dateInfo[j]).find(addFlagByString)
                        if stateFlagsAtLaterStart != -1:
                            stateFlags.pop(i)
        else:
            stateFlags.clear()
            stateFlags = [0]

        
        return stateClass(int(ID), int(population), str(category), str(owner), list(map(int, provinces)), int(0), buildings, resources, dateInfo, cores, claims, stateFlags, impassable)


for file in os.listdir(): 
    if file.endswith(".txt"): 
        file_path = f"{history_states_folder_path}\{file}"
  
        state_obj  = return_state_file_values(file_path)
        statesArray.append(state_obj)     

statesArray.sort(key=lambda x: x.ID)

os.chdir(strategic_regions_folder_path) 
strategicRegionsArray = []
strategicRegionsArray.append(strategicRegionClass(0,"",0))

def return_strategic_region_file_values(file_path): 
    with open(file_path, 'r', errors='ignore') as f: 
        strategicRegionData = f.read()
        strategicRegionData = re.sub(r'\s+', ' ', strategicRegionData).strip()
        strategicRegionData.lower()                                   #Read the file, collapse into a single string and convert to lower case


        id_match = re.search(r'id\s*=\s*(\d+)', strategicRegionData)
        if id_match:
            ID = id_match.group(1)
        else:
            ID = None

        name_match = re.search(r'name=\"(.*?)\"', strategicRegionData)
        if name_match:
            name = name_match.group(1)
        else:
            name = None

        provinces_match = re.search(r'provinces=\{(.*?)\}', strategicRegionData, re.DOTALL)
        if provinces_match:
            provinces = re.findall(r'(\d+)', provinces_match.group(1))
        else:
            provinces = []


        return strategicRegionClass(int(ID),str(name),list(map(int, provinces)))


for file in os.listdir(): 
    if file.endswith(".txt"): 
        file_path = f"{strategic_regions_folder_path}\{file}"
  
        strategic_regions_obj  = return_strategic_region_file_values(file_path)
        strategicRegionsArray.append(strategic_regions_obj)  


#Assign stateIDs to province types
for state in statesArray:
    for prov in range(0,len(state.provinces)):
        currentProv = int(state.provinces[prov])
        provincesArray[currentProv].stateID = state.ID

#Assign Strategic Regions to province types
for strategicRegion in strategicRegionsArray:
    for prov in range(0,len(strategicRegion.provinces)):
        currentProv = int(strategicRegion.provinces[prov])
        provincesArray[currentProv].strategicRegion = strategicRegion.ID

#AcrossTheDnieper/localisation/english
english_loc_path = os.path.join(base_directory, "localisation", "english")

#AcrossTheDnieper/localisation/english/victory_points_l_english.yml
victory_point_names_file_path = os.path.join(english_loc_path, "victory_points_l_english.yml")

for i in provincesArray:
    i.names.clear()

for i in statesArray:
    i.names.clear()

with open(victory_point_names_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        if line[1:15] == "VICTORY_POINTS":
            parts = line.split(':')
            vpID = parts[0].split('_')[-1]
            if vpID.isnumeric():        # Default string, for example -> VICTORY_POINTS_8800:0 "Kyiv"
                vpName = parts[1]
                first_quote_pos = vpName.find('"')
                vpName = vpName[first_quote_pos+1:]
                last_quote_pos = vpName.rfind('"')
                vpName = vpName[:last_quote_pos]

                vpID = int(vpID)
                provincesArray[vpID].names.append(["DEFAULT", vpName])
            else:
                IDAndHandle = parts[0][16:]   #Province ID and handle, for example -> 8800_SOV, with parts[1] being 0 "Kiev"
                IDAndHandle = IDAndHandle.split('_',1)  #Same as before but now split at the first underscore, now ['8800', 'SOV']

                vpName = parts[1]
                first_quote_pos = vpName.find('"')
                vpName = vpName[first_quote_pos+1:]
                last_quote_pos = vpName.rfind('"')
                vpName = vpName[:last_quote_pos]            #Get vpName same as before

                vpID = int(IDAndHandle[0])
                provincesArray[vpID].names.append([IDAndHandle[1], vpName])

#AcrossTheDnieper/localisation/english/state_names_l_english.yml
state_names_file_path = os.path.join(english_loc_path, "state_names_l_english.yml")

with open(state_names_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        if line[1:6] == "STATE":
            parts = line.split(':')
            stateID = parts[0].split('_')[-1]
            if stateID.isnumeric():
                stateName = parts[1]
                first_quote_pos = stateName.find('"')
                stateName = stateName[first_quote_pos+1:]
                last_quote_pos = stateName.rfind('"')
                stateName = stateName[:last_quote_pos]

                stateID = int(stateID)
                statesArray[stateID].names.append(["DEFAULT", stateName])
            else:
                IDAndHandle = parts[0][7:]
                IDAndHandle = IDAndHandle.split('_',1)

                stateName = parts[1]
                first_quote_pos = stateName.find('"')
                stateName = stateName[first_quote_pos+1:]
                last_quote_pos = stateName.rfind('"')
                stateName = stateName[:last_quote_pos]

                stateID = int(IDAndHandle[0])
                statesArray[stateID].names.append([IDAndHandle[1], stateName])

#Code below would allow for a command-line based interface to access data from any province or state, while removing the GUI
#Useful for debugging
runMain = False
while runMain == True:
    typeToSearch = input("Input either \"Province(s)\" or \"State(s)\":\t\t")
    typeToSearch = str.title(typeToSearch)
    IDToSearch = int(input("Enter an ID to search for:\t"))

    if typeToSearch == "Provinces" or typeToSearch == "Province":
        print(provincesArray[IDToSearch])
    elif typeToSearch == "States" or typeToSearch == "State":
        print(statesArray[IDToSearch])

class ImageCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, bg ="black", **kwargs)
        self.bind("<ButtonPress-2>", self.on_start_drag)
        self.bind("<B2-Motion>", self.on_drag,)
        self.bind("<ButtonPress-1>", self.on_left_click)
        #self.bind("<MouseWheel>", self.on_zoom)
        self.bind("<Motion>", self.on_mouse_motion)
        self.start_x = None
        self.start_y = None
        self._image = None
        self._photo_image = None
        self._scale = 1.00
        self.current_colour_r = None
        self.current_colour_g = None
        self.current_colour_b = None
        self.image_top_left_x = 0
        self.image_top_left_y = 0

        self.current_colour_label = tk.Label(master, text="Current Colour: (0, 0, 0)", bg="white")
        self.current_colour_label.pack(side="top", anchor = "nw")
        #self.current_zoom_label = tk.Label(master, text="Current Zoom = 1", bg="white")
        #self.current_zoom_label.pack(side="bottom", anchor="sw")
        #self.original_dimensions_label = tk.Label(master, text="Original dimensions", bg="white")
        #self.original_dimensions_label.place(relx=1.00, y=0, anchor='ne')

        #self.listbox = tk.Listbox(master, selectmode=tk.SINGLE,)
        #self.listbox.place(relx=1.0,y=0,anchor="ne")
        self.loadProvFromIDTitle = tk.Label(master, text = "Load province by ID")
        self.loadProvFromIDTitle.place(relx=1.00,x=-50,y=0,anchor="ne")
        self.enterProvinceID = tk.Entry(master)
        self.enterProvinceID.place(relx=0.95,x=-86,y=26,anchor="ne")
        self.enterProvinceIDButton = tk.Button(master, text="load", command=self.load_province_from_ID)
        self.enterProvinceIDButton.place(relx=1.00,x=-50,y=25,anchor="ne")

        self.loadProvFromIDTitle = tk.Label(master, text = "Current province:", font=('Helvetica',20))
        self.loadProvFromIDTitle.place(relx=0.67,x=0,y=72,anchor="w")

        self.provinceNamesListbox = tk.Listbox(master, selectmode=tk.SINGLE, width = 90)
        self.provinceNamesListbox.place(relx=1.00,x=-30,y=150,anchor="ne")

    def load_province(self, provID):
        self.populate_vp_name_listbox(provID)
        self.loadProvFromIDTitle.config(text=f"Current province: {provID}\nVictoryPoints = {provincesArray[provID].victoryPoints}\nState = {provincesArray[provID].stateID}")

    def load_province_from_ID(self):
        provinceIDToSend = self.enterProvinceID.get()
        self.load_province(int(provinceIDToSend))

    def display_image(self, image):
        self._image = image
        self._photo_image = ImageTk.PhotoImage(self._image)
        self.create_image(0, 0, anchor=tk.NW, image=self._photo_image)
        self.config(scrollregion=self.bbox(tk.ALL))

        #self.original_width = int(self._image.width)
        #self.original_height = int(self._image.height)
        #self.original_dimensions_label.config(text=f"Original width ={self.original_width},Original height ={self.original_height}")

    def populate_vp_name_listbox(self, provID):
        self.provinceNamesListbox.delete(0, tk.END)
        if self.loadProvFromIDTitle.cget("text") != "Current province:":        #If a province has been loaded, load names
            for prov in provincesArray[provID].names:
                self.provinceNamesListbox.insert(tk.END, prov)

    def on_start_drag(self, event):
        self.start_x = event.x
        self.start_y = event.y

    #def on_zoom(self, event):
    #    factor = 0.5 if event.delta < 0 else 2
    #    self._scale *= factor
    #    if self._scale > 8.0 or self._scale < 0.125:
    #        self._scale = np.clip(self._scale, 0.125, 8.0)
    #    else:
    #        pass
    #        #Zoom functionality goes here
    #        print (self._scale)

    #        if self._scale < 1.0:       #Zoom out
    #           newWidth = int(self._image.width * self._scale)
    #            newHeight = int(self._image.height * self._scale)
    #            resized_image = self._image.resize((newWidth, newHeight), Image.LANCZOS)
    #            self._photo_image = ImageTk.PhotoImage(resized_image)
    #            self.delete("all")
    #            self.create_image(0, 0, anchor=tk.NW, image=self._photo_image)

    #   self.current_zoom_label.config(text=f"Current Zoom: {self._scale}")

    def on_drag(self, event):
        if self.start_x is not None and self.start_y is not None:
            delta_x = event.x - self.start_x
            delta_y = event.y - self.start_y
            self.move(tk.ALL, delta_x, delta_y)
            self.start_x = event.x
            self.start_y = event.y

            self.image_top_left_x += delta_x
            self.image_top_left_y += delta_y
    

    def on_mouse_motion(self, event):
        realImageCoordsX = event.x - self.image_top_left_x
        realImageCoordsY = event.y - self.image_top_left_y

        if self._image:
            try:
                pixel_color = self._image.getpixel((realImageCoordsX, realImageCoordsY))
                self.current_colour_r, self.current_colour_g, self.current_colour_b = pixel_color
                self.current_colour_label.config(text=f"Current Colour: ({self.current_colour_r}, {self.current_colour_g}, {self.current_colour_b})")

            except:
                pass

    def on_left_click(self, event):
        for i in provincesArray:
            if i.red == self.current_colour_r and i.green == self.current_colour_g and i.blue == self.current_colour_b:
                self.load_province(i.ID)

        
        


#Main loop to allow for Tkinter

def main():
    #load provinces.bmp
    #map_folder_path is already defined
    provinces_bmp_path = os.path.join(map_folder_path, "provinces.bmp")
    provinces_bmp_image = Image.open(provinces_bmp_path)

    original_width, original_height = provinces_bmp_image.size

    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    #To display the image at 2/3rds of the screens size at all times
    display_width = screen_width // 3 * 2
    display_height = screen_height // 3 * 2

    # Create an ImageCanvas
    canvas = ImageCanvas(root, width=display_width, height=display_height)
    canvas.pack(side="top", anchor = "nw")

    # Display the image on the canvas
    canvas.display_image(provinces_bmp_image)

    root.mainloop()

if __name__ == "__main__":
    main()

#User has closed the window, now create files
print (current_directory)

#Removes all folders in the current directory (AcrossTheDnieper/__map_python__), while leaving any files.
for item in os.listdir(current_directory):
    item_path = os.path.join(current_directory, item)
    if os.path.isdir(item_path):
        shutil.rmtree(item_path)

foldersToCreate = ["localisation/english", "common/scripted_effects", "history/states", "map", "map/strategicregions"]
for folder_name in foldersToCreate:
    folder_path = os.path.join(current_directory, folder_name)
    os.makedirs(folder_path, exist_ok=True)

history_states_folder_path = os.path.join(current_directory, "history", "states")
common_scripted_effects_folder_path = os.path.join(current_directory, "common", "scripted_effects")
localisation_english_folder_path = os.path.join(current_directory, "localisation", "english")
map_folder_path = os.path.join(current_directory, "map")
strategic_regions_folder_path = os.path.join(map_folder_path, "strategicregions")

definitions_csv_file_path = os.path.join(map_folder_path, "definitions.csv")
with open(definitions_csv_file_path, 'w', encoding='utf-8') as f:
    for i in provincesArray:
        print(str(i.ID) + ";" + str(i.red) + ";" + str(i.green) + ";" + str(i.blue) + ";" + i.type + ";" + i.coastal + ";" + i.terrain + ";" + str(i.continent), file=f)

victory_point_names_file_path = os.path.join(localisation_english_folder_path, "victory_points_l_english.yml")
with open(victory_point_names_file_path, 'w', encoding='utf-8-sig') as f:
    print("l_english: ", file=f)
    for i in provincesArray:
        if i.names:
            for j in range (0,len(i.names)):
                if str(i.names[j][0]) == "DEFAULT":
                    print(" VICTORY_POINTS_" + str(i.ID) + ":0 \"" + str(i.names[j][1] + "\""), file=f)
                else:
                    print(" VICTORY_POINTS_" + str(i.ID) + "_" + str(i.names[j][0]) + ":0 \"" + str(i.names[j][1] + "\""), file=f)

state_names_file_path = os.path.join(localisation_english_folder_path, "state_names_l_english.yml")
with open(state_names_file_path, 'w', encoding='utf-8-sig') as f:
    print("l_english: ", file=f)
    for i in statesArray:
        if i.names:
            for j in range (0,len(i.names)):
                if str(i.names[j][0]) == "DEFAULT":
                    print(" STATE_" + str(i.ID) + ":0 \"" + str(i.names[j][1] + "\""), file=f)
                else:
                    print(" STATE_" + str(i.ID) + "_" + str(i.names[j][0]) + ":0 \"" + str(i.names[j][1] + "\""), file=f)

state_names_scripted_effects_file_path = os.path.join(common_scripted_effects_folder_path, "state_and_province_names_scripted_effects.txt")
with open(state_names_scripted_effects_file_path, 'w', encoding='utf-8') as f:
    for state in statesArray:
        if state.ID !=0:
            print ("update_state_" + str(state.ID) + "_names={\t\t#" + str(state.names[0][1]), file=f)
            if len(state.names) != 1:
                print ("\t" + str(state.ID) + "={", file=f)
                print ("\t\tif={\n\t\t\tlimit = { CONTROLLER = { " + str(state.names[1][0]) + " = yes } }"\
                    "\n\t\t\tset_state_name = STATE_" + str(state.ID) + "_" + str(state.names[1][0]), "\n\t\t}", file=f)
                if len(state.names) > 2:
                    for i in range(2,len(state.names)):
                        print ("\t\telse_if={\n\t\t\tlimit = { CONTROLLER = { " + str(state.names[i][0]) + " = yes } }"\
                            "\n\t\t\tset_state_name = STATE_" + str(state.ID) + "_" + str(state.names[i][0]), "\n\t\t}", file=f)

                print ("\t\telse={\n\t\t\treset_state_name=yes\n\t\t}\n\t}", file=f)
            
            for prov in state.provinces:
                if len(provincesArray[prov].names) > 1:
                    print ("\tif={\t\t\t#" + str(provincesArray[prov].names[0][1]) + "\n\t\tlimit={ any_country={ controls_province = " + str(prov) + " "\
                        + str(provincesArray[prov].names[1][0]) + " = yes } }\n\t\tset_province_name = { id = "\
                        + str(prov) + " name = VICTORY_POINTS_" + str(prov) + "_"\
                        + str(provincesArray[prov].names[1][0]) + " }\n\t}",file=f)
                    if len(provincesArray[prov].names) > 2:
                        for i in range(2,len(provincesArray[prov].names)):
                            print ("\telse_if={\n\t\tlimit={ any_country={ controls_province = " + str(prov) + " "\
                                + str(provincesArray[prov].names[i][0]) + " = yes } }\n\t\tset_province_name = { id = "\
                                + str(prov) + " name = VICTORY_POINTS_" + str(prov) + "_"\
                                + str(provincesArray[prov].names[i][0]) + " }\n\t}",file=f)
                    
                    print ("\telse={\n\t\treset_province_name = " + str(prov) +  "\n\t}",file=f)

            print ("}", file=f)
    print ("}\n\nchange_city_names={\n\tZZZ={", file=f)
    for i in range (1,len(statesArray)):
        print ("\t\tupdate_state_" + str(i) + "_names=yes", file=f)
    print ("\t}\n}\nrevert_city_names_to_original={\n\tevery_state = { reset_state_name=yes }", file=f)
    for state in statesArray:
        for i in range(0,len(state.names)):
            if str(state.names[i][0]) == "IS_2016_DECOM":       #Can add more in the future if there's the option to change city names
                print ("\t" + str(state.ID) + "={\n\t\tif={\n\t\t\tlimit={ "\
                    + str(state.names[i][0]) + " = yes }\n\t\t\tset_state_name = STATE_"\
                    + str(state.ID) + "_" + str(state.names[i][0])\
                    + "\n\t\t}\n\t\telse={ reset_state_name = yes }\n\t}",file=f)
    
    for prov in provincesArray:
        if prov.victoryPoints !=0:
            hasUniqueDefaultName = False
            for i in range(0,len(prov.names)):
                if str(prov.names[i][0]) == "IS_2016_DECOM":
                    hasUniqueDefaultName = True
                    print ("\tif={\n\t\tlimit = { " + str(prov.names[i][0]) + " = yes }\n\t\tset_province_name = { id = "\
                        + str(prov.ID) + " name = VICTORY_POINTS_" + str(prov.ID) + "_" + str(prov.names[i][0])\
                        + " }\n\t}\n\telse={\n\t\tset_province_name = { id = " + str(prov.ID) + " name = VICTORY_POINTS_" + str(prov.ID) + " }\n\t}", file=f)
                    
                elif i == (len(prov.names)-1) and hasUniqueDefaultName == False:
                    print ("\tset_province_name = { id = " + str(prov.ID) + " name = VICTORY_POINTS_" + str(prov.ID) + " }", file=f)

    print ("}", file=f)


#Keep these as the last file done, just makes life easier as you have to change the directory
os.chdir(history_states_folder_path) 
for state in statesArray:
    if state.ID !=0:
        filename = f'{state.ID}-State_{state.ID}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            print(\
                "state={\n\tid="\
                +str(state.ID) + "\n\tname=\"STATE_"\
                +str(state.ID)+"\"", file=f)
            if state.resources[0] != 0:
                print ("\tresources={", file=f )
                for i in range (0,len(state.resources)):
                    print ("\t\t" + str(state.resources[i][0]) + " = " + str(state.resources[i][1]),file=f)
                print ("\t}", file=f )
            print("\thistory={\n\t\towner = " + str(state.owner), file=f)
            if state.cores[0] != 0:
                for i in range (0,len(state.cores)):
                    print("\t\tadd_core_of = " + str(state.cores[i][0]), file=f)
            if state.claims[0] != 0:
                for i in range (0,len(state.claims)):
                    print("\t\tadd_claim_by = " + str(state.claims[i][0]), file=f)
            if state.stateFlags[0] != 0:
                for i in range (0,len(state.claims)):
                    print("\t\tset_state_flag = " + str(state.stateFlags[i][0]), file=f)

            for prov in state.provinces:
                if provincesArray[prov].victoryPoints != 0:
                    try:
                        print ("\t\tvictory_points={ " + str(provincesArray[prov].ID) + " "\
                            + str(provincesArray[prov].victoryPoints) + " }" + "\t#" + str(provincesArray[prov].names[0][1]), file=f )
                    except:
                        print ("\t\tvictory_points={ " + str(provincesArray[prov].ID) + " "\
                            + str(provincesArray[prov].victoryPoints) + " }", file=f )
            
            print ("\t\tbuildings={", file=f)
            for prov in state.provinces:
                if provincesArray[prov].buildings[0] != 0:
                    print ("\t\t\t" + str(provincesArray[prov].ID) + " = { ", end="", file=f)
                    for i in range(0,len(provincesArray[prov].buildings)):
                        print (str(provincesArray[prov].buildings[i][0]) + " = " +  str(provincesArray[prov].buildings[i][1]), end=" ", file=f)
                    print ("}", file=f)
            if state.buildings:
                if state.buildings[0] != 0:
                    for i in range(0,len(state.buildings)):
                        print("\t\t\t" + str(state.buildings[i][0])+ " = " + str(state.buildings[i][1]), file=f)
            print ("\t\t}", file=f)
            if state.dateInfo[0] != 0:
                print ("\t\t" + str(state.dateInfo[0]), file=f)
            print ("\t}\n\tprovinces={\n\t\t", end="", file=f)
            for prov in state.provinces:
                print (str(prov), end=" ", file=f)
            if state.impassable != -1:
                impassableString = "\n\timpassable=yes"
            else:
                impassableString = ""
            print("\n\t}\n\tmanpower="\
            + str(state.population) + "\n\tbuildings_max_level_factor=1.000" + impassableString + "\n\tstate_category="\
            + str(state.category) + "\n}", file=f)

os.chdir(strategic_regions_folder_path) 
for strategicRegion in strategicRegionsArray:
    if strategicRegion.ID !=0:
        filename = f'{strategicRegion.ID}-{strategicRegion.name}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            print("strategic_region={\n\tid=" + str(strategicRegion.ID)\
            + "\n\tname = \"" + str(strategicRegion.name) + "\"\n\tprovinces={\n\t\t", end="", file=f)
            for prov in strategicRegion.provinces:
                print (str(prov), end=" ", file=f)
            print("\n\t}\n\tweather={\n\t}\n}", file=f)