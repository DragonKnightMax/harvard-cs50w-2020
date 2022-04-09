document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#profile-page').style.display = 'none';
    document.querySelector('#all-posts').style.display = 'block';
    document.querySelector('#new-post').style.display = 'block';
    document.querySelector('#edit-post').style.display = 'none';

    // for new post
    new_post_form();

    // by default show all posts
    filter_posts('all');

    document.querySelector('#username').addEventListener('click', (event) => {
        event.preventDefault();
        display_profile(0);
    });
});

/*
function check_error(response) {
    // response.ok (status code ranges from 200 to 299)
    if (!response.ok) {
        // throw an error to be catched
        // response.statusText example: 200 -> OK (statusText)
        throw Error(response.statusText); // will take you to the catch
    }
    return response.json();
}
*/

function new_post_form() {

    const new_post_section = document.querySelector('#new-post');
    new_post_section.innerHTML = '';

    const form = document.createElement('div');
    form.innerHTML = `
        <h3>New Post</h3>
        <form id="new-post-form">
            <textarea id="new-post-content"></textarea>
            <input id="new-post-submit" type="submit" value="Post">
        </form>
    `;
    
    // listen to the click on new post button
    form.querySelector('#new-post-form').addEventListener('submit', (event) => {
        
        event.preventDefault();

        // to handle POST request to server for adding new post
        new_post();

        // clear the post content in textarea
        form.querySelector('#new-post-content').value = '';
    });

    new_post_section.append(form);
}


// send POST request to server for adding new post
function new_post() {

    const content = document.querySelector('#new-post-content').value;

    // send POST request
    fetch("/posts/new", {
        method: 'POST',
        body: JSON.stringify({
            content: content,
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.message) {
    
            console.log("Message:", result.message);

            if (document.querySelector('#profile-page').style.display == 'none') {
                filter_posts('all');
            } else {
                user_posts(result.user_id);
            }

        } else if (result.error) {
            // log any error to console
            console.log("Error:", result.error);
        }
    });
}


// get all the posts from server
function filter_posts(category) {

    // empty the all posts section before append
    document.querySelector('#all-posts').innerHTML = '';

    if (category == 'all' || category == 'following') {

        fetch(`/posts/${category}`)
        .then(response => response.json())
        .then(posts => {
            //console.log(posts);
            posts.forEach(post => {
                display_post(post);
            })
        });
    }   

    category = category.charAt(0).toUpperCase() + category.slice(1, category.length);
    document.querySelector('h1').innerHTML = `${category} Posts`;
}


function user_posts(user_id) {
    // empty the all posts section before append
    document.querySelector('#all-posts').innerHTML = '';

    fetch(`/posts/${user_id}`)
    .then(response => response.json())
    .then(posts => {
        // debugging
        console.log(posts);

        posts.forEach(post => {
            display_post(post);
        })
    });
}


// display each post in its own block
function display_post(post) {

    // create a div tag to store post
    const post_div = document.createElement("div");

    // post details like username, content, likes
    post_div.innerHTML = `
        <div id="post-id-${post.id}">
            <div id="show-profile">${post.username}</div>
            <div><button id="edit-button">Edit</button></div>
            <div id="post-content">${post.content}</div>
            <div id="post-timestamp">${post.timestamp}</div>
            <div id="likes_count">${post.likes}</div>
            <button id="like-unlike-button"></button>
        </div>
    `;

    // display edit button for poster
    const edit_button = post_div.querySelector('#edit-button');
    if (post.editable) {
        edit_button.style.display = 'block';
    } else {
        edit_button.style.display = 'none';
    }

    // listen to user click on edit post
    edit_button.addEventListener('click', () => {
        edit_post_form(post.id, post.user_id);
    });

    // display like or unlike button for user to click
    const like_button = post_div.querySelector('#like-unlike-button');
    if (!post.already_liked) {
        like_button.innerHTML = 'Like';
    } else {
        like_button.innerHTML = 'Unlike';
    } 

    // listen to the user's click on like or unlike button
    like_button.addEventListener('click', () => {
        // call function to send POST request
        like_unlike_post(post.id);
    });

    // listen to user click on post username
    const show_profile = post_div.querySelector('#show-profile');
    show_profile.addEventListener('click', () => {
        display_profile(post.user_id);
    });

    // append the post to the all-posts section of index page
    document.querySelector('#all-posts').append(post_div);
}


function like_unlike_post(post_id) {

    fetch('/posts/like', {
        method: 'POST',
        body: JSON.stringify({
            post_id: post_id,
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.message) {
            // debugging
            console.log("Message:", result.message);

            // update post likes count asynchronously
            const post_div = document.querySelector(`#post-id-${post_id}`);
            post_div.querySelector('#likes_count').innerHTML = `${result.likes_count}`;

            // switch the like and unlike button after each click
            const like_button = post_div.querySelector('#like-unlike-button');
            if (like_button.innerHTML === 'Like') {
                like_button.innerHTML = 'Unlike';
            } else {
                like_button.innerHTML = 'Like';
            }

        } else if (result.error) {
            console.log("Error:", result.error);
        }
    });
}


// get user profile details
function display_profile(user_id) {

    document.querySelector('h1').innerHTML = 'Profile';

    const profile_page = document.querySelector('#profile-page');
    profile_page.style.display = 'block';
    profile_page.innerHTML = '';

    document.querySelector('#all-posts').innerHTML = '';

    new_post_form();

    fetch(`/profile/${user_id}`)
    .then(response => response.json())
    .then(result => {

        if(result.error) {
            console.log("Error:", result.error);
            return
        } 

        const profile_container = document.createElement('div');
        profile_container.innerHTML = `
            <div>${result.username}</div>
            <div>Followers: <span id="followers-count">${result.followers_num}</span></div>
            <div>Following: <span id="following-count">${result.following_num}</span></div>
            <div><button id="follow-unfollow-button"></button></div>
            <hr />
        `;

        // display all the user posts
        user_posts(result.user_id);

        // a user should not be able to follow themselves
        const follow_button = profile_container.querySelector('#follow-unfollow-button');
        if (result.is_valid_follow) {

            // for other user, do not display new post form
            document.querySelector('#new-post').style.display = 'none';

            follow_button.style.display = 'block';
            if (!result.is_already_follower) {
                follow_button.innerHTML = 'Follow';
            } else {
                follow_button.innerHTML = 'Unfollow';
            }

        } else {
            follow_button.style.display = 'none';
        }

        // listen to user click on follow or unfollow button
        follow_button.addEventListener('click', () => {
            follow_unfollow_user(user_id);
        });

        // append the user profile info to profile page section in index
        profile_page.append(profile_container);
    });
}


function follow_unfollow_user(user_id) {
    
    fetch('/profile/follow', {
        method: 'POST',
        body: JSON.stringify({
            user_id: user_id,
        })
    })
    .then(response => response.json())
    .then(result => {

        if (result.error) {
            console.log("Error:", result.error);
        } 

        if (result.message) {

            console.log("Message:", result.message);
        
            const follow_button = document.querySelector('#follow-unfollow-button');
            if (follow_button.innerHTML === 'Follow') {
                follow_button.innerHTML = 'Unfollow';
            } else {
                follow_button.innerHTML = 'Follow';
            }

            // update no. of followers and following asynchronously
            document.querySelector('#followers-count').innerHTML = result.followers_num;
            document.querySelector('#following-count').innerHTML = result.following_num;
        }
    });
}


function edit_post_form(post_id, user_id) {
    
    document.querySelector('#new-post').style.display = 'none';

    const edit_post_form_container = document.querySelector('#edit-post');
    edit_post_form_container.style.display = 'block';
    edit_post_form_container.innerHTML = '';

    // get the post container using post id
    const post_to_edit = document.querySelector(`#post-id-${post_id}`);
    
    // get the poster username and original post content to insert into edit post form textarea
    const username = post_to_edit.querySelector('#show-profile').innerHTML;
    const original_content = post_to_edit.querySelector('#post-content').innerHTML;

    // insert edit post form to edit post section in index page
    edit_post_form_container.innerHTML = `
        <form id="edit-post-form">
            <div>${username}</div>
            <textarea id="edit-post-content">${original_content}</textarea>
            <input type="submit" value="Save">
        </form>
    `;

    // listen to the submission (save) of edit post form
    edit_post_form_container.querySelector('#edit-post-form').addEventListener('submit', (event) => {
        event.preventDefault();
        save_edit_post(post_id, user_id);   
    });

    document.querySelector('#all-posts').style.display = 'none';
}


function save_edit_post(post_id, user_id) {

    // get the editted content from new post form textarea
    const new_content = document.querySelector('#edit-post-content').value;

    document.querySelector('#new-post').style.display = 'block';
    document.querySelector('#all-posts').style.display = 'block';
    document.querySelector('#edit-post').style.display = 'none';

    fetch('/posts/edit', {
        method: 'POST',
        body: JSON.stringify({
            "post_id": post_id,
            "content": new_content,
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.message) {

            console.log("Message:", result.message);

            // empty the textarea after user successfully edit the post
            new_content.value = '';

            if (document.querySelector('#profile-page').style.display == 'none') {
                filter_posts('all');
            } else {
                user_posts(user_id);
            }

        } else if (result.error) {
            console.log("Error:", result.error);
        }
    });
}