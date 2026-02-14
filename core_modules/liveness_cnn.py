import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import Xception
from tensorflow.keras.applications.xception import preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from sklearn.utils import class_weight

# --- CONFIGURATION ---
# Enabling XLA compiler can provide a small speed boost on some CPUs
tf.config.optimizer.set_jit(True)

# 224x224 is faster for a hackathon demo than the standard 299x299
IMG_SIZE = (224, 224) 
MODEL_PATH = 'core_modules/xception_deepfake.h5'
BATCH_SIZE = 32 # Higher batch size is generally faster on modern CPUs

def build_xception_model():
    """Initializes Xception with a custom classification head."""
    # Load base model with pre-trained ImageNet weights
    base_model = Xception(weights='imagenet', include_top=False, input_shape=(*IMG_SIZE, 3))
    
    # Freeze the base model to preserve features
    base_model.trainable = False
    
    # Custom classification head
    x = GlobalAveragePooling2D()(base_model.output)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x) # Dropout helps prevent overfitting on small data
    predictions = Dense(1, activation='sigmoid')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Adam optimizer with a stable learning rate
    model.compile(optimizer=Adam(learning_rate=0.001), 
                  loss='binary_crossentropy', 
                  metrics=['accuracy'])
    return model

def train_model():
    """Trains the model for 3 epochs with Turbo Mode settings."""
    if not os.path.exists('dataset'):
        print("[ERROR] 'dataset' folder not found. Run extraction script first.")
        return

    # Data Generators
    datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input, # Required for Xception
        horizontal_flip=True,
        validation_split=0.2
    )

    train_gen = datagen.flow_from_directory(
        'dataset',
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='training'
    )

    val_gen = datagen.flow_from_directory(
        'dataset',
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='validation'
    )

    # Calculate Class Weights to handle your 2.5:1 imbalance
    cw = class_weight.compute_class_weight(
        'balanced', 
        classes=np.unique(train_gen.classes), 
        y=train_gen.classes
    )
    cw_dict = dict(enumerate(cw))
    print(f"[INFO] Applied Class Weights: {cw_dict}")

    model = build_xception_model()

    # --- THE 3-EPOCH TURBO FIT ---
    # We use steps_per_epoch to look at a representative sample each pass
    print("🚀 Starting 3-Epoch Training Session...")
    model.fit(
        train_gen,
        steps_per_epoch=100, 
        validation_data=val_gen,
        validation_steps=20,
        epochs=3, # <--- Set to 3 as requested
        class_weight=cw_dict,
        verbose=1
    )

    # Save the resulting model
    model.save(MODEL_PATH)
    print(f"✅ SUCCESS: Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
