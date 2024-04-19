# CT_getROP

温度，圧力，化学種組成のcsvファイルから，生成速度を計算するスクリプト  

## get_reactions_ROP.py
それぞれの素反応に対する生成速度を計算  
出力されるcsvは，((num_reactions, num_timestep))の形式  

## get_species_ROP.py
それぞれの化学種に対する生成速度を計算  
出力されるcsvは，((num_species, num_timestep))の形式  