# Email PDF Sender

This project allows you to send PDF files as email attachments. The email addresses are extracted from the content of the PDFs. It uses SMTP for sending emails and supports SSL for secure communication.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)


## Installation

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/email-pdf-sender.git
    cd email-pdf-sender
    ```
2. Install required packages:
    ```sh
    pip install -r requirements.txt
    ```
3. Create the necessary directories:
    ```sh
    mkdir -p data/PDFs
    ```

## Usage

1. **Configure the `config.ini` file** with your SMTP server details.
2. **Place the PDF files** to be sent in the `data/PDFs` directory.
3. **Run the program**:
    ```sh
    python main.py
    ```

## Configuration

### Example Configuration (`config/config.ini`)
```ini
[EmailSettings]
smtp_host = host@email.com
smtp_port = 555
smtp_user = example@email.com
smtp_password = password
subject = Subject
body = 
    Body of the email
```
## License

This project is licensed under the MIT license - see the LICENSE file for details
