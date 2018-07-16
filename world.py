_world = {}
starting_position =(0, 0)
def load_tiles():
    tile_map = [[FindGoldRoom(),GiantSpiderRoom(), None, None],[None, StartingRoom(),EmptyCave(),None]]
    for i in range (len(tile_map)):
        rows = random.shuffle(i)
    x_max = len(rows[0].split('\t'))
    for y in range(len(rows)):
        cols = rows[y].split('\t')
        for x in range(x_max):
            tile_name = cols[x].replace('\n', '')
            if tile_name == 'StartingRoom':
                global starting_position
                starting_position = (x, y)
            _world[(x, y)] = None if tile_name == '' else getattr(__import__('tiles'), tile_name)(x, y)
def tile_exists(x, y):
    return _world.get((x, y))