const UserIP = "/userdata"
var userData;

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

function requestuserData(username, password){
    $.ajax({
        type: "POST",
        url: UserIP,
        data: JSON.stringify({ "username":username, "password":password}),
        contentType: "application/json",
        success: function (result) {
            //stores the result in userdata
            userData = result;
        },
        error: function (result, status) {
            console.log("something went wrong!");
            console.log(`status was ${status}`);
            console.log(`results were ${result}`);
        }
    });
}