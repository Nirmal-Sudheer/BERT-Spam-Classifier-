

import pandas as pd
df=messages = pd.read_csv('/content/SMSSpamCollection.txt', sep='\t',
                           names=["label", "message"])
df.head()

df.shape

X=list(df['message'])

y=list(df['label'])

y

y=list(pd.get_dummies(y,drop_first=True)['spam'])

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

"""<h1>Steps for Transformers <br>

1.Call pretrained model <br>
2.Call the tokenizer <br>
3.Convert encodings into dataset object <br>

"""

!pip install transformers

from transformers import DistilBertTokenizerFast
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

train_encodings = tokenizer(X_train, truncation=True, padding=True)
test_encodings = tokenizer(X_test, truncation=True, padding=True)
#Padding to make all sentences the same size and truncation is used to remove the widespaces

y_train

import tensorflow as tf

train_dataset = tf.data.Dataset.from_tensor_slices((
    dict(train_encodings),#Used to create a dictionary from a iterable element like a list/tuple
    y_train
))

test_dataset = tf.data.Dataset.from_tensor_slices((
    dict(test_encodings),
    y_test
))

from transformers import TFDistilBertForSequenceClassification, TFTrainer, TFTrainingArguments
#SeqClass. used for sentiment analysis not question answering

training_args = TFTrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=2,              # total number of training epochs
    per_device_train_batch_size=8,  # batch size per device during training
    per_device_eval_batch_size=16,   # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
    logging_steps=10,
)

with training_args.strategy.scope():
    model = TFDistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")

trainer = TFTrainer(
    model=model,                         # the instantiated Transformer
    args=training_args,                  # training arguments, defined above
    train_dataset=train_dataset,         # training dataset
    eval_dataset=test_dataset             # evaluation dataset
)

trainer.train()

trainer.evaluate(test_dataset)#Returns a low value.



trainer.predict(test_dataset)#Returns all the pred values.

trainer.predict(test_dataset)[1].shape

print(output=trainer.predict(test_dataset)[1])

#Create confusion matrix
from sklearn.metrics import confusion_matrix

cm=confusion_matrix(y_test,output)
print(cm)

#Save model
trainer.save_model('senti_model')

