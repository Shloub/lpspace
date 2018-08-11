import datetime
import html

from myhtml import br, form, myinput, page, select, textarea


CHARACTERS = ["", "bowser", "cf", "dk", "doc", "falco", "fox",
              "game and watch", "ganon", "ic", "jigglypuff", "kirby", "link",
              "luigi", "mario", "marth", "mewtwo", "ness", "peach", "pichu",
              "pikachu", "puff", "roy", "samus", "sheik", "yl", "yoshi",
              "zelda"]

STAGES = ["", "Battlefield", "Dream Land", "Final Destination",
          "Fountain of Dreams", "Pokémon Stadium", "Yoshi's Story"]

DETAILS = "{{BracketMatchDetails|reddit=|comment=|vod=}}"

TEMPLATE = """|{myround}win={win}
"""
for game in range(1, 6):
    TEMPLATE += "|{myround}p1char{game}={p1char{game}} |{myround}p2char{game}={p2char{game}} |{myround}p1stock{game}={p1stock{game}} |{myround}p2stock{game}={p2stock{game}} |{myround}win{game}={win{game}} |{myround}stage{game}={stage{game}}\n".replace("{game}", str(game))
TEMPLATE += """|{myround}date={date}
|{myround}details={details}
"""


def filler(**kwargs):
    today = datetime.date.today()
    day = today.strftime("%d").lstrip("0")
    date = today.strftime("%B {day}, %Y".format(day=day))
    data = {"date": date,
            "details": DETAILS,
            "myround": html.escape(kwargs.get("round", "")),
            "win": "",
            }
    myround = myinput("round", value=data["myround"])
    details = ""
    prevp1char = prevp2char = ""
    for g in range(1, 6):
        s = str(g)
        data["stage" + s] = html.escape(kwargs.get("stage" + s, ""))
        stage = select("stage" + s, STAGES,
                       kwargs.get("stage" + s, ""))
        data["p1char" + s] = html.escape(kwargs.get("p1char" + s, ""))
        if not data["stage" + s]:
            data["p1char" + s] = prevp1char
        prevp1char = data["p1char" + s]
        p1char = select("p1char" + s, CHARACTERS,
                        data["p1char" + s])
        data["p2char" + s] = html.escape(kwargs.get("p2char" + s, ""))
        if not data["stage" + s]:
            data["p2char" + s] = prevp2char
        prevp2char = data["p2char" + s]
        p2char = select("p2char" + s, CHARACTERS,
                        data["p2char" + s])
        data["p1stock" + s] = html.escape(kwargs.get("p1stock" + s, "0"))
        p1stock = myinput("p1stock" + s, mytype="number", mymin="0", mymax="4",
                          value=data["p1stock" + s])
        data["p2stock" + s] = html.escape(kwargs.get("p2stock" + s, "0"))
        p2stock = myinput("p2stock" + s, mytype="number", mymin="0", mymax="4",
                          value=data["p2stock" + s])
        data["win" + s] = ""
        if int(data["p1stock" + s]) > int(data["p2stock" + s]):
            data["win" + s] = "1"
        if int(data["p1stock" + s]) < int(data["p2stock" + s]):
            data["win" + s] = "2"
        details += br + p1char + p2char + stage + br + p1stock + p2stock + '\n'
        if data["p1stock" + s] == data["p2stock" + s] == "0":
            data["p1stock" + s] = data["p2stock" + s] = ""
        if not data["stage" + s]:
            data["p1char" + s] = data["p2char" + s] = ""
    wins = [data["win" + str(g)] for g in range(1, 6)]
    if wins.count("1") >= 3:
        data["win"] = "1"
    if wins.count("2") >= 3:
        data["win"] = "2"
    myform = form(myround + details, "fill", "post")
    myarea = textarea(rows="10", cols="150", txt=TEMPLATE.format(**data))
    return page("filler", myform + myarea)
