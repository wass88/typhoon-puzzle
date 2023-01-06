#!/usr/bin/env python3
import sys

uniq = len(sys.argv) >= 2 and sys.argv[1] == "uniq"

result = input()
if result != "s SATISFIABLE":
    if uniq:
        if result == "s UNSATISFIABLE":
            sys.stderr.write("Unique\n")
            exit(0)
    else:
        raise Exception(f"No solution: {result}")

def read_v(lines, exp_name):
    l = lines.pop(0)
    a, v = l.split(" ")
    if a != "a":
        raise Exception(f"expected a: {l}")
    name, v = v.split("\t")
    if name != exp_name:
        raise Exception(f"expected {exp_name}: {name}")
    return int(v)


lines = sys.stdin.readlines()
h = 1
w = 1
for l in lines:
    a, v = l.split(" ")
    if a != "a":
        print(f"expected a: {l}")
        exit(1)
    name, v = v.split("\t")
    t, y, x = name.split("_")
    if t != "a":
        break
    h = max(h, int(y)+1)
    w = max(w, int(x)+1)

print(f"; Size {h}x{w}")

va = [[-1 for x in range(w)] for y in range(h)]
vt = [[-1 for x in range(w)] for y in range(h)]
vpy = [[-1 for x in range(w)] for y in range(h)]
vpx = [[-1 for x in range(w)] for y in range(h)]


for y in range(h):
    for x in range(w):
        va[y][x] = read_v(lines, f"a_{y}_{x}")

for y in range(h):
    for x in range(w):
        vt[y][x] = read_v(lines, f"t_{y}_{x}")

for y in range(h-1):
    for x in range(w):
        vpy[y][x] = read_v(lines, f"py_{y}_{x}")
for y in range(h):
    for x in range(w-1):
        vpx[y][x] = read_v(lines, f"px_{y}_{x}")

print(";# Area variables\n;", end="")
for y in range(h):
    for x in range(w):
        print(f" {va[y][x]}", end="")
    print("\n;", end="")

print("# Turn variables\n;", end="")
for y in range(h):
    for x in range(w):
        print(f" {vt[y][x]}", end="")
    print("\n;", end="")

print("# Path variables\n; ", end="")
for y in range(h):
    for x in range(w-1):
        if vpx[y][x] == 1:
            print("+--", end="")
        elif vpx[y][x] == 0:
            print("+  ", end="")
        else:
            print("+~~", end="")
    print("+\n; ", end="")
    if y < h-1:
        for x in range(w):
            if vpy[y][x] == 1:
                print("|  ", end="")
            elif vpy[y][x] == 0:
                print("   ", end="")
            else:
                print("!  ", end="")
        print("\n; ", end="")
print()


def str_number(num):
    if num < 0:
        return f"(- {-num})"
    return str(num)


# 唯一解判定のための除外
print("(not (and ")
for y in range(h):
    for x in range(w):
        print(f"(= a_{y}_{x} {va[y][x]})")
        print(f"(= t_{y}_{x} {vt[y][x]})")
        if y < h-1:
            print(f"(= py_{y}_{x} {str_number(vpy[y][x])})")
        if x < w-1:
            print(f"(= px_{y}_{x} {str_number(vpx[y][x])})")
print("))")

if uniq:
    sys.stderr.write("NON Unique\n")
    exit(1)

