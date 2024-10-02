class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Item(metaclass=SingletonMeta):
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


        return f"{self._ownership} used {self.name} and {self.type} increase of {self.value} for {self.time}s."


if __name__ == "__main__":
    # Example weapon
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
    print(isinstance(attack_potion, Weapon))