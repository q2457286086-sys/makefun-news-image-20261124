# The World Today — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/q2457286086-sys/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/q2457286086-sys/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A newspaper front page summing up 24 November 2026's world news in a single
1024×1024 image — an entry for the make.fun `news-image-20261124` bounty.

## What's on the page

- **Lead:** Jensen Huang reinstated as Nvidia CEO, 11 days after stepping
  down amid a "spy" controversy, after Trump intervened.
- **Photo story:** Ukraine says its sea drones sank a Russian warship off
  Libya in a Benghazi operation that also destroyed a Ka-27 helicopter and
  hit cargo ship MV Angara.
- **Secondaries:** NATO vows space defence after reports Russia may launch a
  nuclear space weapon next month; Russian strikes kill at least 14 in the
  Kyiv region, Ukraine says.
- **In brief:** more bodies recovered from the Indonesia candy factory fire;
  Trump offers the Philippines $2.4bn for self-defence; Mexico captures an
  FBI most-wanted drug kingpin with US drone help; GTA VI hacker Arion
  Kurtaj gets 7 years; US states sue Musk firms over sexualised Grok images;
  storms and airline glitches threaten Thanksgiving travel; COP31 talks
  collapse with no deal; Democrats clinch their biggest House majority
  since 1992 (258 seats).

All headlines were checked against reports dated 24 November 2026. No death
toll is printed for the Indonesia factory fire — only that more bodies were
recovered — because no verified figure was available.

## How it was built

- `hero.png` — photorealistic image of the sea-drone strike off Libya at
  dawn, generated for this entry.
- `build_frontpage.py` — a fresh Python/PIL script that composes
  `entry.png` (1024×1024) from `hero.png`: masthead, lead story, photo
  story, two secondary stories, an IN BRIEF band, and a footer.
- `main.ts` — copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default
  `/output`). Run it with `node main.ts`; output is deterministic
  (byte-identical across runs).

## License

MIT — see [LICENSE](LICENSE).
