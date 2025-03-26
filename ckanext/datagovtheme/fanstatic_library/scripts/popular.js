// This js file loads with datagov-popular.html snippet

jQuery(function ($) {

  // This api takes a list of package ids from querystring and returns the view count for each package
  var popular_api = "/datagovtheme/get-popular-count";

  // all ids in a string, comma separated
  var pkgs = {'pkgs': collect_all_packages().join(',')};

  $.getJSON(popular_api, pkgs, function(data) {
    var all_items = $("ul.dataset-list li.dataset-item h3.dataset-heading");
    $.each( data, function( key, val ) {
      all_items.each(function() {
        if ($(this).attr('pkg_id') == key) {
          $(this).find('span.recent-views-datagov').attr('title', val['recent']).html('<i class="fa fa-line-chart"></i> ' + val['recent'] + ' recent views');
          // If the view count is greater than 10, make it visible
          if (val['recent'] >= 10) {
            $(this).find('span.recent-views').css('visibility', 'visible');
          }else{
            $(this).find('span.recent-views').css('display', 'none');
          }
          // remove this items from all_items to reduce the loop time
          all_items = all_items.not(this);
          // break it out of the loop
          return false;
        }
      });
    });
  });

  // We have pkg_id in each dataset-item, added in the template.
  function collect_all_packages() {
    var pkgs = [];
    $("ul.dataset-list li.dataset-item h3.dataset-heading").each(function() {
      pkgs.push($(this).attr('pkg_id'));
    });

    return pkgs;
  } 
});
