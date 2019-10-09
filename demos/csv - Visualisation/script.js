let availableColors = [
    '#000075',
    '#800000',
    '#911eb4',
    '#e6194B',
    '#808000',
    '#9A6324',
    '#e6beff',
    '#aaffc3',
    '#fffac8',
    '#ffd8b1',
    '#fabebe',
    '#a9a9a9',
    '#f032e6',
    '#42d4f4',
    '#3cb44b',
    '#bfef45',
    '#ffe119',
    '#f58231',
    '#469990',
];

let colorChoices = {};

function handleFileSelect(evt) {
    var files = evt.target.files; // FileList object

    // use the 1st (and only) file from the list
    f = files[0];

    var reader = new FileReader();

    // Closure to capture the file information.
    reader.onload = (function(theFile) {
        return function(e) {

            // Load requirements from CSV file
            let reqs = e.target.result;
            // Split the requirements into separate requirements
            reqs = reqs.split('\n');

            getDataFromAPI(reqs);
        };
    })(f);

    // Read in the image file as a data URL.
    reader.readAsText(f);
}

function getDataFromAPI(reqs) {

    // Assign the URL to use, local-host or the actual deployment
    // const url = "http://217.172.12.199:9799/check-quality";
    const url = "http://0.0.0.0:9799/check-quality";

    let responses = [];
    const numLines = reqs.length;

    $("#body").append(`
        <hr>
        <div id="row-ambiguity-result" class="row">
            <div id="legend1" class="col-xs-12 col-md-6"></div>
            <div id="legend2" class="col-xs-12 col-md-6"></div>
        </div>
        <hr>
        <div id="annotatedRequirements">
        </div>
    `);


    // Create request data using OpenReq JSON format, and the sentences provided
    let requestData = {
        "requirements": []
    };

    // Decompose each requirement into the format required for the API
    // Work on each requirement, one at a time
    for (let lineIndex = 0; lineIndex < reqs.length; lineIndex++) {
        let text = reqs[lineIndex];
        requestData["requirements"].push({
            id: lineIndex,
            text: text
        });
    }

    // Pass all requirements to the API
    $.ajax({
            type: "POST",
            url: url,
            async: true,
            contentType: "application/json",
            data: JSON.stringify(requestData),
            success: function (response) {
                responseData = response.data;
            },
            error: function (response) {
                responseData = response.data;
            }
        }).done(function (response) {

            processResponse(reqs, response);

        });
}


function processResponse(reqs, response) {

    function addHeader(number) {
        $("#annotatedRequirements").append(`
            <br>
            <h2>Annotated Use Case ${String.fromCharCode(number + 65)}</h2>
            <br>
        `);
    }

    let ambStats = [];
    let reqIndex = 0;
    let useCaseNumber = 0;

    addHeader(useCaseNumber++);
    $.each(response, function (lineIndex, ambiguities) {

        if (indexCharacters(reqIndex, lineIndex, reqs[lineIndex]))
            reqIndex++;
        else
            addHeader(useCaseNumber++);
        ambStats.push(highlightCharacters(lineIndex, ambiguities));
    });

    showLegend(ambStats);
    showAmbiguityCounts(ambStats);
}

function indexCharacters(reqIndex, lineIndex, text) {
    let letters = text.split('');

    // If this is a blank line in the CSV, handle this special case
    if (letters.length === 1)
        return false;

    let htmlElements = '';
    letters.forEach(function (letter, letterIndex) {
        let htmlClass = 'char';
        if (letter === ' ') {
            htmlClass = 'charSpace'
        }

        htmlElements += `<mark
                class="${htmlClass}"
                style="background-color:${"#FFFFFF"};"
                id="charID_${lineIndex}_${letterIndex}"
            >
                ${letter}
            </mark>`;
    });

    // Wrap the elements in a labelled container for identification later
    htmlElements = `
        <div>
            REQ-${reqIndex+1}. &emsp; ${htmlElements}
        <div>
        <br>
    `;
    $("#annotatedRequirements").append(htmlElements);
    return true;

}


function highlightCharacters(lineIndex, ambiguities) {

    // Variables that dictate styling
    const borderRadius = "5px";
    const highlightSpacingLeft = "5px";
    const highlightSpacingRight = "2px";
    const highlightMarginLeft = "-2px";

    var totalAmbCount = ambiguities.length;
    var visibleAmbCount = 0;
    var visibleAmbs = [];

    // For each ambiguity object sent
    $.each(ambiguities, function (amb_index, ambiguityData) {

        let ambIndexStart = ambiguityData["index_start"];
        let ambIndexEnd = ambiguityData["index_end"];

        // Check if this ambiguity overlaps with an existing one
        for (let charID = ambIndexStart; charID < ambIndexEnd; charID++) {
            let ambChar = $(`[id="charID_${lineIndex}_${charID}"]`);
            if (ambChar.css('background-color') !== 'rgb(255, 255, 255)') {
                return;  // Then this ambiguity overlaps with another, go to the next ambiguity
            }
        }
        visibleAmbCount++;
        visibleAmbs.push(ambiguityData);

        // Set the color of the ambiguity based on the existing ones, or create a new one, or default
        let color = colorChoices[ambiguityData["title"]] || availableColors.pop() || '#ffff00';
        colorChoices[ambiguityData["title"]] = color;

        // Apply css to each letter in the found ambiguity
        for (let charID = ambIndexStart; charID < ambIndexEnd; charID++) {

            let ambChar = $(`[id="charID_${lineIndex}_${charID}"]`);
            ambChar.css("background-color", color);

            // Round the corners of the edges
            if (charID === ambIndexStart) {
                ambChar.css("border-top-left-radius", borderRadius);
                ambChar.css("border-bottom-left-radius", borderRadius);
                ambChar.css("margin-left", highlightSpacingLeft);
                ambChar.css("padding-left", highlightSpacingLeft);
                ambChar.css("margin-left", highlightMarginLeft);
            } else if (charID === ambIndexEnd-1) {
                ambChar.css("border-top-right-radius", borderRadius);
                ambChar.css("border-bottom-right-radius", borderRadius);
                ambChar.css("margin-right", highlightSpacingRight);
                ambChar.css("padding-right", highlightSpacingRight);
            } else {

            }
        }
    });

    return {
        "totalAmbCount": totalAmbCount,
        "visibleAmbCount": visibleAmbCount,
        "visibleAmbs": visibleAmbs
    }
}


function showLegend(ambStats) {

    let visibleAmbs = [];

    $.each(ambStats, function (index, ambStat) {
        visibleAmbs = visibleAmbs.concat(ambStat.visibleAmbs)
    });

    // Get a set of all of the ambiguities. This eliminates duplicates
    let ambiguities = {};
    $.each(visibleAmbs, function (index, visibleAmb) {
        ambiguities[visibleAmb["title"]] = visibleAmb
    });

    // Apply the effects
    let legend1 = $("#legend1");
    let legend2 = $("#legend2");

    let index = 0;
    $.each(ambiguities, function (ambiguityTitle, ambiguityData) {
        let legend = null;
        if (index < Object.keys(ambiguities).length / 2) {
            legend = legend1
        } else {
            legend = legend2
        }
        index++;

        let title = ambiguityData["title"];
        let color = colorChoices[title];
        let description = ambiguityData["description"];
        let htmlElement = `
            <div style="background-color:${color}" class="box"></div>
            <div class="explanationTitle" style="background-color:${color}">${title}</div>
            <div class="explanation">${description}</div>
            <br>`;
        legend.append(htmlElement);
    });
}


function showAmbiguityCounts(ambStats) {

    // Computer totals from individual ambiguity stats
    let totalAmbCount = 0;
    let visibleAmbCount = 0;
    for (i=0;i<ambStats.length;i++) {
        totalAmbCount += ambStats[i].totalAmbCount;
        visibleAmbCount += ambStats[i].visibleAmbCount;
    }

    // Create display string
    htmlText =
        'To increase readability, overlapping ambiguities are hidden. ' +
        'Once the existing ambiguities are addressed and no longer highlighted, the hidden ambiguities will become visible.' +
        '<br/>&nbsp&nbsp&nbsp&nbsp Total Ambiguities &nbsp&nbsp&nbsp&nbsp: ' + totalAmbCount +
        '<br/>&nbsp&nbsp&nbsp&nbsp Visible Ambiguities &nbsp: ' + visibleAmbCount +
        '<br/>&nbsp&nbsp&nbsp&nbsp Hidden Ambiguities  : ' + (totalAmbCount-visibleAmbCount);

    // Add HTML to page
    $('#ambiguity-counts').html(htmlText);
}


$(document).ready(function () {
    document.getElementById('upload').addEventListener('change', handleFileSelect, false);
});



