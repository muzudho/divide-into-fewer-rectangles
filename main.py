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

    pixel_art = []

    for row_number in range(0, height):
        lines = input()
        pixel_art.extend(lines)

    #print(f'{pixel_art=}')
    print()
    print_pixel_art(
            width=width,
            height=height,
            pixel_art=pixel_art)

    # ここまで、入力
    # --------------

    # 以下、解法
    # ----------

    # 縦と横のどちらが短いか？
    WIDTH_IS_SHORTER = 1
    HEIGHT_IS_SHORTER = 2
    if height < width:
        print(f'縦が短い {width=} {height=}')
        short_side = HEIGHT_IS_SHORTER
    else:
        print(f'横が短い {width=} {height=}')
        short_side = WIDTH_IS_SHORTER
    
    if short_side == WIDTH_IS_SHORTER:
        # 横の方が短いときは、反時計回りに９０°回転させる
        old_width = width               # 退避
        old_height = height
        old_pixel_art = pixel_art
        new_width = old_height              # ９０°回転
        new_height = old_width
        new_pixel_art = list(old_pixel_art)     # シャローコピー
        for old_y in range(0, old_height):
            for old_x in range(0, old_width):
                new_x = old_y
                new_y = (width-1-old_x)
                new_pixel_art[new_y * new_width + new_x] = old_pixel_art[old_y * old_width + old_x]

        width = new_width
        height = new_height
        pixel_art = new_pixel_art


    #print(f'{pixel_art=}')
    print()
    print_pixel_art(
            width=width,
            height=height,
            pixel_art=pixel_art)


def print_pixel_art(width, height, pixel_art):
    for y in range(0, height):
        for x in range(0, width):
            index = y * width + x
            print(pixel_art[index], end='')
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
