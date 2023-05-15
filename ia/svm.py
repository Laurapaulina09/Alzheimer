
import cv2
import os
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from sklearn.metrics import confusion_matrix
import pickle

# Definir la ruta de la carpeta principal que contiene las subcarpetas de imágenes
def Modelo(pathImagen):
    import numpy as np
    path = os.getcwd()+'/Dataset'

    # Crear una lista de imágenes y etiquetas correspondientes
    images = []
    labels = []

    # Leer las imágenes y asignarles etiquetas
    for folder_name in os.listdir(path):
        folder_path = os.path.join(path, folder_name)
        if os.path.isdir(folder_path):
            for img_name in os.listdir(folder_path):
                img_path = os.path.join(folder_path, img_name)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                images.append(img)
                labels.append(folder_name)
    # Convertir las listas a matrices numpy
    
    images = np.array(images)
    labels = np.array(labels)

    # Dividir los datos en conjunto de entrenamiento y conjunto de prueba
    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

    # Preprocesamiento de las imágenes
    X_train = X_train.reshape(X_train.shape[0], -1)
    X_test = X_test.reshape(X_test.shape[0], -1)

    # Crear un modelo SVM
    svm_model = SVC(kernel='linear', probability=True)

    # Entrenar el modelo SVM
    svm_model.fit(X_train, y_train)

    # Realizar predicciones en el conjunto de prueba
    y_pred = svm_model.predict(X_test)

    # Calcular las metricas de evaluacion  del modelo
    accuracy = accuracy_score(y_test, y_pred)
    precision=precision_score(y_test, y_pred,average='macro')
    recall=recall_score(y_test, y_pred,average='macro')
    f1=f1_score(y_test, y_pred,average='macro')


    print("Exactitud del modelo SVM: ", accuracy)
    print("Precisión del modelo SVM: ", precision)
    print("Sensibilidad del modelo SVM: ",recall)
    print("Puntaje F1 del modelo SVM",f1)

    # Obtener las predicciones del modelo
    y_pred = svm_model.predict(X_test)

    # Calcular la matriz de confusión
    conf_matrix = confusion_matrix(y_test, y_pred)
    print('\nMatriz de confusión')
    print(conf_matrix)


    #cargar nuevas imagenes 
    with open('modelo_svm.pickle', 'wb') as f:
        pickle.dump(svm_model, f)


    with open('modelo_svm.pickle', 'rb') as f:
        modelo = pickle.load(f)

    from PIL import Image
    import numpy as np

    # Carga la imagen y conviértela en una matriz NumPy
    imagen = Image.open(pathImagen)
    imagen = imagen.convert('L')  # Convierte la imagen a escala de grises
    imagen = imagen.resize((128, 128))  # Cambia el tamaño de la imagen a 128x128
    imagen = np.array(imagen)

    imagen = imagen.flatten()

    prediccion = modelo.predict([imagen])

    return prediccion[0]