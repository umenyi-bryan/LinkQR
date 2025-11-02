#!/usr/bin/env python3
"""Link QR — simple Tkinter GUI with live preview"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import qrcode, io

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Link QR — GUI')
        self.geometry('700x420')
        self.build()

    def build(self):
        frm = ttk.Frame(self)
        frm.pack(fill='both', expand=True, padx=10, pady=10)
        left = ttk.Frame(frm)
        left.pack(side='left', fill='y')
        right = ttk.Frame(frm)
        right.pack(side='right', fill='both', expand=True)

        ttk.Label(left, text='Link:').pack(anchor='w')
        self.link_var = tk.StringVar(value='https://example.com')
        tk.Entry(left, textvariable=self.link_var, width=40).pack()
        ttk.Button(left, text='Generate', command=self.generate).pack(pady=6)
        ttk.Button(left, text='Save PNG...', command=self.save_png).pack(pady=6)
        ttk.Button(left, text='Copy PNG to clipboard', command=self.copy_clip).pack(pady=6)

        self.canvas = tk.Canvas(right, width=400, height=400, bg='black')
        self.canvas.pack(fill='both', expand=True)
        self.img = None
        self.generate()

    def generate(self):
        url = self.link_var.get().strip()
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=2)
        qr.add_data(url); qr.make(fit=True)
        img = qr.make_image(fill_color='#000000', back_color='#ffffff').convert('RGB')
        img = img.resize((400,400), Image.NEAREST)
        self.img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0,0, anchor='nw', image=self.img)

    def save_png(self):
        path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG','*.png')])
        if path:
            url = self.link_var.get().strip()
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=2)
            qr.add_data(url); qr.make(fit=True)
            img = qr.make_image(fill_color='#000000', back_color='#ffffff').convert('RGB')
            img.save(path)
            messagebox.showinfo('Saved', 'Saved to ' + path)

    def copy_clip(self):
        try:
            import pyperclip
            path = 'temp_qr.png'
            url = self.link_var.get().strip()
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=2)
            qr.add_data(url); qr.make(fit=True)
            img = qr.make_image(fill_color='#000000', back_color='#ffffff').convert('RGB')
            img.save(path)
            # Many OS clipboards don't accept raw files from pyperclip; advanced copy omitted.
            messagebox.showinfo('Copied', 'Saved to temp_qr.png. Manual copy required on some OSes.')
        except Exception as e:
            messagebox.showerror('Error', str(e))

if __name__=='__main__':
    App().mainloop()
