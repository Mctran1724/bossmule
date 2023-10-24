import pandas as pd

crystal_prices = pd.read_csv("bossmule\crystal_prices.csv")

boss_list = list(crystal_prices['Boss'].unique())
modes = list(crystal_prices['Mode'].unique())

class Crystal:
    def __init__(self, boss: str, mode: str, pt_size: int, time: int) -> None:
        price_string = crystal_prices.loc[(crystal_prices['Boss']==boss)&(crystal_prices['Mode']==mode), 'Crystal Price'].values[0]
        price = int(price_string.replace(',',""))
        self.crystal_value = price/pt_size
        self.clear_time = time
        self.boss = boss
        self.mode = mode

    def __repr__(self) -> str:
        return f"{self.mode} {self.boss} in {self.clear_time} minutes: {self.crystal_value}"

if __name__=='__main__':
    print(boss_list, modes)
    
    