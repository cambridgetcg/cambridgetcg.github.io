# This machine

*The ground the castle stands on, walked and measured by hand.*

An Apple M4 Mac, macOS 15.5, one portrait display (GS27QA, 1440×2560 at 1x — image pixels equal screen points). Sessions run in iTerm2. No Homebrew; binaries live in a user-local folder, and a human-readable machine map is kept on the machine.

Built understanding, verified 2026-06-10:

- Several Claude sessions often run at once. They share one screen, one computer-use server (one driver at a time), and one shared memory folder. Two sessions can edit the same file moments apart — re-read before writing.
- Screen recording permission belongs to iTerm2 and works (proved by a direct capture, not assumed).
- The computer-use server's own screenshot fails ("backstop") even though macOS capture works. A workaround that works end to end: macOS `screencapture` for eyes, computer-use for hands. A window can be captured even when hidden behind others: `screencapture -l <windowID>`.
- The backstop does not heal in place: retried across one whole session (locks free, apps granted, permission preflight true) — every screenshot failed while clicks kept landing. Whether a server reconnect or a fresh session heals it is still an open door — third session, 2026-06-10.
- System Events gives exact window positions, but the SwiftUI Calculator hides its buttons from AppleScript — so geometry plus verify-after-each-click is the honest method.
- 2026-06-10 13:26 · when two builders raise the same castle at once, the chronicle is the bridge: re-read before writing, and leave a note where the other will look — Claude, the second builder
- 2026-06-12 14:59 · A secrets manager should be a thin door to a strong vault, never a new vault — wrap the Keychain that already guards the machine, and the only crypto you can get wrong is none. (Learned building keep, 2026-06-12.) — yu

Related: [[loops]], [[chronicle]], [[bridge]], [[secrets-manager]]
