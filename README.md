# pgo_simple_gym_stats
Simplified gym stats for all pokemon &amp; quick move combinations. 

Ready .xls table with headers is provided in pokemon_go_gym_simplestats.xls 

As mentioned in table header, the simplified stats are:

"Attack points" : Quick Move power per second * Pokemon's Base Attack. Takes into account *1.25 from matching types

"Defense points" : Simply Base Stamina * Base Defense

I made this for simple quick reference on what is good and what is not.

The multiplicative nature of the points might not best represent the full capabilities of the pokemon + move combinations.

The python script that was used to create a base .csv which turned into the .xls can be found at all_entry_combinations_to_val_pairs.py.

Based on data from: https://gist.github.com/ryankane/daa3aa2de9fce01bbd12e60275218636

Data is renamed and replicated under the json_data folder of this project

