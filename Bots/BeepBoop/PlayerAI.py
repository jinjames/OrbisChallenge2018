from PythonClientAPI.game.PointUtils import *
from PythonClientAPI.game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.game.Enums import Team
from PythonClientAPI.game.World import World
from PythonClientAPI.game.TileUtils import TileUtils

class PlayerAI:

    def __init__(self):
        ''' Initialize! '''
        self.turn_count = 0             # game turn count
        self.target = None              # target to send unit to!
        self.outbound = True            # is the unit leaving, or returning?

    def do_move(self, world, friendly_unit, enemy_units):
        '''
        This method is called every turn by the game engine.
        Make sure you call friendly_unit.move(target) somewhere here!

        Below, you'll find a very rudimentary strategy to get you started.
        Feel free to use, or delete any part of the provided code - Good luck!

        :param world: world object (more information on the documentation)
            - world: contains information about the game map.
            - world.path: contains various pathfinding helper methods.
            - world.util: contains various tile-finding helper methods.
            - world.fill: contains various flood-filling helper methods.

        :param friendly_unit: FriendlyUnit object
        :param enemy_units: list of EnemyUnit objects
        '''

        # increment turn count
        self.turn_count += 1

        # calculate where target is
        # maintain movement to target unless there is threat


        # distance to friendly area
        friendly_return = world.util.get_closest_friendly_territory_from(friendly_unit.position, friendly_unit.snake)
        return_distance = len(world.path.get_shortest_path(friendly_unit.position, friendly_return, friendly_unit.snake))

        # find path to target

        # if unit reaches the target point, reverse outbound boolean and set target back to None
        if self.target is not None and friendly_unit.position == self.target.position:
            self.outbound = not self.outbound
            self.target = None

        # if outbound and no target set, set target as the closest capturable tile at least 1 tile away from your territory's edge.
        if self.outbound and self.target is None:
            edges = [tile for tile in world.util.get_friendly_territory_edges()]
            avoid = []
            for edge in edges:
                avoid += [pos for pos in world.get_neighbours(edge.position).values()]
            self.target = world.util.get_closest_capturable_territory_from(friendly_unit.position, avoid)

        # set next move as the next point in the path to target
        next_move = world.path.get_shortest_path(friendly_unit.position, self.target.position, friendly_unit.snake)[0]

        # move!
        friendly_unit.move(next_move)
        print("Turn {0}: currently at {1}, making {2} move to {3}.".format(
            str(self.turn_count),
            str(friendly_unit.position),
            'outbound' if self.outbound else 'inbound',
            str(self.target.position)
        ))

def distance_closest_enemy(world,friendly_unit, enemy_units):
    closest_distance = max(world.get_height(), world.get_width())
    # closest enemy position
    # distance to any part of snake
    for enemy in enemy_units:
        for body in friendly_unit.snake:
            distance = len(world.path.get_shortest_path(body, enemy.postition, enemy.snake))
            if distance < closest_distance:
                closest_distance = distance
    return closest_distance