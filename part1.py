import os

import datetime

# create empty dictionary to store inventory data
inventory = {}

# read 'ManufacturList.txt'
with open("cis-1348-sp25-project-menengab/ManufacturerList.txt", "r") as file:      # had to use full path to pull the price list, it wasnt working for just naming 'ManufacturerList.txt
    for line in file:                                                                           
        words = line.strip().split(",")                                             # split each line by commas and remove any whitespace
        if len(words) < 3:                                                          # skip any lines that have insufficent data
            continue
                                                                                           
        item_id = words[0].strip()                                                 # get item_id, manufacturer and item_type, while also checking if item is damaged            
        manufacturer = words[1].strip()                                                                 
        item_type = words[2].strip()
        damaged = True if len(words) > 3 and words[3].strip().lower() == "damaged" else False         

# add item details to the inventory dictionary, using item_id as key
        inventory[item_id] = {
            "manufacturer": manufacturer,
            "type": item_type,
            "price": None,                          # placeholder until we read price
            "service_date": None,                   # placeholder until we read service date
            "damaged": damaged
        }

# read 'PriceList.txt'
with open("cis-1348-sp25-project-menengab/PriceList.txt", "r") as file:            
    for line in file:
        words = line.strip().split(",")                                         # split each line by commas and remove any whitespace
        if len(words) < 2:                                                      # skip any lines that have insufficent data
            continue

        item_id = words[0].strip()
        price = float(words[1].strip())

# to check if item_id is in iventory, to then update price     
        if item_id in inventory:
            inventory[item_id]["price"] = price

# read 'ServiceDateslist.txt'
with open("cis-1348-sp25-project-menengab/ServiceDatesList.txt", "r") as file:
    for line in file:
        words = line.strip().split(",")                                         # split each line by commas and remove any whitespace
        if len(words) < 2:                                                      # skip any lines that have insufficent data
            continue

# get item_id and service_date
        item_id = words[0].strip()
        service_date = words[1].strip()

# if item_id is in the inventory, update its service date
        if item_id in inventory:
            inventory[item_id]["service_date"] = datetime.datetime.strptime(service_date, "%m/%d/%Y")


# function to get the manufactureer name for sorting the inventory by manufacturer
def get_manufacturer(item):
    return item[1]["manufacturer"]

# sort items alphabetically by manufacturer
sorted_items = sorted(inventory.items(), key=get_manufacturer)

# function to get item id for sorting item-type inventory files
def get_item_id(item):
    return item[0]                                      # make item_id the dictionary key

# function to get service date for sorting PastServiceDateInventory.txt
def get_service_date(item):
    return item[1]["service_date"]

# function to get price for sorting DamagedInventory.txt (highest to lowest)
def get_price(item):
    return item[1]["price"]

# write new sorted inventory to 'FullInvenntory.txt
with open("FullInventory.txt", "w") as file:
    for item_id, details in sorted_items:
        # change service date to string, and print N/A if not available
        service_date_str = details["service_date"].strftime('%m/%d/%Y') if details["service_date"] else "N/A"  
        # write item details in CSV format         
        file.write(f"{item_id}, {details['manufacturer']}, {details['type']}, {details['price']}, "
                   f"{service_date_str}, {'damaged' if details['damaged'] else ''}\n")
        
# generate item type-specific inventory files
item_types = {}

# loop to group items by their type
for item_id, details in inventory.items():
    item_type = details["type"]
    if item_type not in item_types:
        item_types[item_type] = []                                  # create a new list for each item type
    item_types[item_type].append((item_id,details))                 # add item to the list for its specific type

# loop to write the grouped inventory data to the individual files for each specific item type
for item_type, items in item_types.items():
    sorted_type_items = sorted(items, key=get_item_id)              # sort items by item_id
    with open(f"{item_type}Inventory.txt", "w") as file:
        for item_id, details in sorted_type_items:
            # change service date to string, and print N/A if not available
            service_date_str = details["service_date"].strftime('%m/%d/%Y') if details["service_date"] else "N/A"
            # write item detail for each type
            file.write(f"{item_id}, {details['manufacturer']}, {details['price']}, {service_date_str}, "
                       f"{'damaged' if details['damaged'] else ''}\n")
            
# write PastServiceDateInventory.txt ( sorted by oldest service date )
today = datetime.datetime.today()                                                       # to get today's date
# to filter items with service dates in the past
past_service_items = [(item_id, details) for item_id, details in inventory.items()
                      if details["service_date"] and details["service_date"] < today]    
# sort the past service items by service date   
sorted_past_service = sorted(past_service_items, key=get_service_date)     

with open("PastServiceDateInventory.txt", "w") as file:
    for item_id, details in sorted_past_service:
        service_date_str = details["service_date"].strftime('%m/%d/%Y')
        # write item details for past service items
        file.write(f"{item_id}, {details['manufacturer']}, {details['type']}, {details['price']}, "
                   f"{service_date_str}, {'damaged' if details['damaged'] else ''}\n")
        

# write DamagedInventory.txt ( sorted by price from highest to lowest )
damaged_items = [(item_id, details) for item_id,details in inventory.items() if details["damaged"]]
sorted_damaged = sorted(damaged_items, key=get_price, reverse=True)

with open("DamagedInventory.txt", "w") as file:
    for item_id, details in sorted_damaged:
        # format service date to string, defaulting to N/A if not available
        service_date_str = details["service_date"].strftime('%m/%d/%Y') if details["service_date"] else "N/A"
        # write item details for damaged items
        file.write(f"{item_id}, {details['manufacturer']}, {details['type']}, {details['price']}, {service_date_str}\n")

# print result message 
print("All inventory reports have been created successfully!")