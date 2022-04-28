import lualoader as ll

TECH_GOALS = ["gun-turret","heavy-armor","stack-inserter","physical-projectile-damage-2","weapon-shooting-speed-2","inserter-capacity-bonus-2","rocket-silo"]

def make_plan(goals,time_in_seconds):
    techlist = set( (ll.techs[x] for x in goals) )
    for x in goals:
        techlist.update(ll.techs[x].getAllPrerequisites())
    print(techlist)
    total_tech_cost = dict(ll.TECH_PACK_DICT)
    for t in techlist:
        for x in t.getCost():
            total_tech_cost[x[0]] += x[1]
    print(total_tech_cost)
    print(len(techlist)," has a total cost of:")
    for t,k in total_tech_cost.items():
        print(t,"\t" if len(t) >= 23 else "\t\t",k)
    print("Scanning prerequisites...")

    
    stage1 = ll.filter_techs(ll.RED_TECH,techlist)
    stage1_tech_cost = sum(s.count for s in stage1)
    print("STAGE1: Red tech cost:",stage1_tech_cost)

    stage2 = ll.filter_techs( (ll.RED_TECH,ll.GREEN_TECH),techlist)
    stage2_tech_cost = sum(s.count for s in stage2)
    print("STAGE2: Red/Green tech cost:",stage2_tech_cost)

    stage3 = ll.filter_techs( (ll.RED_TECH,ll.GREEN_TECH,ll.BLUE_TECH),techlist)
    stage3_tech_cost = sum(s.count for s in stage3)
    print("STAGE3: Red/Green/Blue tech cost:", stage3_tech_cost)
    
    stage4 = ll.filter_techs( (ll.RED_TECH,ll.GREEN_TECH,ll.BLUE_TECH,ll.PURPLE_TECH),techlist)
    stage4_tech_cost = sum(s.count for s in stage4)
    print("STAGE4: Red/Green/Blue/Purple tech cost:", stage4_tech_cost)

    stage5 = ll.filter_techs( (ll.RED_TECH,ll.GREEN_TECH,ll.BLUE_TECH,ll.YELLOW_TECH),techlist)
    stage5_tech_cost = sum(s.count for s in stage5)
    print("STAGE5: Red/Green/Blue/Yellow tech cost:", stage5_tech_cost)

    stage6 = ll.filter_techs( (ll.RED_TECH,ll.GREEN_TECH,ll.BLUE_TECH,ll.PURPLE_TECH,ll.YELLOW_TECH),techlist)
    stage6_tech_cost = sum(s.count for s in stage6)
    print("STAGE6: Red/Green/Blue/Purple/Yellow tech cost:", stage6_tech_cost)
    return techlist

make_plan(TECH_GOALS,8*60*60)
