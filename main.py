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
    line = input(prompt)

    write_log(prompt, end='')
    write_log(line)

    width, height = map(int, line.split(' '))

    board_rw = []

    for row_number in range(0, height):
        line = input()
        board_rw.extend(line)

    print() # 改行
    write_log(stringify_board(
            width=width,
            height=height,
            board=board_rw))

    # ここまで、入力
    # --------------


    # 以下、解法
    # ----------

    # 縦と横のどちらが短いか？
    WIDTH_IS_SHORTER = 1
    HEIGHT_IS_SHORTER = 2
    if height < width:
        short_side = HEIGHT_IS_SHORTER
        write_log(f"""\
HEIGHT_IS_SHORTER
""")

    else:
        short_side = WIDTH_IS_SHORTER
        write_log(f"""\
WIDTH_IS_SHORTER
""")


    if short_side == WIDTH_IS_SHORTER:
        # 横の方が短いときは、時計回りに９０°回転させる
        #
        # NOTE 反時計回りより、時計回りの方が、あとで逆回転して戻したときに、連Id が自然な方向に振られる
        #
        width, height, board_rw = rotate90_clockwise(
                width=width,
                height=height,
                board_r=board_rw)

        message = stringify_board(
                width=width,
                height=height,
                board=board_rw)
        write_log(f"""\
ROTATED90 CLOCKWISE
-------------------
{message}""")


    # 千切りフェーズ
    shredded(
            width=width,
            height=height,
            board_rw=board_rw)


    message = stringify_board(
            width=width,
            height=height,
            board=board_rw)
    write_log(f"""\
SHREDDED
--------
{message}""")


    # 浸食フェーズ
    erosion(
            width=width,
            height=height,
            board_rw=board_rw)


    if short_side == WIDTH_IS_SHORTER:
        # 反時計回りに９０°回転させていたのなら、反時計回りに９０°回転させて戻す
        width, height, board_rw = rotate90_counterclockwise(
                width=width,
                height=height,
                board_r=board_rw)

        message = stringify_board(
                width=width,
                height=height,
                board=board_rw)
        write_log(f"""\
ROTATED90 COUNTERCLOCKWISE
--------------------------
{message}""")


    # 結果表示
    message = stringify_board(
            width=width,
            height=height,
            board=board_rw)
    message = f"""\
OUTPUT
------
{message}"""
    print(message)
    write_log(message)


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


def erosion(width, height, board_rw):
    """浸食フェーズ
    """

    # 上の行から浸食済みのId
    erosion_ren_id_set = set()

    # 盤面スキャン
    ren_id = EMPTY

    # 下に進む
    for y1 in range(0, height):

        # 現在処理中の行の中で、既に出てきた連Id
        ren_id_in_same_row = set()
        new_id_set_on_next = set()

        # 右に進む
        for x1 in range(0, width):
            index1 = y1 * width + x1

            # 連Idが変わった。既存、または新しい連Idの始まり
            if ren_id != board_rw[index1]:
                ren_id = board_rw[index1]

                # 空地。次へ
                if board_rw[index1] == EMPTY:
                    continue


                ren_id_in_same_row.add(ren_id)


                # 上の行から浸食済みの連Idなら無視する
                if ren_id in erosion_ren_id_set:
                    continue


                y2 = y1 + 1

                # 下に進む
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
                        write_log("""\
１行下に伸ばせない。浸食終わり。
""")
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

                message = stringify_board(
                        width=width,
                        height=height,
                        board=board_rw)
                write_log(f"""\
EROSION {ren_id=}
-----------------
{message}""")

        erosion_ren_id_set = erosion_ren_id_set.union(new_id_set_on_next)  # 浸食済みのIdとして記憶


def can_falling(width, board_rw, x1, y1, y2, ren_id):
    """１行下に降りれるか？
    """
    target_ren_id = board_rw[y2 * width + x1]

    # 下の行の左外
    if 0 < x1:
        under_left_ren_id = board_rw[y2 * width + x1 - 1]
    else:
        under_left_ren_id = None

    write_log(f"""\
{target_ren_id=} {under_left_ren_id=}
""")

    can_falling_flag = True
    under_right_ren_id = None
    x3 = x1 + 1

    # 右に進む
    while x3 < width:
        under_right_ren_id = board_rw[y2 * width + x3]

        # 右の外の連Idが変わった
        if ren_id != board_rw[y1 * width + x3]:
            break

        # 下が空地だ
        if board_rw[y2 * width + x3] == EMPTY:
            can_falling_flag = False
            break

        # 下の連Idが変わった
        if board_rw[y2 * width + x3] != target_ren_id:
            can_falling_flag = False
            break

        x3 += 1


    write_log(f"""\
{target_ren_id=} {under_right_ren_id=}
""")


    # 下の行の１つの短冊を、２つに分断するようなら、下に浸食しません
    if under_left_ren_id is None or under_right_ren_id is None:
        pass
    elif under_left_ren_id == target_ren_id and under_right_ren_id == target_ren_id:
        return False


    return can_falling_flag


def fill_foot(width, board_rw, x1, y1, y2, ren_id):
    x3 = x1
    while x3 < width:
        # 右の外の連Idが変わった
        if board_rw[y1 * width + x3] != ren_id:
            break

        # 下が空地だ
        if board_rw[y2 * width + x3] == EMPTY:
            break

        # 下の連Idが変わった
        if board_rw[y2 * width + x3] != board_rw[y2 * width + x3]:
            break

        board_rw[y2 * width + x3] = ren_id
        x3 += 1


def stringify_board(width, height, board):
    """盤の表示
    """
    # 最大の連Idを調べる
    max_ren_id = 0
    for y in range(0, height):
        for x in range(0, width):
            index = y * width + x
            ren_id = board[index]
            if isinstance(ren_id, int):
                max_ren_id = max(max_ren_id, ren_id)


    # 最大の連Idの桁数を調べる
    if max_ren_id == 0:
        digits = 1
    else:
        digits = math.floor(math.log10(max_ren_id) + 1)     # 常用対数を取り、１を足し、端数を削除


    text = []

    # 印字
    for y in range(0, height):
        for x in range(0, width):
            index = y * width + x
            ren_id = board[index]
            text.append(str(ren_id).rjust(digits))
        text.append('\n')

    return ''.join(text)


def write_log(text, end='\n'):
    with open('./logs/main.log', mode='a', encoding='utf-8') as f:
        f.write(f'{text}{end}')


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
