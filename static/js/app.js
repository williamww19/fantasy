// import the data from data.js
const tableData = rankings;

// Reference the HTML table using d3
var tbody = d3.select("tbody");

function buildTable(data) {
    // First, clear out any existing data
    tbody.html("");
  
    // Next, loop through each object in the data
    // and append a row and cells for each value in the row
    data.forEach((dataRow) => {
      // Append a row to the table body
      let row = tbody.append("tr");
  
      // Loop through each field in the dataRow and add
      // each value as a table cell (td)
      Object.values(dataRow).forEach((val) => {
        let cell = row.append("td");
        cell.text(val);
        });
    });
  }

// Create a variable to keep track of all the filters as an object.
var filters = {};

function updateFilters() {
    // Save the element that was changed as a variable.
    var inputElement = d3.select(this);
    // Save the value that was changed as a variable
    var inputValue = d3.select(this).property("value")
    // Save the id ofther filter that was changed
    var inputId = d3.select(this).property("id");
    // If a filter value was entered then add that filterId and value
    // to the filters list. Otherwise, clear that filter from the filters object.
    if (inputValue) {
      filters[inputId] = inputValue;
    }
    else {
      delete filters[inputId];
    };

    // Call function to apply all filters and rebuild the data
    filterTable();

};

// use this function to filter the table when data is entered.
function filterTable() {
  //  Set the filtered data to the tableData.
  filteredData = tableData;
  // Loop through all of the filters and keep any data that
  // matches the filter values
  Object.keys(filters).forEach((key) => {
    filteredData = filteredData.filter(row => row[key] === filters[key]);
  })
  buildTable(filteredData);
};

// Attach an event to listen for changes to each filter
d3.selectAll("input").on("change", updateFilters);

// Build the table when the page loads
buildTable(tableData);
