def format_html(text, formatting):
    from collections import defaultdict

    opens = defaultdict(list)
    closes = defaultdict(list)

    for tag, ranges in formatting.items():
        for start, end in ranges:
            opens[start].append(tag)
            closes[end + 1].append(tag)

    result = []
    active = []  # stack of open tags in order of opening

    for i in range(len(text) + 1):
        # Process closes
        if i in closes:
            to_close = set(closes[i])
            # Unwind tags that opened after the ones closing now
            saved = []
            while active and active[-1] not in to_close:
                t = active.pop()
                result.append(f"</{t}>")
                saved.append(t)
            # Close the target tags
            while active and active[-1] in to_close:
                t = active.pop()
                result.append(f"</{t}>")
                to_close.discard(t)
            # Re-open the unwound tags
            for t in reversed(saved):
                result.append(f"<{t}>")
                active.append(t)

        # Process opens
        if i in opens:
            for tag in opens[i]:
                result.append(f"<{tag}>")
                active.append(tag)

        # Emit character
        if i < len(text):
            result.append(text[i])

    # Close any remaining open tags
    for t in reversed(active):
        result.append(f"</{t}>")

    return "".join(result)


text = "Hello world"
formatting = {
    "b": [
        [0, 4],
        # [6,8]
    ],
    "em": [
        [3, 7],
        # [6,8]
    ],
}
f = format_html(text, formatting)
print(f)
