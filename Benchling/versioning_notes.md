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

    

