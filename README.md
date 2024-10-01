# Smart Pulmonary Embolism Application with Computer Vision and AI Integration

![InstantLink Logo](/fei.png)

## Overview

The Smart Pulmonary Embolism Application is a comprehensive solution designed to aid in the diagnosis, treatment, and management of pulmonary embolism. By leveraging computer vision and AI, this application provides functionalities that streamline the process for both patients and doctors, enhancing communication, reducing errors, and improving overall healthcare delivery.

## API Documention
```
https://documenter.getpostman.com/view/29368996/2sAXxJiF2k
```


## Features

1. **Doctor and Lab Communication**:
   - Conduct x-rays and send them automatically to doctors.
   - Daily follow-up by doctors with patients.
   - Machine learning comparison of previous and new x-ray results to save doctors' time.

2. **E-Prescriptions**:
   - Doctors can make e-prescriptions to eliminate errors due to handwriting or misunderstandings.
   - Automatic medicine ordering with a click on the e-prescription.

3. **Appointment Booking**:
   - Book appointments with doctors and labs through the app.

4. **Payment Gateways**:
   - Integrated payment gateways for seamless transactions.

5. **Health Condition Assessment**:
   - Set of questions to get a brief of the user's health condition, assisting doctors in their assessments.

6. **E-Pharmacy**:
   - Medicines can be delivered to the user through the e-pharmacy feature.

## Technology Stack

- **Backend**: Django Rest Framework
- **Real-Time Communication**: WebSockets, Channels, Channels-Redis
- **Machine Learning**: Integration for comparing x-ray results
- **Database**: PostgreSQL
- **Deployment**: Heroku, Gunicorn

## Installation

Navigate to the project directory:


1. Clone the repository:
    ```bash
    git clone https://github.com/Graduation-Pr/FeiAPI.git
    cd FeiAPI
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Start the Django development server:
    ```bash
    python manage.py runserver
    ```

## Key Functionalities Implemented

- **Messaging**: Listing and sending messages via WebSockets.
- **Doctor Plans**: Updating and retrieving plan details for both patients and doctors.
- **Pharmacy Integration**: Refactoring of pharmacy-related functionalities including ordering and payment.
- **Laboratory Management**: Correct retrieval and management of lab booking data.
- **Prescription Management**: Creating, listing, and managing prescriptions with detailed information.
- **Image Handling**: Uploading and handling images in Base64 format.
- **Booking System**: Comprehensive booking system for doctors, labs, and patient plans.
- **Rating and Review System**: Calculation and filtering of doctor ratings based on patient reviews.
- **Product Management**: Listing and managing pharmacy products including medicines and devices.


## Usage

1. **User Registration**:
   - Users can sign up and create an account.

2. **Conducting X-Rays**:
   - Users can conduct x-rays and have them sent automatically to doctors.

3. **Doctor Interaction**:
   - Doctors can follow up with users and compare x-ray results using machine learning.

4. **Prescription and Medicine Ordering**:
   - Doctors can issue e-prescriptions, and users can order medicines with a click.

5. **Booking Appointments**:
   - Users can book appointments with doctors and labs seamlessly.

6. **Payment**:
   - Integrated payment gateways for easy transactions.

## Contributing

Contributions are welcome! If you have ideas for improvements or have found bugs, please follow the steps below to contribute to the project.

### Steps to Contribute

1. **Fork the repository**: Click the "Fork" button at the top right corner of this repository to create a copy of the repository on your GitHub account.

2. **Clone your fork**: Clone your forked repository to your local machine.
    ```bash
    git https://github.com/Graduation-Pr/FeiAPI.git
    cd FeiAPI
    ```

3. **Create a new branch**: Create a new branch for your feature or bug fix.
    ```bash
    git checkout -b feature-branch
    ```

4. **Make your changes**: Make your changes to the codebase.

5. **Commit your changes**: Commit your changes with a clear and descriptive commit message.
    ```bash
    git commit -m 'Add some feature'
    ```

6. **Push to the branch**: Push your changes to the branch on your forked repository.
    ```bash
    git push origin feature-branch
    ```

7. **Open a pull request**: Go to the original repository on GitHub and open a pull request to the `main` branch. Provide a clear description of the changes and any relevant information.

8. **Review process**: Your pull request will be reviewed by the project maintainers. Be prepared to make any necessary changes based on feedback.

Thank you for contributing to the FeiAPI project!

## Contact

- **Menna Hassan**:
  - **LinkedIn**: [Menna Hassan](https://www.linkedin.com/in/menna-hasan-675602269/)
  - **GitHub**: [mennahasan19](https://github.com/mennahasan19)

- **Zeyad Salama**:
  - **LinkedIn**: [Zeyad Salama](https://www.linkedin.com/in/demo-23home/)
  - **GitHub**: [Demo-23home](https://github.com/Demo-23home)


