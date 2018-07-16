import random, world
class Item():
    def __init__(self, name, description, value):
       self.name = name
       self.description = description
       self.value = value
    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.description, self.value)
class Gold(Item):
    def __init__(self, amt):
        self.amt = amt
        super().__init__(name="Gold",
                         description="A round coin with {} stamped on the front.".format(str(self.amt)),
                         value=self.amt)
class Weapon(Item):
    def __init__(self, name, description, value, damage):
        self.damage = damage
        super().__init__(name, description, value)

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage: {}".format(self.name, self.description, self.value, self.damage)

class Rock(Weapon):
    def __init__(self):
        super().__init__(name="Rock",
                         description="a rock used to throw at enemies.",
                         value=0, damage=5)
class Dagger(Weapon):
    def __init__(self):
        super().__init__(name="Dagger",
                         description="a small dagger with rust. Slightly more damaging than rock.",
                         value=10, damage=10)
class Enemy:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage
    def is_alive(self):
        return self.hp > 0
class GiantSpider(Enemy):
    def __init__(self):
        super().__init__(name="Giant Spider", hp=10, damage=2)
class Ogre(Enemy):
    def __init__(self):
        super().__init__(name="Ogre", hp=30, damage=15)
class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def intro_text(self):
        raise NotImplementedError()
    def modify_player(self, player):
        raise NotImplementedError()
    def adjacent_moves(self):
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x-1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves
    def available_actions(self):
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        return moves
class StartingRoom(MapTile):
    def intro_text(self):
        return """
        You find yourself in a cave with a flickering torch on the wall.
        You can make out four paths, each equally as dark and foreboding.
        """
    def modify_player(self, player):
        pass
class LootRoom(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)
    def add_loot(self, player):
        player.inventory.append(self.item)
    def modify_player(self, player):
        self.add_loot(player)
class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            return [action.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()
class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """
    def modify_player(self, player):
        pass
class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
         You see sunlight and have obtained victory!
        """
    def modify_player(self, player):
        player.victory = True
class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())
    def intro_text(self):
        if self.enemy.is_alive():
            return """ 
            A giant spider appears! Prepare for battle!
            """
        else:
            return """
            The spider has died.
            """
class OgreRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Ogre())
    def intro_text(self):
        if self.enemy.is_alive():
            return """
            An Ogre appears! Prepare for battle!
            """
        else:
            return """
            The ogre has died.
            """

class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger)
    def intro_text(self):
        return """
        You picked up a dagger!
        """
class FindGoldRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Gold(random.randint(0, 1000)))
    def intro_text(self):
        return """
        You found gold!
        """



class Player():
    def __init__(self):
        self.inventory = [items.Gold(15), items.Rock()]
        self.hp = 100
        self.location_x, self.location_y = world.starting_position
        self.victory = False
    def is_alive(self):
        return self.hp > 0
    def print_inventory(self):
        for item in self.inventory:
            print(item, '\n')
    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).intro_text())
    def move_north(self):
        self.move(dx=0, dy=-1)
    def move_south(self):
        self.move(dx=0, dy=1)
    def move_east(self):
        self.move(dx=1, dy=0)
    def move_west(self):
        self.move(dx=-1, dy=0)
    def attack(self, enemy):
        best_weapon = None
        max_dmg = 0
        for i in self.inventory:
            if isinstance(i, items.Weapon):
                if i.damage > max_dmg:
                    max_dmg = i.damage
                    best_weapon = i
        print("You use {} against {}".format(best_weapon.name, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print("You killed {}!".format(enemy.name))
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))
    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)
    def flee(self, tile):
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[r])


class Action():
    def __init__(self, method, name, hotkey, **kwargs):
        self.method = method
        self.hotkey = hotkey
        self.name = name
        self.kwargs = kwargs
    def __str__(self):
        return "{}: {}".format(self.hotkey, self.name)
class MoveNorth(Action):
    def __init__(self):
        super().__init__(method=Player.move_north, name='Move north', hotkey='n')
class MoveSouth(Action):
    def __init__(self):
        super().__init__(method=Player.move_south, name='Move south', hotkey='s')
class MoveEast(Action):
    def __init__(self):
        super().__init__(method=Player.move_east, name='Move east', hotkey='e')
class MoveWest(Action):
    def __init__(self):
        super().__init__(method=Player.move_west, name='Move west', hotkey='w')
class ViewInventory(Action):
    def __init__(self):
        super().__init__(method=Player.print_inventory, name='View inventory', hotkey='i')
class Attack(Action):
    def __init__(self, enemy):
        super().__init__(method=Player.attack, name="Attack", hotkey='a', enemy=enemy)
class Flee(Action):
    def __init__(self, tile):
        super().__init__(method=Player.flee, name="Flee", hotkey='f', tile=tile)

    def play(self):
        world.load_tiles()
        player = Player()
        while player.is_alive() and not player.victory:
            room = world.tile_exists(player.location_x, player.location_y)
            room.modify_player(player)
            if player.is_alive() and not player.victory:
                print("Choose an action: \n")
                available_actions = room.available_actions()
                for action in available_actions:
                    print(action)
                action_input = input('Action: ')
                for action in available_actions:
                    if action_input == action.hotkey:
                        player.do_action(action, **action.kwargs)
if __name__ == "__main__":
    play()
