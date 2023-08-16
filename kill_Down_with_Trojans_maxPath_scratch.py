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
    memo[:] = np.nan

    # print("\nmemo before:")      # COMMENT OUT!!!
    # print(memo)                  # COMMENT OUT!!!
    #temp = DP_helper(memo, n, H, tile_types, tile_values, 0, 0, 0, 0)
    #res = H + temp
    #res = temp
    res = DP_helper(memo, n, H, tile_types, tile_values, 0, 0, 0, 0)
    # print("memo after:")         # COMMENT OUT!!!
    # print(memo)                  # COMMENT OUT!!!
    # print("Starting hp:", H)
    # print("res:", res)
    # print("Final hp:", H + res)     # COMMENT OUT!!!
    return -res <= H     # return H + res >= 0


# figure out why this approach doesnt work. can i make it work? tho def seems harder to deal with dying halfway.
# tho i feel like it rly shoudlnt rly be much harder
# o also need to pass H as a constant (min case it was 0 so dont need to know H, but for max u need to set the bound)
# EDIT: still busted, only passes 77/100. fuck it just switch to other method until finish it cuz this is a worse approach from the get go
# O wait... is it case the recursion is summing up the values backwards? or is that how it works
# EDIT2: i think i figured it out. added max hp cap basically (deals with reviving), and then removed penalty for going negative, which will allow u to stock up HP
# so basically i was just thinking of it backwards, cuz the memo sums up backwards, so i SHOULD ALLOW negative hp, and then can add it back up to positive as you go from bottom right to top left in memo (backwards up the memo)
# Actaully i didnt even have a penalty, well yes i did, but i meant i didnt have 2 separate checks, basically the cap and no penalty are both the same check, just FLIP the if statement at the bottom.
# still not perfect but passes 90/100.
# Edit 3: 88/100, capped hp at H instead of 0
# Edit 4: 90/100, changed cap back to 0, cuz it helper doesnt need the starting hp
# Edit 5: 96/100, forgot to change threshold in if statement when changing cap
def DP_helper(memo, n, H, tile_types, tile_values, x, y, pTok, mTok):  #same as min hp needed approach but max hp gain instead
    if x == n-1 and y == n-1:
        if tile_types[x][y] == 0 and pTok != 1:
            # do u need to store in memo here? prob not right
            return -tile_values[x][y]     # oops forgot to flip sign to positive cuz switched approach from max to min
        return 0
    if x >= n or y >= n:
        return -100000000000000
    if not np.isnan(memo[x][y][pTok][mTok]):
        return memo[x][y][pTok][mTok]
    
    ans = -2
    if tile_types[x][y] == 0:
        if pTok == 1:
            tok_down = DP_helper(memo, n, H, tile_types, tile_values, x + 1, y, 0, mTok)
            tok_right = DP_helper(memo, n, H, tile_types, tile_values, x, y + 1, 0, mTok)
            down = DP_helper(memo, n, H, tile_types, tile_values, x + 1, y, 1, mTok) - tile_values[x][y]
            right = DP_helper(memo, n, H, tile_types, tile_values, x, y + 1, 1, mTok) - tile_values[x][y]
            ans = max(tok_down, tok_right, down, right)
        else:
            down = DP_helper(memo, n, H, tile_types, tile_values, x + 1, y, 0, mTok) - tile_values[x][y]
            right = DP_helper(memo, n, H, tile_types, tile_values, x, y + 1, 0, mTok) - tile_values[x][y]
            ans = max(down, right)
    if tile_types[x][y] == 1:
        if mTok == 1:
            tok_down = DP_helper(memo, n, H, tile_types, tile_values, x + 1, y, pTok, 0) + 2 * tile_values[x][y]
            tok_right = DP_helper(memo, n, H, tile_types, tile_values, x, y + 1, pTok, 0) + 2 * tile_values[x][y]
            down = DP_helper(memo, n, H, tile_types, tile_values, x + 1, y, pTok, 1) + tile_values[x][y]
            right = DP_helper(memo, n, H, tile_types, tile_values, x, y + 1, pTok, 1) + tile_values[x][y]
            ans = max(down, right)
        else:
            down = DP_helper(memo, n, H, tile_types, tile_values, x + 1, y, pTok, 0) + tile_values[x][y]
            right = DP_helper(memo, n, H, tile_types, tile_values, x, y + 1, pTok, 0) + tile_values[x][y]
            ans = max(down, right)
    if tile_types[x][y] == 2:
        down = DP_helper(memo, n, H, tile_types, tile_values, x + 1, y, 1, mTok)
        right = DP_helper(memo, n, H, tile_types, tile_values, x, y + 1, 1, mTok)
        ans = max(down, right)
    if tile_types[x][y] == 3:
        down = DP_helper(memo, n, H, tile_types, tile_values, x + 1, y, pTok, 1)
        right = DP_helper(memo, n, H, tile_types, tile_values, x, y + 1, pTok, 1)
        ans = max(down, right)
    # if ans < -H:   #this was the prob, forgot to change from 0 to -H     EDIT: NEED TO FLIP THIS bc of how memo adds up backwards
    #     ans = -191919191919
    # if ans > H:   #now its actually the opposite of the min HP needed approach (that had a lower bound, so this needs an upper bound... p obvious in hindsight, esp if everything else was opposite in sign... actually 3head)
    #     #ans = 0
    #     ans = H
    if ans > 0:   #now its actually the opposite of the min HP needed approach (that had a lower bound, so this needs an upper bound... p obvious in hindsight, esp if everything else was opposite in sign... actually 3head)
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
