## Генетический поиск нейронок
- Проведены работы по созданию отдельно репозитория [генетического поиска](https://github.com/Mike030668/Genetic_generation_net)
- код модифицирован для применения как к ценовым, так и трендовым моделям

##### ноутбуки для поиска моделей
- [ценовая](https://github.com/Mike030668/Project_glass/blob/master/notebooks_gen/gen_price_net_seach.ipynb)
- [трендовая](https://github.com/Mike030668/Project_glass/blob/master/notebooks_gen/train_gen_trend_model.ipynb)

##### как пользоваться?
- настроено для работы в Colab и GPU
- изначально генетика стартует с данных на репозитории, которые были полученны поиском при работе над задачей
  
  <img src="images/gen_seach_1.png" alt="png"  width="400"/>
  
- можно стартавать с пустого состояния
  
  <img src="images/gen_seach_2.png" alt="png"  width="400"/>
  
- в обоих случаях пишется в копию репозиторя в Colab, скачаного ранее командой `!git clone https://github.com/Mike030668/Project_glass.git -q`
