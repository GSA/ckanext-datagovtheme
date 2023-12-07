const { defineConfig } = require("cypress");

module.exports = defineConfig({
    videoCompression: false,
    videoUploadOnPasses: false,
    screenshotOnRunFailure: false,
    env: {
        USER: 'admin',
        USER_PASSWORD: 'password',
    },

    e2e: {
        setupNodeEvents(on, config) {
            // implement node event listeners here
        },
        baseUrl: 'http://localhost:5000',
    },
});
