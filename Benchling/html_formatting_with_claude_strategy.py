from collections import defaultdict

def format_html(text, formatting):
  # formatting = {"b": [[0, 4]], "em": [[3, 7]], ...}
  # ranges are inclusive [start, end]

  # Set up triggers for begins and ends of formats
  begins = defaultdict(list)
  ends = defaultdict(list)
  for format, ranges in formatting.items():
    for range in ranges:
      begins[range[0]].append(format)
      ends[range[1] + 1].append(format)

  # for index, character in text:
  for index, character in enumerate(text):
    # Close any tags which end at this character

    # Open any tags which begin at this character

    # Output the character
  
  # Close any open tags

  # Return the concatenated output


text = "Hello world"
formatting = {
  "b": [
  [0, 4], 
  [6,8]
  ], 
  "em": [[3, 7]],
  "i": [[3, 4]],
  }
f = format_html(text, formatting)
print(f)
