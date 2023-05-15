const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));

async function fetchExchangeRates(baseCurrency) {
  const response = await fetch(`https://api.exchangerate-api.com/v4/latest/${baseCurrency}`);
  const rates = await response.json();
  return rates;
}

(async function() {
  const baseCurrency = 'USD'; // Specify the base currency
  const start = Date.now();
  const exchangeRates = await fetchExchangeRates(baseCurrency);
  const end = Date.now();
  const elapsedTime = (end - start) / 1000;

  console.log(`Exchange rates for ${baseCurrency}:`, exchangeRates.rates);
  console.log(`Fetched in ${elapsedTime} seconds.`);
})();
