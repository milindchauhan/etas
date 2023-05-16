const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));

async function fetchCOVID19Data(country) {
  const response = await fetch(`https://disease.sh/v3/covid-19/historical/${country}?lastdays=1`);
  const data = await response.json();
  return data;
}

function getLatestCOVID19Stats(data, country) {
  const latestData = data.timeline.cases;
  const latestDate = Object.keys(latestData)[0];
  return {
    country: country,
    confirmedCases: latestData[latestDate]
  };
}

async function fetchAndAnalyzeCOVID19Data(country) {
  const data = await fetchCOVID19Data(country);
  const latestStats = getLatestCOVID19Stats(data, country);
  return latestStats;
}

(async function() {
  const country = 'india'; // Specify the country for COVID-19 data
  const start = Date.now();
  const stats = await fetchAndAnalyzeCOVID19Data(country);
  const end = Date.now();
  const elapsedTime = (end - start) / 1000;

  console.log(`COVID-19 Statistics for ${stats.country}:`);
  console.log(`Confirmed Cases: ${stats.confirmedCases}`);
  console.log(`Fetched and analyzed in ${elapsedTime} seconds.`);
})();
