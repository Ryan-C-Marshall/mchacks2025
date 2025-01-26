import math
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import backend.big_data as big_data

GENRE_CUTOFF = 0.7
ARTIST_CUTOFF = 0.8
ERA_CUTOFF = 0.85

all_genres = big_data.all_genres  # cutoff at 0.8 or sm

all_artists = big_data.all_artists  # either the arist is in the prompt or not (0.8 threshold)

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

print("Done artist genres!")

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

def get_descriptors():
  descriptors = []
  for val in metrics_to_words.values():
    descriptors = descriptors + val[0] + val[1]
  
  descriptors = list(set(descriptors)) # remove duplicates from metrics_to_words
  

def get_association_words():
  association_words = []

  association_words += get_descriptors()
  association_words += all_genres
  association_words += big_data.all_eras
  association_words += all_artists


  return association_words

def normalize_descriptor_scores(descriptor_scores: dict):
  """
  Descriptor scores has each descriptor, and the max association value that was found for it
  """
  normalized_descriptor_scores = {}
  for descriptor in get_descriptors:
    mean, stdev = big_data.mean_stdev_descriptors[descriptor]

    normalize_descriptor_scores[descriptor] = (descriptor_scores[descriptor] - mean) / stdev
  
  return normalized_descriptor_scores


def score_metrics(normalized_descriptor_scores: dict):
  """
  Descriptor scores has each descriptor, and a normalized value for that descriptor, which depends on the prompt
  """
  metric_scores = {}

  for key, value in metrics_to_words.items():
    score = 0
    pos_length = len(value[0])
    neg_length = len(value[1])

    for assoc_word in value[0]:
      score += normalized_descriptor_scores[assoc_word] / pos_length
  
    if neg_length != 0:
      for assoc_word in value[1]:
        score -= normalized_descriptor_scores[assoc_word] / neg_length

    metric_scores[key] = score
  
  return metric_scores


def rank_songs(association_word_scores: dict):

  genres = []

  # (1) extract genre data from genres - use a cutoff

  for genre in all_genres:
    if association_word_scores[genre] > GENRE_CUTOFF:
      genres.append(genre)

  # (2) extract genre data from artists

  for artist in all_artists:
    if association_word_scores[artist] > ARTIST_CUTOFF: # (2.1) use a cutoff to determine artists
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
  for era in big_data.all_eras:
    if association_word_scores[era] > ERA_CUTOFF:
      eras.append(era)


  df["Correct Era"] = df["Album Release Date"].apply(
    lambda release_date: 
    any(
      release_date[0:4] in [era[0:4] for era in eras]
    ) if type(release_date) == str else False
  )

  # (5) add field to sort by metrics

  metric_scores = score_metrics(normalize_descriptor_scores(association_word_scores))

  def score_song(row):
    '''
    We have:
    - song danceability, energy, valence
    - score of those three from the prompt
    '''
    return row["Danceability"] * metric_scores["Danceability"] + \
    row["Energy"] * metric_scores["Energy"] + \
    row["Valence"] * metric_scores["Valence"]


  df["Metrics Score"] = df.apply(score_song, axis=1)


  # (5.1) also sort by popularity?

  # (6) sort, starting with least important metrics

  sorted_df = df.sort_values(
    by=["Metrics Score"],
    ascending=True
  )\
  .sort_values(
    by=["Correct Era"],
    ascending=[False],
    key=lambda col: col if col.name == "Correct Era" else None
  )\
  .sort_values(
    by=["Contains Correct Genre"], 
    ascending=[False],
    key=lambda col: col if col.name == "Contains Correct Genre" else None
  )

  print(sorted_df.head)
  
