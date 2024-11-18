#!/bin/bash

set -e

echo The 'INIT_TEMPLATE' environment variable is set to $INIT_TEMPLATE

# Check if the INIT_TEMPLATE environment variable is set to "true"
if [ "$INIT_TEMPLATE" = "true" ]; then
    echo "Initializing the project..."
    npx degit evidence-dev/template . --force
    npm install --silent --force
else
    echo "Skipping template initialization..."
    
    if [ ! -d 'node_modules/@evidence-dev' ]; then
        echo "node_modules does not exist, installing dependencies..."
        npm install --silent --force
    fi
fi

# Running the sources script to update the Evidence sources
npm run sources

# Run the dev server
npm run dev -- --host 0.0.0.0
