import datetime

class InventoryItem:
    """A simple class to hold information about one inventory item"""
    def __init__(self, item_id, manufacturer, item_type, price, service_date, damaged):
        self.id = item_id
        self.manufacturer = manufacturer.lower()                # store in lowercase() to compare easily
        self.type = item_type.lower()   
        self.price = float(price)
        self.service_date = service_date
        self.damaged = damaged.lower()                          # store as 'yes' or 'no' 

    def is_available(self):
        """ see if item is not damaged and not past service date """  
        # get todays date
        today = datetime.datetime.now().date()

        # convert service date string to date object
        year, month, day = map(int, self.service_date.split('-'))
        service_date = datetime.date(year, month, day)

        # check conditions
        return self.damaged == 'no' and service_date >= today

    def display(self):
        """ Return a nicely formatted string of the item info """ 
        return f"{self.id} {self.manufacturer.capitalize()} {self.price}" 

def load_inventory():
    """ Load all inventory data from files """   
    items = []

    # read manufacturer data
    with open('ManufacturerList.txt') as f:
        for line in f:
            parts = line.strip().split(',') 
            item_id = parts[0].strip() 
            manufacturer = parts[1].strip()
            item_type = parts[2].strip()
            damaged = parts[3].strip() if len(parts) > 3 else 'no'

            item = {
                'id': item_id,
                'manufacturer': manufacturer,
                'type': item_type,
                'damaged': damaged
            }
            # add to list
            items.append(item)

    with open('PriceList.txt') as f:
        for line in f:
            parts = line.strip().split(',')
            item_id = parts[0].strip()
            price = parts[1].strip()

            for item in items:
                if item['id'] == item_id:
                    item['price'] = price
                    break

    inventory = []
    for item in items:
        inventory_item = InventoryItem(
            item['id'],
            item['manufacturer'],
            item['type'],
            item['price'],
            item['service_date'],
            item['damaged']
        )
        inventory.append(inventory_item)

    return inventory

def process_query(query, inventory):
    """ handle a user query and print results """
    query = query.lower()                           # clear query
    
    manufacturers = set()
    item_types = set()
    for item in inventory:
        manufacturers.add(item.manufacturer)
        item_types.add(item.type)

    # find which manufacturer and item type are in query
    found_manufacturer = None
    found_type = None

    for word in query.split():
        if word in manufacturers:
            if found_manufacturer is not None:
                print("No such item in inventory")              # more than one manufacturer
                return
            found_manufacturer = word

        if word in item_types:
            if found_type is not None:
                print("No such item in inventory")             # more than one type
                return
            found_type = word

    if not found_manufacturer or not found_type:
        print("No such itme in inventory")
        return
    
    # find matching available items
    matches = []
    for item in inventory:
        if (item.manufacturer == found_manufacturer and
            item.type == found_type and
            item.is_available()):
            matches.append(item)

    if not matches:
        print("No such item in inventory")
        return
    
    # find the most expensive match
    best_item = max(matches, key =lambda x: x.price)
    print(f"Your item is: {best_item.display()}")

    # look for alternatives 
    alternatives = []
    for item in inventory:
        if (item.type == found_type and
            item.manufacturer != found_manufacturer and
            item.is_available()):
            alternatives.append(item)

    if alternatives:
        # find alternative with closest price
        closest = min(alternatives,  key=lambda x: abs(x.price - best_item.price))
        print(f"You may, also, consider: {closest.display()}")

def main():
    """ Main program function """
    print("Inventory Query System")
    print("Enter your query like 'Apple phone' or 'Dell laptop'")
    print("Enterd 'q' to quit\n")

    inventory = load_inventory()

    while True:
        query = input("Query: ").strip()

        if query.lower() == 'q':
            print("Goodbye!")
            break

        process_query(query, inventory)

if __name__ == "__main__":
    main()

# need to solve and debug some small minor issues
    