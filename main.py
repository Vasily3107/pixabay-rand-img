import requests
from random import choice

from tkinter import Tk, Label, Button
from PIL     import Image, ImageTk

base_url = 'https://pixabay.com/api/'
api_key = '49887985-63aeb64f4d9a3bbc19fe37dc6'
api_url = f'{base_url}?key={api_key}&image_type=photo'

root = Tk()

def rand_img() -> None:
    res = requests.get(api_url)

    if res.status_code != 200:
        img_label.config(text=f'Error: {res.status_code}')
        return

    data = res.json()

    img_url = choice(data['hits'])['largeImageURL']
    img_ext = img_url.split('.')[-1]
    img_res = requests.get(img_url)

    if img_res.status_code != 200:
        img_label.config(text=f'Error: {res.status_code}')
        return

    img_bin = img_res.content

    with open(f'img.{img_ext}', 'wb') as f:
        f.write(img_bin)

    img = Image.open(f'img.{img_ext}')
    resize_factor = max(img.size)/400
    new_x, new_y = int(img.size[0]/resize_factor), int(img.size[1]/resize_factor)
    img = img.resize((new_x, new_y))

    img = ImageTk.PhotoImage(img)
    img_label.config(text='', image=img)
    img_label.image = img

Button(root, text='Get random image', command=rand_img).pack(fill='x')

img_label  = Label(root)
img_label.pack(fill='x')

root.title('Random images from Pixabay')
root.geometry('400x400')
root.mainloop()