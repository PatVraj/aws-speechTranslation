# Serverless Speech Transcription & Translation Pipeline

An AWS serverless pipeline to automatically transcribe and translate multi-language audio files using S3, Lambda, Amazon Transcribe, and Amazon Translate.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![AWS SAM](https://img.shields.io/badge/built%20with-AWS%20SAM-orange)
![Python](https://img.shields.io/badge/python-3.9-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 📖 Overview

This project provides a complete, deployable AWS serverless application that creates an automated transcription and translation workflow. It is specifically designed to handle audio files containing multiple, mixed Indian languages (such as Hindi, English, and Tamil) by leveraging **Amazon Transcribe's multi-language identification**.

The pipeline is event-driven: uploading an audio file to an S3 bucket triggers a series of Lambda functions that orchestrate the transcription and translation, with the final, structured data saved as a CSV file for easy analysis.

## ✨ Key Features

* **Automated Workflow:** Simply upload an audio/video file to a designated S3 bucket to trigger the entire process.
* **Multi-Language Identification:** Utilizes Amazon Transcribe to automatically detect and transcribe multiple languages within a single audio file.
* **Intelligent Translation:** Employs Amazon Translate to convert the transcribed text into English, with auto-detection of the source language(s).
* **Structured Data Output:** Aggregates the results and saves them in a clean, appendable CSV format in a final S3 bucket, perfect for local analysis in Excel or other tools.
* **Serverless & Scalable:** Built entirely with AWS Lambda, S3, Amazon Transcribe, and Amazon Translate for a fully managed, scalable, and cost-effective solution.
* **Deployable Infrastructure:** Includes a complete AWS SAM (Serverless Application Model) template for easy, repeatable deployment of the entire stack.

## 🏗️ Architecture

The entire architecture is serverless and event-driven, ensuring cost-efficiency and scalability with no server management required.

```mermaid
graph TD
    A[1. Speech Audio/Video File] -->|Upload| B(Amazon S3: Raw Media Bucket);
    B -->|S3 Event Trigger| C{AWS Lambda: StartTranscription};
    C -->|Initiates Job with Multi-Language ID| D[Amazon Transcribe];
    D -- Transcribed JSON --> G(Amazon S3: Transcribed Text Bucket);
    G -->|S3 Event Trigger| H{AWS Lambda: TranslateAndStore};
    H -->|Sends Text for Translation ('auto' source)| I[Amazon Translate];
    I -- Translated Text --> H;
    H -->|Appends CSV Record| J(Amazon S3: Final Data Bucket);
    J --> K[Downloadable political_speeches_data.csv];
```

## 🛠️ Technology Stack

* **Compute:** AWS Lambda
* **Storage:** Amazon S3
* **AI Services:**
    * Amazon Transcribe (for speech-to-text)
    * Amazon Translate (for translation)
* **Infrastructure as Code:** AWS SAM (Serverless Application Model)
* **Programming Language:** Python 3.9
* **Key Libraries:** Boto3

## 🚀 Getting Started

Follow these instructions to deploy the pipeline to your own AWS account.

### Prerequisites

* An AWS Account.
* The [AWS CLI](https://aws.amazon.com/cli/) installed and configured with your credentials.
* The [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) installed.
* [Docker](https://www.docker.com/products/docker-desktop/) installed and running (required by `sam build`).

### Deployment Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Build the application:**
    This command packages the Lambda functions and their dependencies into deployment artifacts.
    ```bash
    sam build
    ```

3.  **Deploy the application:**
    This command deploys the application to AWS CloudFormation. The `--guided` flag provides an interactive experience for the first deployment.
    ```bash
    sam deploy --guided
    ```
    You will be prompted to enter the following:
    * **Stack Name:** A unique name for this application stack (e.g., `speech-translation-pipeline`).
    * **AWS Region:** Your desired AWS region (e.g., `us-east-1`).
    * **Confirm changes before deploy:** Enter `y`.
    * **Allow SAM CLI IAM role creation:** Enter `y`.
    * **Save arguments to samconfig.toml:** Enter `y`. This will save your choices for future, non-guided deployments.

## ▶️ How to Use

1.  **Find your S3 Bucket Name:** After deployment is complete, check the `Outputs` section in your terminal or the AWS CloudFormation console to find the `RawMediaBucketName`.

2.  **Upload a Speech File:** Upload a supported audio or video file (`.mp3`, `.mp4`, `.wav`) to this bucket. You can do this via the AWS S3 console or the AWS CLI:
    ```bash
    aws s3 cp /path/to/your/local/speech.mp3 s3://<Your-RawMediaBucket-Name>/
    ```

3.  **Monitor the Process:**
    * The upload will trigger the `StartTranscription` Lambda function.
    * Amazon Transcribe will process the file, which may take a few minutes depending on the audio length.
    * Once complete, the JSON output will trigger the `TranslateAndStore` Lambda function.

4.  **Check the Final Output:**
    Navigate to the `FinalDataBucket` (the name is also in the deployment outputs). You will find a file named `political_speeches_data.csv`. Download this file and open it with any spreadsheet program to see the transcribed and translated results. Each new speech you upload will be automatically processed and appended as a new row to this CSV file.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements, please feel free to fork the repository and submit a pull request. You can also open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## ⚖️ License

This project is distributed under the MIT License. See `LICENSE.txt` for more information.

## 📧 Contact

Your Name – [vrpa3077@colorado.edu](mailto:vrpa3077@colorado.edu)

Project Link: [https://github.com/your-username/your-repository-name](https://github.com/your-username/your-repository-name)