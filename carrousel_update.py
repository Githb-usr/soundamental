from PIL import Image
import os

folder = r'D:\PY_Soundamental\media\site\illustrations\carrousel'
target_size = 400  # pixels (largeur et hauteur)
quality = 75       # qualité JPEG (0-100)

for filename in os.listdir(folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        path = os.path.join(folder, filename)
        with Image.open(path) as img:
            img = img.convert("RGB")  # Assure la compatibilité JPEG

            # Redimensionne à 400x400 pixels, coupe si besoin (crop center)
            w, h = img.size
            if w != h:
                min_dim = min(w, h)
                left = (w - min_dim) // 2
                top = (h - min_dim) // 2
                right = left + min_dim
                bottom = top + min_dim
                img = img.crop((left, top, right, bottom))
            img = img.resize((target_size, target_size), Image.LANCZOS)

            # Sauvegarde en JPEG compressé (écrase l’original)
            img.save(path, "JPEG", quality=quality, optimize=True)
            print(f"{filename} → {target_size}x{target_size}px, qualité {quality}")
