fetch('https://api.github.com/users/milindchauhan')
  .then(response => response.json())
  .then(data => console.log(data));