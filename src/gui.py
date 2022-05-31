from tkinter import *
from PIL import ImageTk, Image
import os

from utils import (
    setup_chrome,
    load_image_with_scale,
    inpaint_image,
    get_card_name,
    get_card_subname,
    get_card_trait,
    get_card_text,
    draw_text,
    card_text_to_img,
    put_text_on_img,
    check_backside_exist,
    ICON_TO_TEXT
)

class CanvasWithImage(Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def setup_image(self, img):
        img_w, img_h = img.size
        self.config(width=img_w, height=img_h)
        self.tk_im = ImageTk.PhotoImage(img)
        self.create_image(0, 0, anchor="nw", image=self.tk_im)

class TextBoxWithPlaceholder(Text):
    def __init__(self, parent, placeholder, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.placeholder_text = placeholder
        self.insert_placeholder()
        self.bind('<FocusIn>', self.on_focus_in)
        self.bind('<FocusOut>', self.on_focus_out)

    def insert_placeholder(self):
        ''' insert the placeholder into text box '''
        lbl = Label(self, text=self.placeholder_text, compound='left',
                       fg='darkgray', bg=self.cget('bg'), font=(None,10,'bold'))
        self.window_create('end', window=lbl)
        self.placeholder = self.window_names()[0]

    def on_focus_in(self, event):
        try:
            # check whether the placeholder exists
            item = self.window_cget(1.0, 'window')
            if item == self.placeholder:
                # remove the placeholder
                self.delete(1.0, 'end')
        except:
            # placeholder not found, do nothing
            pass

    def on_focus_out(self, event):
        if self.get(1.0, 'end-1c') == '':
            # nothing input, so add back the placeholder
            self.insert_placeholder()

class CustomTextbox(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.textbox = Text(self, width=50, height=10)
        self.textbox.grid(row=1, column=0, sticky=N+S+E+W)

        self.icon_frame = Frame(self)
        self.icon_frame.grid(row=2, column=0, sticky=N+S+E+W)

        self.icon_images = []
        self.icon_buttons = []
        charset = set()
        idx = 0
        for icon_name, t in ICON_TO_TEXT.items():
            if t in charset:
                continue
            charset.add(t)
            icon_img_path = "data/icons/" + icon_name + ".png"
            img = Image.open(icon_img_path)
            img = img.crop([0,0,75,50])
            img = img.resize((39, 26))
            self.icon_images.append(ImageTk.PhotoImage(img))
            self.icon_buttons.append(self.make_button(idx, t))
            row_idx = idx // 10
            col_idx = idx % 10

            self.icon_buttons[idx].grid(row=row_idx, column=col_idx, sticky=N+S+E+W)
            idx += 1

    def make_button(self, idx, text):
        button = Button(self.icon_frame, image=self.icon_images[idx], width=39, height=26, command=lambda: self.icon_button_action(text))
        return button
    
    def icon_button_action(self, icon_text):
        text = f"<span>{icon_text}</span>"
        self.textbox.insert(INSERT, text)

    def get_text(self):
        text_str = self.textbox.get("1.0", "end-1c").strip()
        text_boxes = text_str.split('\n')
        paragraphs = ["<p>" + text + "</p>" for text in text_boxes]
        text = "".join(paragraphs)

        return text

    def set_text(self, html):
        text = html.replace('<p>', '').replace('</p>', '\n').strip()
        self.textbox.insert(INSERT, text)


class GUIApp():
    def __init__(self, root, args):
        self.args = args
        self.scale = args.image_scale
        self.save_original_size = args.save_original_size
        self.chromedriver = args.chromedriver
        self.is_backside = False

        self.root_frame = Frame(root)
        self.root_frame.pack()

        self.main = None

        self.card_id_frame = Frame(self.root_frame)
        self.card_id_frame.grid(row=0, column=0, sticky=N+S+E+W)

        self.driver = setup_chrome(self.chromedriver)
        self.setup_card_id()

    def setup_card_id(self):
        self.card_id_box = TextBoxWithPlaceholder(self.card_id_frame, "Insert Card ID", height=2)
        self.card_id_box.bind('<Return>', self.get_card_id)
        self.card_id_box.grid(row=0, column=0, sticky=N+S+E+W)

    def get_card_id(self, event):
        self.card_id = self.card_id_box.get("1.0", "end-1c")
        self.card_id = self.card_id.strip()
        self.driver.get(f'https://ko.arkhamdb.com/card/{self.card_id}')

        self.backside_exist = check_backside_exist(self.driver)

        if self.backside_exist:
            self.side_text_variable = StringVar()
            self.side_text_variable.set('Do Backside')
            self.backside_button = Button(self.card_id_frame, textvariable=self.side_text_variable, width=13, height=1, command=self.change_side)
            self.backside_button.grid(row=0, column=1, sticky=N+S+E+W)

        self.setup_everything()

        return 'break'

    def reset_everything(self):
        if self.main:
            self.main.destroy()
        self.main = Frame(self.root_frame)
        self.main.grid(row=1, column=0, sticky=N+S+E+W)

    def setup_everything(self):
        self.reset_everything()
        suffix = ''
        if self.is_backside:
            suffix = '_back'
        filepath = 'data/image/original/' + self.card_id + suffix + '.png'

        self.img = load_image_with_scale(self.driver, filepath, scale=self.scale)
        self.setup_canvas()
        self.canvas.setup_image(self.img)
        self.setup_text()

    def change_side(self):
        if self.is_backside:
            self.side_text_variable.set('Do Backside')
        else:
            self.side_text_variable.set('Do Frontside')
        
        self.is_backside = not self.is_backside

        self.setup_everything()

    def setup_buttons(self, text, row, text_type):
        if text_type == 'card_text':
            self.fontsize = TextBoxWithPlaceholder(self.text_frame, "Insert Font Size", width=25, height=2)
            self.fontsize.grid(row=row,column=0,sticky=N+S+E+W)

            self.custom_text.set_text(text)
            generate_button = Button(self.text_frame, text='Drag & Generate', width=13, height=1, command=lambda: self.generate_button_action(self.fontsize))
            generate_button.grid(row=row,column=1,sticky=E+W)
        else:
            textbox = Label(self.text_frame, text=text, borderwidth=0, width=25, height=1, justify='center', wraplength=500)
            textbox.grid(row=row,column=0,sticky=N+S+E+W)

            insert_button = Button(self.text_frame, text='Drag & Insert', width=13, height=1, command=lambda: self.g_and_i_button_action(text, text_type))
            insert_button.grid(row=row,column=1,sticky=E+W)

    def generate_button_action(self, fontholder):
        font_size = fontholder.get("1.0", "end-1c")
        font_size = font_size.strip()
        try:
            font_size = int(font_size)
        except:
            font_size = 20

        text = self.custom_text.get_text()

        self.canvas.setup_image(self.img)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", lambda event: self.on_button_release_generate(event, text, font_size))
        
        self.rect = None
        self.start_x = None
        self.start_y = None

    def insert_button_action(self):
        top_left_pos = (int(self.start_x), int(self.start_y))
        text_box_size = (int(self.end_x- self.start_x), int(self.end_y - self.start_y))

        self.img = inpaint_image(self.img, top_left_pos, text_box_size)
        self.img = put_text_on_img(self.img, self.text_img, top_left_pos, text_box_size)
        self.canvas.setup_image(self.img)
        
        self.rect = None
        self.start_x = None
        self.start_y = None

    def g_and_i_button_action(self, text, text_type):
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", lambda event: self.on_button_release(event, text, text_type))
        
        self.rect = None
        self.start_x = None
        self.start_y = None

    def setup_text(self):
        self.text_frame = Frame(self.main)
        self.text_frame.grid(row=0,column=1,sticky=N+E+W)

        card_name = get_card_name(self.driver, self.is_backside)
        card_sub_name = get_card_subname(self.driver, self.is_backside)
        card_trait = get_card_trait(self.driver, self.is_backside)
        card_text = get_card_text(self.driver, self.is_backside)

        idx = 0

        self.setup_buttons(card_name, idx, 'card_name')
        idx += 1

        if card_sub_name:
            self.setup_buttons(card_sub_name, idx, 'card_subname')
            idx += 1
        
        if card_trait:
            self.setup_buttons(card_trait, idx, 'card_trait')
            idx += 1

        self.custom_text = CustomTextbox(self.text_frame)

        if card_text:
            self.setup_buttons(card_text, idx, 'card_text')
            idx += 1

        self.custom_text.grid(row=idx, column=0)

        idx += 1

        self.text_canvas = CanvasWithImage(self.text_frame, width=50, height=10)
        self.text_canvas.grid(row=idx,column=0,sticky=N+S+E+W)

        insert_button = Button(self.text_frame, text='Insert', width=13, height=1, command=self.insert_button_action)
        insert_button.grid(row=idx,column=1,sticky=E+W)

        idx += 1

        save_button = Button(self.text_frame, text='Save', width=15, height=3, command=self.save_img)
        save_button.grid(row=idx,column=0,sticky=E+W)
        
    def save_img(self):
        suffix = ''
        if self.is_backside:
            suffix = '_back'

        output_path = 'data/image/translated/' + self.card_id + suffix + '.png'

        if self.save_original_size:
            self.img = self.img.resize((300, 420))

        
        dir_path = output_path.rsplit('/', 1)[0]
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        self.img.save(output_path)

    def setup_canvas(self):
        self.x = self.y = 0
        self.canvas = CanvasWithImage(self.main, cursor="cross", bg='white')
        self.canvas.grid(row=0,column=0,sticky=N+S+E+W)

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        # create rectangle if not yet exist
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red')

    def on_move_press(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)    

    def on_button_release_generate(self, event, text, font_size):
        self.end_x = event.x
        self.end_y = event.y
        text_box_size = (int(self.end_x - self.start_x), int(self.end_y - self.start_y))

        self.text_img = card_text_to_img(text, text_box_size[0], text_box_size[1], font_size=font_size)
        self.text_canvas.setup_image(self.text_img)

        self.rect = None
        self.canvas.bind("<ButtonPress-1>", lambda x: 'break')
        self.canvas.bind("<B1-Motion>", lambda x: 'break')
        self.canvas.bind("<ButtonRelease-1>", lambda x: 'break')

        return 'break'

    def on_button_release(self, event, text, text_type):
        top_left_pos = (int(self.start_x), int(self.start_y))
        text_box_size = (int(event.x - self.start_x), int(event.y - self.start_y))

        self.img = inpaint_image(self.img, top_left_pos, text_box_size)

        self.img = draw_text(self.img, text_type, text, top_left_pos, text_box_size, scale=self.scale)
        self.canvas.setup_image(self.img)

        self.rect = None
        self.canvas.bind("<ButtonPress-1>", lambda x: 'break')
        self.canvas.bind("<B1-Motion>", lambda x: 'break')
        self.canvas.bind("<ButtonRelease-1>", lambda x: 'break')
        
        return 'break'
