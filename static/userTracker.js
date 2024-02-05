function trackClick(event) {
    console.log('clicked')
    // Get timestamp
    const timestamp = new Date().toISOString();
  
    // Get Xpath of the clicked element
    const xpath = getXpath(event.target);
  
    // Get current location
    const location = window.location.href;
  
    // Get IP address (Note: This is just an example and might not work in all environments)
    const ipAddress = getUserIpAddress();
  
    // Get session ID (Assuming you have a session management system in place)
    const sessionId = getSessionId();
  
    // Get username (Assuming you have a way to identify the user)
    const username = getUserName();
  
    // Create log entry
    const logEntry = {
      timestamp,
      action: 'Click',
      xpath,
      location,
      ipAddress,
      sessionId,
      username,
      // Add any other relevant information
    };
  
    // Send log entry to server or store it locally
    sendLogToServer(logEntry);
  }
  
  // Function to get XPath of an element
  function getXpath(element) {
    if (!element || !element.tagName) return null;
    const index = [...element.parentNode.children].indexOf(element) + 1;
    return element.parentNode.tagName
      ? `${getXpath(element.parentNode)}/${element.tagName.toLowerCase()}[${index}]`
      : `/${element.tagName.toLowerCase()}[${index}]`;
  }
  
  // Function to get user IP address (Note: This is just an example)
function getUserIpAddress() {
    // Implement logic to get the user's IP address
    // This might involve making an API call to a service that provides the IP
    const IP = fetch("/getUserIp").then(res => console.log(res))
    console.log("IP",IP)
    return IP; // Example IP address
  }
  
  // Function to get session ID (Assuming you have a session management system in place)
  function getSessionId() {
    // Implement logic to get the current session ID
    return 'example_session_id'; // Example session ID
  }
  
  // Function to get username (Assuming you have a way to identify the user)
  function getUserName() {
    // Implement logic to get the current username
    return 'example_user'; // Example username
  }
  
  // Function to send logs to the server
  function sendLogToServer(logEntry) {
    // Make an HTTP request to send log entry to the server
    // Example with Fetch API:
    console.log(logEntry)
    // fetch('https://yourlogserver.com/log', {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json',
    //   },
    //   body: JSON.stringify(logEntry),
    // });
  }
  
  // Add a click event listener to the document
  document.addEventListener('click', trackClick);
  