describe('Dataset page contact', () => {
    // Uses datasets from data.json local harvest to check
    
    it('check contact email', () => {
        cy.visit('/dataset/test_dataset_04');
        cy.get('section[class="module module-narrow contact"] p[class="module-content"]').should('not.have.text', 'Unknown');
    }); 
});
