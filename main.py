from vectorCalc import * 

satelites1 = [[(7, 0), 5], [(17, 0), 5], [(12, -5), 5]]
satelites2 = [[(0, 3), 4], [(-3, 0), 2]]


def makeForSat(sat): 
    p1 = sat[0]
    r1 = sat[1]
    
    amountX = -2 * p1[0]
    amountY = -2 * p1[1]

    dispoX = p1[0] ** 2
    dispoY = p1[1] ** 2

    res = r1 ** 2

    kreisFormel = "x^2 + y^2 - " + str(amountX * -1) +"x - " + str(amountY * -1) + "y + " + str(dispoX) + " + " + str(dispoY) + " = " + str(res)

    return [(amountX, amountY), dispoX + dispoY, res]


def setInForm(sat): 
    restX = 0
    restX += -2 * sat[0][0]

    restY = 0
    restY += -2 * sat[0][1]

    behind = 0
    behind += sat[0][0] ** 2
    behind += sat[0][1] ** 2

    return [(restX, restY), behind]

def substractTwoForms(form1, form2): 
    return [(form1[0][0] - form2[0][0], form1[0][1] - form2[0][1]), form1[1] - form2[1]]

def getValueForY(sat1, sat2):
    pass

sateliteForms = [setInForm(satelites2[0]), setInForm(satelites2[1])]
results = [satelites2[0][1]**2, satelites2[1][1] ** 2]
print(results)
print(sateliteForms)
subed = substractTwoForms(sateliteForms[0], sateliteForms[1])
#getConnections(makeForSat(satelites1[0]), makeForSat(satelites1[1]))