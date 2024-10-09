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



if __name__ == "__main__":

    #From Lab04:
    """# Example weapon
    belthronding = Weapon(name='Belthronding', rarity='legendary', damage=5000, type='bow')
    print(belthronding.pick_up('Beleg'))
    print(belthronding.equip())
    print(belthronding.use())
    print(belthronding.use())
    #print()

    # Example shield
    broken_pot_lid = Shield(name='Wooden Lid', description='A lid made of wood, useful in cooking. No one will choose it willingly for a shield.', defense=5, broken=True)
    print(broken_pot_lid.pick_up("Beleg"))
    print(broken_pot_lid.equip())
    print(broken_pot_lid.use())
    print(broken_pot_lid.throw_away())
    print(broken_pot_lid.use())
    #print()

    #Example potion
    attack_potion = Potion(name='atk potion temp', ownership=
    'Beleg', type='attack')
    print(attack_potion.use())
    print(attack_potion.use())
    #print()


    print(isinstance(belthronding, Item))
    print(isinstance(broken_pot_lid, Shield))
    print(isinstance(attack_potion, Weapon))"""




    #For Lab05:

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


    # View all the shields in Beleg's backpack
    print("Here are all of the shields in Beleg's backpack: ")
    print(beleg_backpack.view(type='shield'))
    print()

    #View all of the items in Beleg's backpack
    print("Here are all of the items in Beleg's backpack: ")
    print(beleg_backpack.view())
    print()

    # Drop an item
    print("Now removing an item: ")
    print(beleg_backpack.drop_item(broken_pot_lid))
    print()


    # Equip master sword if it is in the backpack
    if master_sword in beleg_backpack:
        print(master_sword.equip())

        # Show off master sword (legendary item)
        print(master_sword)

        # Beleg uses master sword
        print(master_sword.use())
    print()

    # Iterate through backpack and view weapons
    for item in beleg_backpack:
        if isinstance(item, Weapon):
            print(beleg_backpack.view(item=item))
    print()

    """The following is extra outputs:"""
    """
    # View shields in the backpack
    print("Viewing shields:")
    shields = beleg_backpack.view(type='shield')
    for shield in shields:
        print(shield)
    print()

    print("Viewing belthronding:")
    bel = beleg_backpack.view(item=belthronding)
    print(bel)
    print()

    # View all items in the backpack
    print("Viewing all items:")
    all_items = beleg_backpack.view()
    for item in all_items:
        print(item)
    print()

    if hp_potion in beleg_backpack:
        print(hp_potion.use())

    print(gungnir.equip())
    print(gungnir.attack_move())"""