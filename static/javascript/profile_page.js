// Pan Zoom for profile page
let quoteWrapper = document.querySelector('.profile-posts-wrapper');
panzoom(quoteWrapper, {
    maxZoom: 2,
    minZoom: 0.25,
})

// Setup force directed graph on the posts
let posts = document.querySelectorAll('.quote-wrapper');

// Create links between posts by date posted
let links = [];
for (let i = 0; i < posts.length; i++) {
    for (let j = i + 1; j < posts.length; j++) {
        let post1 = posts[i];
        let post2 = posts[j];
        let post1Date = new Date(post1.querySelector('.quote-footer-date-text').innerHTML.trim());
        let post2Date = new Date(post2.querySelector('.quote-footer-date-text').innerHTML.trim());
        let diff = Math.abs(post1Date - post2Date);
        if (diff < (1000 * 60 * 60 * 24)+1) { // 1 day difference
            links.push({source: post1, target: post2});
        }
    }
}

// repeal stronger in the x direction
const simulation = d3.forceSimulation(posts)
    .force("charge", d3.forceManyBody().strength(-100))
    .force("center", d3.forceCenter(200, 200))
    .force("collide", d3.forceCollide().radius(250))
    //.force("link", d3.forceLink().links(links).distance(100))

posts[0].fx = 200;
posts[0].fy = 200;

d3.selectAll(posts)
    .data(posts)
    .style("left", function(d) { return d.x + "px"; })
    .style("top", function(d) { return d.y + "px"; });

simulation.on("tick", function() {
    d3.selectAll(posts)
        .style("left", function(d) { return d.x + "px"; })
        .style("top", function(d) { return d.y + "px"; });
});
