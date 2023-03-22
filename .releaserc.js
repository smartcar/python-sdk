'use strict';

module.exports = {
  branches: 'master',
  plugins: [
    '@semantic-release/commit-analyzer',
    [
      '@google/semantic-release-replace-plugin',
      {
        replacements: [
          {
            files: ['smartcar/__init__.py'],
            from: "__version__ = \"0.0.0\"",
            to: "__version__ = \"${nextRelease.version}\"",
            results: [
              {
                file: 'smartcar/__init__.py',
                hasChanged: true,
                numMatches: 1,
                numReplacements: 1,
              },
            ],
            countMatches: true,
          },
        ],
      },
    ],
    '@semantic-release/release-notes-generator',
    '@semantic-release/github',
  ],
};
