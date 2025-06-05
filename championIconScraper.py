import os
import requests
from tqdm import tqdm
import json

class ChampionIconScraper:
    def __init__(self, output_dir='./champions'):
        self.ddragon_url = "https://ddragon.leagueoflegends.com"
        self.cdragon_base_url = "https://raw.communitydragon.org/latest/game/assets/characters"
        self.champion_map = {}
        self.output_dir = output_dir
        self.special_names = {
            'ambessa': 'ambessa_circle_0.domina.png',
            'anivia': 'cryophoenix_square.png',
            'blitzcrank': 'steamgolem_circle.png',
            'chogath': 'greenterror_circle.png',
            'leblanc': 'leblanc_circle_0.leblanc_rework.png',
            'rammus': 'armordillo_circle.png',
            'orianna': 'oriana_circle.png',
            'shaco': 'jester_circle.png',
            'teemo': 'teemo_circle_0.asu_teemo.png',
            'viktor': 'viktor_circle_0.viktorvgu.png',
            'zilean': 'chronokeeper_circle.png'
        }

        os.makedirs(self.output_dir, exist_ok=True)

    def get_latest_version(self):
        return requests.get(f"{self.ddragon_url}/api/versions.json").json()[0]

    def get_champion_names(self, version):
        url = f"{self.ddragon_url}/cdn/{version}/data/en_US/champion.json"
        champions = requests.get(url).json()['data']
        return champions.keys()

    def download_icon(self, url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
        return False

    def scrape_icons(self):
        version = self.get_latest_version()
        champion_names = self.get_champion_names(version)
        failed = 0
        

        for i, champ_name in enumerate(tqdm(champion_names, desc="Scraping champion icons")):
            self.champion_map[i] = {
                "champ_name": champ_name,
                "champ_images": 1
            }
            lower = champ_name.lower()
            champ_dir = os.path.join(self.output_dir, champ_name)
            os.makedirs(champ_dir, exist_ok=True)

            success = False
            if lower in self.special_names:
                path = f"{self.cdragon_base_url}/{lower}/hud/{self.special_names[lower]}"
                success = self.download_icon(path, os.path.join(champ_dir, "1.png"))
            else:
                urls = [
                    f"{self.cdragon_base_url}/{lower}/hud/{lower}_circle.png",
                    f"{self.cdragon_base_url}/{lower}/hud/{lower}_circle_0.png",
                    f"{self.cdragon_base_url}/{lower}/hud/{lower}_circle_0.{lower}.png"
                ]
                for url in urls:
                    if self.download_icon(url, os.path.join(champ_dir, "1.png")):
                        success = True
                        break

            if not success:
                print(f"\n❌ Failed: {champ_name}")
                print(f"Check URL: {self.cdragon_base_url}/{lower}/hud/")
                failed += 1
                continue

            # Handle special forms
            if lower == 'kayn':
                self.champion_map[i]["champ_images"] += 2
                self.download_icon(f"{self.cdragon_base_url}/kayn/hud/kayn_ass_circle.png",
                                   os.path.join(champ_dir, "2.png"))
                self.download_icon(f"{self.cdragon_base_url}/kayn/hud/kayn_slay_circle.png",
                                   os.path.join(champ_dir, "3.png"))

            if lower == 'gnar':
                self.champion_map[i]["champ_images"] += 1
                self.download_icon(f"{self.cdragon_base_url}/gnarbig/hud/gnarbig_circle.png",
                                   os.path.join(champ_dir, "2.png"))

        with open("champMap.json", 'w') as f:
                json.dump(self.champion_map, f, indent=4)
        print(f"\n✅ Scraping complete. Total failures: {failed}/{len(champion_names)}")


if __name__ == '__main__':
    scraper = ChampionIconScraper(output_dir='./champion_icons')
    scraper.scrape_icons()