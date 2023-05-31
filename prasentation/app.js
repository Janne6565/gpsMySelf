class Point {
  constructor(x, y, canvas) {
    if (canvas === undefined) {
      this.x = x;
      this.y = y;
    } else {
      this.x = canvas.width * (x / 100);
      this.y = canvas.height * (y / 100);
    }
  }

  toString() {
    return "(" + this.x.toFixed(0) + ", " + this.y.toFixed(0) + ")";
  }

  plus(x, y) {
    return new Point(this.x + x, this.y + y);
  }
}

function useABC(a, b, c) {
  const results = [];

  for (let i in [1, -1]) {
    let neg = [1, -1][i];
    let inSqrt = b * b - 4 * a * c;
    if (inSqrt < 0) {
      throw new Error("Can't use sqrt on numbers < 0");
    }
    let top = b * -1 + neg * Math.sqrt(inSqrt);
    let bot = 2 * a;
    results.push(top / bot);
  }

  return results;
}

function getCircleIntersections(midOne, midTwo, radiusOne, radiusTwo) {
  let xr = midOne.x - midTwo.x;
  let yr = midOne.y - midTwo.y;
  let r1 = radiusOne;
  let r2 = radiusTwo;

  if (Math.sqrt(xr ** 2 + yr ** 2) > r1 + r2) {
    raise("Circles are too far apart");
  }

  d = (r2 ** 2 - r1 ** 2 - xr ** 2 - yr ** 2) / (2 * xr);
  a = 1 + yr ** 2 / xr ** 2;
  b = (-2 * (d * yr)) / xr;
  c = d ** 2 - r1 ** 2;

  y = useABC(a, b, c);

  d = (r2 ** 2 - r1 ** 2 - xr ** 2 - yr ** 2) / (2 * yr);
  a = 1 + xr ** 2 / yr ** 2;
  b = (-2 * (d * xr)) / yr;
  c = d ** 2 - r1 ** 2;

  x = useABC(a, b, c);

  realX = [];
  for (let i in x) {
    let before = x[i];
    realX.push(before + midOne.x);
  }

  realY = [];
  for (let i in y) {
    let before = y[i];
    realY.push(before + midOne.y);
  }

  let points = [];
  for (let i = 0; i < realX.length; i++) {
    points.push(new Point(realX[i], realY[i]));
  }
  return points;
}

let checkBoxIntersections = document.getElementById("showIntersections");

function showIntersections() {
  return checkBoxIntersections.checked;
}

let distances = {
  0: 0,
  1: 0,
  2: 0,
};

let positions = {
  0: new Point(0, 0),
  1: new Point(0, 0),
  2: new Point(0, 0),
};

let bestIntersection = undefined;

class Drawer {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext("2d");
    this.width = this.canvas.width;
    this.height = this.canvas.height;
  }

  drawBall(center, radius, color) {
    this.ctx.fillStyle = color;

    this.ctx.beginPath();
    this.ctx.arc(center.x, center.y, radius, 0, 2 * Math.PI);
    this.ctx.closePath();
    this.ctx.fill();
  }

  drawRect(point1, point2, color) {
    this.ctx.fillStyle = color;
    this.ctx.fillRect(
      point1.x,
      point1.y,
      point2.x - point1.x,
      point2.y - point1.y
    );
  }

  drawLine(point1, point2, color, thickness) {
    this.ctx.lineWidth = thickness;
    this.ctx.strokeStyle = color;
    this.ctx.beginPath();
    this.ctx.moveTo(point1.x, point1.y);
    this.ctx.lineTo(point2.x, point2.y);
    this.ctx.stroke();
  }

  drawCircle(center, radius, color, thickness) {
    this.ctx.strokeStyle = color;
    this.ctx.lineWidth = thickness;
    this.ctx.beginPath();
    this.ctx.arc(center.x, center.y, radius, 0, 2 * Math.PI);
    this.ctx.stroke();
  }

  drawString(position, text, color, size) {
    this.ctx.font = size + "px Arial";
    this.ctx.fillStyle = color;
    this.ctx.fillText(text, position.x, position.y);
  }

  clear() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
  }
}

class Satelite {
  constructor(position, color) {
    this.position = position;
    this.color = color;
  }
}

class Display {
  radius = 15;
  instant = false;

  constructor(simulationCanvasId, controlCanvasId) {
    this.controlDrawer = new Drawer(controlCanvasId);

    this.simulationDrawer = new Drawer(simulationCanvasId);
    this.satelites = [
      new Satelite(new Point(50, 15, this.simulationDrawer), "red"),
      new Satelite(new Point(33, 73, this.simulationDrawer), "blue"),
      new Satelite(new Point(70, 60, this.simulationDrawer), "green"),
    ];
    this.receiver = new Point(50, 50, this.simulationDrawer);
    this.velocity = 343;

    this.setMaxTime();
    this.time = 0;
    this.update();
  }

  setVelocity(velocity) {
    this.velocity = velocity;
    this.update();
  }

  setMaxTime() {
    let maxTime = 0;
    for (let sat in this.satelites) {
      let satelite = this.satelites[sat];
      let distance = this.distance(satelite.position, this.receiver);
      let time = distance / this.velocity;
      if (time > maxTime) {
        maxTime = time;
      }
    }
    this.maxTime = maxTime;
  }

  draw() {
    this.simulationDrawer.clear();

    let radius = this.velocity * this.time;

    for (let sat in this.satelites) {
      let satelite = this.satelites[sat];
      this.simulationDrawer.drawBall(
        satelite.position,
        this.radius,
        satelite.color
      );

      let myDistance = this.distance(satelite.position, this.receiver);
      if (myDistance > radius) {
        myDistance = radius;
      }
      this.simulationDrawer.drawCircle(
        satelite.position,
        myDistance,
        satelite.color,
        2
      );

      this.simulationDrawer.drawString(
        satelite.position.plus(15, 15),
        satelite.position.toString(),
        satelite.color,
        20
      );
    }

    this.simulationDrawer.drawString(
      this.receiver.plus(15, 15),
      this.receiver.toString(),
      "black",
      20
    );

    this.simulationDrawer.drawBall(this.receiver, this.radius, "black");

    this.controlDrawer.clear();
    let percentage = this.time / this.maxTime;

    this.controlDrawer.drawLine(
      new Point(percentage * 100, 0, this.controlDrawer),
      new Point(percentage * 100, 100, this.controlDrawer),
      "grey",
      4
    );

    for (let sat in this.satelites) {
      let satelite = this.satelites[sat];
      let distance = this.distance(satelite.position, this.receiver);
      let time = distance / this.velocity;
      let percentage = time / this.maxTime;
      this.controlDrawer.drawLine(
        new Point(percentage * 100, 100, this.controlDrawer),
        new Point(percentage * 100, 0, this.controlDrawer),
        satelite.color,
        6
      );

      this.controlDrawer.drawString(
        new Point((percentage - 0.04) * 100, 59, this.controlDrawer),
        (distance / this.velocity).toFixed(2) + "s",
        satelite.color,
        20
      );
    }
  }

  setSatelitePosition(index, x, y) {
    this.satelites[index].position = new Point(x, y, this.simulationDrawer);
    this.update();
  }

  setReceiverPosition(x, y) {
    this.receiver = new Point(x, y, this.simulationDrawer);
    this.update();
  }

  distance(point1, point2) {
    return Math.sqrt(
      Math.pow(point1.x - point2.x, 2) + Math.pow(point1.y - point2.y, 2)
    );
  }

  setDistances() {
    for (let sat in this.satelites) {
      let satelite = this.satelites[sat];
      let distance = this.distance(satelite.position, this.receiver);
      distances[sat] = distance;
      positions[sat] = satelite.position;
    }
  }

  printInformations() {
    let positionsDiv = document.getElementById("positions");
    let distancesDiv = document.getElementById("distances");

    positionsDiv.innerHTML = "";
    distancesDiv.innerHTML = "";

    for (let sat in this.satelites) {
      let satelite = this.satelites[sat];
      positionsDiv.innerHTML +=
        "Satelite " + sat + " : " + satelite.position.toString() + "<br>";
      distancesDiv.innerHTML +=
        "Satelite " + sat + ": " + (distances[sat] / this.velocity).toFixed(2) + "s &middot; " + this.velocity + " m/s &rArr; " + distances[sat].toFixed(2) + "m<br>";
    }

    let xr = positions[1].x - positions[0].x;
    let yr = positions[1].y - positions[0].y;

    let r1 = distances[1];
    let r2 = distances[0];

    let yd = (r2 ** 2 - r1 ** 2 - xr ** 2 - yr ** 2) / (2 * xr);

    let ya = 1 + yr ** 2 / xr ** 2;

    let yb = (-2 * (yd * yr)) / xr;

    let yc = yd ** 2 - r1 ** 2;

    let resY = useABC(ya, yb, yc);

    let resultsY = [];
    for (let i in resY) {
      resultsY.push((resY[i] + positions[1].y).toFixed(0));
    }

    let xd = (r2 ** 2 - r1 ** 2 - xr ** 2 - yr ** 2) / (2 * yr);
    let xa = 1 + xr ** 2 / yr ** 2;
    let xb = (-2 * (xd * xr)) / yr;
    let xc = xd ** 2 - r1 ** 2;

    let resX = useABC(xa, xb, xc);

    let resultsX = [];

    for (let i in resX) {
      resultsX.push((resX[i] + positions[1].x).toFixed(0));
    }

    let string =
      `
      \\[ \\begin{gather} \\boxed{ x_{1, 2} = \\frac{-( ` +
      xb.toFixed(2) +
      `) \\pm \\sqrt{(` +
      xb.toFixed(2) +
      `) ^2 - 4 \\cdot (` +
      xa.toFixed(2) +
      `) \\cdot (` +
      xc.toFixed(2) +
      `)}} {2 \\cdot ` +
      xa.toFixed(2) +
      `} = [`;

    let index = 0;
    for (let i in resultsX) {
      if (index !== 0) {
        string += ", ";
      }
      string += resX[i].toFixed(2);
      index++;
    }

    string += `] } \\\\ \\\\`;
      
    string += `x_{real} = [x_1 + x_{sat}, x_2 + x_{sat}] = [`;

    index = 0;
    for (let i in resultsX) {
      if (index !== 0) {
        string += ", ";
      }
      string +=
        String(resX[i].toFixed(2)) + " + " + String(positions[1].x.toFixed(2));
      index++;
    }

    string += `] = [`;

    index = 0;
    for (let i in resultsX) {
      if (index !== 0) {
        string += ", ";
      }
      string += String((resX[i] + positions[1].x).toFixed(2));
      index++;
    }

    string +=
      `]\\\\ \\\\ \\\\ \\boxed{ y_{1, 2} = \\frac{-(` +
      yb.toFixed(2) +
      `) \\pm \\sqrt{ (` +
      yb.toFixed(2) +
      `)^2 - 4 \\cdot (` +
      ya.toFixed(2) +
      `) \\cdot (` +
      yc.toFixed(2) +
      `)}} {2 \\cdot ` +
      ya.toFixed(2) +
      `} = [`;

    index = 0;
    for (let i in resY) {
      if (index !== 0) {
        string += ", ";
      }
      string += resY[i].toFixed(2);
      index++;
    }
    string += `] } \\\\ \\\\`;

     
    string += `y_{real} = [y_1 + y_{sat}, y_2 + y_{sat}] = [`;

    index = 0;
    for (let i in resultsY) {
      if (index !== 0) {
        string += ", ";
      }
      string +=
        String(resY[i].toFixed(2)) + " + " + String(positions[1].y.toFixed(2));
      index++;
    }

    string += `] = [`;

    index = 0;
    for (let i in resultsY) {
      if (index !== 0) {
        string += ", ";
      }
      string += String((resY[i] + positions[1].y).toFixed(2));
      index++;
    }

    string += `]\\\\ \\\\`;
    

    string +=
      `p_{1, 2} = [(` +
      resultsX[0] +
      ", " +
      resultsY[0] +
      `), (` +
      resultsX[1] +
      ", " +
      resultsY[1] +
      `)]`;

    string += `\\end{gather} \\]`;

    document.getElementById("calcFiller").innerHTML = string;

    document.getElementById("radiusWanted").innerHTML = distances[2].toFixed(2) + "m";
  }

  update() {
    this.setMaxTime();
    if (this.instant) {
      this.time = this.maxTime;
    }
    this.draw();
    this.setDistances();
    this.markIntersections();
    this.printInformations();
  }

  markIntersections() {
    let intersectionDiv = document.getElementById("intersections");
    intersectionDiv.innerHTML = "";

    let intersections = getCircleIntersections(
      this.satelites[1].position,
      this.satelites[0].position,
      distances[1],
      distances[0]
    );

    let minDistance = -1;
    let index = 0;

    for (let intersection of intersections) {
      if (showIntersections()) {
        this.simulationDrawer.drawBall(intersection, 5, "black");
      }

      let distance = this.distance(intersection, this.satelites[2].position);

      let offset = Math.abs(distance - distances[2]);

      intersectionDiv.innerHTML +=
        ' <span class="fragment" data-fragment-index="' +
        (index + 1) +
        '">' + intersection.toString() + '&rArr; Abstand: ' +
        distance.toFixed(2) +
        'm</span> <span class="fragment" data-fragment-index="' +
        (index + intersections.length + 1) +
        '">&rArr; ' +
        offset +
        "m</span><br>";

      if (minDistance === -1 || offset < minDistance) {
        minDistance = offset;
        bestIntersection = intersection;
      }
      index++;
    }

    document.getElementById("betterIntersection").innerHTML =
      bestIntersection.toString();
    if (showIntersections()) {
      this.simulationDrawer.drawBall(bestIntersection, 5, "red");
    }
  }

  addTime(timeDelta) {
    if (this.time + timeDelta > this.maxTime) {
      this.time = this.maxTime;
    } else {
      this.time += timeDelta;
    }
    this.update();
  }

  setTime(time) {
    if (time < 0) {
      time = 0;
    } else {
      if (time > this.maxTime) {
        time = this.maxTime;
      } else {
        this.time = time;
      }
    }
    this.update();
  }
}

class Manager {
  isPlaying = false;

  constructor(displayId, controlerId, display) {
    this.displayObject = document.getElementById(displayId);
    this.controler = document.getElementById(controlerId);

    this.controler.addEventListener("mousedown", (e) => {
      this.handleControlerEvent(e);
    });

    this.controler.addEventListener("mousemove", (e) => {
      if (e.buttons === 1) {
        this.handleControlerEvent(e);
      }
    });

    this.displayObject.addEventListener("mousedown", (e) => {
      this.handleDisplayEvent(e);
    });

    this.displayObject.addEventListener("mousemove", (e) => {
      if (e.buttons === 1) {
        this.handleDisplayEvent(e);
      }
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        if (this.display.time === this.display.maxTime) {
          this.display.time = 0;
        } else {
          this.isPlaying = !this.isPlaying;
        }
      }
    });

    setInterval(() => {
      this.tick(0.01);
    }, 10);

    this.display = display;
    this.display.update();
  }

  handleDisplayEvent(event) {
    let rect = this.displayObject.getBoundingClientRect();
    let x = event.clientX - rect.left;
    let y = event.clientY - rect.top;

    let percentageX = x / rect.width;
    let percentageY = y / rect.height;

    this.display.setReceiverPosition(percentageX * 100, percentageY * 100);
  }

  handleControlerEvent(event) {
    this.isPlaying = false;

    let rect = this.controler.getBoundingClientRect();
    let x = event.clientX - rect.left;

    let percentage = x / rect.width;

    let time = this.display.maxTime * percentage;
    this.display.setTime(time);
  }

  tick(timeDelta) {
    if (this.isPlaying) {
      this.display.addTime(timeDelta);
    }
  }
}

let display = new Display("simulationCanvas", "controlsCanvas");
let manager = new Manager("simulationCanvas", "controlsCanvas", display);

let inputVelocity = document.getElementById("velocity");

display.setVelocity(inputVelocity.value);
display.update();

checkBoxIntersections.addEventListener("change", () => {
  display.update();
});

let checkboxInstant = document.getElementById("instantCalculations");

checkboxInstant.addEventListener("change", () => {
  display.instant = checkboxInstant.checked;
  display.update();
});

inputVelocity.addEventListener("input", (e) => {
  let newValue = "";

  for (let letter of inputVelocity.value) {
    if ((!isNaN(letter) && letter !== " ") || letter === ".") {
      console.log(letter);
      newValue += String(letter);
    }
  }

  display.setVelocity(newValue);

  inputVelocity.value = newValue + " m/s";

  if (isNaN(inputVelocity.value)) {
    return;
  }
  display.update();
});

inputVelocity.value = display.velocity + " m/s";