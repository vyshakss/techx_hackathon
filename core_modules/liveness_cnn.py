import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def build_deepfake_detector():
    """
    Builds a CNN architecture for binary classification (Real vs Fake).
    """
    model = Sequential([
        # 1. Feature Extraction (Looking for pixel artifacts, blur, and unnatural edges)
        Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        MaxPooling2D(pool_size=(2, 2)),
        
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        
        # 2. Flattening the 2D matrices into a 1D array for the Dense layers
        Flatten(),
        
        # 3. Fully Connected Layers (Making the actual decision)
        Dense(512, activation='relu'),
        Dropout(0.5), # Drops 50% of neurons randomly to prevent overfitting
        
        # 4. Output Layer (Binary Classification: 0 for Real, 1 for Fake)
        Dense(1, activation='sigmoid') 
    ])
    
    # Compile the model with Adam optimizer and binary crossentropy loss
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    
    return model

def train_and_save_model():
    """
    Simulates training the model on the Celeb-DF dataset and saves it as an .h5 file.
    """
    print("Building CNN Architecture...")
    model = build_deepfake_detector()
    model.summary()
    
    # --- NOTE FOR THE HACKATHON ---
    # To actually train this, you need to download the Celeb-DF dataset, 
    # put the real faces in a 'data/real' folder, and fake faces in a 'data/fake' folder.
    # Below is the logic you will use once you download those images.
    
    print("\nPreparing ImageDataGenerators...")
    # This automatically loads images from your folders and scales the pixel values
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
    
    # In a real run, you would uncomment these to load the actual dataset:
    '''
    train_generator = datagen.flow_from_directory(
        'data/',
        target_size=(224, 224),
        batch_size=32,
        class_mode='binary',
        subset='training'
    )
    
    validation_generator = datagen.flow_from_directory(
        'data/',
        target_size=(224, 224),
        batch_size=32,
        class_mode='binary',
        subset='validation'
    )
    
    print("\nTraining the model (this will take time)...")
    model.fit(train_generator, epochs=10, validation_data=validation_generator)
    '''
    
    # 5. Save the trained weights to the .h5 file
    os.makedirs('models', exist_ok=True)
    save_path = 'models/deepfake_model.h5'
    
    # For now, we are saving the "untrained" initialized model just so you have the file structure
    model.save(save_path)
    print(f"\nSuccess! Model architecture saved to {save_path}")

# Run the script to generate the .h5 file
if __name__ == "__main__":
    train_and_save_model()
