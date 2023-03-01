// Pan Zoom for profile page
let quoteWrapper = document.querySelector('.profile-posts-wrapper');
var instance = panzoom(quoteWrapper, {
    maxZoom: 2,
    minZoom: 0.25,
    initialX: 700,
    initialY: 700,
    initialZoom: 1,
    bounds: true,
    boundsPadding: 0.5,
});

instance.zoomAbs(700, 700, 1);

document.addEventListener('keydown', function(event) {
    if (event.key === 't') {
        if(instance.isPaused()) {
            instance.resume();
        } else {
            instance.pause();
        }
    }
});

// Setup force directed graph on the posts
let posts = document.querySelectorAll('.quote-wrapper');

// // Create links between posts by date posted
// let links = [];
// for (let i = 0; i < posts.length; i++) {
//     for (let j = i + 1; j < posts.length; j++) {
//         let post1 = posts[i];
//         let post2 = posts[j];
//         let post1Date = new Date(post1.querySelector('.quote-footer-date-text').innerHTML.trim());
//         let post2Date = new Date(post2.querySelector('.quote-footer-date-text').innerHTML.trim());
//         let diff = Math.abs(post1Date - post2Date);
//         if (diff < (1000 * 60 * 60 * 24)+1) { // 1 day difference
//             links.push({source: post1, target: post2});
//         }
//     }
// }

// center = {x: 1500, y: 1000};

// // repeal stronger in the x direction
// const simulation = d3.forceSimulation(posts)
//     .force("charge", d3.forceManyBody().strength(-100))
//     .force("center", d3.forceCenter(center.x, center.y))
//     .force("collide", d3.forceCollide().radius(250))
//     //.force("link", d3.forceLink().links(links).distance(100))

// posts[0].fx = center.x;
// posts[0].fy = center.y;

// d3.selectAll(posts)
//     .data(posts)
//     .style("left", function(d) { return d.x + "px"; })
//     .style("top", function(d) { return d.y + "px"; })
//     .call(d3.drag()
//         .on("start", dragStarted)
//         .on("drag", dragged)
//         .on("end", dragEnded));

// function dragStarted(d) {
//     if (!d3.event.active) simulation.alphaTarget(0.3).restart();
//     d.fx = d.x;
//     d.fy = d.y;
// }

// function dragged(d) {
//     d.fx = d3.event.x;
//     d.fy = d3.event.y;
// }

// function dragEnded(d) {
//     if (!d3.event.active) simulation.alphaTarget(0);
//     d.fx = null;
//     d.fy = null;
// }

// simulation.on("tick", function() {
//     d3.selectAll(posts)
//         .style("left", function(d) { return d.x + "px"; })
//         .style("top", function(d) { return d.y + "px"; });
// });

// L System Fractal Tree to calculate the position of the quotes
let axiom = "F";
let rules = [
    {a: "F", b: "F[+FF][-FF]F[-F][+F]F"},
]
let angle = 36;
let iterations = 3;
let len = 500;
let offset = {x: 250, y: 50};

function generateTree(sentence) {
    let nextSentence = "";
    for (let i = 0; i < sentence.length; i++) {
        let current = sentence.charAt(i);
        let found = false;
        for (let j = 0; j < rules.length; j++) {
            if (current == rules[j].a) {
                found = true;
                nextSentence += rules[j].b;
                break;
            }
        }
        if (!found) {
            nextSentence += current;
        }
    }
    sentence = nextSentence;
    return sentence;
}

function calculatePositions() {
    let sentence = axiom;
    for (let i = 0; i < iterations; i++) {
        sentence = generateTree(sentence);
    }
    console.log(sentence);

    let pos = {x: 0, y: 0};
    let stack = [];
    let positions = [];
    let curAngle = 90;
    positions.push(pos);

    for (let i = 0; i < sentence.length; i++) {
        let current = sentence.charAt(i);
        if (current == "F" || current == "X") {
            let newPos = {
                x: pos.x + len * Math.cos(curAngle * Math.PI / 180) + offset.x,
                y: pos.y + len * Math.sin(curAngle * Math.PI / 180) + offset.y
            };
            positions.push(newPos);
            pos = newPos;
        } else if (current == "+") {
            curAngle += angle;
        } else if (current == "-") {
            curAngle -= angle;
        } else if (current == "[") {
            stack.push({pos: pos, angle: curAngle});
        } else if (current == "]") {
            let state = stack.pop();
            pos = state.pos;
            angle = state.angle;
        }
    }
    return positions;
}

let center = {x: 1500, y: 50};
let positions = calculatePositions();
for(let i = 0; i < posts.length; i++) {
    posts[i].style.left = positions[i].x + center.x + "px";
    posts[i].style.top = positions[i].y + center.y + "px";
}
