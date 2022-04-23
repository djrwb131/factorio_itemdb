print("LUA!")
require("json")
print("json.lua loaded!")
require("lualib.dataloader")

print("factorio dataloader loaded!")
util = require("lualib.util")
print("util.lua loaded!")
dofile(arg[1].."\\prototypes\\recipe.lua")
print("recipe.lua loaded!")
dofile(arg[1].."\\prototypes\\technology.lua")
print("technology.lua loaded!")
print("Checking data table...")
for key, value in pairs(data) do
    if type(value) == "function" then
        print(key .. " was a function")
        data.key = key
    end
end
print("functions stripped from data table!")
datafile = io.open(arg[2] .. ".json","w")
datafile:write(json.encode(data.raw))
print("json written!")
print("!AUL")
