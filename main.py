import traceback


def main():
    # ここから、入力
    # --------------

    prompt = f"""横幅、縦幅のあとに図形を続けてください。
例：
7 5
..xxx..
xxxxx..
xxxxxxx
..xxxxx
...xxxx
"""
    lines = input(prompt)
    width, height = map(int, lines.split(' '))

    board = []

    for row_number in range(0, height):
        lines = input()
        board.extend(lines)

    # print_board(
    #         width=width,
    #         height=height,
    #         board=board)

    # ここまで、入力
    # --------------


    # 以下、解法
    # ----------

    # 縦と横のどちらが短いか？
    WIDTH_IS_SHORTER = 1
    HEIGHT_IS_SHORTER = 2
    if height < width:
        short_side = HEIGHT_IS_SHORTER
    else:
        short_side = WIDTH_IS_SHORTER


    if short_side == WIDTH_IS_SHORTER:
        # 横の方が短いときは、反時計回りに９０°回転させる
        old_width = width               # 退避
        old_height = height
        old_board = board
        new_width = old_height              # ９０°回転
        new_height = old_width
        new_board = list(old_board)     # シャローコピー
        for old_y in range(0, old_height):
            for old_x in range(0, old_width):
                new_x = old_y
                new_y = (width-1-old_x)
                new_board[new_y * new_width + new_x] = old_board[old_y * old_width + old_x]

        width = new_width
        height = new_height
        board = new_board


    # print_board(
    #         width=width,
    #         height=height,
    #         board=board)


    # 右から左へ連続するものを連（れん）と呼ぶことにする。
    EMPTY = 0
    ren_id = 1
    is_stone_ren = False
    for y in range(0, height):
        for x in range(0, width):
            index = y * width + x

            stone = board[index]
            if stone == 'x':
                if not is_stone_ren:
                    is_stone_ren = True
                board[index] = ren_id
            else:
                if is_stone_ren:
                    ren_id += 1
                    is_stone_ren = False
                board[index] = EMPTY
        
        if is_stone_ren:
            ren_id += 1
            is_stone_ren = False


    end_ren_id = ren_id

    # print_board(
    #         width=width,
    #         height=height,
    #         board=board)


    # 盤面スキャン
    ren_id = EMPTY
    for y1 in range(0, height):
        for x1 in range(0, width):
            index1 = y1 * width + x1

            # 連Idが変わった。新しい連Idの始まり
            if ren_id != board[index1] and board[index1] != EMPTY:
                ren_id = board[index1]

                # 連を下に伸ばせるか判定します

                y2 = y1 + 1
                if y2 < height:
                    can_extend = True
                    x3 = x1 + 1
                    while x3 < width:
                        if board[y1 * width + x3] != ren_id:
                            # 連の幅に達した
                            break

                        if board[y2 * width + x1] == EMPTY:
                            can_extend = False    # 空地には伸ばせない
                            break

                        if board[y2 * width + x1] != board[y2 * width + x3]:
                            can_extend = False    # 下には伸ばせない
                            break

                        x3 += 1

                    # 下に伸ばす
                    if can_extend:
                        x3 = x1
                        while x3 < width:
                            if board[y1 * width + x3] != ren_id:
                                # 連の幅に達した
                                break

                            board[y2 * width + x3] = ren_id
                            x3 += 1

    # 結果表示
    print("""\

RESULT
------""")
    print_board(
            width=width,
            height=height,
            board=board)


def print_board(width, height, board):
    for y in range(0, height):
        for x in range(0, width):
            index = y * width + x
            print(board[index], end='')
        print() # 改行


########################################
# MARK: コマンドから実行時
########################################

if __name__ == '__main__':
    try:
        main()

    except Exception as err:
        print(f"""\
おお、残念！　例外が投げられてしまった！
{type(err)=}  {err=}

以下はスタックトレース表示じゃ。
{traceback.format_exc()}
""")
