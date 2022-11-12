import tkinter as tk
from datetime import datetime

dt = datetime.now()

window = tk.Tk()

frame1 = tk.Frame(master=window, height=120, width=300, bg="#ECF0F3")
frame1.pack(fill=tk.X)

frame_fecha = tk.Frame(master = frame1, height=120, width=50)
frame_fecha.pack(fill=tk.Y)

lbl_dia_num = tk.Label(master=frame_fecha, text= dt.strftime('%d'), bg="#725A68")
lbl_dia_num.place(x=0, y=0)

lbl_dia = tk.Label(master=frame_fecha, text= dt.strftime('%a'), bg="#9EA3AA")
lbl_dia.place(x=7, y=0)

window.mainloop()