# divide-into-fewer-rectangles

方眼紙を塗りつぶして描いた図形を与えると、  
少ない数の長方形に分けるアルゴリズムです。  
詳しくは、例を見てください。  


## 例１

### 概要

![例１概要](./docs/img/202501__pg__29-2316--explain-o1o3.png)  


### 実行例

Input:  

```shell
py main.py
```

Output:  

```plaintext
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

7 5
..xxx..
xxxxx..
xxxxxxx
..xxxxx
...xxxx

RESULT
------
0011100
2211100
2211133
0011133
0005533
```

### アルゴリズム解説

![解説1](./docs/img/202501__pg__29-2322--explain-o1o4.png)  


## その他の実行例

* 📖 [実行例２](./docs/example2.md)
* 📖 [実行例３](./docs/example3.md)
