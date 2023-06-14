# Tweets Capture

Tweets Capture is a Django-based web application that enables users to generate tweets related to a specific country.

## Setup

Before getting started, please ensure that you have Python 3 installed on your system.

1. Clone the repository:
   ```bash
   git clone https://github.com/arabsannan/DjangoWebScrapping.git
   ```
2. Change into the project directory:

   ```bash
   cd DjangoWebScrapping
   ```

3. Create and activate a virtual environment (Windows):
   ```bash
   python -m venv venv
   venv/Scripts/Activate
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a Twitter Developer Account and obtain the necessary API credentials:

   - Visit the Twitter Developer Portal at https://developer.twitter.com and sign in with your Twitter account.
   - Create a new developer account if you don't have one already.
   - Create a new Twitter app within your developer account.
   - Obtain the following API credentials from the app's "Keys and tokens" section:
     - API Key (Consumer Key)
     - API Secret Key (Consumer Secret)
     - Access Token
     - Access Token Secret

6. Create a `.env` file in the root directory and copy the contents from `.env.example`. Update the following variables with the corresponding values obtained from the Twitter Developer Portal:

   ```
   API_KEY=YOUR_API_KEY
   API_SECRET_KEY=YOUR_API_SECRET_KEY
   ACCESS_TOKEN=YOUR_ACCESS_TOKEN
   ACCESS_TOKEN_SECRET=YOUR_ACCESS_TOKEN_SECRET
   ```

7. Run database migrations::
   ```bash
   python manage.py migrate
   ```

8. Start the development server:

   ```bash
   python manage.py runserver
   ```

9. Open the application in your browser:

   ```bash
   http://localhost:8000/
   ```
   

Now you're ready to use Tweets Capture to generate tweets about any country of your choice. Enjoy exploring!
> **_NOTE:_** Please note that the developers need to create a Twitter Developer Account and obtain their own API credentials from the Twitter Developer Portal.
