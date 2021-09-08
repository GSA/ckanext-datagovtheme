setTimeout(function() {
  this.jQuery(function (jQuery) {
    jQuery('[data-toggle="ratings"]').on({
      click: function (event) {
        event.preventDefault();
        var toggle = jQuery(event.target);
        var target = jQuery(toggle.data('target'));

        if (target.is(':visible')) {
          target.hide();
          toggle.trigger('hidden');
        } else {
          target.show();
          toggle.trigger('shown');
        }
      },
      shown: function (event) {
        var link = jQuery(event.target);
        link.data('showText', link.text());
        link.text(link.data('hideText'));
      },
      hidden: function (event) {
        var link = jQuery(event.target);
        link.text(link.data('showText'));
      }
    });
    $('[data-toggle="qa_tooltip"]').tooltip({
    title: "<ul class='tooltip1' style='font-size:.8em; list-style:none; margin:0px; z-index:99;'><li><strong>Scoring Methodology</strong></li><br><li>&#9733; - Available under an open license</li><br><li>&#9733;&#9733; - Available as structured data (eg. Excel instead of a scanned table)</li><br><li>&#9733;&#9733;&#9733; - Uses non-proprietary formats (e.g., CSV instead of Excel)</li><br><li>&#9733;&#9733;&#9733;&#9733; - 'Uses URIs to identify things, so that people can link to it</li><br><li>&#9733;&#9733;&#9733;&#9733;&#9733; - Linked to other data to provide context</li></ul>",
    opacity: 1,
    delay: { show: 400, hide: 200 }
    });
    $('[data-toggle="qa_tooltip2"]').tooltip({
          title: "<ul class='tooltip2' style='font-size:.8em; list-style:none; margin:0px; z-index:99;'><li><strong>Scoring Methodology</strong></li><br><li>&#9733; - Available under an open license</li><br><li>&#9733;&#9733; - Available as structured data (eg. Excel instead of a scanned table)</li><br><li>&#9733;&#9733;&#9733; - Uses non-proprietary formats (e.g., CSV instead of Excel)</li><br><li>&#9733;&#9733;&#9733;&#9733; - 'Uses URIs to identify things, so that people can link to it</li><br><li>&#9733;&#9733;&#9733;&#9733;&#9733; - Linked to other data to provide context</li></ul>",
          opacity: 1,
          delay: { show: 400, hide: 200 }
    });
  });
}, 1000);