import json

class Item:
    def __init__(self, name, description='', rarity='common', ownership=''):
        self.name = name
        self.description = description
        self.rarity = rarity
        self._ownership = ownership

    def pick_up(self, character: str) -> str:
        self._ownership = character
        return f"{self.name} is now owned by {self._ownership}."

    def throw_away(self) -> str:
        self._ownership = None
        return f"{self.name} is thrown away."

    def use(self):
        return f"{self.name} is used."

    def __str__(self):
        if self.rarity == 'legendary':
            return f"🔥🔥🔥*** LEGENDARY ITEM *** 🔥🔥🔥 | Name: {self.name} | Rarity: {self.rarity} | Description: {self.description}"

        else:
            return f"{self.name}: {self.description} (Rarity: {self.rarity})"

    def to_json(self):
        """Convert the item to a dictionary for JSON serialization."""
        return {
            'class': self.__class__.__name__,
            'name': self.name,
            'description': self.description,
            'rarity': self.rarity,
            'ownership': self._ownership
        }

    @classmethod
    def from_json(cls, data):
        """data is the serialized information of an item (or one of its subclasses)
        The instance of the class is returned with the information in data used."""
        """Create an Item (or subclass) instance from JSON data."""
        return cls(**data)


class Weapon(Item):
    def __init__(self, name, damage, type, description='', rarity='common', ownership=''):
        super().__init__(name, description, rarity, ownership)
        self.damage = damage
        self.type = type
        self._used = False
        self._equipped = False

    def use(self) -> str:

        if self._ownership == '':
            return ''  # No output if there is no ownership
        if not self._equipped:  # Check if the weapon is equipped
            return f"{self.name} needs to be equipped before use."
        if self._used:
            return ''
        self._used = True

        if self.rarity == 'legendary':
            att_mult = 1.15
        else:
            att_mult = 1.0

        return f"{self.name} is used, dealing {self.damage * att_mult} damage."

    def _slash(self) -> str:
        return f"{self.name} performs a slashing attack."

    def _spin(self):
        return f"{self.name} spins its enemy out of control."

    def _thrust(self):
        return f"{self.name} thrusts its enemy out of the way."

    def _shoot(self):
        return f"{self.name} shoots its bow."


    def attack_move(self):
        if self.type in ('sword', 'single-handed'):
            return self._slash()
        elif self.type in ('katana', 'double-handed'):
            return self._spin()
        elif self.type in ('spear', 'pike'):
            return self._thrust()
        elif self.type in ('bow', 'ranged-weapon'):
            return self._shoot()

    def equip(self) -> str:
        if self._ownership == '':
            return ''
        self._equipped = True
        return f"{self.name} is equipped by {self._ownership}."

    def to_json(self):
        data = super().to_json()
        data.update({'damage': self.damage, 'type': self.type})
        return data

    @classmethod
    def from_json(cls, data):
        """data is the serialized information of an item (or one of its subclasses).
        The instance of the class is returned with the information in data used."""
        """Create a Weapon instance from JSON data."""
        return cls(**data)

class Shield(Item):
    def __init__(self, name, defense, broken, description='', rarity='common', ownership=''):
        super().__init__(name, description, rarity, ownership)
        self.defense = defense
        self.broken = broken
        self._used = False
        self._equipped = False

    def use(self) -> str:
        if self._ownership == '':
            return ''  # No output if there is no ownership
        if not self._equipped:  # Check if the weapon is equipped
            return f"{self.name} needs to be equipped before use."
        if self._used:
            return ''
        self._used = True

        def_mult = float
        if self.broken == True:
            def_mult = 0.5
        elif self.broken == False:
            if self.rarity == 'legendary':
                def_mult = 1.10
            else:
                def_mult = 1.0
        return f"{self.name} is used, blocking {self.defense * def_mult} damage."

    def equip(self) -> str:
        if self._ownership == '':
            return ''
        self._equipped = True
        return f"{self.name} is equipped by {self._ownership}."

    def to_json(self):
        data = super().to_json()
        data.update({'defense': self.defense, 'broken': self.broken})
        return data

    @classmethod
    def from_json(cls, data):
        """data is the serialized information of an item (or one of its subclasses).
        The instance of the class is returned with the information in data used."""
        """Create a Shield instance from JSON data."""
        return cls(**data)


class Potion(Item):
    def __init__(self, name, type, description='', rarity='common', ownership=''):
        super().__init__(name, description, rarity, ownership)
        self.type = type
        self._used = False
        self.value = int
        self.time = int
        self.hp_time = str

    def use(self) -> str:
        if self._ownership == '':
            return ''  # No output if there is no ownership
        if self._used:
            return "This potion has already been consumed."
        self._used = True

        if self.rarity.lower() == 'common':
            self.value = 50
            if self.type.lower() == 'hp':
                self.hp_time = 'use and done'
            elif self.type.lower() in ('attack', 'defense'):
                self.time = 30

        if self.type == 'hp':
            return f"{self._ownership} used {self.name}."
        else:
            return f"{self._ownership} used {self.name} and {self.type} increase of {self.value} for {self.time}s."

    def to_json(self):
        data = super().to_json()
        data.update({'type': self.type})
        return data

    @classmethod
    def from_json(cls, data):
        """data is the serialized information of an item (or one of its subclasses).
        The instance of the class is returned with the information in data used."""
        """Create a Potion instance from JSON data."""
        return cls(**data)
class Inventory:
    def __init__(self, owner=None):
        self.owner = owner
        self.backpack = []

    def add_item(self, item):
        if item._ownership:  # If the item is owned, remove from previous owner
            item._ownership = None
        item._ownership = self.owner  # Change the ownership to the current owner
        self.backpack.append(item)
        return f"{item.name} added to {self.owner}'s backpack."

    def drop_item(self, item):
        if item in self.backpack:
            self.backpack.remove(item)
            item._ownership = None  # Remove ownership when the item is removed
            return f"{item.name} removed from {self.owner}'s backpack."
        else:
            return f"{item.name} not found in {self.owner}'s backpack."

    def view(self, type=None, item=None):
        """View either the entire collection, a specific item, or items by type"""
        if item:  # View individual item
            if item in self.backpack:
                return str(item)
            else:
                return f"{item.name} is not in the backpack."
        elif type:  # View collection of items based on type (weapon, shield, etc.)
            type_map = {
                'weapon': Weapon,
                'shield': Shield,
                'potion': Potion
            }
            item_type = type_map.get(type)
            if type in type_map:
                return [str(i) for i in self.backpack if isinstance(i, item_type)]
            else:
                return f"No items of type {type} found."
        else:  # View all items
            return [str(i) for i in self.backpack]


    def __iter__(self):
        """Make Inventory class iterable"""
        self._index = 0
        return self


    def __next__(self):
        if self._index < len(self.backpack):
            item = self.backpack[self._index]
            self._index += 1
            return item
        else:
            raise StopIteration


    def __contains__(self, item):
        """Support 'in' operator to check if item is in inventory"""
        return item in self.backpack


    def to_json(self):
        """Convert the inventory and all its items to a JSON-serializable object."""
        return {
            'owner': self.owner,
            'backpack': [item.to_json() for item in self.backpack]
        }

    @classmethod
    def from_json(cls, data):
        """data is the serialized information of an item (or one of its subclasses).
        The inventory is returned in its deserialized form."""

        """Create an Inventory instance from JSON data."""
        inventory = cls(owner=data['owner'])
        for item_data in data['backpack']:
            item_class = globals()[item_data.pop('class')]
            item = item_class.from_json(item_data)
            inventory.add_item(item)
        return inventory

# Function to serialize custom objects with json.dump
def custom_serializer(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable.")


if __name__ == "__main__":
    # Define various items
    belthronding = Weapon(name='Belthronding', rarity='legendary', damage=500, type='bow')
    hp_potion = Potion(name='Health Potion', type='hp', rarity='common')
    master_sword = Weapon(name='Master Sword', rarity='legendary', damage=300, type='sword')
    broken_pot_lid = Shield(name='Wooden Lid', description='A lid made of wood, useful in cooking.', defense=5,
                            broken=True)
    muramasa = Weapon(name='Muramasa', rarity='legendary', damage=580, type='katana')
    gungnir = Weapon(name='Gungnir', rarity='legendary', damage=290, type='spear')
    round_shield = Shield(name='Round Shield', defense=15, broken=False)

    # Create an inventory for Beleg
    beleg_backpack = Inventory(owner='Beleg')

    # Add items to Beleg's backpack
    print(beleg_backpack.add_item(belthronding))
    print(beleg_backpack.add_item(hp_potion))
    print(beleg_backpack.add_item(master_sword))
    print(beleg_backpack.add_item(broken_pot_lid))
    print(beleg_backpack.add_item(muramasa))
    print(beleg_backpack.add_item(gungnir))
    print(beleg_backpack.add_item(round_shield))
    print()

    #For Lab 06:
    # Serialize the inventory to JSON
    json_data = json.dumps(beleg_backpack, default=custom_serializer, indent=4)
    print("Serialized Inventory:")
    print(json_data)

    # Deserialize the JSON back to an Inventory object
    deserialized_data = json.loads(json_data)
    restored_inventory = Inventory.from_json(deserialized_data)

    # Verify restored inventory
    print("\nDeserialized Inventory:")
    print(restored_inventory.to_json())