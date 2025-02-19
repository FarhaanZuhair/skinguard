import tensorflow as tf
import os
from django.conf import settings

# Load the trained model
model_path = os.path.join(settings.BASE_DIR, 'model', 'model.h5')
model = tf.keras.models.load_model(model_path)

def predict_disease(image_path):
    # Load and preprocess the image
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    # Make predictions
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    # Assuming you have a list of class names
    class_names = ['Class1', 'Class2', 'Class3']
    predicted_class = class_names[tf.argmax(score)]
    confidence = 100 * tf.reduce_max(score)

    return predicted_class, confidence