

<div align="center">    
 
# ECG Classifier for LBBB Detection

![{B65A14C1-DC1F-4CDD-8B33-0172456F5D4B}](https://github.com/user-attachments/assets/7814871f-ee07-4c80-99df-6043d61ae3b3)

 



</div>

## 📃Table of Content
- [Description](#-description)
- [Our Progress](#-our-progress)
- [Results](#-results)
- [Screenshots](#-screenshots)
 
<h3 id="-description">🚀Description</h3>   

An AI model using various machine learning algorithms like KNN and SVM for detecting Left Bundle Branch Block (LBBB) in ECG signals. The project includes data preprocessing, feature extraction, model training, evaluation, and deployment through a GUI application.

-------------      
 
<h2 id="-our-progress">⏳Our Progress</h3>

### Data Preprocessing
The data preprocessing step involves:
1. Removing noise from the ECG signals using a **Butterworth bandpass filter**.
2. Normalizing the signals to a standard range to ensure consistent feature extraction.

---

### Feature Extraction
Features are extracted from the preprocessed signals using **wavelet transforms**.  
Statistical features such as:
- Mean
- Standard deviation
- Skewness
- Kurtosis  
are calculated from the wavelet coefficients.

---

### Model Training and Evaluation
Various machine learning models are trained and evaluated on the extracted features, including:
- **K-Nearest Neighbors (KNN)**
- **Support Vector Machine (SVM)**
- **Random Forest**
- **Decision Tree**
- **Naive Bayes**

The best model is selected based on **accuracy** and other evaluation metrics.

---

### Deployment
The best-performing model (**KNN**) is deployed using a **GUI application**.  
This application allows users to:
- Input ECG signals
- Receive a classification result: **Normal** or **LBBB**

![{13FBAD89-C737-46B1-A3AE-C90534AFE065}](https://github.com/user-attachments/assets/3b3b6e00-6708-4fd5-b014-5e0011b06694)


 -------------       
<h3 id="-results">🔬Results</h3>


| Model Name | Train Accuracy | Test Accuracy |
|---|---|---|
| K-Nearest Neighbors | 99% | 100% |
| Naive Bayes  | 100% | 53% |
| Support Vector Machine (SVM) | 100% | 47% |
| Decision Tree | 100% | 35% |
| Random Forest | 100% | 35% |
  


--------------    
<h3 id="-screenshots">📸 Screenshots</h3>

### LBBB detected

![image](https://github.com/user-attachments/assets/4de69a93-f5eb-446c-b0a5-b53ea66f834d)

![image](https://github.com/user-attachments/assets/8e989ddc-646b-4fce-95b9-aa4ce1cbba21)

### well Person

![image](https://github.com/user-attachments/assets/20aea936-09f6-4fed-aa3a-faeb4db9fb2e)

![image](https://github.com/user-attachments/assets/03af1a08-c07c-4e8c-94da-5e1832d1eb08)





  
