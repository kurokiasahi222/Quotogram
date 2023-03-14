function followProfile(user_id) {
    apiRequest(user_id, 'api/follow/user')
        .then(data => {
            console.log("Finished following");
        })
        .catch(error => {
            console.error(error);
        });
    Update_profile_Buttons();
}

function Update_profile_Buttons(){
    const FollowButton = document.querySelectorAll(".follow-button");
    FollowButton.forEach(Button => {
        const ButtonId = Button.getAttribute("data-user-id").split('|')[1];
        fetch("/api/is-following/" + ButtonId)
        .then(response => response.json())
                    .then(data => {
                        //console.log(data);
                        if(data["following"]) {
                            Button.innerHTML="Unfollow";
                            Button.style.backgroundColor = "#8b62a7";
                        }
                        else{
                            Button.innerHTML="Follow";
                            Button.style.backgroundColor = "#17b890";
                        }
                    })
    });
};

Update_profile_Buttons();
//console.log(FollowButton);
const FollowButton = document.querySelectorAll(".follow-button");
FollowButton.forEach(Button => {
    const ButtonId = Button.getAttribute("data-user-id");
    console.log(ButtonId);
    Button.setAttribute('onclick', "followProfile('" + ButtonId + "')");
});


