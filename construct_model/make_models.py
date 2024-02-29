import tensorflow as tf           # библиотека машинного обучения
from prepare_data.constants import GLASS_COLS

GLASS = len(GLASS_COLS)

model_prepprice_path_colab = "/content/drive/Othercomputers/My_comp/Документы/Note_books/Тестовые работы/Alex_Glass/Project_glass/predprice/model"

def baseline(input_shape,
              pred_num,
              activ_out,
              depth,
              nerons = (128,32),
              frame = (2,2),
             ):
    
    layer = tf.keras.layers

    def convs(x, n, f, rate, ln = False):
        x = layer.Conv1D(n, f, padding = "same",
                        dilation_rate = rate,
                        activation="sigmoid")(x)
        x = layer.LayerNormalization()(x) if ln else x
        return x
    
    inputs = layer.Input(shape = input_shape)
    x_1 = convs(x = inputs[:,:,:-GLASS], n = nerons[0],  f = frame[0], rate = 2, ln = True)
    y_1 = convs(x = inputs[:,:,:-GLASS], n = nerons[0], f = frame[0], rate = 4, ln = True)
    u_1 = convs(x = inputs[:,:,:-GLASS], n = nerons[0], f = frame[0], rate = 8, ln = True)
    v_1 = convs(x = inputs[:,:,:-GLASS], n = nerons[0], f = frame[0], rate = 16, ln = True)

    x_2 = convs(x = inputs[:,:,-GLASS:], n = nerons[1],  f = frame[1], rate = 2, ln = True)
    y_2 = convs(x = inputs[:,:,-GLASS:], n = nerons[1], f = frame[1], rate = 4, ln = True)
    u_2 = convs(x = inputs[:,:,-GLASS:], n = nerons[1], f = frame[1], rate = 8, ln = True)
    v_2 = convs(x = inputs[:,:,-GLASS:], n = nerons[1], f = frame[1], rate = 16, ln = True)

    z_1 = layer.concatenate([x_1, y_1, u_1, v_1], axis = -1)
    z_1 = layer.Conv1D(128, frame[1], padding="same", activation="sigmoid")(z_1)
    z_2 = layer.concatenate([x_2, y_2, u_2, v_2], axis = -1)
    z_2 = layer.Conv1D(128, frame[1], padding="same", activation="sigmoid")(z_2)
    z_2 = layer.GlobalMaxPooling1D()(z_2)

    z = layer.Activation("relu")(z_1)
    z = layer.Dropout(0.3)(z)
    z = layer.LayerNormalization()(z)#

    out = layer.LSTM(depth, return_sequences=True)(z)
    out = layer.LSTM(depth//2,  return_sequences=False)(out)
    out = layer.Flatten()(out)
    out = layer.Dense(depth*4, activation='relu')(out)
    out = layer.concatenate([z_2, out], axis = 1)
    
    out = layer.Dropout(0.2)(out)
    out = layer.Dense(pred_num, activation=activ_out)(out)

    return  tf.keras.Model(inputs = inputs, outputs = out)
