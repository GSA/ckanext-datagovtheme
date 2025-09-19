describe('Facets Bureaus', () => {
    it('Check Bureaus name is string', () => {
        cy.visit('/dataset');
        cy.get('.filters h2').its('length').should('be.equal', 7);
        cy.get('.filters h2').eq(6).contains('Bureaus');

        cy.get('nav[aria-label="Bureaus"] span[class="item-label"]')
            .each(($el) => {
                cy.wrap($el).contains(/^[a-zA-Z\s.]*$/)
            })  
    });

});
