// console.log("Hi")

// chrome.action.onClicked.addListener(async (tab) => {
//   // Get data from the website
//   const tabUrl = tab.url;
//   const data = await fetchDataFromWebsite(tabUrl);

//   console.log("Data extracted from the website:", data);

//   // Send data to API
//   const apiResponse = await sendDataToAPI(data);
  
//   // Process API response as needed
//   console.log(apiResponse);
// });

// async function fetchDataFromWebsite(url) {
//   // Use appropriate method to fetch data from the website
//   // For example, you can use fetch API
//   const response = await fetch(url);
//   const data = await response.text();
//   return data;
// }

// async function sendDataToAPI(data) {
//   // Use appropriate method to send data to your API
//   // For example, you can use fetch API
//   const response = await fetch('https://yourapi.com/endpoint', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({ data })
//   });
//   const responseData = await response.json();
//   return responseData;
// }


// console.log("bye")
  
console.log("Hi");

// Fetch the webpage content
fetch('https://www.reddit.com/?rdt=53946&onetap_auto=true&one_tap=true', {
  headers: {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
  }
})
.then(response => {
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.text();
})
.then(html => {
  // Log HTML content to the console
  console.log("HTML content:", html);

  // Send HTML content to API
  sendDataToAPI(html);
})
.catch(error => {
  console.error('There was a problem with the fetch operation:', error);
});

function sendDataToAPI(html) {
  // Send data to your API
  fetch('http://127.0.0.1:5050/extension', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({Title : html })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(responseData => {
    console.log("API response:", responseData);
  })
  .catch(error => {
    console.error('There was a problem sending data to the API:', error);
  });
}

console.log("bye");
