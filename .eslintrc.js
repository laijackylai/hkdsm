module.exports = {
  env: {
    node: true,
  },
  extends: [
    'airbnb-base',
    'prettier'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  rules: {
    "function-paren-newline": ["error", "never"]
  },
};
