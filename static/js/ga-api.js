// Load the Google data JavaScript client library.
google.load('gdata', '2.x', {packages: ['analytics']});

// Set the callback function when the library is ready.
google.setOnLoadCallback(init);

/**
 * This is called once the Google Data JavaScript library has been loaded.
 * It creates a new AnalyticsService object, adds a click handler to the
 * authentication button and updates the button text depending on the status.
 */
function init() {
  myService = new google.gdata.analytics.AnalyticsService('gaExportAPI_acctSample_v2.0');
  scope = 'https://www.google.com/analytics/feeds';
  var button = document.getElementById('authButton');

  // Add a click handler to the Authentication button.
  button.onclick = function() {
    // Test if the user is not authenticated.
    if (!google.accounts.user.checkLogin(scope)) {
      // Authenticate the user.
      google.accounts.user.login(scope);
    } else {
      // Log the user out.
      google.accounts.user.logout();
      getStatus();
    }
  }
  getStatus();
}

/**
 * Utility method to display the user controls if the user is
 * logged in. If user is logged in, get Account data and
 * get Report Data buttons are displayed.
 */
function getStatus() {
/*
  var getAccountButton = document.getElementById('getAccount');
  getAccountButton.onclick = getAccountFeed;
*/

  var dataControls = document.getElementById('dataControls');
  var loginButton = document.getElementById('authButton');
  if (!google.accounts.user.checkLogin(scope)) {
    dataControls.style.display = 'none';   // hide control div
    loginButton.innerHTML = 'Access Google Analytics';
  } else {
    dataControls.style.display = 'block';  // show control div
    loginButton.innerHTML = 'Logout';
  }
}

/**
 * Main method to get account data from the API.
 */
function getAccountFeed() {
  var myFeedUri =
      'https://www.google.com/analytics/feeds/accounts/default?max-results=50';
  myService.getAccountFeed(myFeedUri, handleAccountFeed, handleError);
}

/**
 * Handle the account data returned by the Export API by constructing the inner parts
 * of an HTML table and inserting into the HTML file.
 * @param {object} result Parameter passed back from the feed handler.
 */
function handleAccountFeed(result) {
  // An array of analytics feed entries.
  var entries = result.feed.getEntries();

  // Create an HTML Table using an array of elements.
  var outputTable = ['<table><tr>',
                     '<th>Account Name</th>',
                     '<th>Profile Name</th>',
                     '<th>Profile ID</th>',
                     '<th>Table Id</th></tr>'];

  // Iterate through the feed entries and add the data as table rows.
  for (var i = 0, entry; entry = entries[i]; ++i) {

    // Add a row in the HTML Table array for each value.
    var row = [
      entry.getPropertyValue('ga:AccountName'),
      entry.getTitle().getText(),
      entry.getPropertyValue('ga:ProfileId'),
      entry.getTableId().getValue()
    ].join('</td><td>');
    outputTable.push('<tr><td>', row, '</td></tr>');
  }
  outputTable.push('</table>');

  // Insert the table into the UI.
  document.getElementById('outputDiv').innerHTML =
      outputTable.join('');
}
