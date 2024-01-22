import os

from PIL import Image, ImageDraw, ImageFont

def find_path(png_name):
    """
    Trouve le chemin d'un png depuis un dictionnaire jusqu'à un dossier principal.

    Args:
    - png_name (str) : Nom du fichier png.
    - data_dict (dict) : Dictionnaire contenant les données.
    - main_folder (str) : Nom du dossier principal.

    Returns:
    - str : Chemin complet du png.
    """
    main_folder = "/Users/emmanuellandau/Documents/emoji_bibliothèque"
    for racine, _, fichiers in os.walk(main_folder):
        if png_name in fichiers:
            return os.path.join(racine, png_name)
    return None
def emoji_to_unicode(emoji):
    return 'a' + ' '.join(['\\U{0:08x}'.format(ord(char)) for char in emoji])
def convert_emoji(unicode_text, folder):
    font = r"/System/Library/Fonts/Apple Color Emoji.ttc"
    fnt = ImageFont.truetype(font, size=64, layout_engine=ImageFont.LAYOUT_RAQM)
    # Obtenez les dimensions du texte/emoji
    unicode_text = emoji_to_unicode(unicode_text).encode().decode('unicode_escape').replace(" ", "")
    print(unicode_text)
    text_width, text_height = fnt.getsize(unicode_text)
    im = Image.new("RGBA", (text_width // 2, text_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    # Calculez la position pour centrer l'émoji dans l'image
    x_pos = -64
    y_pos = 0
    draw.text((x_pos, y_pos), unicode_text, fill="white", embedded_color=True, font=fnt)
    # im.show()
    im.save(folder+unicode_text+".png")

# convert_emoji("🤣", "/Users/emmanuellandau/PycharmProjects/SubtiPy/suggesterLab")
# from PIL import Image, ImageDraw, ImageFont
#
# back_ground_color = (50, 50, 50)
#
# im = Image.new("RGB", (500, 200), back_ground_color)
# draw = ImageDraw.Draw(im)
#
# font = ImageFont.truetype('/System/Library/Fonts/Apple Color Emoji.ttc', 64)
#
# unicode_text = "\U0001f602"
# draw.text((10, 100), unicode_text, font=font, embedded_color=True)
# im.show()
