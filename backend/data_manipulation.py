import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

df = pd.read_csv('backend/top_10000_1960-now.csv')
print(df.head())

# Display basic info about the dataset
print(df.info())

# Get summary statistics of numeric columns
print(df.filter(items=["Key","Loudness", "Valence"]).describe())

# words: "Album Release Date" "Popularity" "Artist Genres" "Tempo"

metrics_to_words = {
  "Danceability": [["Dance", "Party"], ["Calm", "Relaxed"]], # happy used for valence already
  "Energy": [["Energy", "Party"], ["Slow", "Calm"]],
  "Loudness": [["Loud", "Hype"], ["Quiet"]], # hype again? change
  "Speechiness": [["Slow"], ["Musical"]],  # putting musical here should naturally discourage lots of speechiness
  "Acousticness": [["Acoustic"], ["Electronic", "EDM"]],
  "Instrumentalness": [["Instrumental"], ["Singing"]],
  "Valence": [["Happy", "Joy"], ["Sad"]]
}

# TODO: add genres to associations

# Case 1: date/era is included
# Case 2: genre(s) is included
# Case 3: artist is included - look at that genre

# other: "Track Name" "Artist Name(s)" "Album Name" "Album Artist Name(s)" "Track Duration (ms)" "Explicit"

def get_association_words():
  association_words = []
  for val in metrics_to_words.values():
    association_words = association_words + val[0] + val[1]
  
  return list(set(association_words))
  

def score_metrics(association_word_scores: dict):
  """
  Example argument: 
  {
  'Dance': 0.9,
  'Happy': 0.9,
  'Calm': 0.2,
  'Relaxed': 0.2,
  'Energy': 0.6,
  'Party': 0.7,
  'Hype': 0.4,
  'Slow': 0.3,
  'Loud': 0.5, 
  'Quiet': 0.1,
  'Musical': 0.8,
  'Acoustic': 0.7,
  'Instrumental': 0.7,
  'Singing': 0.7
  'Electronic': 0.4,
  'EDM': 0.8,
  'Happy': 0.6,
  'Joy': 0.6,
  'Sad': 0.1
  }
  """
  metric_scores = {}

  for key, value in metrics_to_words.items():
    score = 0
    pos_length = len(value[0])
    neg_length = len(value[1])

    for assoc_word in value[0]:
      score += association_word_scores[assoc_word] / pos_length
  
    if neg_length != 0:
      for assoc_word in value[1]:
        score -= association_word_scores[assoc_word] / neg_length

    metric_scores[key] = score
  
  return metric_scores

def rank_songs(metric_scores: dict):
  pass


print(score_metrics({
  'Dance': 0.9,
  'Happy': 0.9,
  'Calm': 0.2,
  'Relaxed': 0.2,
  'Energy': 0.6,
  'Party': 0.7,
  'Hype': 0.4,
  'Slow': 0.3,
  'Loud': 0.5, 
  'Quiet': 0.1,
  'Musical': 0.8,
  'Acoustic': 0.7,
  'Instrumental': 0.7,
  'Singing': 0.7,
  'Electronic': 0.4,
  'EDM': 0.8,
  'Happy': 0.6,
  'Joy': 0.6,
  'Sad': 0.1
  }))