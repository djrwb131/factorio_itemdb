import json
from luaparser import ast
from luaparser import astnodes
from pathlib import Path
#TODO:  This whole thing is stupid. Rewrite this in Lua, then serialize to json,
#       then import into Python. Simple.
INSTALL_LOCATION=Path("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Factorio")
DATA_LOCATION= INSTALL_LOCATION.joinpath("data")
RECIPE_LOCATION_SUFFIX = Path("prototypes\\recipe.lua")
RESEARCH_LOCATION_SUFFIX = Path("prototypes\\technology.lua")
DEFAULT_ENERGY_REQUIRED = 0.5
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
        self.count = d['unit']['count'] if 'count' in d['unit'] else d['unit']['count_formula']
        self.formulaic = 'count_formula' in d['unit']
        self.prerequisites = [x for x in d['prerequisites'].values()] if 'prerequisites' in d else None
        self.recipes_unlocked = None
        if 'effects' in d:
            self.recipes_unlocked = [x['recipe'] for x in d['effects'].values() if x['type'] == 'unlock-recipe']
        
    def __eq__(self,other):
        return self.name == other
    def __str__(self):
        return self.name
    
def to_python(recipe_field):
    if isinstance(recipe_field,astnodes.Field):
        field_value = recipe_field.value
    else:
        field_value = recipe_field
        
    py_val = None
    if      isinstance(field_value,astnodes.String):
        py_val = field_value.s
    elif    isinstance(field_value,astnodes.Number):
        py_val = field_value.n
    elif    isinstance(field_value,astnodes.MultOp):
        py_val = to_python(field_value.left) * to_python(field_value.right)
    elif    isinstance(field_value,astnodes.FalseExpr):
        py_val = False
    elif    isinstance(field_value,astnodes.TrueExpr):
        py_val = True
    elif    isinstance(field_value,astnodes.Table):
        py_val = dict()
        for x in field_value.fields:
            if 'id' in x.key.__dict__:
                key = x.key.id
            else:
                key = x.key.n
            py_val[key] = to_python(x)
    elif    isinstance(field_value,astnodes.Call):
        py_val = "NYI: " + str(field_value.func.value.id) + "." + str(field_value.func.idx.id)
    else:
        print("WARNING: Type %s NYI for key %s" % (field_value, recipe_field.key.id))
        print(recipe_field.to_json())
        print(field_value.to_json())
        input()
        py_val = field_value
    return py_val
def create_follower_upgrade(level, pack1, pack2, pack3, military_pack, high_tech_pack, production_pack, count, addition):
    ingredients = []
    if pack1 != 0:
        ingredients.append(('automation-science-pack', pack1),)
    if pack2 != 0:
        ingredients.append(('logistic-science-pack', pack2),)
    if pack3 != 0:
        ingredients.append(('chemical-science-pack', pack3),)
    if military_pack != 0:
        ingredients.append(('military-science-pack', military_pack),)
    if high_tech_pack != 0:
        ingredients.append(('utility-science-pack', high_tech_pack),)
    if production_pack != 0:
        ingredients.append(('production-science-pack', production_pack),)
    i_dict = dict()
    for i in range(len(ingredients)):
        i_dict[i+1] = ingredients[i]
    json_values = {
        'name': 'follower-robot-count-'+str(level),
        'prerequisites': ['defender'] if level == 1 else ['follower-robot-count-'+str(level-1)] if level != 5 else ['follower-robot-count-'+str(level-1), 'destroyer'],
        'unit': {
            'count': count,
            'time': 30,
            'ingredients': i_dict
def scanLua():
    print("Scanning data folder...")
    recipes = dict()
    technologies = dict()
    # technologies.lua uses a helper function... which we can't process easily. Maybe I should write this whole thing in lua?!?!
    # create_follower_upgrade is rewritten above...
    technologies['follower-robot-count-1'] = create_follower_upgrade(1, 1, 1, 0, 1, 0, 0, 200, 5)
    technologies['follower-robot-count-1'] = create_follower_upgrade(2, 1, 1, 0, 1, 0, 0, 300, 5)
    technologies['follower-robot-count-1'] = create_follower_upgrade(3, 1, 1, 1, 1, 0, 0, 400, 5)
    technologies['follower-robot-count-1'] = create_follower_upgrade(4, 1, 1, 1, 1, 0, 0, 600, 10)
    technologies['follower-robot-count-1'] = create_follower_upgrade(5, 1, 1, 1, 1, 1, 0, 800, 10)
    technologies['follower-robot-count-1'] = create_follower_upgrade(6, 1, 1, 1, 1, 1, 0, 1000, 10)
    items = dict()
    # couldn't find this in recipes.lua or technologies.lua
    items['space-science-pack'] = ['rocket-launch']
    for directory in [ x for x in DATA_LOCATION.iterdir() if x.is_dir() ]:
        print(directory)
        r = directory.joinpath(RECIPE_LOCATION_SUFFIX)
        if r.is_file():
            with open(r) as f:
                lua = ast.parse(f.read())
                for expr in lua.body.body:
                    if expr.source.id == 'data' and expr.func.id == 'extend':
                        print("Recipe data.extend function found. Checking data...")
                        for field in expr.args[0].fields:
                            field_is_recipe = False
                            for recipe_field in field.value.fields:
                                if recipe_field.key.id == 'type':
                                    field_is_recipe = (recipe_field.value.s == 'recipe')
                                    break
                            if field_is_recipe:
                                recipe = dict()
                                for recipe_field in field.value.fields:
                                    if 'id' in recipe_field.key.__dict__:
                                        key = recipe_field.key.id
                                    else:
                                        key = recipe_field.key.n
                                    recipe[key] = to_python(recipe_field)
                                r = Recipe(recipe)
                                recipes[r.name] = r
                                for i in r.results:
                                    if not i in items:
                                        items[i] = [ r ]
                                    else:
                                        items[i].append(r)
                                print("Added recipe [" + str(r) + "]")
        r = directory.joinpath(RESEARCH_LOCATION_SUFFIX)
        if r.is_file():
            with open(r) as f:
                lua = ast.parse(f.read())
                for expr in lua.body.body:
                    if not isinstance(expr,astnodes.Invoke):
                        continue
                    if expr.source.id == 'data' and expr.func.id == 'extend':
                        print("Tech data.extend function found. Checking data...")
                        for field in expr.args[0].fields:
                            field_is_tech = False
                            if not isinstance(field.value,astnodes.Table):
                                continue
                            for tech_field in field.value.fields:
                                if tech_field.key.id == 'type':
                                    field_is_tech = (tech_field.value.s == 'technology')
                                    break
                            if field_is_tech:
                                tech = dict()
                                for tech_field in field.value.fields:
                                    if 'id' in tech_field.key.__dict__:
                                        key = tech_field.key.id
                                    else:
                                        key = tech_field.key.n
                                    tech[key] = to_python(tech_field)
                                t = Tech(tech)
                                technologies[t.name] = t
                                
                                print("Added tech [" + str(t) + "]")
    # class linking
    print("Linking technologies...")
    errors = []
    for r in technologies.values():
        print(r)
        if r.prerequisites:
            for i in range(len(r.prerequisites)):
                try:
                    r.prerequisites[i] = technologies[r.prerequisites[i]]
                except KeyError:
                    errors.append((r,r.prerequisites[i]),)
        if r.recipes_unlocked:
            for i in range(len(r.recipes_unlocked)):
                r.recipes_unlocked[i] = recipes[r.recipes_unlocked[i]]
    print("Done!")
    return (items, recipes, technologies)
