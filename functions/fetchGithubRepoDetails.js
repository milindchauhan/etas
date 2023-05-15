const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));

async function fetchRepositoryDetails(orgName, repoName) {
  const response = await fetch(`https://api.github.com/repos/${orgName}/${repoName}`);
  const repoDetails = await response.json();
  return repoDetails;
}

async function fetchContributors(orgName, repoName) {
  const response = await fetch(`https://api.github.com/repos/${orgName}/${repoName}/contributors`);
  const contributors = await response.json();
  return contributors;
}

async function fetchOrganizationData(orgName, repoName) {
  const repositoryDetails = await fetchRepositoryDetails(orgName, repoName);
  const contributors = await fetchContributors(orgName, repoName);
  return { repositoryDetails, contributors };
}

(async function() {
  const orgName = 'openai'; // Specify the organization name
  const repoName = 'openai-cookbook'; // Specify the repository name
  const start = Date.now();
  const organizationData = await fetchOrganizationData(orgName, repoName);
  const end = Date.now();
  const elapsedTime = (end - start) / 1000;

  console.log(`Repository Details:`, organizationData.repositoryDetails);
  console.log(`Contributors:`, organizationData.contributors);
  console.log(`Fetched in ${elapsedTime} seconds.`);
})();
