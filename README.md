<div align="center">
  <h1><strong>SnapSense Telegram Bot</strong></h1>

  ![Python version](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge)
  ![GitHub license](https://img.shields.io/github/license/Roodaki/SnapSense-Telegram-Bot.svg?style=for-the-badge)
  [![Telegram Bot](https://img.shields.io/badge/Telegram-@SnapSenseBot-blue?style=for-the-badge&logo=telegram)](https://t.me/SnapSenseBot)
</div>

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Bot](#running-the-bot)
  - [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

[SnapSense](https://t.me/SnapSenseBot) is an AI-powered Telegram bot designed to provide users with a simple and intuitive way to perform advanced image analysis directly through their chat application. By integrating various cutting-edge computer vision models, the bot allows users to unlock insights from their images, ranging from identifying objects and recognizing emotions to extracting text and manipulating image backgrounds.

## Features

[SnapSense](https://t.me/SnapSenseBot) currently supports the following image analysis tasks:

* **🔎 Object Detection:** Utilizes the [YOLO](https://docs.ultralytics.com/) model to detect, classify, and locate objects within images, marking them with bounding boxes.
* **😊 Emotion Recognition:** Analyzes detected faces in an image to determine and report the dominant emotion and confidence scores for various emotional states using [DeepFace](https://github.com/serengil/deepface).
* **🔞 Sensitive Content Detection:** Employs [NudeNet](https://github.com/notAI-tech/NudeNet) to identify potentially sensitive or explicit content, providing a summary of detected classes and the option to return a censored image.
* **📝 Text Extraction (OCR):** Leverages [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) to extract readable text from images, converting image-based text into machine-readable format.
* **✂️ Background Removal:** Processes images using [Rembg](https://github.com/danielgatis/rembg) to automatically isolate the foreground subject and remove the background, producing an image with a transparent background.
* **🧩 Image Segmentation:** Applies the [Segment Anything Model (SAM)](https://github.com/facebookresearch/segment-anything) to divide an image into meaningful segments, visualizing the results by coloring different regions or objects.

## Project Structure

The project follows a specific structure to organize its files and directories:
```
├── bot/
│   ├── handlers.py
│   ├── keyboards.py        
│   ├── strings.py
│   └── utils.py            
├── models/                 
│   ├── background_removal/
│   │   └── background_removal.py
│   ├── emotion_recognition/
│   │   └── emotion_recognition.py
│   ├── image_segmentation/
│   │   └── image_segmentation.py
│   ├── nudity_detection/
│   │   └── nudity_detection.py
│   ├── object_detection/
│   │   └── object_detection.py
│   ├── text_extraction/
│   │   └── text_extraction.py
├── .env
├── .gitignore
├── config.yaml
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
```

## Getting Started

Follow these steps to get the [SnapSense](https://t.me/SnapSenseBot) bot up and running on your system.

### Requirements
* Python 3.8+
* A Telegram Bot Token from [@BotFather](https://t.me/botfather).
* Sufficient disk space for installing dependencies and downloading AI model weights (some models download weights on the first run, which can be large).
* A stable internet connection for downloading models and dependencies.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Roodaki/SnapSense-Telegram-Bot.git
    cd SnapSense-Telegram-Bot
    ```

2.  **Create and activate a virtual environment (highly recommended):**

    ```bash
    python -m venv .venv
    # On Windows:
    .venv\Scripts\activate
    # On macOS and Linux:
    # source .venv/bin/activate
    ```

3.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **Environment Variables:**
    Create a file named `.env` in the root directory of the project. Add your Telegram Bot Token:

    ```dotenv
    TELEGRAM_BOT_TOKEN=<YOUR_BOT_TOKEN_HERE>
    ```
    Replace `<YOUR_BOT_TOKEN_HERE>` with the token provided by BotFather. 

2. **Install Tesseract OCR:**
   Tesseract is an external dependency specifically required for the Text Extraction feature. Follow the official [Tesseract Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html) for your operating system to install it. Ensure that the `tesseract` command is available in your system's PATH after installation.

3. **Download Model Weights:**
  Some AI models require downloading pre-trained weights or checkpoints. While libraries like DeepFace and NudeNet often handle this automatically on first use, others like SAM and YOLO require manual download and configuration.

    * **Segment Anything Model (SAM):** Download the desired model checkpoint from the official [SAM Model Checkpoints](https://github.com/facebookresearch/segment-anything?tab=readme-ov-file#model-checkpoints) repository.
    * **YOLO Models (Ultralytics):** Ultralytics can often download models automatically, but you might choose to download specific versions manually from [Ultralytics YOLO Repository](https://github.com/ultralytics/ultralytics) if needed.


5.  **Application and Model Settings:**
    Edit the `config.yaml` file to set up application parameters and specify paths and settings for each AI model:

    * **`app.database_dir`**: Set the path to a directory where the bot will store temporary image files and results. Make sure this directory exists and the bot has write permissions.
    * **`app.drop_pending_updates`**: Set to `true` to ignore messages sent to the bot while it was offline.
    * **`models.object_detection.model_path`**: Specify the path to the YOLO model file you downloaded (e.g., a `.pt` file).
    * **`models.object_detection.conf`**, **`models.object_detection.iou`**: Adjust confidence and IOU thresholds for object detection.
    * **`models.image_segmentation.checkpoint_path`**: Specify the path to the downloaded SAM model checkpoint file.
    * **`models.image_segmentation.model_type`**: Set the type of SAM model (e.g., `vit_h`, `vit_l`, `vit_b`).
    * **`models.*.preferred_device`**: For models that support it, set to `cuda` if you have an NVIDIA GPU and CUDA installed, otherwise use `cpu`.
    * **Other Model Settings**: Review the sections for `nudity_detection`, `emotion_recognition`, `text_extraction`, and `background_removal` in `config.yaml` to customize their behavior if necessary.


### Running the Bot

With dependencies installed and configuration set up, you can start the bot:

1.  **Activate your virtual environment** (if not already active).
2.  **Execute the main script:**

    ```bash
    python main.py
    ```

The bot will connect to the Telegram API and begin polling for updates.

### Usage

Interact with the bot directly on Telegram:

1.  **Send the `/start` command:** This initializes your session and presents the main menu.
2.  **Select a Task:** Use the inline keyboard to choose the desired image analysis operation (e.g., Object Detection, Background Removal).
3.  **Send a Photo:** After selecting a task, send the photo you wish to analyze.
4.  **Receive Results:** The bot will process the photo using the chosen AI model and send you the result, which could be a modified image, a text message, or both, depending on the task.
5.  **Repeat or Cancel:** After receiving the result, the bot will automatically return to the main menu. You can select another task or use the `/cancel` command to stop any ongoing operation and return to the main menu.

## Contributing

We welcome contributions to improve [SnapSense](https://t.me/SnapSenseBot)! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Commit your changes (`git commit -am 'Add some feature'`).
4.  Push to the branch (`git push origin feature/your-feature-name`).
5.  Create a new Pull Request on GitHub.

Please ensure your code is clean, well-commented, and follows the project's structure.

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
