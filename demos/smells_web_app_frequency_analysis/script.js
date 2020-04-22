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

    let wordCount = 0;
    for (var i = 0; i < reqs.length; i++) {
        wordCount += reqs[i].split(' ').length;
    }

    function addHeader(number) {
        $("#annotatedRequirements").append(`
            <br>
            <h2>Annotated Use Case ${String.fromCharCode(number + 65)}</h2>
            <br>
        `);
    }

    var amb_counts = {
        'Ambiguous Adverb or Adjective' : 0,
        'Comparatives and Superlatives' : 0,
        'Coordination' : 0,
        'Negative Statement' : 0,
        'Subjective Language' : 0,
        'Vague Pronoun' : 0,
        'Compound Noun' : 0,
        'Nominalization' : 0,
        'Other / Misc' : 0,
    };
    const amb_key = 'language_construct';
    $.each(response, function (req_index, ambiguities) {

        $.each(ambiguities, function (amb_index, amb) {
            if (amb[amb_key] in amb_counts) {
                amb_counts[amb[amb_key]] += 1;
            } else {
                amb_counts[amb[amb_key]] = 1;
                console.log('Missing Language Construct: '+amb[amb_key])
            }
        });
    });

    let tableText = '';
    console.log("Number of Requirements: " + Object.keys(response).length);
    for (var key in amb_counts) {
        console.log(key.padEnd(30, ' ') + " : " + amb_counts[key]);
        tableText += `<tr><td>${key}</td><td>&nbsp&nbsp&nbsp:&nbsp&nbsp&nbsp${amb_counts[key]}</td></tr>`
    }

    // Create display string
    htmlElements = `
        <br/>
        <h4># Requirements: ${Object.keys(response).length}</h4>
        <h4># of Words: ${wordCount}</h4>
        <table style="padding: 5px;">
            <tr>
                <th>Ambiguity Indicator</th>
                <th>Count</th>
              </tr>
            ${tableText}
        </table>
        </div>`;

    // Add HTML to page
    $('#ambiguity-smell-counts').html(htmlElements);
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

$(document).ready(function () {
    document.getElementById('upload').addEventListener('change', handleFileSelect, false);
});

