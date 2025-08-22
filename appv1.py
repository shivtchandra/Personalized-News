import streamlit as st
import google.generativeai as genai
from newsapi import NewsApiClient
import datetime
import requests
from bs4 import BeautifulSoup

st.markdown("""
<style>
/* Main app background */
.stApp {
    background-color: #0A0A0A;
    color: #CCCCCC;
}

/* Sidebar styling */
[data-testid="stSidebar"]{
    background-color: #141414;
}

/* Button styling */
.stButton>button {
    border: 2px solid #00A99D;
    background-color: transparent;
    color: #00A99D;
    border-radius: 8px;
    padding: 0.5em 1em;
    font-weight: bold;
}
.stButton>button:hover {
    border-color: #00877A;
    background-color: #00A99D;
    color: #FFFFFF;
}

/* Header styling */
h1, h2, h3, h4, h5, h6 {
    color: #00A99D;
}

/* Styling for the news article cards */
div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] {
    border: 1px solid #424242;
    border-radius: 10px;
    padding: 1rem;
    margin-top: 1rem;
    background-color: #1E1E1E;
}

/* Link color */
a {
    color: #00C2B2;
}

</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if 'articles' not in st.session_state:
    st.session_state.articles = []
if 'summaries' not in st.session_state:
    st.session_state.summaries = {}

# --- Functions ---

def fetch_articles(api_key, topics):
    """Fetches real articles from NewsAPI."""
    newsapi = NewsApiClient(api_key=api_key)
    query = " OR ".join(topics)
    try:
        all_articles = newsapi.get_everything(q=query, language='en', sort_by='publishedAt', page_size=50)
        return all_articles['articles']
    except Exception as e:
        st.error(f"Failed to fetch news from NewsAPI. Error: {e}")
        return []

def calculate_match_score(article, topics):
    """Calculates a 'match score' for an article."""
    score = 0
    content = (article['title'] or "") + (article['description'] or "")
    content_lower = content.lower()
    for topic in topics:
        if topic.lower() in content_lower:
            score += 1
    if not topics: return 0
    return min((score / len(topics)) * 100, 100)

# --- NEW: Web Scraper Function ---
def scrape_article_text(url):
    """
    Visits a URL, scrapes the main article text, and returns it.
    Returns None if scraping fails.
    """
    try:
        # Set a user-agent header to mimic a real browser visit
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all paragraph tags and join their text. This is a simple but
        # effective method for many news sites.
        paragraphs = soup.find_all('p')
        
        # Combine the text from all paragraphs into a single string
        full_text = "\n".join([p.get_text() for p in paragraphs])
        
        # Basic check to see if we got meaningful content
        if len(full_text) < 200: # If text is too short, it might be a paywall or error
            return None
            
        return full_text
    except requests.exceptions.RequestException as e:
        st.warning(f"Could not fetch article for scraping. Error: {e}")
        return None
    except Exception as e:
        st.warning(f"An error occurred during scraping: {e}")
        return None


def summarize_with_gemini(api_key, article_content):
    """Summarizes the given article content using the Gemini API."""
    if not article_content or len(article_content.strip()) < 200:
        return "Article content is too short or unavailable to summarize."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        # --- UPDATED: A better prompt for full-text articles ---
        prompt = f"Please provide a high-quality, neutral, five-sentence summary of the following news article:\n\n---\n\n{article_content}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary with Gemini: {e}"

# --- Streamlit App UI ---

st.set_page_config(layout="wide")
st.title("Your Personalized News Feed ")
st.markdown(f"##### Real-time news for you, updated {datetime.date.today().strftime('%B %d, %Y')}")

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
except KeyError:
    st.error("API keys not found! Please add GEMINI_API_KEY and NEWS_API_KEY to your .streamlit/secrets.toml file.")
    st.stop()

st.sidebar.header("Your Interests")
st.sidebar.markdown("""
**Suggestions:**
- **Topics:** AI, Startups, Technology, Health, Finance, Climate Change, EV, Space Exploration, Biotechnology
- **Companies:** Nvidia, Tesla, Reliance, Tata Motors
- **Places:** Hyderabad, India, Silicon Valley
""")

user_input = st.sidebar.text_input(
    "Enter topics, companies, or places (separated by commas):",
    "AI, Startups, Hyderabad" # Default value
)

if st.sidebar.button("Generate My Feed", type="primary"):
    # --- CHANGE: Process the text input into a list ---
    if user_input:
        # Split the string by commas and strip any extra whitespace from each topic
        selected_topics = [topic.strip() for topic in user_input.split(',') if topic.strip()]
    else:
        selected_topics = []

    if not selected_topics:
        st.warning("Please enter at least one topic.")
    else:
        # --- (The rest of the workflow remains the same) ---
        with st.spinner("Fetching real news articles..."):
            articles = fetch_articles(NEWS_API_KEY, selected_topics)
        
        if articles:
            scored_articles = [{'article': a, 'score': calculate_match_score(a, selected_topics)} for a in articles if calculate_match_score(a, selected_topics) > 20]
            st.session_state.articles = sorted(scored_articles, key=lambda x: x['score'], reverse=True)
            st.session_state.summaries = {}
            st.success(f"Found {len(st.session_state.articles)} relevant articles for your topics: **{', '.join(selected_topics)}**")
        else:
            st.session_state.articles = []
            st.error(f"No relevant articles found for **{', '.join(selected_topics)}**. Try different topics.")

if st.session_state.articles:
    st.markdown("---")
    for item in st.session_state.articles[:10]:
        article = item['article']
        article_url = article['url']

        st.markdown(f"### [{article['title']}]({article_url})")
        
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**Source:** {article['source']['name']} | **Published:** {article['publishedAt'][:10]}")
            st.write(article['description'])
        
        with col2:
            st.write("**Match Meter:**")
            st.progress(int(item['score']))
            st.markdown(f"<h4 style='text-align: center;'>{int(item['score'])}%</h4>", unsafe_allow_html=True)

        if st.button("Summarize with Gemini 🤖", key=article_url):
            with st.spinner(f"Scraping article from {article['source']['name']}..."):
                full_text = scrape_article_text(article_url)
            
            if full_text:
                with st.spinner("Gemini is summarizing the full text..."):
                    summary = summarize_with_gemini(GEMINI_API_KEY, full_text)
                    st.session_state.summaries[article_url] = summary
            else:
                st.warning("Scraping failed. Summarizing the short description instead.")
                summary = summarize_with_gemini(GEMINI_API_KEY, article['description'])
                st.session_state.summaries[article_url] = summary
        
        if article_url in st.session_state.summaries:
            st.info(st.session_state.summaries[article_url])

        st.markdown("---")
        
# This 'elif' must directly follow the 'if' block above
elif 'selected_topics' in locals() and not selected_topics:
     st.info("Select your topics and click 'Generate My Feed' to get started.")
