def format_html(text, formatting):
    # formatting = {"b": [[0, 4]], "em": [[3, 7]], ...}
    # ranges are inclusive [start, end]
    # Add a format to the stack when index == format[0]
    stack = []
    format_step_by_type = {key:0 for key in formatting.keys()}
    format_range=make_range(
      formatting, 
      format_step_by_type, 
      set(),
      )
    output = ""
    for index, char in enumerate(text):
      next_stack = []
      popped_list = []
      prefix = ""
      suffix = ""
      print(f"beginning: {index=} {char=} {stack=} {format_range=}")
      for format, this_format_range in format_range.items():
        # print(f"  {format=} {this_format_range=}")

        # If this format has no range left, skip
        if not this_format_range:
          continue
        # Start of formatting range
        if index == this_format_range[0]:
          stack.append(format)
          prefix += f"<{format}>"
          # print(f"    {stack=}")
        # End of formatting range
        elif index == this_format_range[1]:
          # Pop off stack until reach format whose range just ended
          # May have to modify if multiple formats end at the same character
          print(f"    About to pop; {format=} {this_format_range[1]=}")
          popped = None
          while popped != format:
            popped = stack.pop()
            popped_list.append(popped)
            if popped != format:
              next_stack.append(popped)
          #   print(f"      {popped=} because {index=}")
          # print(f"    {next_stack=}")
          for format in popped_list:
            suffix += f"</{format}>"
          stack = next_stack[::-1]
          # print(f"    updated {stack=}")
          format_range=make_range(
            formatting, 
            format_step_by_type, 
            {format},
            )
          continue
          # Re-start formats that were closed because another format had to be closed

      print(f"  end: {index=} {char=} {stack=} {format_range=}")
      output += prefix + char + suffix
    return output

def make_range(
  formatting: dict, 
  format_step_by_type, 
  formats_to_advance: set,
  ):
  # print(f"  make_range {formatting=} {format_step_by_type=} {formats_to_advance=}")
  new_format_range = dict()
  for format in formatting.keys():
    format_step = format_step_by_type[format]
    if format in formats_to_advance:
      format_step += 1
    format_step_by_type[format] = format_step
    # If there is a next format_step, use it
    try:
      new_format_range[format] = formatting[format][format_step]
    except IndexError:
      new_format_range[format] = None
  # print(f"    {new_format_range=} {format_step_by_type=}")
  return new_format_range


text = "Hello world"
formatting = {
  "b": [
  [0, 4], 
  # [6,8]
  ], 
  "em": [[3, 7]],
  }
f = format_html(text, formatting)
print(f)
