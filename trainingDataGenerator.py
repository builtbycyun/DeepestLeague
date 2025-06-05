import random
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
class TrainingDataGenerator:
    def __init__(self):
        self.champ_map = {}
        with open("champMap.json", "r") as f:
            self.champ_map = eval(f.read())

    def generate_map(self):
        selected_champs = random.sample(range(0,len(self.champ_map)), 10)

        map_path = ['lolmap.png','lolmap_bounties.png','lolmap_hextech.png'][random.randint(0,2)]
        map = Image.open(f'assets/{map_path}').convert("RGBA")

        enhancer = ImageEnhance.Brightness(map)
        factor = random.randint(7, 15) / 10
        map = enhancer.enhance(factor)

        map = map.resize((469, 469))

        for champ in selected_champs:
            champ_name = self.champ_map[champ]['champ_name']
            champ_image = random.randint(1, self.champ_map[str(champ)]['champ_images'])
            
            img = Image.open(f"champions/{champ_name}/{str(champ_image)}.png").convert("RGBA")
            h, w = img.size
            


        map.show()



        



if __name__ == '__main__':
    generator = TrainingDataGenerator()
    generator.generate_map()