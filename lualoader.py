import json
from pathlib import Path
import subprocess as proc
import string
#TODO:  This whole thing is stupid. Rewrite this in Lua, then serialize to json,
#       then import into Python. Simple.
INSTALL_LOCATION=Path("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Factorio")
DATA_LOCATION= INSTALL_LOCATION.joinpath("data")
RECIPE_LOCATION_SUFFIX = Path("prototypes\\recipe.lua")
RESEARCH_LOCATION_SUFFIX = Path("prototypes\\technology.lua")
DEFAULT_ENERGY_REQUIRED = 0.5
LUA_PATH = '.\\lua\\?.lua;.\\lua\\?\\init.lua;' + str(DATA_LOCATION.joinpath('core')) + '\\?.lua;' + str(DATA_LOCATION.joinpath('core')) + '\\?\\init.lua'
LUA_CPATH = '.\\lua\\?.dll'
class Recipe:
    def __init__(self,d):
        self.name = d['name']
        #TODO: clean this up, should use temporary variables instead of indexing the dict param
        if 'normal' in d:
            d['ingredients'] = d['normal']['ingredients']
            if 'result' in d['normal']:
                d['result'] = d['normal']['result']
            else:
                d['results'] = d['normal']['results']
        self.ingredients = [
                (d['ingredients'][x]['name'], d['ingredients'][x]['amount'])
                    if 'type' in d['ingredients'][x]
                else (d['ingredients'][x][1],d['ingredients'][x][2])
                for x in d['ingredients']
            ]
        if 'energy_required' in d:
            self.time = d['energy_required']
        else:
            self.time = DEFAULT_ENERGY_REQUIRED
        if 'result' in d:
            if 'result_count' in d:
                rc = d['result_count']
            else:
                rc = 1
            self.results = [ (d['result'],rc) ]
        else:
            self.results = [
                (d['results'][r]['name'], d['results'][r]['amount'])
                    if 'type' in d['results'][r] else
                (d['results'][r]['name'], d['results'][r]['probability'])
                    if 'probability' in d['results'][r] else
                (d['results'][r][1],d['results'][r][2])
                for r in d['results'].keys()
            ]
            
    def __eq__(self,other):
        return self.name == other
    def __str__(self):
        return self.name


class Tech:
    def __init__(self,d):
        self.name = d['name']
        self.ingredients = [ (d['unit']['ingredients'][r][1], d['unit']['ingredients'][r][2]) for r in d['unit']['ingredients'] ]
        self.time = d['unit']['time']
        self.count = d['unit']['count'] if 'count' in d['unit'] else None
        self.formulaic = 'count_formula' in d['unit']
        if self.formulaic:
            count_formula = d['unit']['count_formula']
            print('[', count_formula,']')
            
            for i in range(len(count_formula)):
                if not count_formula[i] in string.digits:
                    if count_formula[i] == '(':
                        self.count_formula = count_formula[0:i] + '*' + count_formula[i:]
                    else:
                        self.count_formula = count_formula
                    break
            l = locals()
            l['L'] = int(self.name[-1])
            exec("g = " + self.count_formula,l)
            self.count = l['g']
        self.prerequisites = [x for x in d['prerequisites'].values()] if 'prerequisites' in d else None
        self.recipes_unlocked = None
        if 'effects' in d:
            self.recipes_unlocked = [x['recipe'] for x in d['effects'].values() if x['type'] == 'unlock-recipe']
        
    def __eq__(self,other):
        return self.name == other
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __hash__(self):
        return hash(self.name + str(self.ingredients))
    
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
            lua_path += LUA_PATH + ';' + str(directory) + "\\?.lua;" + str(directory) + "\\?\\init.lua"
            process_return = proc.run("lua\\lua lua\\scanner.lua \"" + str(directory) + "\" " + str(directory.name),capture_output=True, env = { "LUA_PATH": lua_path } )
            print(process_return.stdout.decode('utf-8'))
            print(process_return.stderr.decode('utf-8'))
    print("Scanning JSON files...")
    data = {}
    for d in dirs:
        with open(d.name + ".json") as data_json:
            data.update(json.load(data_json))
    print("Recipes:")
    print(data["recipe"].keys())
    print("Technologies:")
    print(data["technology"].keys())
    return (items, recipes, technologies)


items, recipes, techs = scanLua()
