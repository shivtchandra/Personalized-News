# Personalized News Feed – Streamlit App

This repository provides a robust Streamlit application designed for personalized, real-time news aggregation and intelligent summarization. Users can generate a highly tailored news feed based on their interests, companies, and locations—then quickly review relevance scores and concise AI-powered summaries.

***

## Try the App

Access the live demo here:

**[Personalized News Feed – Streamlit App](https://personalized-news-weavzb5mbg3jtdggyns6k8.streamlit.app/)**

***

## Features

- **Tailored News Selection:** Input topics, companies, or places in the sidebar to curate your feed according to your interests. Example entries: `AI, Startups, Hyderabad, Tesla, Climate Change`.
- **Live Article Retrieval:** Integrates with NewsAPI to deliver up-to-date articles from trusted news sources.
- **Dynamic Scoring:** Every article receives a match score (0–100%) showing how closely it aligns with your chosen topics.
- **One-Click Summaries:** Instantly generate objective, five-sentence summaries using Google Gemini Generative AI. The app intelligently scrapes full article text for higher quality summaries where available.
- **User-Friendly Interface:** Modern dark mode design, progress bars for relevance, and clear article cards for efficient navigation.
- **Session Memory:** Maintains your article feed and generated summaries throughout your interaction for a seamless user experience.
- **Custom CSS:** Advanced styling is implemented for both the main app and sidebar, including cards for articles and modern button design.

***

## Installation

1. **Clone the Repository:**

    ```bash
    https://github.com/shivtchandra/Personalized-News.git
    cd Personalized-News
    ```

2. **Install Required Packages:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure API Keys:**

    Create a file named `.streamlit/secrets.toml` in your project root, as follows:

    ```toml
    GEMINI_API_KEY = "<your-gemini-api-key>"
    NEWS_API_KEY = "<your-newsapi-key>"
    ```

***

## Usage

Launch the app locally with Streamlit:

```bash
streamlit run app.py
```

**How it works:**

1. **Enter your interests** (topics, companies, or places) in the sidebar, separated by commas.
2. **Click "Generate My Feed."** The application will fetch the latest matching articles and display the most relevant ones at the top.
3. **Explore Your Feed:**
    - Each article displays its title, source, publication date, relevance score, and description.
    - Click "Summarize with Gemini" to receive an instant, five-sentence summary using Gemini AI. If a full-text scrape fails, the summary will be generated from the description.

***

## Technical Details

- **Article Fetching:** Utilizes NewsAPIClient to search and retrieve relevant articles.
- **Relevance Calculation:** Uses a topic matching algorithm that scores each article for personalized relevance.
- **Web Scraping:** BeautifulSoup parses article web pages, extracting the main text for better summaries.
- **Summarization:** Employs the Google Generative AI (Gemini) API for concise, objective summarization.
- **Session Management:** Articles and summaries persist via Streamlit's session state.
- **Styling:** Thorough use of CSS for:
    - Dark mode backgrounds and text
    - Custom sidebar style
    - Stylish buttons and progress bars
    - Card layout for articles

***

## Troubleshooting

- Ensure your NewsAPI and Gemini API keys are active and entered correctly in `.streamlit/secrets.toml`.
- The scraper may not extract full content from every article (paywall, restricted or unusual site layouts).
- API quotas may apply to NewsAPI and Gemini, depending on your account tier.


***

## Credits

- [Streamlit](https://streamlit.io/)
- [NewsAPI](https://newsapi.org/)
- [Google Generative AI Gemini](https://ai.google.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

***

**Live Demo:**  
[https://personalized-news-weavzb5mbg3jtdggyns6k8.streamlit.app/](https://personalized-news-weavzb5mbg3jtdggyns6k8.streamlit.app/)
