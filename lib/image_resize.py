import os
from PIL import Image


def resize_png_files(root_dir):
    for file in os.listdir(root_dir):
        if file.lower().endswith(".png"):
            image_path = os.path.join(root_dir, file)
            try:

                print(image_path)
                image = Image.open(image_path)

                new_16name = image_path.replace(".png", "_16x16.png")
                print(new_16name)
                resized16_image = image.resize((16, 16), Image.LANCZOS)
                resized16_image.save(new_16name, "PNG")

                new_32name = image_path.replace(".png", "_32x32.png")
                print(new_32name)
                resized32_image = image.resize((32, 32), Image.LANCZOS)
                resized32_image.save(new_32name, "PNG")

                new_24name = image_path.replace(".png", "_24x24.png")
                print(new_24name)
                resized24_image = image.resize((24, 24), Image.LANCZOS)
                resized24_image.save(new_24name, "PNG")

                # Delete the original file
                os.remove(image_path)
                # print(f"Deleted original: {image_path}")
            except Exception as e:
                print(f"Error processing {image_path}: {e}")


path = os.path.abspath(".")
print(path)
resize_png_files(path)
