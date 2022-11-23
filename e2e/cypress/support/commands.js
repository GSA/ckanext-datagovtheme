Cypress.Commands.add('login', (userName, password, loginTest) => {
  /**
   * Method to fill and submit the CKAN Login form
   * :PARAM userName String: user name of that will be attempting to login
   * :PARAM password String: password for the user logging in
   * :RETURN null:
   */
  if (!loginTest) {
      cy.visit('/user/login');
  }
  if (!userName) {
      userName = Cypress.env('USER');
      cy.log(userName, process.env);
  }
  if (!password) {
      password = Cypress.env('USER_PASSWORD');
  }
  cy.hide_debug_toolbar();

  cy.get('#field-login').type(userName);
  cy.get('#field-password').type(password);
  cy.get('.btn-primary').eq(1).click();
});

Cypress.Commands.add('logout', () => {
  cy.clearCookies();
});


Cypress.Commands.add('create_organization', (orgName, orgDesc) => {
  /**
   * Method to create organization via CKAN API
   * :PARAM orgName String: Name of the organization being created
   * :PARAM orgDesc String: Description of the organization being created
   * :PARAM orgTest Boolean: Control value to determine if to use UI to create organization
   *      for testing or to visit the organization creation page
   * :RETURN null:
   */

  cy.request({
      url: '/api/action/organization_create',
      method: 'POST',
      body: {
          description: orgDesc,
          title: orgName,
          approval_status: 'approved',
          state: 'active',
          name: orgName,
      },
  });
});


Cypress.Commands.add('delete_organization', (orgName) => {
  /**
   * Method to purge an organization from the current state
   * :PARAM orgName String: Name of the organization to purge from the current state
   * :RETURN null:
   */
  cy.request({
      url: '/api/action/organization_delete',
      method: 'POST',
      failOnStatusCode: false,
      body: {
          id: orgName,
      },
  });
  cy.request({
      url: '/api/action/organization_purge',
      method: 'POST',
      failOnStatusCode: false,
      body: {
          id: orgName,
      },
  });
});

// Cypress.Commands.add('delete_dataset', (datasetName) => {
//   /**
//    * Method to purge a dataset from the current state
//    * :PARAM datasetName String: Name of the dataset to purge from the current state
//    * :RETURN null:
//    */
//   cy.request({
//       url: '/api/action/dataset_purge',
//       method: 'POST',
//       body: {
//           id: datasetName,
//       },
//   });
// });

Cypress.Commands.add(
  'create_harvest_source',
  (dataSourceUrl, harvestTitle, harvestDesc, harvestType, harvestPrivate, invalidTest) => {
      /**
       * Method to create a new CKAN harvest source via the CKAN harvest form
       * :PARAM dataSourceUrl String: URL to source the data that will be harvested
       * :PARAM harvestTitle String: Title of the organization's harvest
       * :PARAM harvestDesc String: Description of the harvest being created
       * :PARAM harvestType String: Harvest source type. Ex: waf, datajson
       * :RETURN null:
       */
      if (!invalidTest) {
          cy.get('#field-url').type(dataSourceUrl);
      }
      cy.get('#field-title').type(harvestTitle);
      cy.get('#field-name').then(($field_name) => {
          if ($field_name.is(':visible')) {
              $field_name.type(harvestTitle);
          }
      });

      cy.get('#field-notes').type(harvestDesc);
      cy.get('[type="radio"]').check(harvestType);

      // Validate private_datasets defaults to Private
      cy.get('#field-private_datasets').find(':selected').contains('Private');

      cy.get('#field-private_datasets').select(harvestPrivate);

      cy.get('input[name=save]').click();
  }
);

Cypress.Commands.add('delete_harvest_source', (harvestName) => {
  cy.visit('/harvest/admin/' + harvestName);
  cy.wait(3000);
  cy.contains('Clear').click({ force: true });

  // Confirm harvest clear
  cy.wait(1000);
  cy.contains(/^Confirm$/).click();

  cy.wait(3000);
  cy.visit('/harvest/delete/' + harvestName + '?clear=True');
});

Cypress.Commands.add('start_harvest_job', (harvestName) => {
  cy.visit('/harvest/' + harvestName);
  cy.hide_debug_toolbar();

  cy.contains('Admin').click();
  // Wait for all pages to load, avoid bug
  // https://github.com/ckan/ckanext-harvest/issues/440
  cy.wait(3000);
  cy.get('.btn-group>.btn:first-child:not(:last-child):not(.dropdown-toggle)').click({ force: true });
  // Confirm harvest start
  cy.wait(1000);
  cy.contains(/^Confirm$/).click();

  // Confirm stop button exists, harvest is started/queued
  cy.wait(500);
  cy.contains('Stop');
});

// Cypress.Commands.add('create_dataset', (ckan_dataset) => {
//   var options = {
//       method: 'POST',
//       url: '/api/3/action/package_create',
//       headers: {
//           'cache-control': 'no-cache',
//           'content-type': 'application/json',
//       },
//       body: JSON.stringify(ckan_dataset),
//   };

//   return cy.request(options);
// });


Cypress.Commands.add('hide_debug_toolbar', () => {
  cy.get('#flHideToolBarButton').then(($button) => {
      if ($button.is(':visible')) {
          cy.get('#flHideToolBarButton').click();
      }
  });
});
