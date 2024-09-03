from bandwagon import BandsPattern, BandsPatternsSet, LADDER_100_to_4k

ladder = LADDER_100_to_4k.modified(label="Ladder", background_color="#ffffaf")

patterns = [
    BandsPattern([450, 630], ladder, label="Pp"),
    BandsPattern([350, 630], ladder, label="Pf"),
    BandsPattern([250, 630], ladder, label="Ps"),
    BandsPattern([180, 250, 630], ladder, label="Pss"),
]
patterns_set = BandsPatternsSet(patterns=[ladder] + patterns, ladder=ladder,
                                label="Test Pseudomonas", ladder_ticks=3)
ax = patterns_set.plot()
ax.figure.savefig("simple_band_patterns.png", bbox_inches="tight", dpi=200)
