const fs = require('fs');
const path = require('path');

// Read environment
const isProduction = process.env.REACT_APP_ENV === 'production';
const productionUrl = process.env.REACT_APP_BASE_URL || 'http://lsg.cs.bgu.ac.il';

// Read package.json
const packagePath = path.join(__dirname, 'package.json');
const package = require(packagePath);

// Update homepage based on environment
package.homepage = isProduction ? productionUrl : '.';

// Write back to package.json
fs.writeFileSync(packagePath, JSON.stringify(package, null, 2));

console.log(`Updated package.json for ${isProduction ? 'production' : 'development'} environment`); 