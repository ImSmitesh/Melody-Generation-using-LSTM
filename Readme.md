# 🎵 Melody Generation Using LSTM

A deep learning project that leverages Long Short-Term Memory (LSTM) networks to generate musical melodies. This project processes MIDI files, trains an LSTM model on musical sequences, and generates new melodies based on learned patterns.

---

## 📁 Project Structure

```plaintext
Melody-Generation-using-LSTM/
├── file_dataset/                           # Directory containing MIDI files for training
├── mapping.json                            # JSON file mapping notes to integers
├── Data preprocessing/generator.py         # Script to generate melodies using the trained model
├── Data preprocessing/Model/               # Trained LSTM model
├── Data preprocessing/pre_processing.py    # Script for preprocessing MIDI files
├── Data preprocessing/train.py             # Script to train the LSTM model
└── README.md # Project documentation
```


## 🎯 Objective

The goal of this project is to:

- Process MIDI files to extract musical sequences.
- Train an LSTM-based neural network to learn musical patterns.
- Generate new melodies by predicting subsequent notes in a sequence.



# Melody Generation using LSTM

## Installation

### Clone the Repository
#### Using Git
```bash
git clone https://github.com/ImSmitesh/Melody-Generation-using-LSTM.git
cd Melody-Generation-using-LSTM
```

## Dataset Preparation

Add your `.mid` files inside the `file_dataset/` directory.

### Step 2: Preprocess the Dataset
#### Run the Preprocess Script
```bash
python preprocess.py
```

## Model Training

```bash
python train.py
```

## Melody Generation

```bash
python melodygenerator.py
```

## Model Architecture

#### Input
*   Integer-encoded musical sequences

#### LSTM Layers
*   Capture sequence patterns

#### Dense Layer
*   Predicts the next note (softmax activation)