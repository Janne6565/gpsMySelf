
function useABC(a, b, c, debug){
    const results = [];

    for (let neg in [1, -1]){
        
        let inSqrt = Math.pow(b,2)-4*a*c;
        if(inSqrt < 0){
            console.log("Cant use sqrt on numbers < 0");
        }
        let top = b * -1 + (neg*(Math.SQRT2(inSqrt)));
        let bot = 2*a;
        results.push(top/bot);

        return results;

    }
}

function calculateWithAxys0(c1, c2, debug){
    let xr = c1[0][0] - c2[0][0];
    let yr = c1[0][1] - c2[0][1];
    let r1 = c1[1];
    let r2 = c2[1];

    // Wenn eine Achse = 0 ist (sonst 0 Division)

    if(xr == 0 && yr != 0) {
        xy = [xr, yr];
    }else if(yr == 0 && xr != 0) {
        xy = [yr, xr];
    }else{
        circlesSameSpot(c1, c2, debug);
    }

    if(Math.SQRT2(Math.pow(xr,2) + Math.pow(yr,2) > r1 + r2)){
        console.log("Circles are too far apart");
    }

    let y = (Math.pow(r2,2)-Math.pow(r1,2)-xy[1]**2)/(2*xy[1]);

    const xVals= [];

    for(let val in [1, -1]){

        xVals.push(val * Math.SQRT2(Math.pow(r1,2)-Math.pow(y,2)));

    }

    if (yr == 0){
        return [(y, xVals[0]), (y, xVals[1])];
    }else{
        return [(xVals[0], y), (xVals[1], y)];
    }


}

function circlesSameSpot (c1, c2, debug) {
    if(c1 == c2){
        console.log("Circles are equal");
    }else{
        console.log("Circles are not touching");
    }
}

function calculateIntersections(c1, c2, debug) {
    let xr = c1[0][0] - c2[0][0]; // Relative Koordinaten, zur vereinfachung des Problems
    let yr = c1[0][1] - c2[0][1]; 
    let r1 = c1[1];
    let r2 = c2[1];

    if (xr == 0 && yr == 0){
        return circlesSameSpot(c1, c2, False);
    }
    if (Math.SQRT2(Math.pow(xr,2) + Math.pow(yr,2)) > r1 + r2){  // Punkte zu weit entfernt 
        console.log("Circles are too far apart");
    }
    if (xr == 0 || yr == 0){
        return calculateWithAxys0(c1, c2, debug);
    }

    const resultForX = []
    const resultForY = []
    for(xy in [(xr, yr, resultForX), (yr, xr, resultForY)]){
        let d = (Math.pow(rw,2)-Math.pow(r1,2))-Math.pow(xy[0],2)-Math.pow(xy[1],2);
        let a = 1 + (Math.pow(xy[0],2))/(Math.pow(xy[1],2));
        let b = -(d * xy[0])/((Math.pow(xy[1],2)));
        let c = ((Math.pow(d,2))/(4*(Math.pow(xy[1],2))-((Math.pow(r1,2)))));
        xy[2].push(useABC(a, b, c, debug));
    }

    resultForX = resultForX[0]; 
    resultForY = resultForY[0];
    const points = [];

    for (let i = 0; i < resultForX.length; i++) { 
        if (xr > 0 && yr > 0 || xr < 0 && yr < 0){
            points.push((resultForX[i], resultForY[resultForY.length - i - 1]));
        }else{
            points.push((resultForX[i], resultForY[i]));
        }
      }
  
    
    return points;
}


function testNewCalculation(c1, c2){
    let xr = c1[0][0] - c2[0][0];
    let yr = c1[0][1] - c2[0][1];
    let r1 = c1[1];
    let r2 = c2[1];

    if (xr == 0 && yr == 0){
        return circlesSameSpot(c1, c2, False);
    }
    if (Math.SQRT2(Math.pow(xr,2) + Math.pow(yr,2)) > r1 + r2){ // Punkte zu weit entfernt 
        console.log("Circles are too far apart");
    }

    let d = (Math.pow(r2,2) - Math.pow(r1,2) - Math.pow(xr,2) - Math.pow(yr,2)) / (2 * xr);
    let a = 1 + (Math.pow(yr,2)) / (Math.pow(xr,2));
    let b = -2 * (d * yr) / xr;
    let c = Math.pow(d,2) - Math.pow(r1,2);

    y = useABC(a, b, c, False);


    d = (Math.pow(r2,2) - Math.pow(r1,2) - Math.pow(xr,2) - Math.pow(yr,2)) / (2 * yr);
    a = 1 + (Math.pow(xr,2)) / (Math.pow(yr,2));
    b = -2 * (d * xr) / yr;
    c = Math.pow(d,2) - Math.pow(r1,2);

    x = useABC(a, b, c, False);

    return (x, y);
}

print(testNewCalculation(((0, 0), 1), ((0.87539, -1.48), 1)));