#!/usr/bin/env python
# Ex2
# Niv Swisa 307929257, Martin Mazas 329834857, Yarin Mizrahi 205663917

import math
from tkinter import *

file_name = 'coordinates.txt'
height = width = 1000
window = Tk()
window.title("Ex 2")
window.geometry("1000x1000")
canvas = Canvas(window, width=width, height=height, bg='black')
img = PhotoImage(width=width, height=height)
canvas.create_image((width // 2, height // 2), image=img, state="normal")
file_name_entry = Entry(window, width=10)
with open(file_name) as coordinates:
    data = coordinates
    fileLines = data.read().splitlines()

lines = []
circles = []
curves = []


# Draw a single pixel
def draw_pixel(x, y):
    global img
    # Check that the point is on the window
    if x < 0 or y < 0:
        return
    img.put("#fff", (x, y))


def my_line(lines_coord):
    # Convert lines to int
    lines_coord[0] = int(lines_coord[0])
    lines_coord[1] = int(lines_coord[1])
    lines_coord[2] = int(lines_coord[2])
    lines_coord[3] = int(lines_coord[3])

    # DDA Algorithm
    delta_x = lines_coord[0] - lines_coord[2]
    delta_y = lines_coord[1] - lines_coord[3]
    _range = max(abs(delta_x), abs(delta_y))
    if _range == 0:
        return
    else:
        dx = delta_x / _range
        dy = delta_y / _range
        x = lines_coord[2]
        y = lines_coord[3]
        for i in range(_range):
            draw_pixel(round(x), round(y))
            x += dx
            y += dy


# Draw circle pixel
def draw_pixel_circle(x_center, y_center, x, y):
    draw_pixel(round(x_center + x), round(y_center + y))
    draw_pixel(round(x_center - x), round(y_center + y))
    draw_pixel(round(x_center + x), round(y_center - y))
    draw_pixel(round(x_center - x), round(y_center - y))
    draw_pixel(round(x_center + y), round(y_center + x))
    draw_pixel(round(x_center - y), round(y_center + x))
    draw_pixel(round(x_center + y), round(y_center - x))
    draw_pixel(round(x_center - y), round(y_center - x))


# Radius calculation
def calculate_radius(xx0, xx1, yy0, yy1):
    x_minus_x = pow((xx0 - xx1), 2)
    y_minus_y = pow((yy0 - yy1), 2)
    return math.sqrt((x_minus_x + y_minus_y))


# Draw circle
def my_circle(circles_coord):
    x0 = int(circles_coord[0])
    y0 = int(circles_coord[1])
    x1 = int(circles_coord[2])
    y1 = int(circles_coord[3])

    radius = calculate_radius(x0, x1, y0, y1)
    x = 0
    y = radius
    p = 3 - 2 * radius

    # Bresenham's algorithm
    while x < y:
        draw_pixel_circle(x0, y0, x, y)
        if p < 0:
            p = p + 4 * x + 6
        else:
            draw_pixel_circle(x0, y0, x + 1, y)
            p = p + 4 * (x - y) + 10
            y -= 1
        x += 1
    if x == y:
        draw_pixel_circle(x0, y0, x, y)


# Draw curve
def my_curve(curves_coord):
    xx0 = int(curves_coord[0])
    yy0 = int(curves_coord[1])
    xx1 = int(curves_coord[2])
    yy1 = int(curves_coord[3])
    xx2 = int(curves_coord[4])
    yy2 = int(curves_coord[5])
    xx3 = int(curves_coord[6])
    yy3 = int(curves_coord[7])

    num_of_lines = 20

    # Bezier curves
    dt = 1 / num_of_lines
    ax = -xx0 + 3 * xx1 - 3 * xx2 + xx3
    bx = 3 * xx0 - 6 * xx1 + 3 * xx2
    cx = -3 * xx0 + 3 * xx1
    dx = xx0

    ay = -yy0 + 3 * yy1 - 3 * yy2 + yy3
    by = 3 * yy0 - 6 * yy1 + 3 * yy2
    cy = -3 * yy0 + 3 * yy1
    dy = yy0

    f_x, f_y = xx0, yy0
    t = dt
    while t < 1.0:
        xt, yt = int(ax * pow(t, 3) + bx * pow(t, 2) + cx * t + dx), int(ay * pow(t, 3) + by * pow(t, 2) + cy * t + dy)
        my_line([f_x, f_y, xt, yt])
        f_x, f_y = xt, yt
        t += dt
    my_line([xt, yt, xx3, yy3])


def rotation_x(coord):
    rotated = []
    coord[0] = int(coord[0])*(-1) + 1000
    coord[2] = int(coord[2])*(-1) + 1000
    rotated.append(coord[0])
    rotated.append(int(coord[1]))
    rotated.append(coord[2])
    rotated.append(int(coord[3]))
    if len(coord) == 8:
        coord[4] = int(coord[4]) * (-1) + 1000
        coord[6] = int(coord[6]) * (-1) + 1000
        rotated.append(coord[4])
        rotated.append(int(coord[5]))
        rotated.append(coord[6])
        rotated.append(int(coord[7]))
    return rotated


def rotation_y(coord):
    rotated = []
    coord[1] = int(coord[1])*(-1) + 800
    coord[3] = int(coord[3])*(-1) + 800
    rotated.append(int(coord[0]))
    rotated.append(coord[1])
    rotated.append(int(coord[2]))
    rotated.append(coord[3])
    if len(coord) == 8:
        coord[5] = int(coord[5]) * (-1) + 800
        coord[7] = int(coord[7]) * (-1) + 800
        rotated.append(int(coord[4]))
        rotated.append(coord[5])
        rotated.append(int(coord[6]))
        rotated.append(coord[7])
    return rotated


def clean():
    global img, lines, circles, curves
    canvas.delete(img)
    img = PhotoImage(width=width, height=height)
    canvas.create_image((width // 2, height // 2), image=img, state="normal")


def rot_x():
    clean()
    for ll in range(len(lines) - 1):
        canvas.bind('<Button-1>', my_line(rotation_x(lines[ll + 1])))
    for cc in range(len(circles) - 1):
        canvas.bind('<Button-1>', my_circle(rotation_x(circles[cc + 1])))
    for cr in range(len(curves) - 1):
        canvas.bind('<Button-1>', my_curve(rotation_x(curves[cr + 1])))


def rot_y():
    clean()
    for ll in range(len(lines) - 1):
        canvas.bind('<Button-1>', my_line(rotation_y(lines[ll + 1])))
    for cc in range(len(circles) - 1):
        canvas.bind('<Button-1>', my_circle(rotation_y(circles[cc + 1])))
    for cr in range(len(curves) - 1):
        canvas.bind('<Button-1>', my_curve(rotation_y(curves[cr + 1])))


def select_file():
    global file_name_entry, file_name
    file_name = file_name_entry.get()
    initialize()


def initialize():
    global data, lines, circles, curves, coordinates, fileLines
    with open(file_name) as coordinates:
        data = coordinates
        fileLines = data.read().splitlines()
    # Read coordinates flag(l -> line_flag, cir -> circle_flag, cur -> curve_flag)
    l = cir = cur = 0

    if len(lines) > 0:
        lines = []
    if len(circles) > 0:
        circles = []
    if len(curves) > 0:
        curves = []
    for li in fileLines:
        # Activate line flag
        if li.find('lines') != -1:
            cir = 0
            l = 1
            cur = 0
        # Activate circle flag
        if li.find('circles') != -1:
            cir = 1
            l = 0
            cur = 0
        # Activate curve flag
        if li.find('curves') != -1:
            cir = 0
            l = 0
            cur = 1
        # Append lines coordinates to a line list
        if l == 1:
            line_list = li[1:-1].split(',')
            lines.append(line_list)
        # Append circle coordinates to a circle list
        elif cir == 1:
            circle_list = li[1:-1].split(',')
            circles.append(circle_list)
        # Append curve coordinates to a curve list
        elif cur == 1:
            curves_list = li[1:-1].split(',')
            curves.append(curves_list)

    canvas.grid(row=3, column=3)
    # Draw lines, circles and curves
    for ll in range(len(lines) - 1):
        canvas.bind('<Button-1>', my_line(lines[ll + 1]))
    for cc in range(len(circles) - 1):
        canvas.bind('<Button-1>', my_circle(circles[cc + 1]))
    for cr in range(len(curves) - 1):
        canvas.bind('<Button-1>', my_curve(curves[cr + 1]))


def main():
    initialize()
    file_name_entry.place(x=100)
    select_file_btn = Button(window, text="Select", command=select_file)
    select_file_btn.place(x=300)
    clean_btn = Button(window, text="Clean", command=clean)
    clean_btn.place(x=50)
    rot_x_btn = Button(window, text="RotateX", command=rot_x)
    rot_x_btn.grid(row=0, column=1)
    rot_x_btn.place(x=550)
    rot_y_btn = Button(window, text="RotateY", command=rot_y)
    rot_y_btn.grid(row=0, column=1)
    rot_y_btn.place(x=400)
    window.mainloop()


if __name__ == '__main__':
    main()