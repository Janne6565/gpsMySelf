

// koordinaten und distanzen
// getIntersection([0, 0], [3, 0], [0, 4], 2.5, 3.6, 4.2)
// p1 = [0, 0];
// p2 = [3, 0];
// p3 = [0, 4];
// d1 = 2.5;
// d2 = 3.6;
// d3 = 4.2;
function getIntersection(p1, p2, p3, d1, d2, d3, debug = false) {
    // distanz ausrechnen
    const r1Sq = d1 * d1; //6.25
    const r2Sq = d2 * d2; //12.96
    const r3Sq = d3 * d3; //17.64
    if (debug) console.log(r1Sq, r2Sq, r3Sq);

    // differenz zwischen zwei punkten
    const p2p1 = [p2[0] - p1[0], p2[1] - p1[1]]; // [3-0, 0-0] = [3, 0]
    const p3p1 = [p3[0] - p1[0], p3[1] - p1[1]]; // [0-0, 4-0] = [0, 4]
    if (debug) console.log(p2p1, p3p1);

    // punkt produkt (dot product fuck)
    const p2p1Sq = p2p1[0] * p2p1[0] + p2p1[1] * p2p1[1]; // [9+0]
    const p3p1Sq = p3p1[0] * p3p1[0] + p3p1[1] * p3p1[1]; // [0+16]
    if (debug) console.log(p2p1Sq, p3p1Sq)

    // koeffizienten und so lol
    const A = (r1Sq - r2Sq + p2p1Sq) / 2; // (6.25 - 12.96 + 9) / 2 = 1.145
    const B = (r1Sq - r3Sq + p3p1Sq) / 2; // (6.25 - 17.64 + 16) / 2 = 2.305
    if (debug) console.log(A, B)

    // x und y ausrechnen (pythagoras)
    const x = (A * p3p1[1] - B * p2p1[1]) / (p2p1[0] * p3p1[1] - p3p1[0] * p2p1[1]); // (1.145 * 4 - 2.305 * 0) / (3 * 4 - 0 *)
    const y = (A * p3p1[0] - B * p2p1[0]) / (p2p1[1] * p3p1[0] - p3p1[1] * p2p1[0]); // (1.145 * 0 - 2.305 * 3) / (3 * 0 - 4 *)
    if (debug) console.log(x, y)

    return { x, y };
}




new Vue({
    el: '#firstPage',
    data() {
        return {
            title: "Ortungsysteme auf einer Flachen Ebene"
        }
    },
    methods: {
        
    },
    created() { 
        
    }
})

new Vue({
    el: "#secondPage", 
    data() {
        return {
            position: getIntersection([0, 0], [3, 0], [0, 4], 2.5, 3.6, 4.2),
        }
    },
    methods: {

    },
    created() {

    }
})
