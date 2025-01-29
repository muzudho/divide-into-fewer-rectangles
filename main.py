########################################
# MARK: コマンドから実行時
########################################

if __name__ == '__main__':
    try:
        print(f"""横幅、縦幅のあとに図形を続けてください。
例：
7 5
..xxx..
xxxxx..
xxxxxxx
..xxxxx
...xxxx
""")
        lines = input()
        width, height = map(int, lines.split(' '))

        pixel_art = []

        for row_number in range(0, height):
            lines = input()
            pixel_art.append(lines)

        print(f'{pixel_art=}')

    except Exception as err:
        print(f"""\
おお、残念！　例外が投げられてしまった！
{type(err)=}  {err=}

以下はスタックトレース表示じゃ。
{traceback.format_exc()}
""")
