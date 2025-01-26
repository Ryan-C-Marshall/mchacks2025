import math
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
  artists = row["Artist Name(s)"]
  artists: list = artists.split(", ") if type(artists) == str else []

  genres: list = row["Artist Genres"]
  genres = set(genres.split(",")) if type(genres) == str else set()

  genres = list(set.intersection(genres, set(all_genres)))

  for artist in artists:
    artist_genres[artist] = artist_genres.get(artist, []) + genres

print(artist_genres)
'''
# print(df.head())

# Display basic info about the dataset
# print(df.info())

# Get summary statistics of numeric columns
# print(df.filter(items=["Key","Loudness", "Valence"]).describe())
'''

### PANDAS STUFF - END ###

metrics_to_words = {
  "Danceability": [["Dance", "Party"], ["Calm", "Relaxed"]],
  "Energy": [["Energetic", "Party"], ["Slow", "Chill"]],
  "Valence": [["Happy", "Joy"], ["Sad"]]
}

def get_association_words():
  association_words = []
  for val in metrics_to_words.values():
    association_words = association_words + val[0] + val[1]
  
  association_words = list(set(association_words)) # remove duplicates from metrics_to_words
  
  association_words += all_genres
  association_words += all_artists
  association_words += metadata.all_eras

  return association_words


def score_metrics(descriptor_scores: dict):
  """
  Descriptor scores has each descriptor, and the max association value that was found for it
  """
  metric_scores = {}

  for key, value in metrics_to_words.items():
    score = 0
    pos_length = len(value[0])
    neg_length = len(value[1])

    for assoc_word in value[0]:
      score += descriptor_scores[assoc_word] / pos_length
  
    if neg_length != 0:
      for assoc_word in value[1]:
        score -= descriptor_scores[assoc_word] / neg_length

    metric_scores[key] = score
  
  return metric_scores


def rank_songs(association_word_scores: dict):

  genres = []

  # (1) extract genre data from genres - use a cutoff of TODO (0.8?)

  for genre in all_genres:
    if association_word_scores[genre] > 0.8: # FIXME
      genres.append(genre)

  # (2) extract genre data from artists

  for artist in all_artists:
    if association_word_scores[artist] > 0.8: # (2.1) use a cutoff of 0.8 to determine artists
      genres = genres + artist_genres[artist]

  # (3) add a field to sort by: fit in genre / don't fit in genre

  df["Contains Correct Genre"] = df["Artist Genres"].apply(
    lambda artist_genres: 
    any(
      genre in genres for genre in map(str.strip, artist_genres.split(","))
    ) if type(artist_genres) == str else False
  )

  # (4) add a field to sort by correct / incorrect era

  eras = []
  for era in metadata.all_eras:
    if association_word_scores[era] > 0.8: # FIXME
      eras.append(era)


  df["Correct Era"] = df["Album Release Date"].apply(
    lambda release_date: 
    any(
      release_date[0:4] in [era[0:4] for era in eras]
    ) if type(release_date) == str else False
  )

  # (5) add field to sort by metrics

  def score_song(row):
    '''
    We have:
    - song danceability, energy, valence
    - score of those three from the prompt
    '''
    pass


  df["Metrics Score"] = df.apply(score_song, axis=1)


  # (5.1) also sort by popularity?

  # (6) sort, starting with least important metrics

  sorted_df = df.sort_values(
    by=["Contains Correct Genre"], 
    ascending=[False],
    key=lambda col: col if col.name == "Contains Correct Genre" else None
  )

  print(sorted_df.head)
  
  
rank_songs()