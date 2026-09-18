const https = require('https');

https.get('https://html.duckduckgo.com/html/?q=5000%E4%B8%87+aave+%E6%8D%9F%E5%A4%B1', {
  headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' }
}, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    const matches = data.match(/<a class="result__snippet[^>]*>(.*?)<\/a>/gi);
    if (matches) {
      matches.forEach(m => console.log(m.replace(/<[^>]+>/g, '').trim()));
    } else {
      console.log('No matches found.');
    }
  });
}).on('error', (e) => console.error(e));
