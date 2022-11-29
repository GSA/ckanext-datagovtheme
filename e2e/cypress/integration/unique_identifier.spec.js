describe('Dataset page identifier', () => {
    // Uses datasets from seed.py which created test ones to check

    it('check unique identifier is not unknow', () => {
        cy.visit('/dataset/test_dataset_04');
        cy.get('th[property="rdfs:label"]').contains('Unique Identifier')
            .get('td[property="rdf:value"]').should('not.have.text', 'Unknown');
    });
});
