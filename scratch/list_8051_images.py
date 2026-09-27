import os
images = [f for f in os.listdir("Images") if "8051" in f or "controller" in f]
print("Matching images in Images/:")
for img in sorted(images):
    print(" -", img)
