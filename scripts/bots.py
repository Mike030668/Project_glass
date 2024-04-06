import numpy as np

def cond_long (state,
               id_pr_up,
               id_tr_up,
               id_pr_lw,
               id_tr_lw,
               correct_price,
               id_pr_up_tresh,
               id_tr_lw_tresh,
               tresh_hold
               ):

    """
    id_pr_up - id предсказаний выше текущей цены [0,1] из индексов [0,1,2,3,4]
    id_tr_up - тренд рост id из индексов [0,1,2,3,4]
    id_pr_lw - id предсказаний ниже текущей цены [0,1,3] из индексов [0,1,2,3,4]
    id_tr_lw - тренд падения id из индексов [0,1,2,3,4]
    correct_price - корректируем ли цену сравнивая прошлое и текцщее
                    cur_price - по разнице предскахания с текущей
                    pred_price - по разнице предскаханий с шага t и t-1
                    False - не корректируем

    id_pr_up_tresh - id предсказаний выше текущей с учетом tresh_hold
    id_tr_lw_tresh - id предсказаний ниже текущей цены с учетом tresh_hold
    tresh_hold - в % от cur_price
    """
    cur_price = state["last_price"] #[-1]
    # коррекция 0
    delta = 0
    # корректор предсказания цены от сравнения прошлого предсказание и текцщей цены
    if correct_price == "Michal":
        delta = state["pred_prices"][-2][0] - cur_price
    
    # корректор предсказания цены от сравнения прошлого предсказание и текцщего предсказания следующей цены
    elif correct_price == "Aleksei":
        delta = state["pred_prices"][-2][1] - state["pred_prices"][-1][0]

    # Вход лонг
    # Покупаем когда
    # контроль по цене если заданы индексы
    if len(id_pr_up):
        if correct_price == "Michal":
            # Сетка 1 показывает id_pr_up предсказаний выше текущей цены И
            cond_1 =  all(state["pred_prices"][-1][id_pr_up] - delta > cur_price)

        elif correct_price == "Aleksei":
            # текущая цена< приземленный прогноз
            cond_1 =  cur_price < cur_price - delta 

    # одобряем если нет контроля
    else:
        cond_1 = True

    # контроль по цене c tresh_hold если заданы индексы
    if len(id_pr_up_tresh):
        if correct_price == "Michal":
             # Сетка 1 показывает id_pr_up предсказаний выше текущей цены И
            cond_1_t =  all(state["pred_prices"][-1][id_pr_up_tresh] - delta > cur_price*(100 + tresh_hold)/100)
        
        elif correct_price == "Aleksei":
            cond_1_t =  cur_price*(100 + tresh_hold)/100 < cur_price - delta

    # одобряем если нет контроля
    else:
        cond_1_t = True

    # контроль по тренду если заданы индексы
    if len(id_tr_up):
        # Сетка 2 изменила состояние Флэт или Падение
        cond_2 = all(state["pred_trend"][-2] < 1)
        # на Рост по всем id_tr_up.
        cond_3 = all(state["pred_trend"][-1][id_tr_up] == 1)
        cond_4 = cond_2 and cond_3
    # одобряем если нет контроля
    else:
        cond_4 = True
    # Вход лонг
    enter_long = cond_1 and cond_4 and cond_1_t


    # Выход из лонга
    # Продаем позицию если
    # контроль по цене если заданы индексы
    if len(id_pr_lw):
        if correct_price == "Michal":
            # Сетка 1 показывает id_pr_lw предсказания ниже текущей цены И
            cond_5 =  all(state["pred_prices"][-1][id_pr_lw] - delta < cur_price)

        elif correct_price == "Aleksei":
            cond_5 =  cur_price > cur_price - delta 

    # одобряем если нет контроля
    else:
        cond_5 = True

    # контроль по цене c tresh_hold если заданы индексы
    if len(id_tr_lw_tresh):
         if correct_price == "Michal":
            # Сетка 1 показывает id_pr_up предсказаний выше текущей цены И
            cond_5_t =  all(state["pred_prices"][-1][id_tr_lw_tresh] - delta < cur_price*(100 - tresh_hold)/100)

         elif correct_price == "Aleksei":
            cond_5_t =   cur_price*(100 + tresh_hold)/100 > cur_price - delta

    # одобряем если нет контроля
    else:
        cond_5_t = True


    # контроль по тренду если заданы индексы
    if len(id_tr_lw):
        # Сетка 2 изменила состояние на Падение на id_pr_lw минутах.
        a = np.array(state["pred_trend"][-2][id_tr_lw])
        cond_6 = all(a >= 0)
        a = np.array(state["pred_trend"][-1][id_tr_lw])
        cond_7 = all(a == -1)
        cond_8 = cond_6 and cond_7
    # одобряем если нет контроля
    else:
        cond_8 = True


    # Выход из лонга
    exit_long = cond_5 and cond_8 and cond_5_t

    # Вход лонг
    if enter_long and not exit_long : return 1  #  
    # Выход из лонга
    elif exit_long and not enter_long : return -1  #  
    # спим
    else:  return 0



def cond_short(state,
               id_pr_up,
               id_tr_up,
               id_pr_lw,
               id_tr_lw,
               correct_price,
               id_pr_up_tresh,
               id_tr_lw_tresh,
               tresh_hold
                ):

    """
    id_pr_up - id предсказаний выше текущей цены [0,1] из индексов [0,1,2,3,4]
    id_tr_up - тренд рост id из индексов [0,1,2,3,4]
    id_pr_lw - id предсказаний ниже текущей цены [0,1,3] из индексов [0,1,2,3,4]
    id_tr_lw - тренд падения id из индексов [0,1,2,3,4]
    correct_price - корректируем ли цену сравнивая прошлое и текцщее
                    cur_price - по разнице предскахания с текущей
                    pred_price - по разнице предскаханий с шага t и t-1
                    False - не корректируем

    id_pr_up_tresh - id предсказаний выше текущей с учетом tresh_hold
    id_tr_lw_tresh - id предсказаний ниже текущей цены с учетом tresh_hold
    tresh_hold - в % от cur_price
    """
    cur_price = state["last_price"]#[-1]
    # коррекция 0
    delta = 0
    # корректор предсказания цены от сравнения прошлого предсказание и текцщей цены
    if correct_price == "Michal":
        delta = state["pred_prices"][-2][0] - cur_price
    
    # корректор предсказания цены от сравнения прошлого предсказание и текцщего предсказания следующей цены
    elif correct_price == "Aleksei":
        delta = state["pred_prices"][-2][1] - state["pred_prices"][-1][0]

    # Вход шорт
    # Покупаем когда
     # контроль по цене если заданы индексы
    if len(id_pr_lw):
        # Сетка 1 показывает id_pr_lw предсказаний ниже текущей цены И
        if correct_price == "Michal":
            # Сетка 1 показывает id_pr_up предсказаний выше текущей цены И
            cond_1 =  all(state["pred_prices"][-1][id_pr_up] - delta < cur_price)

        elif correct_price == "Aleksei":
            # текущая цена< приземленный прогноз
            cond_1 =  cur_price > cur_price - delta 

    # одобряем если нет контроля
    else:
        cond_1 = True

    # контроль по цене c tresh_hold если заданы индексы
    if len(id_tr_lw_tresh):
        # Сетка 1 показывает id_pr_lw предсказаний ниже текущей цены И
        if correct_price == "Michal":
             # Сетка 1 показывает id_pr_up предсказаний выше текущей цены И
            cond_1_t =  all(state["pred_prices"][-1][id_pr_up_tresh] - delta < cur_price*(100 + tresh_hold)/100)
        
        elif correct_price == "Aleksei":
            cond_1_t =   cur_price*(100 + tresh_hold)/100 > cur_price - delta

    # одобряем если нет контроля
    else:
        cond_1_t = True

    # контроль по тренду если заданы индексы
    if len(id_tr_lw):
        # Сетка 2 изменила состояние Флэт или Рост
        cond_2 = all(state["pred_trend"][-2][id_tr_lw] > -1)
        # Падение по всем пяти минутам.
        cond_3 = all(state["pred_trend"][-1][id_tr_lw] == -1)
        cond_4 = cond_2 and cond_3
    # одобряем если нет контроля
    else:
        cond_4 = True

    # Вход лонг
    enter_short = cond_1 and cond_4 and cond_1_t

    # Выход из шорта
    # Продаем позицию если
    # контроль по цене если заданы индексы
    if len(id_pr_up):
        if correct_price == "Michal":
            # Сетка 1 показывает id_pr_up предсказания выше текущей цены  И
            cond_5 =  all(state["pred_prices"][-1][id_pr_up] - delta > cur_price)

        elif correct_price == "Aleksei":
            cond_5 =  cur_price > cur_price - delta 

    # одобряем если нет контроля
    else:
        cond_5 = True

    # контроль по цене c tresh_hold если заданы индексы
    if len(id_pr_up_tresh):
        if correct_price == "Michal":
            # Сетка 1 показывает id_pr_up_tresh предсказания выше текущей цены  И
            cond_5_t =  all(state["pred_prices"][-1][id_pr_up_tresh] - delta > cur_price*(100 + tresh_hold)/100)

        elif correct_price == "Aleksei":
            cond_5_t =   cur_price*(100 + tresh_hold)/100 < cur_price - delta

    # одобряем если нет контроля
    else:
        cond_5_t = True


    # контроль по цене если заданы индексы
    if len(id_tr_up):
        # Сетка 2 изменила состояние на Рост на  id_tr_up минуте
        a = np.array(state["pred_trend"][-2][id_tr_up])
        cond_6 = all(a <= 0)
        a = np.array(state["pred_trend"][-1][id_tr_up])
        cond_7 = all(a == 1)
        con_8 = cond_6 and cond_7
    # одобряем если нет контроля
    else:
        con_8 = True

    # Выход из шорта
    exit_short = cond_5 and con_8 and cond_5_t

    # Вход шорта
    if enter_short and not exit_short: return -1 #  
    # Выход из шорта
    elif exit_short and not enter_short: return 1 #   
    # спим
    else:  return 0
    
#######################################################################################

def long_Short(action,
               lg_id_pr_up = [],
               lg_id_tr_up = [],
               lg_id_pr_lw = [],
               lg_id_tr_lw = [],
               sh_id_pr_up = [],
               sh_id_tr_up = [],
               sh_id_pr_lw = [],
               sh_id_tr_lw = [],
               correct_price = False,
               lg_id_pr_up_tresh = [],
               lg_id_pr_lw_tresh = [],
               sh_id_pr_up_tresh = [],
               sh_id_pr_lw_tresh = [],
               tresh_hold = 0.
 ):
    """
    декоратор для управления функциями
    action in ('long', 'short', 'mix')
    """
    def mix_action (state, long_action, short_action):
      # получаем индексы шорта
      short_act = short_action(state,
                               sh_id_pr_up, sh_id_tr_up,
                               sh_id_pr_lw, sh_id_tr_lw,
                               correct_price,
                               sh_id_pr_up_tresh, sh_id_pr_lw_tresh,
                               tresh_hold
                               )
      # получаем индексы лонга
      long_act = long_action(state,
                             lg_id_pr_up, lg_id_tr_up,
                             lg_id_pr_lw, lg_id_tr_lw,
                             correct_price,
                             lg_id_pr_up_tresh, lg_id_pr_lw_tresh,
                             tresh_hold
                             )

      # используем long, short или оба
      if action == 'long' : return [long_act, 0]
      elif action == 'short' : return [0, short_act]
      else:
          return  [long_act, short_act], correct_price
      
    return mix_action