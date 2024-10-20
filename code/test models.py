import pickle
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def load_model_and_preprocessor(file_path):

    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data['model'], data['label_encoder'], data['preprocessor']

def test_model(model, label_encoder, preprocessor, test_data):

    X_test = preprocessor.transform(test_data.drop('Type of connection', axis=1))
    y_test = label_encoder.transform(test_data['Type of connection'])

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    confusion = confusion_matrix(y_test, y_pred)

    return accuracy, report, confusion, y_test, y_pred

def accuracy_per_class(confusion, label_encoder):

    accuracy = {}
    for i in range(confusion.shape[0]):
        class_accuracy = confusion[i, i] / sum(confusion[i, :]) if sum(confusion[i, :]) > 0 else 0
        class_name = label_encoder.inverse_transform([i])[0]
        accuracy[class_name] = class_accuracy
    return accuracy

def save_results(file_path, accuracy, report, confusion, class_accuracy):

    with open(file_path, 'w') as f:
        f.write(f'Accuracy: {accuracy:.2f}\n')
        f.write('Classification Report:\n')
        f.write(report)
        f.write('\nConfusion Matrix:\n')
        f.write(f'{confusion}\n')
        f.write('Class Accuracy:\n')
        for class_label, acc in class_accuracy.items():
            f.write(f'Accuracy for class "{class_label}": {acc:.2f}\n')

model_file_path = '/run/media/alessandro/TOSHIBA EXT/BACKUP ENDEAVOUR OS/tesi/dataset mio/Risultati e modelli/Multiclasse/best_knn_model.pkl'
test_data_path = '/run/media/alessandro/TOSHIBA EXT/BACKUP ENDEAVOUR OS/tesi/dataset Coimbra/Dataset_Multiclass.csv'
output_file_path = '/path/to/your/output/results.txt'

test_data = pd.read_csv(test_data_path)
model, label_encoder, preprocessor = load_model_and_preprocessor(model_file_path)
accuracy, report, confusion, y_test, y_pred = test_model(model, label_encoder, preprocessor, test_data)
class_accuracy = accuracy_per_class(confusion, label_encoder)

for class_label, acc in class_accuracy.items():
    print(f'Accuracy for class "{class_label}": {acc:.2f}')

save_results(output_file_path, accuracy, report, confusion, class_accuracy)
