import json
from pathlib import Path
import subprocess as proc
import string

INSTALL_LOCATION=Path("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Factorio")
DATA_LOCATION= INSTALL_LOCATION.joinpath("data")
RECIPE_LOCATION_SUFFIX = Path("prototypes\\recipe.lua")
RESEARCH_LOCATION_SUFFIX = Path("prototypes\\technology.lua")

DEFAULT_ENERGY_REQUIRED = 0.5
DEFAULT_RESULT_COUNT = 1

LUA_PATH = '.\\lua\\?.lua;.\\lua\\?\\init.lua;' + str(DATA_LOCATION.joinpath('core')) + '\\?.lua;' + str(DATA_LOCATION.joinpath('core')) + '\\?\\init.lua'
LUA_CPATH = '.\\lua\\?.dll'
class Recipe:
    def __init__(self,d):
        # Keep a copy of the raw data in case we need it
        self.raw = d
        self.name = d['name']
        # Link to research required, if applicable
        self.unlocked_by = None

        # There are a few ways information is serialized in the factorio data files.
        # This area of code sanitizes the serialized data.

        # Honestly, who even plays expensive mode?
        if 'normal' in d:
            ingr = d['normal']
        else:
            ingr = d

        if 'energy_required' in ingr:
            self.energy_required = ingr['energy_required']
        else:
            self.energy_required = DEFAULT_ENERGY_REQUIRED
            
        # Sanitize result data
        if 'result' in ingr:
            if 'result_count' in ingr:
                rc = ingr['result_count']
            else:
                rc = DEFAULT_RESULT_COUNT
            self.results = (  (ingr['result'],rc), )
        elif 'results' in ingr:
            self.results = []
            for r in ingr['results']:
                if isinstance(r,dict):
                    self.results.append( (r['name'],r['amount']))
                elif isinstance(r,list):
                    self.results.append( tuple(r) )
                else:
                    print("ERROR IN RECIPE " + self.name + ": results were malformed")
                    print(self.raw['results'])
            self.results = tuple(self.results)
        else:
            print("ERROR IN RECIPE " + self.name + ": no recipe results?")
        self.ingredients = ( (x[0],x[1]) if isinstance(x,list) else (x['name'],x['amount']) for x in ingr['ingredients'] )
            
    def __hash__(self):
        return hash(self.name)
    def __eq__(self,other):
        return self.name == other
    def __str__(self):
        return self.name
RED_TECH = "automation-science-pack"
GREEN_TECH = "logistic-science-pack"
GREY_TECH = "military-science-pack"
GRAY_TECH = GREY_TECH
BLUE_TECH = "chemical-science-pack"
PURPLE_TECH = "production-science-pack"
YELLOW_TECH = "utility-science-pack"
WHITE_TECH = "space-science-pack"
# for default values
TECH_PACK_DICT = {
    RED_TECH: 0,
    GREEN_TECH: 0,
    GREY_TECH: 0,
    BLUE_TECH: 0,
    PURPLE_TECH: 0,
    YELLOW_TECH: 0,
    WHITE_TECH:0 
}
class Tech:
    def __init__(self,d):
        self.raw = d
        self.name = d['name']
        self.ingredients = tuple(d['unit']['ingredients'])

        if 'count_formula' in d['unit']:
            count_formula = d['unit']['count_formula']

            #TODO: make this work in every case
            for i in range(1,len(count_formula)):
                if not count_formula[i] in string.digits:
                    if count_formula[i] == '(' and count_formula[i-1] in string.digits:
                        self.count_formula = count_formula[0:i] + '*' + count_formula[i:]
                    else:
                        self.count_formula = count_formula
                    break
            l = locals()
            l['L'] = int(self.name.split('-')[-1])
            # tsk tsk...
            exec("g = " + self.count_formula,l)
            self.count = l['g']
        else:
            self.count = d['unit']['count']
        
        if 'prerequisites' in d:
            self.prerequisites = d['prerequisites']
        else:
            self.prerequisites = None
        self.recipes_unlocked = None
        if 'effects' in d:
            self.recipes_unlocked = tuple(x['recipe'] for x in d['effects'] if x['type'] == 'unlock-recipe')
        
    def __eq__(self,other):
        return self.name == other
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __hash__(self):
        return hash(self.name)
    
    def getCost(self):
        return [ (x[0],x[1]*self.count) for x in self.ingredients ]
    
    def getAllPrerequisites(self):
        if not self.prerequisites:
            return set()
        r = set(n for n in self.prerequisites)
        for x in self.prerequisites:
            r.update(x.getAllPrerequisites())
        return r
    def getTotalCost(self):
        ret = dict()
        for i in self.getCost():
            ret[i[0]] = i[1]
        
        if self.prerequisites:
            for p in self.getAllPrerequisites():
                r = p.getCost()
                for ri in r:
                    try:
                        if ri[0] in ret:
                            ret[ri[0]] += ri[1]
                        else:
                            ret[ri[0]] = ri[1]
                    except TypeError as te:
                        print(te)
                        print(ret[ri[0]])
                        print(ri[1])
                        
        return_value = [ (x,ret[x]) for x in ret.keys() ]
        return return_value
            
def scanLua():
    print("Scanning data folder...")
    recipes = dict()
    technologies = dict()
    items = dict()
    lua_path = str(LUA_PATH)
    dirs = []
    with open(Path("lua/TEMPFILE"),"w") as f:
        for directory in [ x for x in DATA_LOCATION.iterdir() if x.is_dir() and x.name != 'core' ]:
            dirs.append(directory)
            print("Directory: " + str(directory) )
            #TODO: make these paths multiplatform
            lua_path += LUA_PATH + ';' + str(directory) + "\\?.lua;" + str(directory) + "\\?\\init.lua"
            #TODO: fix pathing here
            process_return = proc.run("lua\\lua lua\\scanner.lua \"" + str(directory) + "\" " + str(directory.name),capture_output=True, env = { "LUA_PATH": lua_path, "LUA_CPATH":  LUA_CPATH } )
            print(process_return.returncode)
            print(process_return.stdout.decode('utf-8'))
            print(process_return.stderr.decode('utf-8'))
    print("Scanning JSON files...")
    data = {}
    for d in dirs:
        with open(d.name + ".json") as data_json:
            data.update(json.load(data_json))

    #TODO: Implement Item class
    for i in data["item"].values():
        if 'science' in i["name"]:
            print(i)
        items[i["name"]] = i

    for i in data["tool"].values():
        if 'science' in i["name"]:
            print(i)
        items[i["name"]] = i
        
    for r in data["recipe"]:
        rc = Recipe(data["recipe"][r])
        recipes[rc] = rc
    
    for t in data["technology"]:
        tc = Tech(data["technology"][t])
        if tc.recipes_unlocked:
            for r in tc.recipes_unlocked:
                recipes[r].unlocked_by = tc
        technologies[tc] = tc

    for t in technologies.values():
        if t.prerequisites is not None:
            for p in range(len(t.prerequisites)):
                t.prerequisites[p] = technologies[t.prerequisites[p]]
            t.prerequisites = tuple(t.prerequisites)

    print("Items:",str(len(items)))
    print("Recipes:",str(len(recipes)))
    print("Technologies:", str(len(technologies)))

    return (items, recipes, technologies)


items, recipes, techs = scanLua()
def filter_techs(packs,techlist = techs,exclusive = True):
    if isinstance(packs,str):
        packs = set( (packs,) )
    elif isinstance(packs,list) or isinstance(packs,tuple):
        packs = set(packs)
    elif isinstance(packs,dict):
        packs = set(packs.values())
    elif isinstance(packs,set):
        pass
    else:
        return None
    plen = len(packs)
    ret = set()
    for t in techlist:
        if not exclusive or exclusive and len(t.ingredients) == plen:
            if len(set(x[0] for x in t.ingredients).intersection(packs)) == plen:
                ret.add(t)
    return ret
