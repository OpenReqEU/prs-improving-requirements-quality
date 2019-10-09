let colorPalette = {
    "Actually": '#ff8a80',
    "Ambiguous Positioning": '#ff5252',
    "Ambiguous Words": '#ff80ab',
    "Continuance": '#ff4081',
    "Dangerous Plural": '#ea80fc',
    "Imprecise": '#e040fb',
    "Inside Behaviour": '#b388ff',
    "Missing Content": '#7c4dff',
    "Negative": '#8c9eff',
    "Negative Reason": '#536dfe',
    "Optional": '#82b1ff',
    "Pronoun": '#448aff',
    "Speculation": '#80d8ff',
    "Too Broad": '#40c4ff',
    "Weak": '#84ffff',
    "Wishful Thinking": '#18ffff',
    "Vague": '#a7ffeb',
    "Unclear Inclusion": '#64ffda',
    "Ambiguous Plural": '#b9f6ca',
    "Both": '#69f0ae',
    "Dangerous Reference Plural": '#ccff90',
    "Unclear Associativity": '#b2ff59',
    "Passive Ambiguity": '#ffab40',
    "Adjective": '#ff9e80',
    "Adverb": '#ff6e40',
    "Comparative Adjective": '#ffca80',
    "Comparative Adverb": '#ff9f40',
    "Comparative Verbs": '#ff4059',
    "Coordination starting with Adjective": '#1fc1b4',
    "Coordination starting with verbs": '#0f7b96',
    "Coordination starting with a noun": '#109651',
    "Postfix coordination of two nouns": '#28ff90',
    "Coordination starting with an adverb": '#e0dc0d',
    "Coordination of two verbs starting with a noun": '#a81e03',
    "Postfix Coordination of two verbs followed by a noun": '#ba6251',
    "Postfix Coordination of two verbs followed by an adverb": '#c6830d',
    "Default": '#ffff00'
};

$(document).ready(function () {

    // Get the Title and populate in the page
    let title = getUrlParameter('requirementTitle');
    $('#ambiguity-title').html(title);

    // Get the requirement text and populate in page
    let text = getUrlParameter('requirementText');
    $('#txt-ambiguity-text').val(text);

    // Split into individual sentences
    let sentences = text.match(/[^\.!\?]+[\.!\?]+["']?|$/g);  // Split into sentences
    if (sentences[sentences.length-1].length === 0) {sentences.pop()}  // Remove empty sentence at end
    // If sentence has no period at the end, it will not be caught, so add it
    if (sentences.length === 0) {sentences = [text]}
    // Assign the URL to use, local-host or the actual deployment
    let url = "http://0.0.0.0:9799/check-quality";
    // let url = "http://217.172.12.199:9799/check-quality";

    // Create request data using OpenReq JSON format, and the sentences provided
    let requestData = {
        "requirements": [
        ]
    }

    // Loop over all sentences, push them to requestData one at a time
    $.each(sentences, function (index, sentence) {
        sentence = sentence.replace(/^\s+/g, '');  // Strip whitespace left by regular expression
        requestData["requirements"].push({
            "id": index,
            "text": sentence
        });
    });

    let responseData = '';

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
    }).done(function (data) {
        // Our implementation only sends a single "requirement" to the API, stored at ID 0
        // So, the response is to be unpacked with the assumption that everything is stored under the ID 0
        data = data["0"];

        console.log(data)

        function indexCharacters(text) {
            let letters = text.split('');
            let htmlElements = '';
            letters.forEach(function (letter, index) {
                let htmlClass = 'char';
                if (letter === ' ') {htmlClass = 'charSpace'}

                htmlElements += `<mark
                        class="${htmlClass}"
                        style="background-color:${"#FFFFFF"}"
                        id="charID_${index}"
                    >
                        ${letter}
                    </mark>`;

            });
            $("#result").html(htmlElements);
        }

        function highlightCharacters() {
            const borderRadius = '5px';
            const highlightSpacingLeft = '5px';
            const highlightSpacingRight = '2px';

            // Figure out the length of each sentence to handle the response with individual sentences
            let sentences = text.match(/[^\.!\?]+[\.!\?]+["']?|$/g);  // Split into sentences
            if (sentences[sentences.length-1].length === 0) {sentences.pop()}  // Remove empty sentence at end
            let sentenceIndexes = [0];  // The first sentence (at index 0 in this list) can be found at index 0
            sentences.forEach((sentence, index) => {
                // If this sentence has any spaces at the beginning of it, it will affect where it starts, so add those
                sentenceIndexes[index] += sentence.search(/\S/);
                // Push the next sentence into the list
                // It starts at the length of this sentence, plus the index of the last sentence
                sentenceIndexes.push(sentence.trim().length + sentenceIndexes[index]);
            });

            var totalAmbCount = 0;
            var visibleAmbCount = 0;
            var visibleAmbs = [];

            // Loop over each sentence
            $.each(data, function (sentenceIndex, sentenceData) {
                // Loop over each ambiguity found in each sentence
                $.each(sentenceData, function (index, ambiguityData) {
                    totalAmbCount++;

                    let ambIndexStart = ambiguityData["index_start"] + sentenceIndexes[sentenceIndex];
                    let ambIndexEnd = ambiguityData["index_end"] + sentenceIndexes[sentenceIndex];

                    // Check if this ambiguity overlaps with an existing one
                    for (let charID = ambIndexStart; charID < ambIndexEnd; charID++) {
                        let ambChar = $(`[id="charID_${charID}"]`);
                        if (ambChar.css('background-color') !== 'rgb(255, 255, 255)') {
                            return;  // Then this ambiguity overlaps with another, go to the next ambiguity
                        }
                    }
                    visibleAmbCount++;
                    visibleAmbs.push(ambiguityData);

                    let color = colorPalette[ambiguityData["title"]] || colorPalette["Default"];

                    // Apply css to each letter in the found ambiguity
                    for (let charID = ambIndexStart; charID < ambIndexEnd; charID++) {

                        let ambChar = $(`[id="charID_${charID}"]`);
                        ambChar.css("background-color", color);

                        // Round the corners of the edges
                        if (charID === ambIndexStart) {
                            ambChar.css("border-top-left-radius", borderRadius);
                            ambChar.css("border-bottom-left-radius", borderRadius);
                            ambChar.css("margin-left", highlightSpacingLeft);
                            ambChar.css("padding-left", highlightSpacingLeft);
                        } else if (charID === ambIndexEnd-1) {
                            ambChar.css("border-top-right-radius", borderRadius);
                            ambChar.css("border-bottom-right-radius", borderRadius);
                            ambChar.css("margin-right", highlightSpacingRight);
                            ambChar.css("padding-right", highlightSpacingRight);
                        } else {

                        }
                    }
                });
            });

            return {
                "totalAmbCount": totalAmbCount,
                "visibleAmbCount": visibleAmbCount,
                "visibleAmbs": visibleAmbs
            }
        }

        function showLegend(ambStats) {

            // Get a set of all of the ambiguities. This eliminates duplicates
            let ambiguities = {};
            $.each(ambStats['visibleAmbs'], function (index, ambiguityData) {
                ambiguities[ambiguityData["title"]] = ambiguityData
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
                let color = colorPalette[title] || colorPalette["Default"];
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

            htmlText =
                'To increase readability, overlapping ambiguities are hidden. ' +
                'Once the existing ambiguities are addressed and no longer highlighted, the hidden ambiguities will become visible.' +
                '<br/>&nbsp&nbsp&nbsp&nbsp Total Ambiguities &nbsp&nbsp&nbsp&nbsp: ' + ambStats['totalAmbCount'] +
                '<br/>&nbsp&nbsp&nbsp&nbsp Visible Ambiguities &nbsp: ' + ambStats['visibleAmbCount'] +
                '<br/>&nbsp&nbsp&nbsp&nbsp Hidden Ambiguities  : ' + (ambStats['totalAmbCount']-ambStats['visibleAmbCount']);

            $('#ambiguity-counts').html(htmlText);
        }
        console.log(text)
        indexCharacters(text);
        ambStats = highlightCharacters();
        showLegend(ambStats);
        showAmbiguityCounts(ambStats);
    });


    // EXTRA CODE

            // $('#col-ambiguity-result').empty();
        //
        // let wordColorTuples = [];
        // culmIndex = 0;
        // // Loop over sentence
        // $.each(data, function (sentenceIndex, sentence) {
        //     console.log(data);
        //     // Loop over ambiguities in sentence
        //     $.each(sentence, function (ambID, amb) {
        //         // console.log("Adding ambiguity results: ");
        //         // console.log(amb);
        //
        //         let color = colorPalette[culmIndex % 8];
        //         let markup = buildAmbiguityMarkup(amb, color);
        //         $("div#col-ambiguity-result").append(markup);
        //         wordColorTuples.push([amb.text, color]);
        //
        //         culmIndex++;
        //     });
        // });
        // highlightResult(wordColorTuples);

        // else {
        //     let markup = "<h2>No ambiguities found.</h2><br>"
        //     markup += '<object id="tick_icon" type="image/svg+xml" data="./img/tick_icon.svg">Your browser does not support SVG</object>';
        //     $("div#col-ambiguity-result").append(markup);
        // }

    /***** AMBIGUITY VIEW END *************************/

});

function buildAmbiguityMarkup(o, color) {

    return '<div style="background-color:' + color + '" class="box"></div><div class="explanation">Title: ' + o.title + '</div><br><div class="explanation">Explanation: ' + o.description + '</div><br>';
}

function highlightResult(wordsColorTuples) {
    console.log("Highlighting new result.");
    console.log(wordsColorTuples);
    let options = [];
    $(wordsColorTuples).each(function (index, value) {
        let word = value[0];
        let color = value[1];
        options.push({color: color, words: [word]})
    });
    // console.log("With options:");
    // console.log(options);
    $("#txt-ambiguity-text").highlightTextarea({
        words: options
    });
}

function highlightRequirementResult(wordsColorTuples) {
    // console.log("Highlighting new result.");
    let options = []
    $(wordsColorTuples).each(function (index, value) {
        let word = value[0];
        let color = value[1];
        options.push({color: color, words: [word]})
    });
    // console.log("With options:");
    // console.log(options);
    $("#txt-fr-nfr-text").highlightTextarea({
        words: options
    });
}


function unhighlighteResult() {
    console.log("Unhighlighting previous result.");
    $("#txt-ambiguity-text").highlightTextarea('destroy');
}

function clearAmbiguityResult() {
    $("#col-ambiguity-result").empty();
    unhighlighteResult();
}

function clearRequirementsResult() {
    $("#col-fr-nfr-result").empty();
    $("#txt-fr-nfr-text").highlightTextarea('destroy');
}

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};