from room import Room
from player import Player
from world import World
from util import Stack, Queue
import random
from ast import literal_eval
# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"
# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)
# Print an ASCII map
world.print_rooms()
player = Player(world.starting_room)
# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
explored_rooms = {}
opposite_direction = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
# Initialize room directions
def initialize_room_direction(room):
    explored_rooms[room.id] = {}
    for direction in room.get_exits():
        explored_rooms[room.id][direction] = "?"

# Get the unvisted directions of room 
def get_unvisited_directions(directions):
    unvisited_directions = []
    for direction in directions:
        if directions[direction] == "?":
            unvisited_directions.append(direction)
    return unvisited_directions

# Get the closest room with unvisited path.
def breadth_first_search():
    queue = Queue()
    queue.enqueue([player.current_room.id])
    visited_rooms = set()
    while queue.size() > 0:
        current_path = queue.dequeue()
        current_room = current_path[-1]
        if current_room not in visited_rooms:
            visited_rooms.add(current_room)
            # find the unvisited path and return it.
            for direction in explored_rooms[current_room]:
                if explored_rooms[current_room][direction] == '?':
                    return current_path
                elif explored_rooms[current_room][direction] not in visited_rooms:
                    queue.enqueue(current_path + [explored_rooms[current_room][direction]])
    return current_path

while len(explored_rooms) < len(room_graph):
    current_room = player.current_room
    # If current room is not visited then initialize its directions.
    if current_room.id not in explored_rooms:
        initialize_room_direction(current_room)
    # Get all unvisited directions of the rooom.
    directions = get_unvisited_directions(explored_rooms[current_room.id])
    # If there are no unvisited directions in the current room.
    if len(directions) == 0:
        # Use the BFS to find the closest room with unvisited path.
        rooms = breadth_first_search()
        for room in rooms:
            for direction in explored_rooms[current_room.id]:
                if explored_rooms[current_room.id][direction] == room and current_room.id != room:
                    # Add direction in traversal path.
                    traversal_path.append(direction)
                    # Get next room.
                    next_room = current_room.get_room_in_direction(direction)
                    # Update current room direction with next room id.
                    explored_rooms[current_room.id][direction] = next_room.id
                    # Check the next room is already explored or not.
                    if next_room.id not in explored_rooms:
                        initialize_room_direction(next_room)
                    # Update next room direction with the room id the player came from.
                    explored_rooms[next_room.id][opposite_direction[direction]] = current_room.id
                    # Move Player to the given direction.(next room)
                    player.travel(direction)
    else:
        # choose a random direction
        new_route = random.choice(directions)
        # Add direction in traversal path.
        traversal_path.append(new_route)
        # Get next room.
        next_room = current_room.get_room_in_direction(new_route)
        # Update current room direction with next room id.
        explored_rooms[current_room.id][new_route] = next_room.id
        # Check the next room is already explored or not.
        if next_room.id not in explored_rooms:
            initialize_room_direction(next_room)
        # Update next room direction with the room id the player came from.
        explored_rooms[next_room.id][opposite_direction[new_route]] = current_room.id
         # Move Player to the given direction.(next room)
        player.travel(new_route)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)
if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

# hints:
# use DFT then if stuck use BFS - using returned path for BFS to move player not during BFS