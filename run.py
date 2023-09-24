from main import ed
sol = []
for i in range(500):
    ans = ed()
    sol.append(ans)
sol.sort()
print("OPTIMAL_COST : ",sol[0][0])
print("NEST WITH OPTIMAL COST : ",sol[0][1])

