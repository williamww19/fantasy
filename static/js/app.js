// import the data from data.js
const tableData = weekly_stats;

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
    // Call your function with the table ID as an argument
    applyColorScaleToTable('weekly_stats');
};

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

// Define your function
function applyColorScaleToTable(tableId) {
  // Define the color scale
  var colorScale = d3.scaleLinear().domain([0, 10, 100]).range(['#769FCA', 'white', '#FF6C65']);

  // Get the table element by ID
  var table = document.getElementById(tableId);
  
  // Get all the cells in the table
  var cells = table.querySelectorAll('table td');

  // Get the number of columns in the table
  var numColumns = document.querySelectorAll('table tr:first-child td').length;

  // Loop through each column
  for (var i = 0; i < numColumns; i++) {
  // Get all the cells in the column
      var columnIndex = document.querySelectorAll('table th')[i].textContent.trim();

      if ( columnIndex != 'Team' && columnIndex != 'FGM/A' && columnIndex != 'FTM/A' && columnIndex != 'Week' && columnIndex != 'GP') {
        var columnCells = document.querySelectorAll('table td:nth-child(' + (i + 1) + ')');
        
        // Get the values of the cells in the column
        var values = [];
        columnCells.forEach(function(cell) {
          values.push(cell.textContent.trim());
        });
        
        // Compute the domain of the color scale based on the values in the column
        if ( columnIndex != 'TO' ) {
          var domain = [d3.min(values), d3.mean(values), d3.max(values)];
        }
        else {
          var domain = [d3.max(values), d3.mean(values), d3.min(values)];
        }
        colorScale.domain(domain);
        
        // Set the background color of each cell in the column based on its value
        columnCells.forEach(function(cell) {
          cell.style.backgroundColor = colorScale(cell.textContent.trim());
        });
      };
  }
}  


// Attach an event to listen for changes to each filter
d3.selectAll("input").on("change", updateFilters);

// Build the table when the page loads
buildTable(tableData);
