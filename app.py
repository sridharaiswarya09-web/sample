import streamlit as st
import requests
import pandas as pd

# -------------------------------
# CONFIGURATION
# -------------------------------
API_KEY = "YOUR_API_KEY"
BASE_URL = "https://newsapi.org/v2/top-headlines"

st.set_page_config(
    page_title="Global News Dashboard",
    page_icon="📰",
    layout="wide"
)

# -------------------------------
# TITLE
# -------------------------------
st.title("📰 Global News Dashboard")
st.markdown("Stay updated with the latest headlines worldwide.")

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("News Filters")

country = st.sidebar.selectbox(
    "Select Country",
    {
        "India": "in",
        "United States": "us",
        "United Kingdom": "gb",
        "Canada": "ca",
        "Australia": "au",
        "Germany": "de",
        "France": "fr"
    }
)

category = st.sidebar.selectbox(
    "Select Category",
    [
        "business",
        "entertainment",
        "general",
        "health",
        "science",
        "sports",
        "technology"
    ]
)

keyword = st.sidebar.text_input(
    "Search Keyword",
    placeholder="AI, Cricket, Tesla..."
)

num_articles = st.sidebar.slider(
    "Number of Articles",
    min_value=5,
    max_value=50,
    value=10
)

# -------------------------------
# FETCH NEWS
# -------------------------------
def fetch_news(country, category, keyword):
    params = {
        "apiKey": API_KEY,
        "country": country,
        "category": category,
        "pageSize": num_articles
    }

    if keyword:
        params["q"] = keyword

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: Unable to fetch news")
        return None

# -------------------------------
# BUTTON
# -------------------------------
if st.sidebar.button("Fetch News"):
    with st.spinner("Fetching latest headlines..."):
        news_data = fetch_news(country, category, keyword)

    if news_data and news_data["status"] == "ok":

        articles = news_data["articles"]

        st.success(f"Found {len(articles)} articles")

        for article in articles[:num_articles]:

            st.divider()

            col1, col2 = st.columns([1, 3])

            with col1:
                if article["urlToImage"]:
                    st.image(
                        article["urlToImage"],
                        use_container_width=True
                    )

            with col2:
                st.subheader(article["title"])

                if article["source"]:
                    st.caption(
                        f"Source: {article['source']['name']}"
                    )

                if article["description"]:
                    st.write(article["description"])

                st.markdown(
                    f"[Read Full Article]({article['url']})"
                )

    else:
        st.warning("No articles found.")

# -------------------------------
# DATA TABLE VIEW
# -------------------------------
st.markdown("---")
st.subheader("📊 News Overview Table")

if st.button("Show News Table"):

    news_data = fetch_news(country, category, keyword)

    if news_data and news_data["status"] == "ok":

        records = []

        for article in news_data["articles"]:
            records.append({
                "Title": article["title"],
                "Source": article["source"]["name"],
                "Published": article["publishedAt"]
            })

        df = pd.DataFrame(records)

        st.dataframe(
            df,
            use_container_width=True
        )