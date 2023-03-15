# Module 1 Group Assignment

CSCI 5117, Spring 2023, [assignment description](https://canvas.umn.edu/courses/355584/pages/project-1)

## App Info:

* Team Name: Upper Five
* App Name: Quotagram
* App Link: https://quotagram.onrender.com/

### Students

* Anwaar Hadi, hadi0013
* Jason Woitalla, woita006
* William Mleziva, mlezi006
* Aditi Patil, patil112
* Ash Kuroki, kurok011


## Key Features

**Describe the most challenging features you implemented
(one sentence per bullet, maximum 4 bullets):**

* One of the most challenging features that we implemented was the rendering of the quote board, which included positioning the quotes on the board as well as working with the visualization library for the quote board.

## Testing Notes

**Is there anything special we need to know in order to effectively test your app? (optional):**

* There are no special notes needed to test the website.


## Screenshots of Site
Desktop version homepage
![Desktop version homepage](/static/images/photos/homepage_web.png)

Mobile version homepage
![Mobile version homepage](/static/images/photos/homepage_mobile.png)

Quote Modal
![Quote modal](/static/images/photos/quote_modal.png)

Post Creation (adding quotes)
![Create post](/static/images/photos/create_post.png)

Profile page
![Profile page](/static/images/photos/profile_page.png)

Explore (Search) Page
![Explore page](/static/images/photos/explore_search.png)


## Mock-ups

![Paper mockups of the homepage](/static/images/photos/Page1.png)
**Figure 1:** This is the mockup of the homepage https://www.quotagram.com/. There are 2 similar but different views here. The top is unauthenticated version and the bottom is what the page looks like after login. Note that in the unauthenticated view all buttons that perform an action the only authenticated users can perform will be grayed out. 

![Homepage links](/static/images/photos/Page2.png)
**Figure 2:** These are the pages that are available to users from the homepage. The more info modal is available for both unauthenticated and authenticated users. It will probably blur the background or have a subtle color to obstruct the other content on the homepage to bring it into focus. The new post page is a pretty standard form requiring users to fill out the necessary parts for a post.

![Profile pages](/static/images/photos/Page3.png)
**Figure 3:** There are two options we have for the profile page which we dub "the quote board". The top one is the safer more standard approach. It just displays the users posts and any quotes they've saved to their quote board. It will either scroll infinitely or just display a finite number of quotes at a time allowing users to scroll pages. The second option is more fun and displays their board much like a real life board. This will probably interact with a drawing api / custom JavaScript so we will only implement this design if we have the time and resources.

![Explore Page](/static/images/photos/Page4.png)
This is our explore and search page. Very standard search bar at the top and also allows users to view quotes in different categories much how the Netflix homepage works.


## External Dependencies

* Micromodal.js [Website Link](https://micromodal.vercel.app/): A JavaScript library that is used to display modals on our page. This library makes modal setup very easy and handles all of the JavaScript heavy lifiting. It has no CSS or HTML so the modals are fully customizable by us.
* Panzoom [GitHub Link](https://github.com/anvaka/panzoom): A JavaScript library that allows to pan and zoom DOM elements. This is used for the profile page to allow users to pan and zoom around their profile page quote board.
* Font Awesome [Website Link](https://fontawesome.com/): An icon library that we pull from quite a bit to get nice high quality icons on our pages.

Stack overflow and various online articles were used throughout building this project. A lot of times the code in their solution was exactly the code needed for our uses. These particlar cases have been documented within the actual code itself and can be found in the source files. 