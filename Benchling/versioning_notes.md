# Versioning questions

## Use cases

1. Retrieve document at version N
    - To retrieve a document and version in, I would take the document ID and go into the document version table and then extract version number n.
    - **indexing**. You'd want a composite index on (DocumentID, Version_number) so this lookup is fast, especially if documents have hundreds of versions. That's a natural follow-up the interviewer might ask — "how would you optimize this query?"


1. Show diff between two versions
    - Go to the document version table, search by document ID, and extract the two versions. I would compare the JSON content between the two versions as well as the formatting range. For example, if the letter a was regular in one version and bold in the second version, I would show the a becoming bold in the second version.
    - Content: Fetch both versions and do a diff of the text content first — what was inserted, deleted, or unchanged. This is essentially the same algorithm as git diff, and there's a classic algorithm for it called Myers diff (or the simpler longest common subsequence approach). 
    - Formatting: For each character, check whether its formatting has changed, for example regular to bold.
        - This gets more complicated if text is inserted or deleted between versions: You can't just compare the formatting at index n. You'd have to map one version's text onto another, adjust the indexing of one version, and then do the formatting comparison.

1. Roll back to a prior version
    - To roll back to a prior version, I'd go to the DocumentVersion table. For the given DocumentID, I'd retrieve the desired Version_number; this would be faster if we indexed on the composite key of (DocumentID, Version_number).
        - For the snapshot scheme, it would be easy, simply retrieve that content and formatting_ranges.
        - For the delta scheme, we'd store occasional snapshots, say every 10th version (snapshot checkpoints). Then we'd go back to the last checkpoint before the desired version and replay the deltas until we get to the desired version. We'd do this in both DocumentVersion and Formatting_range tables.
    - After we restored an old version, we'd want to save it as a new version. That would let us track when the rollback occurred and who did it.

1. Multiple users editing
    - For multiple users editing, probably the most important thing is that each of them has all the updates as soon as possible for real-time collaboration. So we'd want to make foreign updates in near-real time.
        - That would be easier with the delta approach because we don't have to ship around the whole document, just changes.
        - Perhaps the safest, but resource-intensive, approach would be to make each delta that's shipped around its own DocumentVersion. Alternatively we could create a DocumentVersion with some frequency that combines multiple people's changes, though that would lose the audit logging of who did what, so it's probably unappealing.
    - You'd likely need a message broker like Kafka or a WebSocket server to fan out deltas to all connected users in real time.

## Tradeoffs

1. Full snapshots vs. deltas: Full snapshots allow easy jumping to versions for rollback or diffs, but use a lot of storage and would have to be compared to create a diff. Deltas are smaller per entry but more cumbersome to jump to: You'd probably save checkpoint snapshots, go back to the last snapshot before the desired version,  and then replay changes to get to the desired version (reconstruction cost).
    - The reconstruction cost can be bounded. With checkpoint snapshots every N versions, the worst case reconstruction is always N delta replays, never the full version history. So you're trading storage cost (more snapshots = more storage) against reconstruction cost (fewer snapshots = more replays).
    - N is a tunable parameter — you'd set it based on your read/write ratio. A document that gets read frequently but edited rarely warrants more frequent snapshots. That's because reads trigger reconstruction, so it's worth caching more snapshots to prevent more reconstruction steps.
    - This is a similar tradeoff to database indexing: indexes speed up reads at the cost of write overhead and storage--that's why you don't index every column. Snapshot checkpointing similarly makes it so you don't have to go through row by row--you can jump to a row that's close to the one you want. 
    - The more a document is read from vs. written to, the more checkpoint snapshots you'd want to store.
    - Full snapshots are much simpler to implement and reason about, so you'd probably start with them, then move to deltas after you prove your product is valuable and observe the read/write patterns.

1. SQL vs. NoSQL:
    - NoSQL is better for storage flexibility for the document content itself. They tend to be flexible in their schemas, which is good if your document structure might change. They're optimized for retrieving whole documents based on their ID.
    - SQL is better on joins and querying, for example creating the audit log. Modern PostgreSQL SQL contains JSON as a data type, including binary, which makes it close to e.g. MongoDB in terms of efficiency of storing JSON.

1. Granularity — do you version per keystroke, per save, per session?
    - Per keystroke would probably be excessive, especially if you're storing a snapshot in DocumentVersion. Something like per save probably makes sense, or if your system auto-saves you'd version on that--probably when the user pauses typing. Per session may not be frequent enough because a user may make a ton of changes during a long session and not want to be forced to lose them all to undo a mistake. But when the user wants to roll back, you might want to present versions per session at least coarsely first ("I remember that yesterday's version didn't have this new problem") so the user isn't looking at dozens of versions.
    - We might add a bookmarking flag to DocumentVersion IsStartOfSession so we track those session versions, and let the user attach a label to it.
        - With AI, we might auto-generate a suggested label by diffing it compared to the previous bookmark. GitHub CoPilot does something similar for git diffs.
        - Given the proprietary data stored in Benchling lab notebooks, we'd want the AI to run within a privacy-compliant boundary, not get sent to public ChatGPT.
    - On per-keystroke being excessive: Correct, especially for snapshots. Though notably Google Docs does capture very fine-grained operations internally — but they're deltas, not snapshots, and they're compacted over time. So the granularity question is partly a function of your storage model.
    - On per-save / auto-save: This is the right default. The "pause in typing" trigger is called debouncing as mentioned earlier, and it's the standard approach in real collaborative editors.

