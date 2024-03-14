import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras import layers
import pandas as pd 
# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)

from IPython import display

def pd_to_tf(dataFrame, features):
    # Create a symbolic input
    input = tf.keras.Input(shape=(), dtype=tf.float32)
    # Perform a calculation using the input
    result = 2*input + 1
    #calc = tf.keras.Model(inputs=input, outputs=result)

    # Build a set of symbolic tf.keras.Input objects
    # It will match the name and data type of the columns in the original CSV
    inputs = {}
    for name, column in features.items():
        dtype = column.dtype
        if dtype == object:
            dtype = tf.string
        else:
            dtype = tf.float32

        inputs[name] = tf.keras.Input(shape=(1,), name=name, dtype=dtype)
    

    # Concatenate the numeric inputs
    # then run them through a normalization layer
    numeric_inputs = {name:input for name,input in inputs.items()
                  if input.dtype==tf.float32}

    x = layers.Concatenate()(list(numeric_inputs.values()))
    norm = layers.Normalization()
    norm.adapt(np.array(dataFrame[numeric_inputs.keys()]))
    all_numeric_inputs = norm(x)

    # Collect all the symbolic preprocessing units
    # so we can concatenate them layer
    preprocessed_inputs = [all_numeric_inputs]

    # String inputs need to mapped to integer indices in a vocabulary
    # This is done by making a vocabulary out of the features in the original CSV
    # The indices are then converted into float32 through CategoryEncoding
    for name, input in inputs.items():
        if input.dtype == tf.float32:
            continue

        lookup = layers.StringLookup(vocabulary=np.unique(features[name]))
        one_hot = layers.CategoryEncoding(num_tokens=lookup.vocabulary_size())

        x = lookup(input)
        x = one_hot(x)
        preprocessed_inputs.append(x)

    # We concatenate the results from both preprocessed inputs
    preprocessed_inputs_cat = layers.Concatenate()(preprocessed_inputs)

    # From the preprocessed inputs
    # we create a model that can handle the preprocessing 
    preprocessing = tf.keras.Model(inputs, preprocessed_inputs_cat)

    # Convert the dataframe into a dictionary of tensors
    df_features_dict = {name: np.array(value) 
        for name, value in fraud_features.items()}

    features_dict = {name:values[:1] for name, values in df_features_dict.items()}
    preprocessing(features_dict)

    return preprocessing, df_features_dict, inputs

# Creates a model using our CSV data
# The CSV data needs to be preprocessed
# because TensorFlow can not directly use
# pandas DataFrames
def fraud_model(preprocessing_head, inputs):
    body = tf.keras.Sequential([
        layers.Dense(64),
        layers.Dense(1)
    ])

    preprocessed_inputs = preprocessing_head(inputs)
    result = body(preprocessed_inputs)
    model = tf.keras.Model(inputs, result)

    model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                optimizer=tf.keras.optimizers.Adam())
    return model

def df_to_dataset(dataframe, target, shuffle=True, batch_size=32):
    dataframe = dataframe.copy()
    labels = dataframe.pop(target)
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)
    return ds

train_data = pd.read_csv("archive/fraudTrain.csv")  # Returns a pandas DataFrame type

# Shorten the data into 500 to train with, rather than all of it for now
frauds = train_data.loc[train_data['is_fraud'] == 1]
train_data = pd.concat([train_data.sample(n=7000), frauds.sample(n=3000)])

# Get the features and target we are going to be fitting our model to
train_data.dropna(ignore_index=True)
fraud_features = train_data.copy()
fraud_target = fraud_features.pop('is_fraud')

test_data = pd.read_csv('archive/fraudTest.csv')
test_data = test_data.sample(n=5000)
test_features = test_data.copy()
test_target = test_features.pop('is_fraud')

fraud_preprocessing, fraud_features_dict, inputs = pd_to_tf(train_data, fraud_features)

model = fraud_model(fraud_preprocessing, inputs)
model.fit(x=fraud_features_dict, y=fraud_target, epochs=10)

pred = model.predict(df_to_dataset(test_data, 'is_fraud', shuffle=False, batch_size=len(test_data)), verbose=0)

_, test_features_dict, _ = pd_to_tf(test_data, test_features)

evaluated = model.evaluate(x=test_features_dict, y=test_target)
print(evaluated)


#m = tf.keras.metrics.Accuracy(name='is_fraud')
#m.update_state(pred)
#print(m.result().numpy())