---
name: videos-stay-off-the-code-branches
description:
  "Lesson videos are made in scratch/ in ftc31459-26-27-biobuzz; each page's current video and the
  guide's screenshots are archived in corbels-lfs-lessons, never on main, a lessons branch or a
  solutions branch."
metadata:
  type: project
---

Videos made for the guide stay in `scratch/` in `ftc31459-26-27-biobuzz` while they are being
made. The current video of each page, and the guide's screenshots, are archived in
`corbels-lfs-lessons`, on the branch named for the `ftc31459-26-27-biobuzz` branch they belong
to. They are never committed to `main`, a lessons branch or a solutions branch of
`ftc31459-26-27-biobuzz`.

**Why:** the user (Mike), 2026-10-02: *"let's leave the videos in scratch in ftc31459 until we
decide that we have a good book, in which case we are likely going to need to put them on a dated
or versioned throwaway branch so they don't become part of the main, lessons, or solutions branches
ever."* Then, 2026-10-11: *"Yes video and images are archived in corbels-lessons. Let's call it
corbels-lfs-lessons."* The plan is `.docs/2026-10-11-lfs-lessons.md`.

**How to apply:** never `git add` a video on a code branch of `ftc31459-26-27-biobuzz`.
`/scratch/` is in the subproject's `.gitignore` from `54054fa` on `lessons-try`; a branch that does
not carry that commit does not ignore it.
