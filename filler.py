import datetime
import html
import re

from myhtml import br, form, myinput, page, select, textarea


CHARACTERS = ["", "bowser", "cf", "dk", "doc", "falco", "fox",
              "game and watch", "ganon", "ic", "jigglypuff", "kirby", "link",
              "luigi", "mario", "marth", "mewtwo", "ness", "peach", "pichu",
              "pikachu", "puff", "roy", "samus", "sheik", "yl", "yoshi",
              "zelda"]

STAGES = ["", "Battlefield", "Dream Land", "Final Destination",
          "Fountain of Dreams", "Pokémon Stadium", "Yoshi's Story"]

DETAILS = "{{BracketMatchDetails|reddit=|comment=|vod=}}"


def load(s):
    if not s:
        return {}
    m = re.search("\|(\w*)p1=", s)
    myround = m.group(1)
    m = re.search("\|" + myround + "p1=(\w*)", s)
    p1 = m.group(1)
    m = re.search("\|" + myround + "p2=(\w*)", s)
    p2 = m.group(1)
    m = re.search("\|" + myround + "p1flag=(\w*)", s)
    p1flag = m.group(1)
    m = re.search("\|" + myround + "p2flag=(\w*)", s)
    p2flag = m.group(1)
    return {"myround": myround,
            "p1": p1,
            "p2": p2,
            "p1flag": p1flag,
            "p2flag": p2flag,
            }


def filler(**kwargs):
    data = {"details": DETAILS,
            "myround": html.escape(kwargs.get("round", "")),
            "p1": html.escape(kwargs.get("p1", "")),
            "p2": html.escape(kwargs.get("p2", "")),
            "p1flag": html.escape(kwargs.get("p1flag", "")),
            "p2flag": html.escape(kwargs.get("p2flag", "")),
            "win": "",
            }
    data.update(load(kwargs.get("load", "")))
    data["server_date"] = html.escape(kwargs.get("server_date", "today"))
    server_date = select("server_date", ["today", "yesterday"],
                         data["server_date"])
    data["set_len"] = html.escape(kwargs.get("set_len", "bo5"))
    set_len = select("set_len", ["bo5", "bo3"],
                     data["set_len"])
    nbgames = 5
    if data["set_len"] == "bo3":
        nbgames = 3
    today = datetime.date.today()
    if data["server_date"] == "yesterday":
        today -= datetime.timedelta(days=1)
    day = today.strftime("%d").lstrip("0")
    date = today.strftime("%B {day}, %Y".format(day=day))
    data["date"] = date
    myround = myinput("round", value=data["myround"])
    p1 = myinput("p1", value=data["p1"])
    p2 = myinput("p2", value=data["p2"])
    p1flag = myinput("p1flag", value=data["p1flag"])
    p2flag = myinput("p2flag", value=data["p2flag"])
    details = ""
    prevp1char = prevp2char = ""
    for g in range(1, nbgames+1):
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
        details += p1char + p2char + stage + br + p1stock + p2stock + br + '\n'
        if data["p1stock" + s] == data["p2stock" + s] == "0":
            data["p1stock" + s] = data["p2stock" + s] = ""
        if not data["stage" + s]:
            data["p1char" + s] = data["p2char" + s] = ""
    wins = [data["win" + str(g)] for g in range(1, nbgames+1)]
    data["p1score"] = wins.count("1")
    data["p2score"] = wins.count("2")
    if data["p1score"] >= (nbgames//2)+1:
        data["win"] = "1"
        nbgames = data["p1score"] + data["p2score"]
    if data["p2score"] >= (nbgames//2)+1:
        data["win"] = "2"
        nbgames = data["p1score"] + data["p2score"]
    myform = form(myround + br + p1 + p2 + br + p1flag + p2flag + br
                  + details + server_date + set_len,
                  "fill", "post")
    template = """|{myround}p1={p1} |{myround}p1flag={p1flag} |{myround}p1score={p1score}
|{myround}p2={p2} |{myround}p2flag={p2flag} |{myround}p2score={p2score}
|{myround}win={win}
"""
    for game in range(1, nbgames+1):
        template += ("|{myround}p1char{game}={p1char{game}} "
                     "|{myround}p2char{game}={p2char{game}} "
                     "|{myround}p1stock{game}={p1stock{game}} "
                     "|{myround}p2stock{game}={p2stock{game}} "
                     "|{myround}win{game}={win{game}} "
                     "|{myround}stage{game}={stage{game}}\n"
                     ).replace("{game}", str(game))
    template += """|{myround}date={date}
|{myround}details={details}"""
    myarea = textarea(rows="12", cols="150", txt=template.format(**data))
    loadarea = textarea("load")
    loadform = form(loadarea, "load", "post")
    return page("filler", myform + myarea + loadform)
