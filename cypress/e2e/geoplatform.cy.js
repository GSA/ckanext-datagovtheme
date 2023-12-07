describe('Geoplatform Link', () => {
    it('Get other data resources section', () => {
        cy.intercept(
            {
                method: 'GET',
                url: 'https://stg-api.geoplatform.gov/v3/public/lookups/data-gov/dataset?name=u-s-hourly-precipitation-data2',
            },
            {
                statusCode: 200,
                body: {
                    geoplatform_url: 'https://stg.geoplatform.gov/metadata/36da2c52-1e55-5e9b-959b-7c415478c757',
                },
            }
        );

        cy.visit('/dataset/u-s-hourly-precipitation-data2');
        cy.get('section[id="dataset-other-resources"]').should('exist');
    });
});
