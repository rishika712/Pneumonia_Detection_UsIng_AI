# Pneumonia Detection Using AI 🧠🫁

This project uses deep learning to detect **pneumonia from chest X-ray images**. It includes a trained CNN model and a user-friendly web interface built with **Streamlit**.

## 🔍 Features

- Upload a chest X-ray to detect pneumonia
- Deep learning model (CNN) with high accuracy
- Simple web interface using Streamlit
- Login and registration system
- Custom-styled UI

## 📁 Project Structure
Pneumonia_Detection_UsIng_AI/
├── dataset/ # Dataset files
├── model/ # Saved CNN model
├── pneumonia_cnn_model.ipynb # Model training notebook
├── app.py # Streamlit web app
├── requirements.txt # Dependencies
└── README.md # Project documentation

## 💻 How to Run

1. Clone this repository:
git clone https://github.com/rishika712/Pneumonia_Detection_UsIng_AI.git
cd Pneumonia_Detection_UsIng_AI

2. Install required libraries:
pip install -r requirements.txt

3. Run the app:
streamlit run app.py

> Make sure the trained model file (`pneumonia_model.h5`) is in the right folder.

## 📊 Dataset

- **Source**: [Kaggle - Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)
- Two classes: `NORMAL` and `PNEUMONIA`

## 🧠 Model Details

- Convolutional Neural Network (CNN)
- Built with TensorFlow and Keras
- Trained, validated, and tested on chest X-ray images

## 🌐 Deployment

- Built using **Streamlit**
- Can be deployed on Streamlit Cloud, Render, or Heroku

## 🔐 Authentication

- Basic login/signup system using a text file
- Styled buttons and background for better user experience

## 🛠️ Technologies Used

- Python
- TensorFlow / Keras
- OpenCV
- Streamlit
- NumPy / Pandas

## 🚀 Future Enhancements

- Improve UI/UX
- Add admin dashboard
- Support detection of other diseases

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or pull requests.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

**Made by [Rishika](https://github.com/rishika712)**




