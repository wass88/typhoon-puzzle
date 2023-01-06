#!/usr/bin/env python3

# 変数
# a: 領域ラベル
# t: 0:直進 1:曲がる 2:開始 3:終了
# p: パス 1...max_path
#
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

print("; Turn variables (0: straight, 1: right turn, 2: start, 3: end")
for y in range(h):
    for x in range(w):
        print(f"(int t_{y}_{x} 0 3)")

print("; Path variables")
for y in range(h):
    for x in range(w):
        print(f"(int p_{y}_{x} 1 {max_path})")

print("; Start constraints (t=2)")
for a in range(1, nums+1):
    area_num, y, x = area_nums[a-1]
    print(f"(and (= a_{y}_{x} {a}) (= t_{y}_{x} 2))")

for y in range(h):
    for x in range(w):
        if puzzle[y][x] < 0:
            print(f"(!= t_{y}_{x} 2)")

print("; start path number is 1")
for y in range(h):
    for x in range(w):
        print(f"(imp (= t_{y}_{x} 2) (= p_{y}_{x} 1))")

print("")

print("; Area has only one end (t=3)")
for a in range(1, nums+1):
    res = ""
    for y in range(h):
        for x in range(w):
            res += f"(if (and (= a_{y}_{x} {a}) (= t_{y}_{x} 3)) 1 0)"
    print(f"(= (+ {res}) 1)")


d4 = [[1, 0], [0, -1], [-1, 0], [0, 1]]
print("; Straight constraints (t=0)")
for y in range(h):
    for x in range(w):
        res = ""
        for d in range(4):
            from_d = d4[(d+2) % 4]
            to_d = d4[d]
            from_y = y + from_d[0]
            from_x = x + from_d[1]
            to_y = y + to_d[0]
            to_x = x + to_d[1]
            if 0 <= from_y < h and 0 <= from_x < w and 0 <= to_y < h and 0 <= to_x < w:
                res += f"(and "
                res += f"(= (- p_{y}_{x} 1) p_{from_y}_{from_x}) "
                res += f"(= (+ p_{y}_{x} 1) p_{to_y}_{to_x}) "
                res += f"(= a_{y}_{x} a_{from_y}_{from_x}) "
                res += f"(= a_{y}_{x} a_{to_y}_{to_x}) "
                res += f")"
        if res != "":
            print(f"(imp (= t_{y}_{x} 0) (or {res}))")
        else:
            print(f"(!= t_{y}_{x} 0)")

print("; Turn right constraints (t=1)")
for y in range(h):
    for x in range(w):
        res = ""
        for d in range(4):
            from_d = d4[(d+1) % 4]
            to_d_ = d4[d]
            from_y = y + from_d[0]
            from_x = x + from_d[1]
            to_y = y + to_d_[0]
            to_x = x + to_d_[1]
            if 0 <= from_y < h and 0 <= from_x < w and 0 <= to_y < h and 0 <= to_x < w:
                res += f"(and "
                res += f"(= (- p_{y}_{x} 1) p_{from_y}_{from_x}) "
                res += f"(= (+ p_{y}_{x} 1) p_{to_y}_{to_x}) "
                res += f"(= a_{y}_{x} a_{from_y}_{from_x}) "
                res += f"(= a_{y}_{x} a_{to_y}_{to_x}) "
                res += f")"
        if res != "":
            print(f"(imp (= t_{y}_{x} 1) (or {res}))")
        else:
            print(f"(!= t_{y}_{x} 1)")

print("; Count Turn right (t=1)")
for a in range(1, nums+1):
    area_num, _, _ = area_nums[a-1]
    res = ""
    for y in range(h):
        for x in range(w):
            res += f"(if (and (= a_{y}_{x} {a}) (= t_{y}_{x} 1)) 1 0)"
    print(f"(= (+ {res}) {area_num})")
