const QueryIP = "/JobQuery"; 

function QueryJob(keywords, location){
    $.ajax({
        type: "POST",
        url: QueryIP,
        data: JSON.stringify({ "keywords": keywords, "location": location}),
        contentType: "application/json",
        success: handleQueryResponse,
        error: function (result, status) {
            console.log("something went wrong!");
            console.log(`status was ${status}`);
            console.log(`results were ${result}`);
        }
    });
}

function handleQueryResponse(result){
    console.log(`json result: ${JSON.stringify(result)}`);

    mainDiv = document.getElementsByClassName("searchResults")[1];

    console.log(mainDiv);

    mainDiv.innerHTML = ''

    for (var i = 0; i < result.length; i++){
        var jobHTML = `<p>${result[i].title}, ${result[i].location}, ${result[i].link}</p>`;
        mainDiv.innerHTML = mainDiv.innerHTML.concat(jobHTML);
    }

    console.log(mainDiv.innerHTML);
}


function startQuery(){
    //keywords = document.getElementById("Search").value;
    //location = document.getElementById("Location").value;

    //console.log(`Searching for ${keywords} with location ${location} at url ${QueryIP}`);

    QueryJob("a", "b");
}

    