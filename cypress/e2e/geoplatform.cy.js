describe("Geoplatform Link", () => {
    it("Check if other data resources section is visible", () => {
        cy.intercept(
            {
                method: "GET",
                url: "https://stg-api.geoplatform.gov/v3/public/lookups/data-gov/dataset?name=test_mock_geoplatform_data",
            },
            {
                statusCode: 200,
                body: {
                    geoplatform_url: "https://www.youtube.com/",
                },
            }
        );

        cy.visit("/dataset/test_mock_geoplatform_data");
        cy.wait(10000);
        cy.get('section[id="geoplatform-link-section"]')
            .scrollIntoView()
            .should("be.visible");
    });

    it("Check if other data resources section is not visible", () => {
        cy.intercept(
            {
                method: "GET",
                url: "https://stg-api.geoplatform.gov/v3/public/lookups/data-gov/dataset?name=test_bad_mock_geoplatform_data",
            },
            {
                statusCode: 404,
                body: {},
            }
        );

        cy.visit("/dataset/test_bad_mock_geoplatform_data");
        cy.get('section[id="geoplatform-link-section"]').should(
            "not.be.visible"
        );
    });
});
