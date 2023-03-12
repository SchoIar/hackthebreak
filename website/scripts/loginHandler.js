const UserIP = "/userdata"
const xpID = "/increaseXP"
var userData;

//attempts to query the server using the current cookies to update the user data
updateUserData();

function storeCookies(username, password){
    //writes the username and password cookies to the document
    document.cookie = `username=${username}; path=/`;
    document.cookie = `password=${password}; path=/`;
}

function getUsername(){
    //reads all teh cookies (adds a ; at the end for consistency (last cookie is the only one that doesn't end with ;))
    let allCookies = document.cookie.concat(";");

    var username = "";

    //defiens a regex filter to find the username
    let searchfilter = /username=(\S*);/g;

    //executes the filter on the cookies
    SearchResult = searchfilter.exec(allCookies);

    //checks if a result was found
    if(SearchResult != null){
        //if so, stores the users username
        username = SearchResult[1];
    }

    //returns the username
    return username;
}

function getPassword(){
    //reads all teh cookies (adds a ; at the end for consistency (last cookie is the only one that doesn't end with ;))
    let allCookies = document.cookie.concat(";");

    var password = ""

    //defiens a regex filter to find the username
    let searchfilter = /password=(.*);/g;

    //executes the filter on the cookies
    SearchResult = searchfilter.exec(allCookies);

    //checks if a result was found
    if(SearchResult != null){
        //if so, stores the users username
        password = SearchResult[1];
    }

    //returns the username
    return password;
}

function updateUserData(){
    //gets the username fromt eh cookies
    var username = getUsername();

    //checks if there was a username stored in the cookies
    if(username == ""){
        console.log("no user data found");
    }else{
        //gets the password from the cookies
        var password = getPassword();

        if(password == ""){
            console.assert.log("no password found")
        }else{
            requestuserData(username, password);
        }
    }
}

function requestuserData(username, password){
    $.ajax({
        type: "POST",
        url: UserIP,
        data: JSON.stringify({ "username":username, "password":password, "create":true}),
        contentType: "application/json",
        success: function (result) {
            //stores the result in userdata
            userData = result;

            console.log(JSON.stringify(userData));
            //updates the html with the user data
            updateUserFields();
        },
        error: function (result, status) {
            console.log("something went wrong!");
            console.log(`status was ${status}`);
            console.log(`results were ${result}`);
        }
    });
}

function updateUserFields(){
    //gets the fields to be filled out
    

    dataFields = document.getElementsByClassName("UserData")[0].getElementsByClassName("userInfo");

    //updates the fields found
    dataFields.xp.innerHTML = "exp: ".concat(userData.xp);
    dataFields.streak.innerHTML = "streak: " + userData.streak;
    dataFields.username.innerHTML = "user: " + userData.username;
}

function addExpForApp(){
    //gets the username fromt eh cookies
    var username = getUsername();

    //checks if there was a username stored in the cookies
    if(username == ""){
        alert("must have a valid user ID to gain xp");
    }else{
        //gets the password from the cookies
        var password = getPassword();

        if(password == ""){
            alert("must have a valid user ID to gain xp");
        }else{
            $.ajax({
                type: "POST",
                url: xpID,
                data: JSON.stringify({ "username":username, "password":password, "xp":20}),
                contentType: "application/json",
                success: function (result) {
                    console.log("xp added");
                },
                error: function (result, status) {
                    console.log("something went wrong!");
                    console.log(`status was ${status}`);
                    console.log(`results were ${result}`);
                }
            });
        }
    }
}

function newUserInfoButton(){
    //reads the elements the user inputs text to
    inputFields = document.getElementsByClassName("form-control");

    //reads the username and password and stores them as cookies
    storeCookies(inputFields.email.value, inputFields.password.value);

    //attempts to query the server using the current cookies to update the user data
    updateUserData();
}