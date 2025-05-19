# OxPhish

<div align="center">
  <img src="https://img.shields.io/badge/Version-2.1.0-blue.svg" alt="Version 2.1.0">
  <img src="https://img.shields.io/badge/Python-3.7+-brightgreen.svg" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License MIT">
</div>

<p align="center">
  <b>OxPhish - Advanced Phishing Tool for Security Testing and Educational Purposes</b>
</p>

## ⚠️ Disclaimer

**OxPhish is designed for educational purposes and legitimate security testing only!** Unauthorized use of this tool against systems or individuals without explicit permission is illegal and unethical. The developers assume no liability for misuse or damage caused by this program.

## 📋 Overview

OxPhish is a powerful and modern phishing tool built in Python that helps security professionals and organizations test their vulnerability to phishing attacks. This tool provides an easy-to-use interface to create convincing phishing scenarios with customizable templates, email sending capabilities, and both local and remote deployment options.

## ✨ Features

- 🎯 **Multiple Templates**: Ready-made templates for Google, Facebook, and Instagram login pages
- 🌐 **Flexible Deployment**: Run locally or via Serveo tunnel for external access
- 📧 **Email Campaign**: Send phishing emails to targets with customizable templates
- 📱 **QR Code Generation**: Create QR codes for phishing URLs for mobile targeting
- 📊 **Detailed Logging**: Comprehensive logging of captured credentials
- 🧩 **Customizable**: Easy to extend with new templates or features

## 🔧 Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/Oxeser/OxPhish.git
```

2. Navigate to the project directory:
```bash
cd OxPhish
```

3. Start to Phishing
```bash
bash setup.sh
```

### Dependencies

- Flask
- qrcode
- smtplib (built-in)
- email (built-in)

## 🚀 Usage

### Basic Usage

1. Run the tool:
```bash
python main.py
```

2. Follow the interactive menu to:
   - Select a phishing template
   - Configure email settings (if using email campaign)
   - Choose deployment method (local server or Serveo tunnel)

### Example Workflow

1. Select a template (e.g., Google)
2. Configure email settings with your Gmail credentials
3. Add target email addresses
4. Choose deployment method (Serveo recommended for external access)
5. Send phishing emails with the generated URL
6. Monitor and collect credentials as targets interact with the phishing page

## 📊 Available Templates

- **Google**: Login page mimicking Google authentication
- **Facebook**: Login page mimicking Facebook authentication
- **Instagram**: Login page mimicking Instagram authentication

## 🔒 Security Features

- Automatic port selection to avoid conflicts
- Secure credential storage in encrypted format
- Detailed logging of all activities

## 🛠️ Advanced Configuration

### Custom Templates

To add a custom template:

1. Create an HTML file in the `templates` directory
2. Ensure the form action points to `/login`
3. Include input fields with names that match the expected parameters

### Email Configuration

For Gmail users, you'll need to:
1. Enable "Less secure app access" or
2. Generate an App Password if you have 2FA enabled

## 📝 Logs

Captured data is stored in the `logs` directory with the following format:
```
logs/{template_name}_captured_{timestamp}.txt
```

Each log contains:
- Timestamp
- IP Address
- User Agent
- Template used
- Captured credentials

## 🔄 Updates

### Version 2.1.0
- Added QR code generation
- Improved Serveo tunnel stability
- Enhanced email template customization
- Bug fixes and performance improvements

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- GitHub: [https://github.com/Oxeser](https://github.com/Oxeser)
- Issues: [https://github.com/Oxeser/OxPhish/issues](https://github.com/Oxeser/OxPhish/issues)

## 📸 Screenshots

![OxPhish Main Menu](https://raw.githubusercontent.com/Oxeser/OxPhish/main/images/menu.png)
![OxPhish Template Selection](https://raw.githubusercontent.com/Oxeser/OxPhish/main/images/template.png)
![OxPhish Attack Method](https://raw.githubusercontent.com/Oxeser/OxPhish/main/images/attack.png)

---

<p align="center">
  <b>Made with ❤️ by Oxeser</b>
</p>
