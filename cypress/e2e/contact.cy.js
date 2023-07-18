describe('Dataset page contact', () => {
    // Uses datasets from seed.py which created test ones to check

    it('check contact email', () => {
        cy.visit('/dataset');
        cy.get('#search-big').type('test 01 dataset{enter}');
        cy.get('ul.dataset-list > li:first a').click({force: true});
        cy.get('.additional-info').contains('test@email.com');
    });
});
