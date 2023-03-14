// Pan Zoom for profile page
var quoteWrapper = document.querySelector('.profile-posts-wrapper');
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

// L System Fractal Tree to calculate the position of the quotes
let posts = document.querySelectorAll('.quote-wrapper');
let axiom = "F";
let rules = [
    {a: "F", b: "FF+[+F-F-F]-[-F+F+F]"},
]
let angle = 28;
let iterations = 3;
let len = 700;

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

    let pos = {x: -len, y: 0};
    let stack = [];
    let positions = [];
    let curAngle = 0;

    for (let i = 0; i < sentence.length; i++) {
        let current = sentence.charAt(i);
        if (current == "F" || current == "X") {
            let newPos = {
                x: pos.x + (len * Math.cos(curAngle * Math.PI / 180)),
                y: pos.y + (len * Math.sin(curAngle * Math.PI / 180))
            };
            positions.push(newPos);
            if(positions.length == posts.length) {
                break;
            }
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
            curAngle = state.angle;
        }
    }
    return positions;
}

let center = {x: 30, y: 700};
let positions = calculatePositions();
for(let i = 0; i < posts.length; i++) {
    posts[i].style.transform = "translate(" + (positions[i].x + center.x) + "px, " + (positions[i].y + center.y) + "px)";
}

var isDragging = false;
document.addEventListener("mousedown", function(event) {
    var draggable = event.target.closest(".quote-pin-handle");

    if (draggable) {
        const circle = draggable.querySelector(".quote-pin-handle-circle");
        const pin = draggable.querySelector(".quote-pin-handle-thumbtack");

        if(!isDragging) {
            isDragging = true;
            instance.pause();

            let post = draggable.closest(".quote-wrapper");
            let wrapperPos = quoteWrapper.getBoundingClientRect();
            let postPos = post.getBoundingClientRect();

            circle.style.display = "none";
            pin.style.display = "block";

            let mousePos = {
                x: event.clientX - postPos.left + wrapperPos.left - instance.getTransform().x, 
                y: event.clientY - postPos.top + wrapperPos.top - instance.getTransform().y
            };
            post.style.zIndex = 1000;
            draggable.style.filter = "drop-shadow(0.25em 0.25em 0.5em rgba(0, 0, 0, 0.75))";
            
            let drag = function(event) {
                let translatedX = (event.clientX - mousePos.x - instance.getTransform().x) / instance.getTransform().scale;
                let translatedY = (event.clientY - mousePos.y - instance.getTransform().y) / instance.getTransform().scale;
                post.style.transform = "translate(" + translatedX + "px, " + translatedY + "px)";
            }

            let drop = function(event) {
                isDragging = false;
                instance.resume();
                post.style.zIndex = 0;
                draggable.style.filter = "none";
                circle.style.display = "block";
                pin.style.display = "none";
                document.removeEventListener("mousemove", drag);
                document.removeEventListener("mouseup", drop);
            }

            document.addEventListener("mousemove", drag);
            document.addEventListener("mouseup", drop);
        }
    }
});
