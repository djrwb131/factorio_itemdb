import lualoader as ll
import string 

from pathlib import Path
from flask import Flask, render_template, Response
# This should take a technology and a time frame, and return a
# complete strategy from original spawn.
tech_goals = ["gun-turret","modular-armor","stack-inserter","physical-projectile-damage-2","weapon-shooting-speed-2","inserter-capacity-bonus-2","rocket-silo"]
def generate_stages(t):
    TECH_GOALS = set(ll.techs[x] for x in t)
    for x in t:
        TECH_GOALS.update(ll.techs[x].getAllPrerequisites())
# Stage 1: Completed when there is an automated, steady supply of 
# red packs, produced at the specified rate, and all red-only 
# technologies are completed.
    stage1 = {
        "stage_number" : 1,
        "outputs": {
            "automation-science-pack": 18,
        },
        "techs": ll.filter_techs(ll.RED_TECH,TECH_GOALS)
    }
# Stage 2: Completed when there is an automated, steady supply of
# green packs, produced at the specified rate, and all red/green 
# technologies are completed.
    stage2 = {
        "stage_number": 2,
        "outputs": {
            "logistic-science-pack": 18,
        },
        "techs": ll.filter_techs( (ll.RED_TECH,ll.GREEN_TECH), TECH_GOALS)
    }
# Stage 3: Completed when there is an automated, steady supply of
# blue packs, produced at the specified rate, and all red/green/blue
# technologies are completed.
    stage3 = {
        "stage_number": 3,
        "outputs": {
            "chemical-science-pack": 18,
        },
        "techs": ll.filter_techs( (ll.RED_TECH,ll.GREEN_TECH,ll.BLUE_TECH), TECH_GOALS)
    }
# Stage 4: Completed when there is an automated, steady supply of
# purple packs, produced at the specified rate, and all red/green/blue/purple
# technologies are completed.
    stage4 = {
        "stage_number": 4,
        "outputs": {
            "production-science-pack": 18,
        },
        "techs": ll.filter_techs( (ll.RED_TECH,ll.GREEN_TECH,ll.BLUE_TECH,ll.PURPLE_TECH), TECH_GOALS)
    }
# Stage 5: Completed when there is an automated, steady supply of
# yellow packs, produced at the specified rate, and all red/green/blue/yellow
# technologies are completed. You may remove purple production during this stage.
    stage5 = {
        "stage_number": 5,
        "outputs": {
            "utility-science-pack": 18,
        },
        "techs": ll.filter_techs( (ll.RED_TECH,ll.GREEN_TECH,ll.BLUE_TECH,ll.YELLOW_TECH), TECH_GOALS)
    }
# Stage 6: Completed when all packs have automated, steady supplies,
# produced at their specified rates, and all relevant technologies are completed.
# All technology research is cut upon completion of stage 6.
    stage6 = {
        "stage_number": 6,
        "techs": ll.filter_techs( (ll.RED_TECH,ll.GREEN_TECH,ll.BLUE_TECH,ll.PURPLE_TECH,ll.YELLOW_TECH), TECH_GOALS)
    }
    stage6["outputs"] = stage1['outputs'] | stage2['outputs'] | stage3['outputs'] | stage4['outputs'] | stage5['outputs']

# Stage 7: Completed when a steady supply of rocket parts has been established at
# the specified rate.
    stage7 = {
        "stage_number": 7,
        "outputs": { "rocket-part": 2}
    }
# Stage 8: Completed when a rocket is fired into space, and all relevant 
# celebrations have occured. Stage 8 must be completed within 8 hours.
    return [stage1,stage2,stage3,stage4,stage5,stage6,stage7]

app = Flask(__name__)
@app.route("/")
def get_checklist():
    return render_template( "app.html",stages=generate_stages(tech_goals),items=ll.items,recipes=ll.recipes,techs=ll.techs )

@app.route("/images/items/<name>")
def get_item_icon(name):
    try:
        item_icon = None
        if not name in ll.items:
            return Response(status=404)
        else:
            if 'icon' in ll.items[name]:
                item_icon = Path(ll.items[name]['icon'].replace("__base__/","base/").replace("__core__/","core/"))
            else:
                item_icon = Path(ll.items[name]['icons'][0]['icon'].replace("__base__/","base/").replace("__core__/","core/"))
        with open(ll.DATA_LOCATION.joinpath(item_icon),"rb") as f:
            ret = f.read()
            return ret
    except KeyError as ke:
        print(name)
        print(item_icon if item_icon else "Item icon couldn't be loaded")
        print(ll.techs[name].raw if name in ll.techs else "Not in techs")

@app.route("/images/techs/<name>")
def get_tech_icon(name):
    try:
        item_icon = None
        if not name in ll.techs:
            return Response(status=404)
        else:
            if 'icon' in ll.techs[name].raw:
                item_icon = Path(ll.techs[name].raw['icon'].replace("__base__/","base/").replace("__core__/","core/"))
            else:
                item_icon = Path(ll.techs[name].raw['icons'][0]['icon'].replace("__base__/","base/").replace("__core__/","core/"))
        print(item_icon)
        print(ll.DATA_LOCATION)
        print(ll.DATA_LOCATION.joinpath(item_icon))
        print(ll.INSTALL_LOCATION)
        with open(ll.DATA_LOCATION.joinpath(item_icon),"rb") as f:
            ret = f.read()
            return ret
    except KeyError as ke:
        print(name)
        print(item_icon if item_icon else "Item icon couldn't be loaded")
        print(ll.techs[name].raw if name in ll.techs else "Not in techs")