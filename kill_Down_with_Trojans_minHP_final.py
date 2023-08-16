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
    memo = np.full((n, n, 2, 2), -1)            #just dont allow negative values

    # print("\nmemo before:")      # COMMENT OUT!!!
    # print(memo)                  # COMMENT OUT!!!
    #temp = DP_helper(memo, n, H, tile_types, tile_values, 0, 0, 0, 0)
    #res = H + temp
    #res = temp
    res = DP_helper(memo, n, tile_types, tile_values, 0, 0, 0, 0)
    # print("memo after:")         # COMMENT OUT!!!
    # print(memo)                  # COMMENT OUT!!!
    #print("Starting hp:", H)
    #print("temp:", temp)
    #print("Final hp:", res)     # COMMENT OUT!!!
    return res <= H


# currently passes 96/100 -_-
def DP_helper(memo, n, tile_types, tile_values, x, y, pTok, mTok):  #add tokens later
    if x == n-1 and y == n-1:
        if tile_types[x][y] == 0 and pTok != 1:
            return tile_values[x][y]     # oops forgot to flip sign to positive cuz switched approach from max to min
        return 0
    if x >= n or y >= n:
        return 100000000000000
    if memo[x][y][pTok][mTok] != -1:
        return memo[x][y][pTok][mTok]
    
    ans = -2
    if tile_types[x][y] == 0:
        if pTok == 1:
            tok_down = DP_helper(memo, n, tile_types, tile_values, x + 1, y, 0, mTok)
            tok_right = DP_helper(memo, n, tile_types, tile_values, x, y + 1, 0, mTok)
            down = DP_helper(memo, n, tile_types, tile_values, x + 1, y, 1, mTok) + tile_values[x][y]
            right = DP_helper(memo, n, tile_types, tile_values, x, y + 1, 1, mTok) + tile_values[x][y]
            ans = min(tok_down, tok_right, down, right)
        else:
            down = DP_helper(memo, n, tile_types, tile_values, x + 1, y, 0, mTok) + tile_values[x][y]
            right = DP_helper(memo, n, tile_types, tile_values, x, y + 1, 0, mTok) + tile_values[x][y]
            ans = min(down, right)
    if tile_types[x][y] == 1:
        if mTok == 1:
            tok_down = DP_helper(memo, n, tile_types, tile_values, x + 1, y, pTok, 0) - 2 * tile_values[x][y]
            tok_right = DP_helper(memo, n, tile_types, tile_values, x, y + 1, pTok, 0) - 2 * tile_values[x][y]
            down = DP_helper(memo, n, tile_types, tile_values, x + 1, y, pTok, 1) - tile_values[x][y]
            right = DP_helper(memo, n, tile_types, tile_values, x, y + 1, pTok, 1) - tile_values[x][y]
            ans = min(down, right)
        else:
            down = DP_helper(memo, n, tile_types, tile_values, x + 1, y, pTok, 0) - tile_values[x][y]
            right = DP_helper(memo, n, tile_types, tile_values, x, y + 1, pTok, 0) - tile_values[x][y]
            ans = min(down, right)
    if tile_types[x][y] == 2:
        down = DP_helper(memo, n, tile_types, tile_values, x + 1, y, 1, mTok)
        right = DP_helper(memo, n, tile_types, tile_values, x, y + 1, 1, mTok)
        ans = min(down, right)
    if tile_types[x][y] == 3:
        down = DP_helper(memo, n, tile_types, tile_values, x + 1, y, pTok, 1)
        right = DP_helper(memo, n, tile_types, tile_values, x, y + 1, pTok, 1)
        ans = min(down, right)
    if ans < 0:
        ans = 0
    memo[x][y][pTok][mTok] = ans     #are these the right values for ptok and mtok in memo
    return ans

def write_output_file(output_file_name, result):
    with open(output_file_name, 'w') as file:
        file.write(str(int(result)))


def main(input_file_name):
    n, H, tile_types, tile_values = load_input_file(input_file_name)
    #print_tile_data(tile_types, tile_values)
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
