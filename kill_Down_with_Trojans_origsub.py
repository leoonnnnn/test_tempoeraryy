import numpy as np
import scipy


def load_input_file(file_name):
    with open(file_name, 'r') as file:
        n, H = map(int, file.readline().split())
        tile_types = np.zeros((n, n), dtype=int)
        tile_values = np.zeros((n, n), dtype=int)

        for i in range(n * n):
            if i == 0:
                continue  # the initial tile is zero type with zero value
            x, y, t, v = map(int, file.readline().split())
            tile_types[x][y] = t
            tile_values[x][y] = v

    return n, H, tile_types, tile_values


def print_tile_data(tile_types, tile_values):
    print("Tile Types:")
    print(tile_types)
    print("\nTile Values:")
    print(tile_values)


def DP(n, H, tile_types, tile_values):
    memo = np.empty((n, n, 2, 2))
    memo[:] = np.nan                 # use np.nan as the null value

    #print("\nmemo before:")      # COMMENT OUT!!!
    #print(memo)                  # COMMENT OUT!!!
    temp = DP_helper(memo, n, H, tile_types, tile_values, 0, 0, 0, 0)
    res = H + temp
    #print("memo after:")         # COMMENT OUT!!!
    #print(memo)                  # COMMENT OUT!!!
    print("Starting hp:", H)
    print("temp:", temp)
    print("Final hp:", res)     # COMMENT OUT!!!
    return res >= 0


def DP_helper(memo, n, hp, tile_types, tile_values, x, y, pTok, mTok):  #add tokens later
    #BCs -------------------------
    if x >= n or y >= n:    #out of bounds
        return -100000
    if hp < 0:
        return -123    # not allowed to revive, so penalize reviving    #change to -123 for debugging with memo
    if not np.isnan(memo[x][y][pTok][mTok]):
        return memo[x][y][pTok][mTok]

    type = 0
    if tile_types[x][y] == 0:
        type = -1        #take damage
        #print(x, y, "damage")
    elif tile_types[x][y] == 1:
        type = 1         #heal
        #print(x, y, "heal")
    elif tile_types[x][y] == 2:
        pTemp = pTok
        pTok = 1         # pick up protection token
        print(pTemp, pTok)
        #print("picked up prot token, count:", pTok, " at ", x, y)
    elif tile_types[x][y] == 3:
        mTok = 1         # pick up protection token
    #else:
        #maybe for token stuff, edit: nvm
    
    curval = tile_values[x][y] * type
    print(curval)

    if x == n-1 and y == n-1:
        #print(hp, curval, 1 - pTok, x, y)
        return curval * (1 - pTok)   # reached bottom right
    #BCs end ---------------------

    #print(x, y, pTok, memo[x][y][pTok])
    #print(x, y, type, tile_values[x][y])
    #print(tile_types[x][y])
    # if hp < 0:
    #     return -123 
    down = DP_helper(memo, n, hp + curval, tile_types, tile_values, x+1, y, pTok, mTok) + curval  # move down
    #print("down", x, y)
    right = DP_helper(memo, n, hp + curval, tile_types, tile_values, x, y+1, pTok, mTok) + curval    # move right
    #print("right", x, y)
    down_ptoken = -12345
    right_ptoken = -12345
    if tile_types[x][y] == 0 and pTok == 1:
        down_ptoken = DP_helper(memo, n, hp, tile_types, tile_values, x+1, y, 0, mTok)  # move down + use token
        #print("pdown", x, y)
        right_ptoken = DP_helper(memo, n, hp, tile_types, tile_values, x, y+1, 0, mTok)    # move right + use token
        #print("pright", x, y)
    down_mtoken = -12345
    right_mtoken = -12345
    if tile_types[x][y] == 0 and pTok == 1:
        down_mtoken = DP_helper(memo, n, hp, tile_types, tile_values, x+1, y, pTok, 0) + curval * mTok   # move down + use token
        #print("pdown", x, y)
        right_mtoken = DP_helper(memo, n, hp, tile_types, tile_values, x, y+1, pTok, 0) + curval * mTok    # move right + use token
        #print("pright", x, y)
    memo[x][y][pTok][mTok] = max(down, right, down_ptoken, right_ptoken,  down_mtoken, right_mtoken)    #should it be pTok or use_pTok (like this or inverse, think about it with some simple examples)
    return max(down, right, down_ptoken, right_ptoken,  down_mtoken, right_mtoken)   #test that it works by spitting out the max path sum


def write_output_file(output_file_name, result):
    with open(output_file_name, 'w') as file:
        file.write(str(int(result)))


def main(input_file_name):
    n, H, tile_types, tile_values = load_input_file(input_file_name)
    print_tile_data(tile_types, tile_values)
    result = DP(n, H, tile_types, tile_values)
    print("Result: " + str(result))
    output_file_name = input_file_name.replace(".txt", "_out.txt")
    write_output_file(output_file_name, result)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python kill_Down_with_Trojans.py a_file_name.txt")
    else:
        main(sys.argv[1])
