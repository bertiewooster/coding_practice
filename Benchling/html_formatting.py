def format_html(text, formatting):
    # formatting = {"b": [[0, 4]], "em": [[3, 7]], ...}
    # ranges are inclusive [start, end]
    # Add a format to the stack when index == format[0]
    stack = []
    next_stack = []
    format_step_by_type = {key:0 for key in formatting.keys()}
    format_range=make_range(
      formatting, 
      format_step_by_type, 
      set(),
      )
    print(f"{format_range=}")
    output = ""
    for index, char in enumerate(text):
      print(f"beginning: {index=} {char=} {stack=}")
      for format, this_format_range in format_range.items():
        print(f"  {format=} {this_format_range=} {this_format_range[0]=} {this_format_range[1]=}")
        if index == this_format_range[0]:
          stack.append(format)
          print(f"    {stack=}")
        elif index == this_format_range[1]:
          popped = stack.pop()
          print(f"    {popped=} because {index=}")
      print(f"  end: {index=} {char=} {stack=}")
      output += char
    return output

def make_range(
  formatting: dict, 
  format_step_by_type, 
  formats_to_advance: set,
  ):
  new_format_range = dict()
  for format in formatting.keys():
    format_step = format_step_by_type[format]
    if format in formats_to_advance:
      format_step += 1
    new_format_range[format] = formatting[format][format_step]
  return new_format_range


text = "Hello world"
formatting = {"b": [[0, 4]], "em": [[3, 7]]}
f = format_html(text, formatting)
print(f)
