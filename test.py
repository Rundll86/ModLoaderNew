from conkits import Choice,Colors256

sth = Choice(options=["A", "B", "C"])
sth.set_keys({"up": "H", "down": "P", "confirm": "\r"})
sth.checked_ansi_code=Colors256.BACK255+Colors256.FORE0
sth.run()