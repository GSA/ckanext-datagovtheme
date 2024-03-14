describe("Dataset page identifier", () => {
    // Uses datasets from seed.py which created test ones to check

    it("check unique identifier is not unknown", () => {
        cy.visit("/dataset");
        cy.get("ul.dataset-list > li:first a").click({ force: true });
        cy.get('th[property="rdfs:label"]')
            .contains("Identifier")
            .get('td[property="rdf:value"]')
            .should("not.have.text", "Unknown");
    });
});
