#clean the first 10 spaces of each line of the text file locations.txt
#and write the cleaned data to a new file called locations_clean.txt

file = open("distances_optimize\locations.txt", "r")
file_clean = open("distances_optimize\locations_clean.txt", "w")
for line in file:
    #find first instance of tab
    tab_index = line.find("\t")
    line = line[:tab_index]
    file_clean.write(line + " UIUC, Illinois\n")
file.close()
file_clean.close()
print("Done!")