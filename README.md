# pgo_simple_gym_stats
Simplified gym stats for all pokemon &amp; move combinations. 

Ready .xls table with headers and ability to input your own IV and level is provided in gym_stats.xls 

Gym attack% (Att%) is relative score based on att*def*sta*[attack dps]

Gym def% (Def%) is relative score based on att*def*sta*[defender dps],
assuming that dodging results in 30% reduction of defender charge move dps.
No energy gain for hp loss is taken into account for Att% or Def%.

To calculate your pokemon's effectiveness on gym attack or defense at its 
current level, these scores should be multiplied by the level effect on the previous sheet.

To adjust to scores to your pokemon's IV, input known IV to the input sheet.
You may also input your pokemon's level, resulting in accordingly scaled Att% and Def%
on the far right of the first sheet.

Training (Train%) gives you the pokemon's relative effectiveness on gym attack
at any fixed CP compared to other 'mons. More precisely, this is:
Att^(-1/2)*Def^(1/4)*Sta^(1/4)*[attack dps]
Level does not affect pokemon's training ability at a fixed CP.

* STAB is taken into account.
* Legacy moves are still on the output list. A bit of need-to-know-basis thing to know which they are.
* All scores are relative to best possible pokemon for the task at 100% IV and max level
* Crits are currently disabled for these scores, as they are for the game.

Hoping this helps someone, has been a big help to me.

I personally mark the Att%, Def%, Train% and level effect with IV and move types
for each of my useful 'mons, using 2 digits for each attribute and single char per move type.

I have bolded top 100 Att% 'mons (move combos), underlined top 100 Def% 
and put the top 100 Train% into italics.

Input data and calculations / ugly scripts can be found at:
https://github.com/dosi/pgo_simple_gym_stats


The python script that was used to create a base .csv which turned into the .xls can be found at all_entry_combinations_to_val_pairs.py.

Based on data from: https://gist.github.com/ryankane/daa3aa2de9fce01bbd12e60275218636 .
Crit rates and recent (2016-07-30) changes to powers of moves are based on data from: https://thesilphroad.com/research -> moves.

Data is renamed and replicated under the json_data folder of this project.

Basic formulas based on: https://drive.google.com/file/d/0B0TeYGBPiuzaenhUNE5UWnRCVlU/view

- dosibjrn

