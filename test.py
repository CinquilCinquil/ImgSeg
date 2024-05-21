from PIL import Image # Python library for image processing

I = Image.open("test_files/test1.png")
w, h = I.size

I = I.resize((16,16), Image.Resampling.BICUBIC)

I.save("wtf.png")