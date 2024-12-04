from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI()

# Configuração da pasta estática
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


# Configuração da API do YouTube
YOUTUBE_API_KEY = "AIzaSyBLrGVtdt6tvvHtHPq5Su2hELBkIInMMTA"  # Substitua pela sua API Key
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
analyzer = SentimentIntensityAnalyzer()

@app.get("/analyze")
def analyze_video(video_id: str):
    try:
        comments = []
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=10,
            order="relevance"
        ).execute()

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        results = []
        for comment in comments:
            sentiment = analyzer.polarity_scores(comment)
            results.append({
                "comment": comment,
                "sentiment": sentiment
            })

        print("Results being returned:", {"video_id": video_id, "analysis": results})  # Log dos resultados
        return {"video_id": video_id, "analysis": results}
    except Exception as e:
        print("Error in analyze_video:", e)  # Log do erro
        return {"error":
           str(e)}
