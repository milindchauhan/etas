const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));

async function fetchPosts() {
  const response = await fetch('https://jsonplaceholder.typicode.com/posts');
  const data = await response.json();
  return data;
}

async function fetchComments(postId) {
  const response = await fetch(`https://jsonplaceholder.typicode.com/comments?postId=${postId}`);
  const data = await response.json();
  return data;
}

async function fetchUserData(userId) {
  const response = await fetch(`https://jsonplaceholder.typicode.com/users/${userId}`);
  const data = await response.json();
  return data;
}

async function fetchAllData() {
  const posts = await fetchPosts();
  const comments = [];
  const users = {};

  for (const post of posts) {
    // const postId = post.id;
    // const postComments = await fetchComments(postId);
    // comments.push(...postComments);

    const userId = post.userId;
    if (!users[userId]) {
      users[userId] = await fetchUserData(userId);
    }
  }

  return { posts, comments, users };
}

(async function() {
  const start = Date.now();
  const data = await fetchAllData();
  const end = Date.now();
  const elapsedTime = (end - start) / 1000;

  console.log(`Fetched ${data.posts.length} posts, ${data.comments.length} comments, and ${Object.keys(data.users).length} users in ${elapsedTime} seconds.`);
})();
