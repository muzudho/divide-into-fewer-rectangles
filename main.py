import math
import traceback


EMPTY = 0

def main():
    # ここから、入力
    # --------------

    prompt = f"""\
横幅、縦幅のあとに図形を続けてください。

EXAMPLE
-------
7 5
..xxx..
xxxxx..
xxxxxxx
..xxxxx
...xxxx

INPUT
-----
"""
    lines = input(prompt)
    width, height = map(int, lines.split(' '))

    board_rw = []

    for row_number in range(0, height):
        lines = input()
        board_rw.extend(lines)

    # print_board(
    #         width=width,
    #         height=height,
    #         board=board_rw)

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


    # print('★A')
    # print_board(
    #         width=width,
    #         height=height,
    #         board=board_rw)

    if short_side == WIDTH_IS_SHORTER:
        # 横の方が短いときは、時計回りに９０°回転させる
        #
        # NOTE 反時計回りより、時計回りの方が、あとで逆回転して戻したときに、連Id が自然な方向に振られる
        #
        width, height, board_rw = rotate90_clockwise(
                width=width,
                height=height,
                board_r=board_rw)


    # print('★B')
    # print_board(
    #         width=width,
    #         height=height,
    #         board=board_rw)


    # 千切りフェーズ
    end_ren_id = shredded(
            width=width,
            height=height,
            board_rw=board_rw)


    # print('★C')
    # print_board(
    #         width=width,
    #         height=height,
    #         board=board_rw)


    # 浸食フェーズ
    erosion(
            width=width,
            height=height,
            board_rw=board_rw,
            end_ren_id=end_ren_id)


    if short_side == WIDTH_IS_SHORTER:
        # 反時計回りに９０°回転させていたのなら、反時計回りに９０°回転させて戻す
        width, height, board_rw = rotate90_counterclockwise(
                width=width,
                height=height,
                board_r=board_rw)


    # 結果表示
    print("""\
TERMINATED
----------""")
    print_board(
            width=width,
            height=height,
            board=board_rw)


def rotate90_counterclockwise(width, height, board_r):
    """反時計回りに９０°回転
    """
    # 反時計回り
    old_width = width               # 退避
    old_height = height
    old_board_r = board_r
    new_width = old_height              # ９０°回転
    new_height = old_width
    new_board_w = list(old_board_r)     # シャローコピー
    for old_y in range(0, old_height):
        for old_x in range(0, old_width):
            new_x = old_y
            new_y = (width-1-old_x)
            new_board_w[new_y * new_width + new_x] = old_board_r[old_y * old_width + old_x]

    return new_width, new_height, new_board_w


def rotate90_clockwise(width, height, board_r):
    """時計回りに９０°回転
    """
    # 反時計回り
    old_width = width               # 退避
    old_height = height
    old_board_r = board_r
    new_width = old_height              # ９０°回転
    new_height = old_width
    new_board_w = list(old_board_r)     # シャローコピー
    for old_y in range(0, old_height):
        for old_x in range(0, old_width):
            new_x = (height-1-old_y)
            new_y = old_x
            new_board_w[new_y * new_width + new_x] = old_board_r[old_y * old_width + old_x]

    return new_width, new_height, new_board_w


def shredded(width, height, board_rw):
    """千切りフェーズ
    """
    # 右から左へ連続するものを連（れん）と呼ぶことにする。
    ren_id = 1
    is_stone_ren = False
    for y in range(0, height):
        for x in range(0, width):
            index = y * width + x

            stone = board_rw[index]
            if stone == 'x':
                if not is_stone_ren:
                    is_stone_ren = True
                board_rw[index] = ren_id
            else:
                if is_stone_ren:
                    ren_id += 1
                    is_stone_ren = False
                board_rw[index] = EMPTY
        
        if is_stone_ren:
            ren_id += 1
            is_stone_ren = False

    return ren_id


def erosion(width, height, board_rw, end_ren_id):
    """浸食フェーズ

    Parameters
    ----------
    end_ren_id : int
        使われていない連Id。既存の全ての連Idより大きい。
    """

    # 上の行から浸食済みのId
    erosion_ren_id_set = set()

    # 盤面スキャン
    ren_id = EMPTY
    for y1 in range(0, height):

        # 現在処理中の行の中で、既に出てきた連Id
        ren_id_in_same_row = set()
        new_id_set_on_next = set()

        for x1 in range(0, width):
            index1 = y1 * width + x1

            # 連Idが変わった。既存、または新しい連Idの始まり
            if ren_id != board_rw[index1]:
                ren_id = board_rw[index1]

                # 連Id が 0 なら空地。無視する
                if board_rw[index1] == EMPTY:
                    continue

                # 現在処理中の行の中で、処理した連Id が、再び出てきたケース
                if ren_id in ren_id_in_same_row:
                    # まだ使われていないIdを付けたい

                    old_ren_id = board_rw[y1 * width + x1]
                    board_rw[y1 * width + x1] = end_ren_id

                    x3 = x1 + 1
                    while x3 < width:
                        if board_rw[y1 * width + x3] != ren_id:     # 連の幅に達した
                            break

                        if board_rw[y1 * width + x1] == EMPTY:      # 空地に達した
                            break

                        if old_ren_id != board_rw[y1 * width + x3]:     # 連続が終わった
                            break

                        board_rw[y1 * width + x3] = end_ren_id
                        x3 += 1

                    ren_id = end_ren_id
                    end_ren_id += 1

                ren_id_in_same_row.add(ren_id)


                # 上の行から浸食済みの連Idなら無視する
                if ren_id in erosion_ren_id_set:
                    continue


                y2 = y1 + 1
                while y2 < height:

                    # 連を１行下に伸ばせるか判定します
                    can_falling_flag = can_falling(
                            width=width,
                            board_rw=board_rw,
                            x1=x1,
                            y1=y1,
                            y2=y2,
                            ren_id=ren_id)

                    # １行下に伸ばせないなら終わり
                    if not can_falling_flag:
                        break


                    new_id_set_on_next.add(ren_id)  # 浸食済みのIdとして記憶

                    fill_foot(
                            width=width,
                            board_rw=board_rw,
                            x1=x1,
                            y1=y1,
                            y2=y2,
                            ren_id=ren_id)

                    y2 += 1

                print(f"""\
EROSION {ren_id=}
-----------------""")
                print_board(
                        width=width,
                        height=height,
                        board=board_rw)

        erosion_ren_id_set = erosion_ren_id_set.union(new_id_set_on_next)  # 浸食済みのIdとして記憶


def can_falling(width, board_rw, x1, y1, y2, ren_id):
    """１行下に降りれるか？
    """
    can_falling_flag = True
    x3 = x1 + 1
    while x3 < width:
        # 連の幅に達した
        if board_rw[y1 * width + x3] != ren_id:
            break

        # 空地に達した
        if board_rw[y2 * width + x3] == EMPTY:
            can_falling_flag = False
            break

        # 連Idが変わった
        if board_rw[y2 * width + x1] != board_rw[y2 * width + x3]:
            can_falling_flag = False
            break

        x3 += 1

    return can_falling_flag


def fill_foot(width, board_rw, x1, y1, y2, ren_id):
    x3 = x1
    while x3 < width:
        # 連の幅に達した
        if board_rw[y1 * width + x3] != ren_id:
            break

        # 空地に達した
        if board_rw[y2 * width + x3] == EMPTY:
            break

        # 連Idが変わった
        if board_rw[y2 * width + x3] != board_rw[y2 * width + x3]:
            break

        board_rw[y2 * width + x3] = ren_id
        x3 += 1


def print_board(width, height, board):
    """盤の表示
    """
    # 最大の連Idを調べる
    max_ren_id = 0
    for y in range(0, height):
        for x in range(0, width):
            index = y * width + x
            ren_id = board[index]
            max_ren_id = max(max_ren_id, ren_id)


    # 最大の連Idの桁数を調べる
    digits = math.floor(math.log10(max_ren_id) + 1)     # 常用対数を取り、１を足し、端数を削除


    text = []

    # 印字
    for y in range(0, height):
        for x in range(0, width):
            index = y * width + x
            ren_id = board[index]
            text.append(str(ren_id).rjust(digits))
        text.append('\n')

    print(''.join(text))


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
