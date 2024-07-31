import os

from PIL import Image

dir = os.getcwd() + "\\ImageCompressor\\database\\"

if __name__ == "__main__":
  for file in os.listdir(dir):
    name, ext = os.path.splitext(dir + file)
    if ext in ['.jpg','.png']:
      img = Image.open(dir + file)
      img = img.resize((img.width // 2, img.height // 2))
      output_name = os.path.join(dir, name + " (compressed)" + ext)
      img.save(output_name, optimize=True, quality=60, subsampling=1)