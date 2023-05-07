const fetch = require('node-fetch');

async function fetchData() {
  const response1 = await fetch('https://jsonplaceholder.typicode.com/posts/1');
  const data1 = await response1.json();
  console.log(data1);

  const response2 = await fetch('https://jsonplaceholder.typicode.com/comments?postId=1');
  const data2 = await response2.json();
  console.log(data2);
}

fetchData();