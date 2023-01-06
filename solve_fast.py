#!/usr/bin/env python3

# 変数
# a: 領域ラベル
# t: 0:直進 1:曲がる 2:開始 3:終了
# py: 1:上から下に縦辺あり 0:なし -1:逆向き
# px: 1:左から右に横辺あり 0:なし -1:逆向き

# 制約
# t=0 同じ領域で直進
# t=1 同じ領域で曲がる
# t=2 指定場所にp=1、a=ラベル
# t=3 領域に1つ

h, w = map(int, input().split(" "))
puzzle = [
    [int(x) if x != "-" else -1 for x in input().split(" ")]
    for y in range(h)
]

# WORKAROUND
max_path = h*w

nums = sum((1 for row in puzzle for x in row if x >= 0))
for y in range(h):
    print(";", end="")
    for x in range(w):
        if puzzle[y][x] >= 0:
            print(f" {puzzle[y][x]}", end="")
        else:
            print(" _", end="")
    print()

print(f"; {nums} numbers")

area_nums = []  # number on pos
for y in range(h):
    for x in range(w):
        if puzzle[y][x] >= 0:
            area_nums.append((puzzle[y][x], y, x))

print("; Area variables")
for y in range(h):
    for x in range(w):
        print(f"(int a_{y}_{x} {1} {nums})")

print("; Turn variables (0: straight, 1: right turn, 2: start, 3: end)")
for y in range(h):
    for x in range(w):
        print(f"(int t_{y}_{x} 0 3)")

print("; Path variables")
for y in range(h-1):
    for x in range(w):
        print(f"(int py_{y}_{x} -1 1)")
for y in range(h):
    for x in range(w-1):
        print(f"(int px_{y}_{x} -1 1)")

print("; Loop variables")
for y in range(h):
    for x in range(w):
        print(f"(int l_{y}_{x} 1 {w*h})")

# 線の開始地点は固定
print("; Start constraints (t=2)")
for a in range(1, nums+1):
    area_num, y, x = area_nums[a-1]
    print(f"(and (= a_{y}_{x} {a}) (= t_{y}_{x} 2))")

for y in range(h):
    for x in range(w):
        if puzzle[y][x] < 0:
            print(f"(!= t_{y}_{x} 2)")


def degree(y, x):
    res = "(+"
    if y > 0:
        res += f" (- py_{y-1}_{x})"
    if y < h-1:
        res += f" py_{y}_{x}"
    if x > 0:
        res += f" (- px_{y}_{x-1})"
    if x < w-1:
        res += f" px_{y}_{x}"
    res += ")"
    return res


def abs_degree(y, x):
    res = "(+"
    if y > 0:
        res += f" (abs py_{y-1}_{x})"
    if y < h-1:
        res += f" (abs py_{y}_{x})"
    if x > 0:
        res += f" (abs px_{y}_{x-1})"
    if x < w-1:
        res += f" (abs px_{y}_{x})"
    res += ")"
    return res


print("; start of path (t=2)")
for y in range(h):
    for x in range(w):
        print(
            f"(imp (= t_{y}_{x} 2) (and (= {degree(y, x)} 1) (= {abs_degree(y,x)} 1)))")

print("; end of path (t=3)")
for y in range(h):
    for x in range(w):
        print(
            f"(imp (= t_{y}_{x} 3) (and (= {degree(y, x)} -1) (= {abs_degree(y,x)} 1)))")

print("; Area has only one end (t=3)")
for a in range(1, nums+1):
    res = ""
    for y in range(h):
        for x in range(w):
            res += f"(if (and (= a_{y}_{x} {a}) (= t_{y}_{x} 3)) 1 0)"
    print(f"(= (+ {res}) 1)")

print("; Count Turn right (t=1)")
for a in range(1, nums+1):
    area_num, _, _ = area_nums[a-1]
    res = ""
    for y in range(h):
        for x in range(w):
            res += f"(if (and (= a_{y}_{x} {a}) (= t_{y}_{x} 1)) 1 0)"
    print(f"(= (+ {res}) {area_num})")

print("; Straight constraints (t=0)")
for y in range(h):
    for x in range(w):
        res = ""
        if y > 0 and y < h-1:
            res += f"(= (* py_{y-1}_{x} py_{y}_{x}) 1)"
        if x > 0 and x < w-1:
            res += f"(= (* px_{y}_{x-1} px_{y}_{x}) 1)"
        print(
            f"(imp (= t_{y}_{x} 0) (and (= {abs_degree(y, x)} 2) (or {res})))")

print("; Turn right constraints (t=1)")
for y in range(h):
    for x in range(w):
        res = ""
        if y > 0 and x > 0:
            res += f"(and (= py_{y-1}_{x} 1) (= px_{y}_{x-1} -1))"
        if y > 0 and x < w-1:
            res += f"(and (= py_{y-1}_{x} -1) (= px_{y}_{x} -1))"
        if y < h-1 and x > 0:
            res += f"(and (= py_{y}_{x} 1) (= px_{y}_{x-1} 1))"
        if y < h-1 and x < w-1:
            res += f"(and (= py_{y}_{x} -1) (= px_{y}_{x} 1))"
        print(
            f"(imp (= t_{y}_{x} 1) (and (= {abs_degree(y, x)} 2) (or {res})))")


print("; Line with same area")
for y in range(h):
    for x in range(w):
        if y < h - 1:
            print(f"(imp (!= py_{y}_{x} 0) (= a_{y}_{x} a_{y+1}_{x}))")
        if x < w - 1:
            print(f"(imp (!= px_{y}_{x} 0) (= a_{y}_{x} a_{y}_{x+1}))")

# 輪の存在を否定
print("; No loop")
for y in range(h):
    for x in range(w):
        if y < h - 1:
            print(
                f"(imp (= py_{y}_{x}    1 ) (= (+ l_{y}_{x} 1) l_{y+1}_{x}))")
            print(
                f"(imp (= py_{y}_{x} (- 1)) (= (- l_{y}_{x} 1) l_{y+1}_{x}))")
        if x < w - 1:
            print(
                f"(imp (= px_{y}_{x}    1 ) (= (+ l_{y}_{x} 1) l_{y}_{x+1}))")
            print(
                f"(imp (= px_{y}_{x} (- 1)) (= (- l_{y}_{x} 1) l_{y}_{x+1}))")
