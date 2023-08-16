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
    # print("memo after:")         # COMMENT OUT!!!
    # print(memo)                  # COMMENT OUT!!!
    # print("Starting hp:", H)
    # print("temp:", temp)
    # print("Final hp:", res)     # COMMENT OUT!!!
    return res >= 0


def DP_helper(memo, n, H, tile_types, tile_values, x, y, pTok, mTok):  #hp as param is the problem, bc having hp there is like a dif fxn call, so just do the same thing but do min hp needed and remove hp from fxn call, cuz this is acutally the 5d memo O(Hn^2) solution but with a wrong memo. The reason why max doesnt make sense, is cuz u can hit negative on the way to the end, which is the opposite direction of maximizing. And once u hit negative u end. tho, actually should still work because for the minimizing solution we still check if ans < 0 and cap at 0. Wait actually, maximizing hp gain is basically same as min hp needed.
    #BCs -------------------------
    if x == n-1 and y == n-1:     #last tile value doesnt matter unless its damage
        if tile_types[x][y] == 0 and pTok != 1:       # damage tile and no prot token
            return -tile_values[x][y]
        return 0
    if x >= n or y >= n:    #out of bounds
        #print(-100000)
        return -100000
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
        pTok = 1         # pick up protection token
        #print("picked up prot token, count:", pTok, " at ", x, y)
    elif tile_types[x][y] == 3:
        mTok = 1         # pick up protection token
    #else:
        #maybe for token stuff, edit: nvm
    
    curval = tile_values[x][y] * type
    #print(curval)
    #BCs end ---------------------

    #print(x, y, pTok, memo[x][y][pTok])
    #print(x, y, type, tile_values[x][y])
    #print(tile_types[x][y])
    # if hp < 0:
    #     return -123 
    down = DP_helper(memo, n, H, tile_types, tile_values, x+1, y, pTok, mTok) + curval  # move down
    #print(x, y, "down")
    right = DP_helper(memo, n, H, tile_types, tile_values, x, y+1, pTok, mTok) + curval    # move right
    #print(x, y, "right")
    ans = max(down, right)
    if tile_types[x][y] == 0 and pTok == 1:
        down_token = DP_helper(memo, n, H, tile_types, tile_values, x+1, y, 0, mTok)  # use token + move down
        #print(x, y, "pdown")
        right_token = DP_helper(memo, n, H, tile_types, tile_values, x, y+1, 0, mTok)    # use token + move right
        #print(x, y, "pright")
        ans = max(down, right, down_token, right_token)
    if tile_types[x][y] == 1 and mTok == 1:
        down_token = DP_helper(memo, n, H, tile_types, tile_values, x+1, y, pTok, 0) + curval * 2   # use token + move down
        #print(x, y, "mdown", down_mtoken)
        right_token = DP_helper(memo, n, H, tile_types, tile_values, x, y+1, pTok, 0) + curval * 2    # use token + move right
        ans = max(down, right, down_token, right_token)
        #print(x, y, "mright", right_mtoken)
    if ans < -H:    #no reviving, penalize
        ans = -123454321
    memo[x][y][pTok][mTok] = ans
    return ans   #test that it works by spitting out the max path sum


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
