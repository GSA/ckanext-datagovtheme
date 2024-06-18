jQuery(function ($) {

  var pupolar_api = "/datagovtheme/get-popular-count";
  var pkgs = {'pkgs': collect_all_packages().join(',')};
  $.getJSON(pupolar_api, pkgs, function(data) {
    $.each( data, function( key, val ) {
      $("ul.dataset-list li.dataset-item h3.dataset-heading").each(function() {
        if ($(this).attr('pkg_id') == key) {
          $(this).find('span.recent-views').attr('title', val['recent']).html('<i class="fa fa-line-chart"></i> ' + val['recent'] + ' recent views');
          if (val['recent'] >= 10) {
            $(this).find('span.recent-views').css('visibility', 'visible');
          }
        }
      });
    });
  });

  function collect_all_packages() {
    var pkgs = [];
    $("ul.dataset-list li.dataset-item h3.dataset-heading").each(function() {
      pkgs.push($(this).attr('pkg_id'));
    });

    return pkgs;
  } 
});
