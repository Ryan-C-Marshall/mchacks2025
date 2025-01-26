import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import metadata

all_genres = metadata.all_genres  # cutoff at 0.8 or sm

all_artists = metadata.all_artists  # either the arist is in the prompt or not (0.8 threshold)

artist_genres = {
  # TODO
}

# other available fields: 
# "Track Name" "Artist Name(s)" "Album Name" "Album Artist Name(s)" "Track Duration (ms)" "Explicit"



### PANDAS STUFF ###
df = pd.read_csv('backend/top_10000_1960-now.csv')

artist_genres = {}
for _, row in df.iterrows():
  artists: list = row["Artist Name(s)"].split(",")
  genres: list = list(set(row["Artist Genres"].split(",")))

  for genre in genres:
    if genre not in all_genres:
      genres.remove(genre)

  print("Artists: " + str(artists) + ", genres: " + str(genres))

  for artist in artists:
    artist_genres[artist] = artist_genres.get(artist, []) + genres


# print(df.head())

# Display basic info about the dataset
# print(df.info())

# Get summary statistics of numeric columns
# print(df.filter(items=["Key","Loudness", "Valence"]).describe())

### PANDAS STUFF - END ###

metrics_to_words = {
  "Danceability": [["Dance", "Party"], ["Calm", "Relaxed"]], # happy used for valence already
  "Energy": [["Energetic", "Party"], ["Slow", "Calm"]],
  "Acousticness": [["Acoustic"], ["Electronic"]],
  "Instrumentalness": [["Instrumental"], ["Singing"]],
  "Valence": [["Happy", "Joy"], ["Sad"]]
}

'''
energy is bad - energetic?

'''

def get_association_words():
  association_words = []
  for val in metrics_to_words.values():
    association_words = association_words + val[0] + val[1]
  
  association_words = list(set(association_words)) # remove duplicates from metrics_to_words
  
  association_words += all_genres
  association_words += all_artists

  return association_words


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


def rank_songs(association_word_scores: dict):

  # (1) extract genre data from genres - use a cutoff of TODO (0.8?)

  # (2) extract genre data from artists
  
  # (2.1) use a cutoff of 0.8 to determine artists

  # (3) split songs into two lists: fit in genre, and don't fit in genre

  # (4) if date, split each list into correct and incorrect era

  # (5) sort each (either both, or all four) lists by metrics

  # (5.1) also sort by popularity?

  # (6) combine all lists, return

  pass

'''
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
'''
