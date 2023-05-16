import streamlit as st
from PIL import Image, ImageDraw
from streamlit_cropper import st_cropper
import os
import openai

img_file = "static/roomsq2.png"
img = Image.open(img_file)

with st.sidebar:
    openai.api_key = st.text_input("Enter your OpenAI API key here")

aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
aspect_dict = {
    "1:1": (1, 1),
    "16:9": (16, 9),
    "4:3": (4, 3),
    "2:3": (2, 3),
    "Free": None
}

st.write(img.size)

aspect_ratio = aspect_dict[aspect_choice]

img = Image.open(img_file)
# Get a cropped image from the frontend
cropped_img = st_cropper(img, realtime_update=True, box_color='#FF0000',
                            aspect_ratio=aspect_ratio, return_type="box")

text = st.text_input("Write a description. Can be a sentance or just a word")
b1 = st.button("Search", key=5)


def mask_image(img, cropped_img):
    mask = Image.new("RGBA", img.size, (0, 0, 0, 255))
    im1 = Image.new("RGBA", img.size, (255,0,0,255))
    draw = ImageDraw.Draw(mask, 'RGBA')
    draw.rectangle([(cropped_img["left"], cropped_img["top"]), (cropped_img["left"] + cropped_img["width"], cropped_img["top"] + cropped_img["height"])], fill=(0,0,0,0))
    mask.save("static/mask.png")

def genereate_new_img(im, prompt):
    if text:
        response = openai.Image.create_edit(image=open("static/roomsq2.png", "rb"), mask=open("static/mask.png", "rb"), prompt=prompt, n=2, size="512x512")
        results = response.to_dict()["data"]
        st.image([results[0]['url'], results[1]['url']])
        return results
    else:
        st.write("Please enter your OpenAI API key in the side bar.")



if b1:
    mask_image(img, cropped_img)
    with st.spinner():
        genereate_new_img("", text)

   


