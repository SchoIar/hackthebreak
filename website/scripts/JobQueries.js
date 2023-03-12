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
    console.log(`json result: ${result.yourMom}`);
}


function startQuery(){
    //keywords = $("#Search").Text;
    //location = $("#Location").Text;

    //console.log(`Searching for ${keywords} with location ${location} at url ${QueryIP}`);

    QueryJob("work", "Canada");
}

    