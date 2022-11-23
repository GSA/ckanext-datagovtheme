describe('Dataset', () => {
    // Uses datasets from data.json local harvest to check

    it('check unique identifier is not unknow', () => {
        cy.visit('/dataset/test_dataset_04');
        cy.get('span[property="dct:identifier"]').should('not.have.text', 'Unknown');
    });
    

});
