var button = document.createElement("button");
button.innerHTML = "Export";

// Append somewhere
var body = document.getElementsByTagName("body")[0];
body.appendChild(button);

// Add event handler
button.addEventListener ("click", function() {
    var fields = Object.keys(iris_data[0])
    var replacer = function(key, value) { return value === null ? '' : value } 
    var csv = iris_data.map(function(row){
        return fields.map(function(fieldName){
            return JSON.stringify(row[fieldName], replacer)
        }).join(',')
    })

    // add header column
    csv.unshift(fields.join(','))
    csv = csv.join('\r\n');

    // Make it downloadable
    var encodedUri = encodeURI(csv);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "iris_data.csv");
    
    // Required for FF
    document.body.appendChild(link);
    link.click();
});